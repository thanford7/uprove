import os
import sys
from pathlib import Path

import django
from upapp.scraper.scraper.utils.geodict import LOCATIONS

sys.path.append(Path(__file__).resolve().parent.parent.parent.parent.parent.as_posix())
os.environ['DJANGO_SETTINGS_MODULE'] = 'up.settings'
django.setup()

from upapp.models import Country, EmployerJob, RoleTitle, State

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
        location__isnull=False
    )

    states = {s.stateName: s for s in State.objects.all()}
    countries = {c.countryName: c for c in Country.objects.all()}

    for job in nonNormalizedJobs:
        if not (normalizedFields := LOCATIONS.get(job.location)):
            continue

        stateStr = normalizedFields['state']
        if stateStr and stateStr not in states:
            newState = State(stateName=stateStr)
            newState.save()
            states[newState.stateName] = newState
        job.state = states[stateStr] if stateStr else None

        countryStr = normalizedFields['country']
        if countryStr and countryStr not in countries:
            newCountry = Country(countryName=countryStr)
            newCountry.save()
            countries[newCountry.countryName] = newCountry
        job.country = countries[countryStr] if countryStr else None

        for updateField in locationUpdateFields:
            if updateField in ['state', 'country']:
                continue
            setattr(job, updateField, normalizedFields[updateField])

    EmployerJob.objects.bulk_update(nonNormalizedJobs, locationUpdateFields, 500)


def normalizeJobTitles(employerJobs=None):
    nonNormalizedJobs = employerJobs or EmployerJob.objects.filter(
        isScraped=True,
        # role__isnull=True
    )
    roleTitles = {r.roleTitle: r for r in RoleTitle.objects.all()}

    for job in nonNormalizedJobs:
        job.role = normalizeJobTitle(job.jobTitle, roleTitles)

    EmployerJob.objects.bulk_update(nonNormalizedJobs, ['role'], 500)


def normalizeJobTitle(jobTitle, roleTitles):
    if not jobTitle:
        return None
    jobTitle = jobTitle.lower()
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
            return roleTitles['Product management leader']
        else:
            return roleTitles['Product manager']
    elif ('product ' in jobTitle) and ('marketing' in jobTitle):
        if isLeadershipRole:
            return roleTitles['Product marketing management leader']
        else:
            return roleTitles['Product marketing manager']
    elif ('project manager' in jobTitle) or ('program manager' in jobTitle):
        if isLeadershipRole:
            return roleTitles['Project management leader']
        else:
            return roleTitles['Project manager']
    elif ('account manager' in jobTitle) or ('account executive' in jobTitle):
        return roleTitles['Account manager']
    # TODO: Add market research analyst
    elif ('data' not in jobTitle) and (
            ('analyst' in jobTitle)
            or ('strategy' in jobTitle)
            or ('business operations' in jobTitle)
    ):
        if isManagerRole or isLeadershipRole:
            return roleTitles['Strategy and operations leader']
        else:
            return roleTitles['Business analyst']
    elif (
            ('engineer' not in jobTitle)
            and ('scien' not in jobTitle)
            and (('data analyst' in jobTitle) or ('analytics' in jobTitle))
    ):
        if isManagerRole or isLeadershipRole:
            return roleTitles['Data analytics leader']
        else:
            return roleTitles['Data analyst']
    elif (
            (('data' in jobTitle) or ('analytics' in jobTitle))
            and ('engineer' in jobTitle)
            and ('software engineer' not in jobTitle)
    ):
        if isManagerRole or isLeadershipRole:
            return roleTitles['Data engineering manager']
        else:
            return roleTitles['Data engineer']
    elif ('customer success' in jobTitle) or ('success manager' in jobTitle):
        if isLeadershipRole:
            return roleTitles['Customer success leader']
        else:
            return roleTitles['Customer success manager']
    elif ('operations' in jobTitle):
        if isLeadershipRole or isManagerRole:
            return roleTitles['Strategy and operations leader']
        elif ('business' in jobTitle):
            return roleTitles['Business analyst']

# normalizeLocations()
# normalizeJobTitles()
