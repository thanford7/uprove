import scrapy
from django.utils import timezone
from html_sanitizer import Sanitizer
from html_sanitizer.sanitizer import bold_span_to_strong, italic_span_to_em, tag_replacer, target_blank_noopener
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from upapp.scraper.scraper.items import JobItem
from upapp.scraper.scraper.utils.seleniumSetup import getDomElOrNone, getSelenium, getWebElementHtml, getWebElementWait,\
    retryClick, WEBDRIVER_WAIT_SECONDS


def fontSizeToHeaderSanitizer(element):
    style = element.get('style')
    if not style or ('font-size' not in style):
        return element

    fontSizeStyle = next((s for s in style.split(';') if 'font-size' in s), None)
    fontSizePx = fontSizeStyle.split(':')[1].strip()
    if 'px' not in fontSizePx:
        return element

    fontSize = float(fontSizePx.replace('px', '').strip())
    if fontSize >= 16:
        element.tag = 'h5'
    else:
        element.tag = 'h6'

    element.style = None

    return element


def headerSizeReducerSanitizer(element):
    if element.tag in ('h1', 'h2', 'h3', 'h4'):
        element.tag = 'h5'

    return element


def divToPSanitizer(element):
    if element.tag == 'div':
        element.tag = 'p'

    return element


def spanToPSanitizer(element):
    if element.tag == 'span' and element.text and element.text.strip():
        element.tag = 'p'

    return element


def getStripOrNone(val, transformFn=None):
    if not val:
        return val
    return val.strip() if not transformFn else transformFn(val)


sanitizer = Sanitizer({
    'tags': {
        'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'p', 'ul', 'ol',
        'li', 'br', 'sub', 'sup', 'hr',
    },
    'element_preprocessors': [
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer('b', 'strong'),
        tag_replacer('i', 'em'),
        tag_replacer('form', 'p'),
        target_blank_noopener,
        fontSizeToHeaderSanitizer,
        headerSizeReducerSanitizer,
        divToPSanitizer,
        spanToPSanitizer
    ],
})


class BreezySpider(scrapy.Spider):
    name = None
    companyName = None
    start_urls = None

    def parse(self, response):
        yield from response.follow_all(css='.positions-container li a', callback=self.parseJob)

    def parseJob(self, response):
        summaryHtml = response.xpath('//div[@class="banner"]')

        yield JobItem(
            companyName=self.companyName,
            applicationUrl=response.url,
            jobTitle=summaryHtml.xpath('.//h1/text()').get(),
            location=summaryHtml.xpath('.//li[@class="location"]/span/text()').get(),
            jobDepartment=summaryHtml.xpath('.//li[@class="department"]/span/text()').get(),
            jobDescription=sanitizer.sanitize(response.xpath('//div[@class="description"]').get()),
            isFullTime=summaryHtml.xpath('.//li[@class="type"]/span/text()').get() == '%LABEL_POSITION_TYPE_FULL_TIME%',
        )


class GreenhouseSpider(scrapy.Spider):
    name = None
    companyName = None
    start_urls = None

    def parse(self, response):
        for departmentSection in response.xpath('//section[@class="level-0"]'):
            department = departmentSection.xpath('.//h3/text()').get() or departmentSection.xpath('.//h2/text()').get()
            jobLinks = departmentSection.xpath('./div[@class="opening"]//a')
            yield from response.follow_all(jobLinks, callback=self.parseJob, meta={'jobDepartment': department})

            for subDepartmentSection in departmentSection.xpath('.//section[@class="child level-1"]'):
                department = subDepartmentSection.xpath('.//h4/text()').get()
                jobLinks = subDepartmentSection.xpath('.//div[@class="opening"]//a')
                yield from response.follow_all(jobLinks, callback=self.parseJob, meta={'jobDepartment': department})

    def parseJob(self, response):
        jobDepartment = response.request.meta['jobDepartment']
        location = getStripOrNone(response.xpath('//div[@id="header"]//div[@class="location"]/text()').get())

        yield JobItem(
            companyName=self.companyName,
            applicationUrl=response.url,
            jobTitle=response.xpath('//div[@id="header"]//h1/text()').get(),
            location=location,
            jobDepartment=jobDepartment,
            jobDescription=sanitizer.sanitize(response.xpath('//div[@id="content"]').get()),
            isFullTime=True,
        )


