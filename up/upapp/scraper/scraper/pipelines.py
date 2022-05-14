# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django.utils import timezone

from scraper.utils.normalize import normalizeLocations, normalizeJobTitles
from upapp.models import Employer, EmployerJob


class ScraperPipeline:
    employers = None
    scrapedEmployers = None
    jobUpdateAttributes = ['applicationUrl', 'jobDepartment', 'jobDescription']

    def open_spider(self, spider):
        self.employers = {employer.companyName: {
            'employer': employer,
            'jobs': {self.generateJobKey(j): j for j in employer.employerJob.all() if j.isScraped},
            'foundJobs': set()
        } for employer in Employer.objects.prefetch_related('employerJob').all()}
        self.scrapedEmployers = set()

    def close_spider(self, spider):
        # Set the close date of a job if it no longer exists on the employers job page
        for employerData in self.employers.values():
            if employerData['employer'].companyName not in self.scrapedEmployers:
                continue
            for jobKey, job in employerData['jobs'].items():
                if jobKey not in employerData['foundJobs'] and not job.closeDate:
                    job.closeDate = timezone.now().date()
                    job.save()

        # Update location attributes (e.g. city)
        normalizeLocations()
        normalizeJobTitles()

        if driver := getattr(spider, 'driver', None):
            driver.close()

    def process_item(self, item, spider):
        companyName = item['companyName']
        employerData = self.employers.get(companyName)
        if not employerData:
            employer = Employer(companyName=companyName, createdDateTime=timezone.now(), modifiedDateTime=timezone.now())
            employer.save()
            self.employers[companyName] = {
                'employer': employer,
                'jobs': {},
                'foundJobs': set()
            }
        else:
            employer = employerData['employer']
        self.scrapedEmployers.add(companyName)

        if not item['isFullTime']:
            return item

        newJob = EmployerJob(
            jobTitle=item['jobTitle'],
            location=item['location'],
            isScraped=True,
            createdDateTime=timezone.now()
        )
        if not (job := employerData['jobs'].get(self.generateJobKey(newJob))):
            newJob.employer = employer
            self.updateJob(newJob, item)
            employerData['jobs'][self.generateJobKey(newJob)] = newJob
            job = newJob
        else:
            self.updateJob(job, item)

        employerData['foundJobs'].add(self.generateJobKey(job))

        return item

    def isSameJob(self, job, jobData):
        for attr in self.jobUpdateAttributes:
            if getattr(job, attr) != jobData.get(attr):
                return False

        if not job.openDate:
            return False

        if job.closeDate:
            return False

        return True

    def updateJob(self, job, jobData):
        if self.isSameJob(job, jobData):
            return job

        for attr in self.jobUpdateAttributes:
            setattr(job, attr, jobData.get(attr))

        job.openDate = job.openDate or timezone.now().date()
        job.closeDate = None
        job.modifiedDateTime = timezone.now()
        job.save()
        return job

    @staticmethod
    def generateJobKey(job):
        return (job.jobTitle, job.location)
