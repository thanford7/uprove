from datetime import datetime

from django.db.transaction import atomic
from psycopg2 import IntegrityError
from rest_framework import authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.apis import setSkills
from upapp.models import CustomProject, Employer, EmployerJob
from upapp.modelSerializers import getSerializedEmployer, getSerializedEmployerJob
import upapp.security as security
from upapp.utils import dataUtil, dateUtil


class EmployerView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, employerId=None):
        if employerId:
            isEmployer = security.isPermittedEmployer(request, employerId)
            data = getSerializedEmployer(self.getEmployer(employerId), isEmployer=isEmployer)
        else:
            data = [getSerializedEmployer(e, isEmployer=False) for e in self.getEmployers()]
        return Response(status=status.HTTP_200_OK, data=data)

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        try:
            employer = Employer(
                companyName=data['companyName'],
                logo=data.get('logo'),
                modifiedDateTime=datetime.utcnow(),
                createdDateTime=datetime.utcnow()
            )
            employer.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedEmployer(employer, isEmployer=True))
        except IntegrityError:
            return Response(f'Company with name={data["companyName"]} already exists.', status=status.HTTP_409_CONFLICT)

    @atomic
    def put(self, request, employerId=None):
        employerId = employerId or request.data.get('id')
        if not employerId:
            return Response('Employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        if not any((security.isPermittedAdmin(request), security.isPermittedEmployer(request, employerId))):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        employer = self.getEmployer(employerId)
        data = request.data
        try:
            dataUtil.setObjectAttributes(employer, request.data, {
                'companyName': None,
                'logo': None
            })
            employer.save()
            return Response(status=status.HTTP_200_OK, data=getSerializedEmployer(employer, isEmployer=True))
        except IntegrityError:
            return Response(f'Company with name={data["companyName"]} already exists.', status=status.HTTP_409_CONFLICT)

    def delete(self, request, employerId=None):
        employerId = employerId or request.data.get('id')
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not employerId:
            return Response('Employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        self.getEmployer(employerId).delete()
        return Response(status=status.HTTP_200_OK, data=employerId)

    @staticmethod
    def getEmployer(employerId):
        try:
            return Employer.objects.prefetch_related(
                'employerJob',
                'employerJob__allowedProjects',
                'employerJob__allowedProjects__skills',
                'employerJob__jobApplication',
                'employerJob__jobApplication__userProject',
                'employerJob__jobApplication__userProject__user',
                'employerJob__jobApplication__userProject__customProject',
                'employerJob__jobApplication__userProject__customProject__project',
                'employerJob__jobApplication__userProject__customProject__project__function',
                'employerJob__jobApplication__userProject__customProject__skills',
                'employerJob__jobApplication__userProject__files',
                'employerJob__jobApplication__userProject_videos',
                'employerJob__jobApplication__userProject__images',
            ).get(id=employerId)
        except Employer.DoesNotExist as e:
            raise e

    @staticmethod
    def getEmployers():
        return Employer.objects.all()


class JobPostingView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    @atomic
    def post(self, request):
        data = request.data
        if not security.isPermittedEmployer(request, data['employerId']):
            return Response('You do not have permission to post for this employer', status=status.HTTP_401_UNAUTHORIZED)

        employerJob = EmployerJob(
            employer_id=data['employerId'],
            jobTitle=data['jobTitle'],
            jobDescription=data['jobDescription'],
            openDate=dateUtil.deserializeDateTime(data.get('openDate'), dateUtil.FormatType.DATE, allowNone=True),
            salaryFloor=data.get('salaryFloor'),
            salaryCeiling=data.get('salaryCeiling'),
            salaryUnit=data.get('salaryUnit'),
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow()
        )
        employerJob.save()

        self.setCustomProjects(employerJob, data['allowedProjects'])

        return Response(status=status.HTTP_200_OK, data=getSerializedEmployerJob(self.getEmployerJob(employerJob.id), isEmployer=True))

    @atomic
    def put(self, request, jobId=None):
        data = request.data
        jobId = jobId or data['id']
        if not security.isPermittedEmployer(request, data['employerId']):
            return Response('You do not have permission to post for this employer', status=status.HTTP_401_UNAUTHORIZED)

        if not jobId:
            return Response('Job ID is required', status=status.HTTP_400_BAD_REQUEST)

        employerJob = self.getEmployerJob(jobId)
        dateGetter = lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE, allowNone=True)
        dataUtil.setObjectAttributes(employerJob, data, {
            'jobTitle': None,
            'jobDescription': None,
            'openDate': {'propFunc': dateGetter},
            'pauseDate': {'propFunc': dateGetter},
            'closeDate': {'propFunc': dateGetter},
            'salaryFloor': None,
            'salaryCeiling': None,
            'salaryUnit': None
        })
        employerJob.save()

        self.setCustomProjects(employerJob, data['allowedProjects'])
        return Response(status=status.HTTP_200_OK, data=getSerializedEmployerJob(self.getEmployerJob(employerJob.id), isEmployer=True))

    @atomic
    def delete(self, request, jobId=None):
        data = request.data
        jobId = jobId or data['id']

        if not jobId:
            return Response('Job ID is required', status=status.HTTP_400_BAD_REQUEST)

        job = self.getEmployerJob(jobId)

        if not security.isPermittedEmployer(request, job.employer_id):
            return Response('You do not have permission to delete for this employer', status=status.HTTP_401_UNAUTHORIZED)

        job.delete()
        return Response(status=status.HTTP_200_OK, data=jobId)

    @staticmethod
    def getEmployerJob(jobId):
        try:
            return EmployerJob.objects.prefetch_related(
                'allowedProjects',
                'allowedProjects__skills',
                'jobApplication',
                'jobApplication__userProject',
                'jobApplication__userProject__user',
                'jobApplication__userProject__customProject',
                'jobApplication__userProject__customProject__project',
                'jobApplication__userProject__customProject__project__function',
                'jobApplication__userProject__customProject__skills',
                'jobApplication__userProject__files',
                'jobApplication__userProject_videos',
                'jobApplication__userProject__images',
            ).get(id=jobId)
        except EmployerJob.DoesNotExist as e:
            raise e

    @staticmethod
    def getEmployerJobs(employerId):
        return EmployerJob.objects.prefetch_related(
            'allowedProjects',
            'allowedProjects__skills',
            'jobApplication',
            'jobApplication__userProject',
            'jobApplication__userProject__user',
            'jobApplication__userProject__customProject',
            'jobApplication__userProject__customProject__project',
            'jobApplication__userProject__customProject__project__function',
            'jobApplication__userProject__customProject__skills',
            'jobApplication__userProject__files',
            'jobApplication__userProject_videos',
            'jobApplication__userProject__images',
        ).filter(employer_id=employerId)

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
            cp.project_id,
            ','.join(skillIds),
            cp.skillLevelBit
        )

    @staticmethod
    def setCustomProjects(employerJob, allowedProjects, isClearExisting=True):
        existingCustomProjects = JobPostingView.getCustomProjects()
        if isClearExisting:
            employerJob.allowedProjects.clear()

        for customProjectData in allowedProjects:
            customProject = CustomProject(
                project_id=customProjectData['projectId'],
                skillLevelBit=customProjectData['skillLevelBit']
            )

            if not (existingCustomProject := existingCustomProjects.get(
                    JobPostingView.generateUniqueCustomProjectKey(customProject, skillIds=customProjectData['skillIds'])
                )
            ):
                customProject.save()
                setSkills(customProject, customProjectData['skillIds'])
            projectToAdd = existingCustomProject or customProject
            if projectToAdd.id in [ap.id for ap in employerJob.allowedProjects.all()]:
                continue
            employerJob.allowedProjects.add(projectToAdd)


class JobProjectLinkView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    @atomic
    def post(self, request, projectId):
        data = request.data
        if not data.get('jobIds'):
            return Response('Job ID is required', status=status.HTTP_400_BAD_REQUEST)

        jobs = EmployerJob.objects.filter(id__in=data['jobIds'])
        customProjectData = {'projectId': int(projectId), 'skillLevelBit': data['skillLevelBit'], 'skillIds': data['skillIds']}
        for job in jobs:
            if not security.isPermittedEmployer(request, job.employer_id):
                return Response('You do not have permission to alter this job', status=status.HTTP_401_UNAUTHORIZED)
            JobPostingView.setCustomProjects(job, [customProjectData], isClearExisting=False)

        user = security.getSessionUser(request)
        return Response(status=status.HTTP_200_OK,
                        data=[getSerializedEmployerJob(job, isEmployer=False) for job in JobPostingView.getEmployerJobs(user['employerId'])])