class JazzHRSpider(scrapy.Spider):
    name = None
    companyName = None
    start_urls = None

    def parse(self, response):
        jobs = response.css('.jobs-list a')
        yield from response.follow_all(jobs, callback=self.parseJob)

    def parseJob(self, response):
        jobSummary = response.xpath('//div[@class="job-header"]')

        jobType = getStripOrNone(jobSummary.xpath('(.//li[@title="Type"]//text())[2]').get())

        yield JobItem(
            companyName=self.companyName,
            applicationUrl=response.url,
            jobTitle=getStripOrNone(jobSummary.xpath('.//h1/text()').get()),
            location=getStripOrNone(jobSummary.xpath('(.//li[@title="Location"]//text())[2]').get()),
            jobDepartment=getStripOrNone(jobSummary.xpath('(.//li[@title="Department"]//text())[2]').get()),
            jobDescription=sanitizer.sanitize(
                response.xpath('//div[@id="job-description"]//div[@class="description"]').get()
            ),
            isFullTime='full' in jobType.lower() if jobType else True,
        )


class LeverSpider(scrapy.Spider):
    name = None
    companyName = None
    start_urls = None

    def parse(self, response):
        yield from response.follow_all(response.xpath('//div[@class="posting"]//a'), callback=self.parseJob)

    def parseJob(self, response):
        jobSummary = response.xpath('//div[@class="posting-headline"]')
        categories = jobSummary.xpath('.//div[@class="posting-categories"]/div/text()')
        location = None
        jobDepartment = None
        positionType = None
        if len(categories) == 1:
            location = categories
        elif len(categories) == 2:
            location, jobDepartment = categories
        elif len(categories) == 3:
            location, jobDepartment, positionType = categories

        def parseItemFn(item):
            item = item.get()
            if not item:
                return item
            return item.replace('/', '').strip()

        location = parseItemFn(location) if location else None
        jobDepartment = parseItemFn(jobDepartment) if jobDepartment else None
        positionType = parseItemFn(positionType).lower() if positionType else None

        jobDescription = ''
        for content in response.xpath('//div[@class="section page-centered"]//div'):
            if not content.xpath('.//text()').get():
                continue
            jobDescription += content.get()

        yield JobItem(
            companyName=self.companyName,
            applicationUrl=response.url,
            jobTitle=getStripOrNone(jobSummary.xpath('.//h2/text()').get()),
            location=location,
            jobDepartment=jobDepartment,
            jobDescription=sanitizer.sanitize(jobDescription),
            isFullTime=('full' in positionType or 'remote' in positionType) if positionType else True,
        )


class Barn2DoorSpider(BreezySpider):
    companyName = 'Barn2Door'
    name = "barn2Door"
    start_urls = [
        'https://barn2door-inc.breezy.hr/?',
    ]


class ZoomoSpider(scrapy.Spider):
    name = "zoomo"
    start_urls = [
        'https://apply.workable.com/zoomo/',
    ]
    html = None
    driver = None

    def __init__(self):
        self.driver = getSelenium()
        self.driver.get('https://apply.workable.com/zoomo/')
        jobsEl = getWebElementWait(self.driver, '#jobs')

        # # Filter for full time positions only
        retryClick(jobsEl, '#worktypes-filter_input')  # Open the filter
        retryClick(jobsEl, '#worktypes-filter_listbox li[value="full"]')  # Select full time option

        # Load all jobs
        def getRunSeconds(start):
            return (timezone.now() - start).seconds

        loadBtnSelector = 'button[data-ui="load-more-button"]'
        loadJobsBtn = getDomElOrNone(self.driver, jobsEl, loadBtnSelector)
        start = timezone.now()
        while loadJobsBtn and getRunSeconds(start) < 20:
            retryClick(jobsEl, loadBtnSelector, isAllowNotFound=True)
            loadJobsBtn = getDomElOrNone(self.driver, jobsEl, loadBtnSelector)

        # Refetch the job HTML data
        self.html = getWebElementHtml(self.driver, getWebElementWait(self.driver, '#jobs'))
        super().__init__()

    def parse(self, response):
        resp = Selector(text=self.html)
        jobs = resp.xpath('//ul/li[@data-ui="job"]')
        for job in jobs:
            applicationUrl = response.urljoin(job.xpath('.//a/@href').get())
            self.driver.get(applicationUrl)
            def getJobDetail():
                body = WebDriverWait(self.driver, WEBDRIVER_WAIT_SECONDS).until(lambda d: d.find_element(By.TAG_NAME, 'main'))
                jobDetail = Selector(text=getWebElementHtml(self.driver, body))
                jobDescription = jobDetail.xpath('//div[@data-ui="job-description"]').get()
                jobRequirements = jobDetail.xpath('//div[@data-ui="job-requirements"]').get()
                jobBenefits = jobDetail.xpath('//div[@data-ui="job-benefits"]').get()
                return (jobDescription, jobRequirements, jobBenefits)

            (jobDescription, jobRequirements, jobBenefits) = getJobDetail()
            # Retry if failure
            if not all([jobDescription, jobRequirements, jobBenefits]):
                (jobDescription, jobRequirements, jobBenefits) = getJobDetail()

            yield JobItem(
                companyName='Zoomo',
                applicationUrl=applicationUrl,
                jobTitle=job.xpath('.//h2[@data-ui="job-title"]/span/text()').get(),
                location=job.xpath('.//span[@data-ui="job-location"]/text()').get(),
                jobDepartment=job.xpath('.//span[@data-ui="job-department"]/text()').get(),
                jobDescription=sanitizer.sanitize(
                    (jobDescription or '') + (jobRequirements or '') + (jobBenefits or '')
                ),
                isFullTime=job.xpath('.//span[@data-ui="job-type"]/text()').get() == 'Full time',
            )


