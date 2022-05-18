import os
import sys
from pathlib import Path

import django
from upapp.scraper.scraper.utils.geodict import LOCATIONS

sys.path.append(Path(__file__).resolve().parent.parent.parent.parent.parent.as_posix())
os.environ['DJANGO_SETTINGS_MODULE'] = 'up.settings'
django.setup()

from upapp.models import Country, EmployerJob, RoleLevel, State

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
    'Customer success manager': ['customer experience', 'customer success'],
    'Market research analyst': ['market research']
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
    roleLevels = {(r.role.name.lower(), r.roleLevelBit): r for r in RoleLevel.objects.prefetch_related('role').all()}

    for job in nonNormalizedJobs:
        job.roleLevel = normalizeJobTitle(job.jobTitle, roleLevels)

    EmployerJob.objects.bulk_update(nonNormalizedJobs, ['roleLevel'], 500)


def normalizeJobTitle(jobTitle, roleLevels):
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
            or ('head' in jobTitle)
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
            return roleLevels[('product management', 2)]
        else:
            return roleLevels[('product management', 1)]
    elif ('product ' in jobTitle) and ('marketing' in jobTitle):
        if isLeadershipRole:
            return roleLevels[('product marketing', 2)]
        else:
            return roleLevels[('product marketing', 1)]
    elif ('project manager' in jobTitle) or ('program manager' in jobTitle):
        if isLeadershipRole:
            return roleLevels[('project management', 2)]
        else:
            return roleLevels[('project management', 1)]
    elif ('account manager' in jobTitle) or ('account executive' in jobTitle):
        return roleLevels[('account management', 1)]
    elif ('market' in jobTitle) and (('research' in jobTitle) or ('analyst' in jobTitle)):
        return roleLevels[('market research', 1)]
    elif ('data' not in jobTitle) and (
            ('analyst' in jobTitle)
            or ('strategy' in jobTitle)
            or ('business operations' in jobTitle)
    ):
        if isManagerRole or isLeadershipRole:
            return roleLevels[('business analysis', 2)]
        else:
            return roleLevels[('business analysis', 1)]
    elif (
            ('engineer' not in jobTitle)
            and ('scien' not in jobTitle)
            and (('data analyst' in jobTitle) or ('analytics' in jobTitle))
    ):
        if isManagerRole or isLeadershipRole:
            return roleLevels[('data analysis', 2)]
        else:
            return roleLevels[('data analysis', 1)]
    elif (
            (('data' in jobTitle) or ('analytics' in jobTitle))
            and ('engineer' in jobTitle)
            and ('software engineer' not in jobTitle)
    ):
        if isManagerRole or isLeadershipRole:
            return roleLevels[('data analysis', 2)]
        else:
            return roleLevels[('data analysis', 1)]
    elif ('customer success' in jobTitle) or ('success manager' in jobTitle):
        if isLeadershipRole:
            return roleLevels[('customer success', 2)]
        else:
            return roleLevels[('customer success', 2)]
    elif ('operations' in jobTitle):
        if isLeadershipRole or isManagerRole:
            return roleLevels[('business analysis', 2)]
        elif ('business' in jobTitle):
            return roleLevels[('business analysis', 1)]
