from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.urls import reverse

from upapp.models import BlogPost, EmployerJob, Project, UserProfile


class Static_Sitemap(Sitemap):

    changefreq = 'yearly'

    def items(self):
        return [
            'index', 'about', 'contact', 'loginPage', 'privacy', 'projects',
            'signUp', 'termsOfService'
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item in ['index', 'projects', 'signUp']:
            return 1.0
        else:
            return 0.3


class Blog_Sitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(publishDate__lte=datetime.today())

    def location(self, blog):
        return f'/blog/{blog.id}/'

    def lastmod(self, blog):
        return blog.modifiedDateTime


class JobPosting_Sitemap(Sitemap):
    changefreq = 'hourly'
    priority = 1.0

    def items(self):
        jobFilter = Q(openDate__lte=datetime.today())
        jobFilter &= (Q(pauseDate__isnull=True) | Q(pauseDate__gte=datetime.today()))
        jobFilter &= (Q(closeDate__isnull=True) | Q(closeDate__gte=datetime.today()))
        return EmployerJob.objects.filter(jobFilter)

    def location(self, job):
        return f'/job-posting/{job.id}/'

    def lastmod(self, job):
        return job.modifiedDateTime


class Profile_Sitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return UserProfile.objects.filter(makePublic=True)

    def location(self, profile):
        return f'/profile/{profile.id}/'

    def lastmod(self, profile):
        return profile.modifiedDateTime


class Project_Sitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Project.objects.all()

    def location(self, project):
        return f'/project/{project.id}/'

    def lastmod(self, project):
        return project.modifiedDateTime


sitemaps = {
    'static': Static_Sitemap(),
    'blog': Blog_Sitemap(),
    'jobPosting': JobPosting_Sitemap(),
    'profile': Profile_Sitemap(),
    'project': Project_Sitemap()
}