class QuipSpider(GreenhouseSpider):
    companyName = 'quip'
    name = "quip"
    start_urls = [
        'https://boards.greenhouse.io/quip',
    ]


class QuartetHealthSpider(GreenhouseSpider):
    companyName = 'Quartet Health'
    name = "quartetHealth"
    start_urls = [
        'https://boards.greenhouse.io/quartethealth',
    ]


class ProdegeSpider(scrapy.Spider):
    name = "prodege"
    start_urls = [
        'http://jobs.jobvite.com/careers/prodege/jobs',
    ]

    def parse(self, response):
        allJobs = response.xpath('//div[@class="jv-wrapper"]')
        for department, jobTable in zip(allJobs.xpath('.//h3/text()'), allJobs.xpath('.//table[@class="jv-job-list"]')):
            yield from response.follow_all(jobTable.xpath('.//a'), callback=self.parseJob, meta={'jobDepartment': getStripOrNone(department.get())})

    def parseJob(self, response):
        jobDepartment = response.request.meta['jobDepartment']
        jobTitle = getStripOrNone(response.xpath('//h2[@class="jv-header"]/text()').get())
        locations = response.xpath('//p[@class="jv-job-detail-meta"]/text()')[1:]  # The first text item is the job department
        jobDescription = sanitizer.sanitize(response.xpath('//div[@class="jv-job-detail-description"]').get())
        for location in locations:
            location = getStripOrNone(location.get()) or ''
            location = ', '.join([l.strip() for l in location.split(',')])
            yield JobItem(
                companyName='Prodege',
                applicationUrl=response.url,
                jobTitle=jobTitle,
                location=location,
                jobDepartment=jobDepartment,
                jobDescription=jobDescription,
                isFullTime=True,
            )


class PilotSpider(GreenhouseSpider):
    companyName = 'Pilot'
    name = 'pilot'
    start_urls = [
        'https://boards.greenhouse.io/pilothq/',
    ]


class OnnaSpider(GreenhouseSpider):
    companyName = 'Onna'
    name = 'onna'
    start_urls = ['https://boards.greenhouse.io/onna']


class NomadHealthSpider(GreenhouseSpider):
    companyName = 'Nomad Health'
    name = 'nomadHealth'
    start_urls = ['https://boards.greenhouse.io/nomadhealth']


class MolocoSpider(GreenhouseSpider):
    companyName = 'Moloco'
    name = 'moloco'
    start_urls = ['https://boards.greenhouse.io/moloco']


class LiberisSpider(GreenhouseSpider):
    companyName = 'Liberis'
    name = 'liberis'
    start_urls = ['https://boards.greenhouse.io/liberis']


class KindbodySpider(GreenhouseSpider):
    companyName = 'Kindbody'
    name = 'kindbody'
    start_urls = ['https://boards.greenhouse.io/kindbody/']


