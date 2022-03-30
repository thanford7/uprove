# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import os
import sys
from pathlib import Path

import django
from scrapy_djangoitem import DjangoItem
from scrapy.item import Item, Field

sys.path.append(Path(__file__).resolve().parent.parent.parent.parent.as_posix())
os.environ['DJANGO_SETTINGS_MODULE'] = 'up.settings'
django.setup()

from upapp.models import Employer, EmployerJob


class EmployerJobItem(DjangoItem):
    django_model = EmployerJob


class EmployerItem(DjangoItem):
    django_model = Employer


class JobItem(Item):
    companyName = Field()
    applicationUrl = Field()
    jobTitle = Field()
    location = Field()
    jobDepartment = Field()
    jobDescription = Field()
    isFullTime = Field()
