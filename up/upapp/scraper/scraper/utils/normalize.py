import os
import sys
from pathlib import Path

import django
from upapp.scraper.scraper.utils.geodict import LOCATIONS

sys.path.append(Path(__file__).resolve().parent.parent.parent.parent.parent.as_posix())
os.environ['DJANGO_SETTINGS_MODULE'] = 'up.settings'
django.setup()

from upapp.models import EmployerJob

locationUpdateFields = ['isRemote', 'city', 'state', 'country', 'region']
ROLE_PROJECT_MAP = {
    'Product management leader': ['product management'],
    'Product manager': ['product management'],
    'Product marketing management leader': ['market research', 'product marketing'],
    'Product marketing manager': ['market research', 'product marketing'],
    'Project management leader': ['project management'],
    'Project manager': ['project management'],
    'Account manager': [],
    'Strategy and operations leader': ['business analysis', 'operations management'],
    'Business analyst': ['business analysis', 'operations management'],
    'Data analytics leader': [],
    'Data analyst': [],
    'Data engineering manager': [],
    'Data engineer': [],
    'Customer success leader': ['customer experience', 'customer success'],
    'Customer success manager': ['customer experience', 'customer success']
}


def normalizeLocations():
    nonNormalizedJobs = EmployerJob.objects.filter(
        isScraped=True,
        location__isnull=False,
        isRemote__isnull=True
    )

    for job in nonNormalizedJobs:
        if not (normalizedFields := LOCATIONS.get(job.location)):
            continue

        for updateField in locationUpdateFields:
            setattr(job, updateField, normalizedFields[updateField])

    EmployerJob.objects.bulk_update(nonNormalizedJobs, locationUpdateFields, 500)


def normalizeJobTitles():
    nonNormalizedJobs = EmployerJob.objects.filter(
        isScraped=True,
        # role__isnull=True
    )

    for job in nonNormalizedJobs:
        if not job.jobTitle:
            continue
        job.role = None
        jobTitle = job.jobTitle.lower()
        isManagerRole = 'manager' in jobTitle
        isLeadershipRole = (
                ('vp' in jobTitle)
                or ('vice president' in jobTitle)
                or ('director' in jobTitle)
                or ('principal' in jobTitle)
                or ('lead' in jobTitle)
        )

        if (
                ('product ' in jobTitle)
                and ('design' not in jobTitle)
                and ('product marketing' not in jobTitle)
                and ('product specialist' not in jobTitle)
                and ('product analyst' not in jobTitle)
                and ('engineer' not in jobTitle)
        ):
            if isLeadershipRole:
                job.role = 'Product management leader'
            else:
                job.role = 'Product manager'
        elif ('product ' in jobTitle) and ('marketing' in jobTitle):
            if isLeadershipRole:
                job.role = 'Product marketing management leader'
            else:
                job.role = 'Product marketing manager'
        elif ('project manager' in jobTitle) or ('program manager' in jobTitle):
            if isLeadershipRole:
                job.role = 'Project management leader'
            else:
                job.role = 'Project manager'
        elif ('account manager' in jobTitle) or ('account executive' in jobTitle):
            job.role = 'Account manager'
        elif ('data' not in jobTitle) and (
                ('analyst' in jobTitle)
                or ('strategy' in jobTitle)
                or ('business operations' in jobTitle)
        ):
            if isManagerRole or isLeadershipRole:
                job.role = 'Strategy and operations leader'
            else:
                job.role = 'Business analyst'
        elif (
                ('engineer' not in jobTitle)
                and ('scien' not in jobTitle)
                and (('data analyst' in jobTitle) or ('analytics' in jobTitle))
        ):
            if isManagerRole or isLeadershipRole:
                job.role = 'Data analytics leader'
            else:
                job.role = 'Data analyst'
        elif (
                (('data' in jobTitle) or ('analytics' in jobTitle))
                and ('engineer' in jobTitle)
                and ('software engineer' not in jobTitle)
        ):
            if isManagerRole or isLeadershipRole:
                job.role = 'Data engineering manager'
            else:
                job.role = 'Data engineer'
        elif ('customer success' in jobTitle) or ('success manager' in jobTitle):
            if isLeadershipRole:
                job.role = 'Customer success leader'
            else:
                job.role = 'Customer success manager'
        elif ('operations' in jobTitle):
            if isLeadershipRole or isManagerRole:
                job.role = 'Strategy and operations leader'
            elif ('business' in jobTitle):
                job.role = 'Business analyst'

    EmployerJob.objects.bulk_update(nonNormalizedJobs, ['role'], 500)

# normalizeLocations()
# normalizeJobTitles()