class HavenlySpider(GreenhouseSpider):
    companyName = 'Havenly'
    name = 'havenly'
    start_urls = ['https://boards.greenhouse.io/havenly']


class GradleSpider(GreenhouseSpider):
    companyName = 'Gradle'
    name = 'gradle'
    start_urls = ['https://boards.greenhouse.io/gradle']


class ComplyAdvantageSpider(GreenhouseSpider):
    companyName = 'Comply Advantage'
    name = 'complyAdvantage'
    start_urls = ['https://boards.greenhouse.io/complyadvantage']


class BlockRenovationSpider(GreenhouseSpider):
    companyName = 'Block Renovation'
    name = 'blockRenovation'
    start_urls = ['https://boards.greenhouse.io/blockrenovation']


class LinkSquaresSpider(BreezySpider):
    companyName = 'LinkSquares'
    name = 'linkSquares'
    start_urls = ['https://linksquares.breezy.hr/']


class OutschoolSpider(LeverSpider):
    companyName = 'Outschool'
    name = 'outschool'
    start_urls = ['https://jobs.lever.co/outschool/']


class MediaflySpider(LeverSpider):
    companyName = 'Mediafly'
    name = 'mediafly'
    start_urls = ['https://jobs.lever.co/Mediafly/']


class KandjiSpider(LeverSpider):
    companyName = 'Kandji'
    name = 'kandji'
    start_urls = ['https://jobs.lever.co/kandji']


class JerrySpider(LeverSpider):
    companyName = 'Jerry'
    name = 'jerry'
    start_urls = ['https://jobs.lever.co/getjerry/']


class IroncladSpider(LeverSpider):
    companyName = 'Ironclad'
    name = 'ironclad'
    start_urls = ['https://jobs.lever.co/ironcladapp']


class HiveSpider(LeverSpider):
    companyName = 'Hive'
    name = 'hive'
    start_urls = ['https://jobs.lever.co/hive/']


class FountainSpider(LeverSpider):
    companyName = 'Fountain'
    name = 'fountain'
    start_urls = ['https://jobs.lever.co/fountain']


class FLYRLabsSpider(LeverSpider):
    companyName = 'FLYR Labs'
    name = 'flyr'
    start_urls = ['https://jobs.lever.co/flyrlabs']


class DISQOSpider(LeverSpider):
    companyName = 'DISQO'
    name = 'disqo'
    start_urls = ['https://jobs.lever.co/disqo']


class AttentiveSpider(LeverSpider):
    companyName = 'Attentive'
    name = 'attentive'
    start_urls = ['https://www.attentivemobile.com/careers']

    html = None
    driver = None

    def __init__(self):
        self.driver = getSelenium()
        self.driver.get('https://www.attentivemobile.com/careers')
        self.html = getWebElementHtml(self.driver, getWebElementWait(self.driver, '#lever-jobs-container'))
        super().__init__()

    def parse(self, response):
        resp = Selector(text=self.html)
        jobs = resp.xpath('//li[@class="lever-job"]//a')
        yield from response.follow_all(jobs, callback=self.parseJob)


class CurologySpider(LeverSpider):
    companyName = 'Curology'
    name = 'curology'
    start_urls = ['https://jobs.lever.co/curology']


class CoverGeniusSpider(LeverSpider):
    companyName = 'Cover Genius'
    name = 'covergenius'
    start_urls = ['https://jobs.lever.co/covergenius']


class BounteousSpider(LeverSpider):
    companyName = 'Bounteous'
    name = 'bounteous'
    start_urls = ['https://jobs.lever.co/bounteous']


class LeapSpider(JazzHRSpider):
    companyName = 'Leap'
    name = 'leap'
    start_urls = ['https://leap.applytojob.com/apply']


class FlorenceHealthcareSpider(JazzHRSpider):
    companyName = 'Florence Healthcare'
    name = 'florence'
    start_urls = ['https://florencehealthcare.applytojob.com/apply']


class AzaleaHealthSpider(JazzHRSpider):
    companyName = 'Azalea Health'
    name = 'azaleaHeath'
    start_urls = ['https://azaleahealth.theresumator.com/apply']


class ExabeamSpider(LeverSpider):
    companyName = 'Exabeam'
    name = 'exabeam'
    start_urls = ['https://jobs.lever.co/exabeam']
