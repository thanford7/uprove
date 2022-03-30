import scrapy
from django.utils import timezone
from html_sanitizer import Sanitizer
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from scraper.items import JobItem
from scraper.utils.seleniumSetup import getDomElOrNone, getSelenium, getWebElementHtml, getWebElementWait,\
    retryClick, WEBDRIVER_WAIT_SECONDS


sanitizer = Sanitizer()


class Barn2DoorSpider(scrapy.Spider):
    name = "barn2Door"
    start_urls = [
        'https://barn2door-inc.breezy.hr/?',
    ]

    def parse(self, response):
        yield from response.follow_all(css='.positions-container li a', callback=self.parseJob)  # can pass meta data with meta={}

    def parseJob(self, response):
        # can get meta data with response.request.meta[]
        summaryHtml = response.xpath('//div[@class="banner"]')

        yield JobItem(
            companyName='Barn2Door',
            applicationUrl=response.url,
            jobTitle=summaryHtml.xpath('.//h1/text()').get(),
            location=summaryHtml.xpath('.//li[@class="location"]/span/text()').get(),
            jobDepartment=summaryHtml.xpath('.//li[@class="department"]/span/text()').get(),
            jobDescription=sanitizer.sanitize(response.xpath('//div[@class="description"]').get()),
            isFullTime=summaryHtml.xpath('.//li[@class="type"]/span/text()').get() == '%LABEL_POSITION_TYPE_FULL_TIME%',
        )


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
