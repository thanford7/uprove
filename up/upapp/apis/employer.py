from collections import defaultdict

from django.db.models import Q
from django.db.transaction import atomic
from django.utils import timezone
from psycopg2 import IntegrityError
from rest_framework import authentication, status
from rest_framework.response import Response

from upapp.apis.lever import getLeverRequestWithRefresh
from upapp.apis import UproveAPIView
from upapp.apis.project import ProjectView
from upapp.models import *
from upapp.modelSerializers import getSerializedEmployer, getSerializedEmployerJob, \
    getSerializedOrganization, CUSTOMER_SUCCESS_ROLE_IDS
import upapp.security as security
from upapp.utils import dataUtil, dateUtil


class EmployerView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, employerId=None):
        if employerId:
            data = getSerializedEmployer(self.getEmployer(employerId), employerId=employerId)
        elif searchText := self.data.get('search'):
            searchText = searchText[0]
            employerFilter = Q(companyName__iregex=f'^.*{searchText}.*$')
            data = [getSerializedEmployer(e) for e in self.getEmployers(employerFilter)]
        else:
            data = [getSerializedEmployer(e) for e in self.getEmployers()]
        return Response(status=status.HTTP_200_OK, data=data)

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        employer = Employer(createdDateTime=timezone.now())
        self.updateEmployer(employer)

        return Response(status=status.HTTP_200_OK, data=getSerializedEmployer(employer, employerId=employer.id))

    @atomic
    def put(self, request, employerId=None):
        employerId = employerId or request.data.get('id')
        if not employerId:
            return Response('Employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        if not any((security.isPermittedAdmin(request), security.isPermittedEmployer(request, employerId))):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        employer = self.getEmployer(employerId)
        self.updateEmployer(employer)

        return Response(status=status.HTTP_200_OK, data=getSerializedEmployer(employer, employerId=employerId))

    @atomic
    def delete(self, request, employerId=None):
        employerId = employerId or request.data.get('id')
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not employerId:
            return Response('Employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        self.getEmployer(employerId).delete()
        return Response(status=status.HTTP_200_OK, data=employerId)

    @atomic
    def updateEmployer(self, employer):
        try:
            dataUtil.setObjectAttributes(employer, self.data, {
                'companyName': None,
                'logo': {'isProtectExisting': True},
                'description': None,
                'companySize_id': {'formName': 'companySizeId'},
                'glassDoorUrl': None,
                'isDemo': {'isProtectExisting': True},
                'isClient': {'isProtectExisting': True}
            })
            employer.save()
        except IntegrityError:
            raise ValueError(f'Company with name={self.data["companyName"]} already exists.')


    @staticmethod
    def getEmployer(employerId):
        try:
            return Employer.objects.prefetch_related(
                'employerJob',
                'employerJob__jobApplication'
            ).get(id=employerId)
        except Employer.DoesNotExist as e:
            raise e

    @staticmethod
    def getEmployers(filter=None):
        filter = filter or Q()
        return Employer.objects.filter(filter)


class EmployerCandidateFavoriteView(UproveAPIView):

    def post(self, request):
        employerId = self.data.get('employerId')
        if not security.isPermittedEmployer(request, employerId):
            return Response('You do not have permission to edit this employer', status=status.HTTP_401_UNAUTHORIZED)

        if not (candidateId := self.data.get('candidateId')):
            return Response('A candidate ID is required', status=status.HTTP_400_BAD_REQUEST)

        try:
            candidateFavorite = EmployerCandidateFavorite.objects.get(
                employer_id=employerId, candidate_id=candidateId
            )
            for job in candidateFavorite.jobs.all():
                candidateFavorite.remove(job)
        except EmployerCandidateFavorite.DoesNotExist:
            candidateFavorite = EmployerCandidateFavorite(
                employer_id=employerId,
                candidate_id=candidateId,
                createDate=timezone.now().date()
            )
            candidateFavorite.save()

        for jobId in self.data.get('jobIds', []):
            candidateFavorite.jobs.add(jobId)


class JobPostingView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permittedCountries = ['USA', 'UK', 'Canada']
    permittedRoles = ['customer success', 'account manage', 'customer experience']

    def get(self, request):
        customProjects = CustomProject.objects.select_related('project').all()
        if jobId := self.data.get('id'):
            return Response(
                status=status.HTTP_200_OK,
                data=getSerializedEmployerJob(self.getEmployerJobs(jobId=jobId), customProjects=customProjects)
            )

        if employerId := self.data.get('employerId'):
            employerId = employerId[0]
            if not (security.isPermittedEmployer(request, employerId) or self.isAdmin):
                return Response('You do not have permission to view this employer', status=status.HTTP_401_UNAUTHORIZED)
            jobFilter = Q()
            if searchText := self.data.get('search'):
                searchText = searchText[0]
                jobFilter = Q(jobTitle__iregex=f'^.*{searchText}.*$')
            return Response(
                status=status.HTTP_200_OK,
                data=[
                    getSerializedEmployerJob(j, customProjects=customProjects)
                    for j in self.getEmployerJobs(employerId=employerId, jobFilter=jobFilter)
                ]
            )

    @atomic
    def post(self, request):
        if not (security.isPermittedEmployer(request, self.data['employerId']) or self.isAdmin):
            return Response('You do not have permission to post for this employer', status=status.HTTP_401_UNAUTHORIZED)

        employerJob = EmployerJob(
            employer_id=self.data['employerId'],
            modifiedDateTime=timezone.now(),
            createdDateTime=timezone.now()
        )
        self.updateEmployerJob(employerJob)
        customProjects = CustomProject.objects.select_related('project').all()
        return Response(status=status.HTTP_200_OK,
                        data=getSerializedEmployerJob(
                            self.getEmployerJobs(jobId=employerJob.id),
                            employerId=employerJob.employer_id,
                            customProjects=customProjects
                        ))

    @atomic
    def put(self, request, jobId=None):
        jobId = jobId or self.data['id']
        if not (security.isPermittedEmployer(request, self.data['employerId']) or self.isAdmin):
            return Response('You do not have permission to post for this employer', status=status.HTTP_401_UNAUTHORIZED)

        if not jobId:
            return Response('Job ID is required', status=status.HTTP_400_BAD_REQUEST)

        employerJob = self.getEmployerJobs(jobId=jobId)
        self.updateEmployerJob(employerJob)
        customProjects = CustomProject.objects.select_related('project').all()
        return Response(status=status.HTTP_200_OK,
                        data=getSerializedEmployerJob(
                            self.getEmployerJobs(jobId=employerJob.id),
                            employerId=employerJob.employer_id,
                            customProjects=customProjects
                        ))

    @atomic
    def delete(self, request, jobId=None):
        jobId = jobId or self.data['id']

        if not jobId:
            return Response('Job ID is required', status=status.HTTP_400_BAD_REQUEST)

        job = self.getEmployerJobs(jobId=jobId)

        if not security.isPermittedEmployer(request, job.employer_id):
            return Response('You do not have permission to delete for this employer',
                            status=status.HTTP_401_UNAUTHORIZED)

        job.delete()
        return Response(status=status.HTTP_200_OK, data=jobId)

    @atomic
    def updateEmployerJob(self, employerJob):

        # Hard coding customer success as the role
        employerJob.roleLevel = self.getCustomerSuccessRoleLevel()

        dateGetter = lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE, allowNone=True)
        dataUtil.setObjectAttributes(employerJob, self.data, {
            'jobTitle': None,
            'jobDescription': None,
            'openDate': {'propFunc': dateGetter},
            'pauseDate': {'propFunc': dateGetter},
            'closeDate': {'propFunc': dateGetter},
            'salaryFloor': None,
            'salaryCeiling': None,
            'city': None,
            'isRemote': None,
            'state_id': {'formName': 'stateId'},
            'country_id': {'formName': 'countryId'},
        })
        employerJob.save()

    @staticmethod
    def getCustomerSuccessRoleLevel():
        # Hard coding customer success as the role
        customerSuccessRole = Role.objects.get(name='Customer Success')
        return RoleLevel.objects.get(role=customerSuccessRole, roleLevelBit=RoleLevel.Level.ENTRY.value)

    @staticmethod
    def getEmployerJobs(jobId=None, employerId=None, jobFilter=None, isIncludeDemo=False):
        jobFilter = jobFilter or Q()
        if jobId:
            jobFilter &= Q(id=jobId)
        else:
            if employerId:
                jobFilter &= Q(employer_id=employerId)
            elif not isIncludeDemo:
                jobFilter &= Q(employer__isDemo=False)

        jobs = EmployerJob.objects\
            .select_related(
                'state',
                'country',
                'roleLevel',
                'roleLevel__role',
                'employer',
                'employer__companySize'
            )\
            .prefetch_related(
                'jobApplication',
            )\
            .filter(jobFilter)\

        if jobId:
            if not jobs:
                raise EmployerJob.DoesNotExist
            return jobs[0]

        return jobs

    @staticmethod
    def getEmployerJobFilter(isIncludeClosed=False, isEmployer=False):
        filter = Q()
        if not isIncludeClosed:
            filter &= Q(openDate__lte=timezone.now().date()) & (
                Q(closeDate__isnull=True) | Q(closeDate__gt=timezone.now().date())
            ) & (
                Q(pauseDate__isnull=True) | Q(pauseDate__gt=timezone.now().date())
            )

        if not isEmployer:
            filter &= Q(isInternal=False)
            filter &= Q(country__isnull=True) | Q(country__countryName__in=JobPostingView.permittedCountries)
            filter &= Q(roleLevel__isnull=False)

            roleFilter = Q()
            for roleName in JobPostingView.permittedRoles:
                roleFilter |= Q(roleLevel__role__name__iregex=roleName)

            filter &= roleFilter

        return filter

    @staticmethod
    def getProjectsByRoleIdMap():
        projectsByRole = defaultdict(list)
        for project in ProjectView.getProjects():
            if project.role_id in CUSTOMER_SUCCESS_ROLE_IDS:
                for id in CUSTOMER_SUCCESS_ROLE_IDS:
                    projectsByRole[id].append(project)
            else:
                projectsByRole[project.role_id].append(project)

        return projectsByRole

    @staticmethod
    def getCustomProjects(asDict=True):
        customProjects = CustomProject.objects.prefetch_related('skills').all()
        if asDict:
            customProjects = {JobPostingView.generateUniqueCustomProjectKey(cp): cp for cp in customProjects}

        return customProjects

    @staticmethod
    def generateUniqueCustomProjectKey(cp, skillIds=None):
        skillIds = [str(id) for id in skillIds] if skillIds else [str(s.id) for s in cp.skills.all()]
        skillIds.sort()
        return (
            cp.project_id if hasattr(cp, 'project_id') else cp.id,
            ','.join(skillIds),
            cp.skillLevelBit if hasattr(cp, 'skillLevelBit') else 1
        )


class UserProjectEvaluationView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    @atomic
    def put(self, request):
        from upapp.apis.user import UserProjectView  # Avoid circular import
        if not any([self.isAdmin, self.isEmployer]):
            return Response('You are not permitted to evaluate this project', status=status.HTTP_401_UNAUTHORIZED)

        if not (userProjectId := self.data.get('userProjectId')):
            return Response('A user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        existingEvaluationCriteria = {upec.id: upec for upec in UserProjectEvaluationCriterion.objects.filter(userProject_id=userProjectId)}
        for evaluationCriterionData in self.data.get('evaluationCriteria'):
            if evaluationCriterion := existingEvaluationCriteria.get(evaluationCriterionData['id']):
                isChanged = dataUtil.setObjectAttributes(evaluationCriterion, evaluationCriterionData, {
                    'value': None
                })
                if isChanged:
                    evaluationCriterion.save()
            else:
                UserProjectEvaluationCriterion(
                    userProject_id=userProjectId,
                    employer_id=self.user.employer_id if not self.isAdmin else None,
                    evaluator_id=self.data['evaluatorId'],
                    evaluationCriterion_id=evaluationCriterionData['id'],
                    value=evaluationCriterionData.get('value', 0),
                    createdDateTime=timezone.now(),
                    modifiedDateTime=timezone.now()
                ).save()

        userProject = UserProjectView.getUserProjects(userProjectId=userProjectId)
        for app in userProject.jobApplication.all():
            if app.leverOpportunityKey:
                employer = EmployerView.getEmployer(app.employerJob.employer_id)
                getLeverRequestWithRefresh(
                    employer,
                    f'opportunities/{app.leverOpportunityKey}/addTags',
                    bodyCfg={
                        'tags': ['uprove-assessment-scored']},
                    isJSON=True,
                    method='POST'
                )

        return Response(status=status.HTTP_200_OK)


class OrganizationView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request):
        if id := self.data.get('id'):
            try:
                org = Organization.objects.get(id=id)
                return Response(status=status.HTTP_200_OK, data=getSerializedOrganization(org))
            except Organization.DoesNotExist as e:
                raise e
        elif search := self.data.get('search'):
            q = Q(name__iregex=f'^.*{search}.*$')

            if orgTypes := self.data.get('orgType'):
                q &= Q(orgType__in=orgTypes)

            orgs = Organization.objects.filter(q)
            return Response(status=status.HTTP_200_OK, data=[getSerializedOrganization(o) for o in orgs])

    @staticmethod
    @atomic
    def updateOrCreateOrg(data):
        try:
            org = Organization.objects.get(name=data['name'], orgType=data['orgType'])
        except Organization.DoesNotExist:
            org = Organization()

        if newLogo := data.get('newLogo'):
            org.logo = newLogo

        dataUtil.setObjectAttributes(org, data, {
            'name': None,
            'orgType': None,
            'user_id':  {'formName': 'userId'}
        })
        org.save()
        return org
