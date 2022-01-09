import os
from datetime import datetime
from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User as DjangoUser
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from django.db.transaction import atomic
from django.template import loader
from django.templatetags.static import static
from django.utils import crypto
from rest_framework import status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

from upapp import security
from upapp.apis import UproveAPIView
from upapp.models import *
from upapp.modelSerializers import getSerializedUser, getSerializedJobApplication, getSerializedUserProject
from upapp.utils import dataUtil, dateUtil

__all__ = [
    'OrganizationView', 'UserVideoView', 'UserFileView', 'UserImageView', 'UserEducationItemView',
    'UserExperienceItemView', 'UserContentItemView', 'UserView', 'UserProfileView', 'UserProjectView'
]


class OrganizationView(APIView):
    def post(self, request):
        pass

    def put(self, request, educationId):
        pass

    @staticmethod
    def getOrganization(orgId):
        try:
            return Organization.objects.get(id=orgId)
        except Organization.DoesNotExist as e:
            raise e


class UserVideoView(APIView):
    def post(self, request):
        pass

    def put(self, request, videoId):
        pass

    @staticmethod
    def getVideo(videoId):
        try:
            return UserVideo.objects.get(id=videoId)
        except UserVideo.DoesNotExist as e:
            raise e


class UserFileView(APIView):
    def post(self, request):
        pass

    def put(self, request, fileId):
        pass

    @staticmethod
    def getFile(fileId):
        try:
            return UserFile.objects.get(id=fileId)
        except UserFile.DoesNotExist as e:
            raise e


class UserImageView(APIView):
    def post(self, request):
        pass

    def put(self, request, imageId):
        pass

    @staticmethod
    def getImage(imageId):
        try:
            return UserImage.objects.get(id=imageId)
        except UserImage.DoesNotExist as e:
            raise e


class UserEducationItemView(APIView):
    def post(self, request):
        pass

    def put(self, request, educationId):
        pass

    @staticmethod
    def getEducationItem(educationId):
        try:
            return UserEducation.objects.select_related('school').get(id=educationId)
        except UserEducation.DoesNotExist as e:
            raise e


class UserExperienceItemView(APIView):
    def post(self, request):
        pass

    def put(self, request, experienceId):
        pass

    @staticmethod
    def getExperienceItem(experienceId):
        try:
            return UserExperience.objects.select_related('organization').get(id=experienceId)
        except UserExperience.DoesNotExist as e:
            raise e


class UserContentItemView(APIView):

    def post(self, request):
        pass

    def put(self, request, contentId):
        pass

    @staticmethod
    def getContentItem(contentId):
        try:
            return UserContentItem.objects.prefetch_related('section', 'section__contentObject').get(id=contentId)
        except UserExperience.DoesNotExist as e:
            raise e


class UserView(UproveAPIView):

    def get(self, request, userId=None):
        return Response(getSerializedUser(self.getUser(userId)), status=status.HTTP_200_OK)

    @atomic
    def put(self, request, userId=None):
        from upapp.viewsAuth import setUproveUser

        userId = userId or request.data.get('id')
        if not userId:
            return Response('User ID is required to perform this operation', status=status.HTTP_400_BAD_REQUEST)
        if not (security.isPermittedAdmin(request) or security.isSelf(request, userId)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = self.getUser(userId)
        self.updateUser(user, request.data)
        currentUproveUser = security.getSessionUser(request)
        if security.isSelf(request, userId) or not currentUproveUser:
            setUproveUser(request, user.djangoUser)
        return Response(getSerializedUser(user), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        try:
            user, hasPassword = self.createUser(request.data, security.isPermittedAdmin(request))
        except IntegrityError:
            return Response((
                f'User with email={self.data["email"]} already exists. If you forgot your password, ' +
                'please use the \'reset password\' link in the sign in menu.'
            ), status=status.HTTP_409_CONFLICT)
        if not hasPassword:
            self.sendPasswordResetEmail(request, user.email, {
                'subject_template_name': 'email/newUserPasswordEmailSubject.txt',
                'email_template_name': 'email/newUserPasswordBody.html',
                'html_email_template_name': 'email/newUserPassword.html',
                'extra_email_context': {
                    'supportEmail': 'community@uprove.co'
                }
            })

        return Response(status=status.HTTP_200_OK, data=getSerializedUser(user))

    @atomic
    def delete(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not (userId := request.data.get('id')):
            return Response('User ID is required to perform this operation', status=status.HTTP_400_BAD_REQUEST)

        user = self.getUser(userId)
        if user.djangoUser.is_superuser:
            user.djangoUser.is_active = False
            return Response('Super user deactivated, but not deleted', status=status.HTTP_200_OK)

        user.djangoUser.delete()
        user.delete()
        return Response(status=status.HTTP_200_OK, data=userId)

    @staticmethod
    def sendPasswordResetEmail(request, email, emailCfg):
        reset_form = UprovePasswordResetForm({'email': email})
        assert reset_form.is_valid()
        reset_form.save(
            request=request,
            **emailCfg
        )

    @staticmethod
    def getUser(userId):
        try:
            return User.objects\
                .select_related('djangoUser')\
                .prefetch_related(
                    'profile',
                    'profile__section',
                    'profile__section__sectionItem',
                    'profile__section__sectionItem__contentObject',
                    'education',
                    'experience',
                    'contentItem',
                    'contentItem__section',
                    'video',
                    'file',
                    'image',
                    'tag'
                )\
                .get(id=userId)
        except User.DoesNotExist as e:
            raise e

    @staticmethod
    def getUserProfiles(userId):
        try:
            return User.objects\
                .select_related('djangoUser')\
                .prefetch_related(
                    'profile'
                    'profile__section',
                    'profile__section__sectionItem',
                    'profile__section__sectionItem__contentObject',
                    'education',
                    'experience',
                    'contentItem',
                    'contentItem__section',
                    'video',
                    'file',
                    'image',
                    'tag'
                )\
                .get(id=userId)
        except User.DoesNotExist as e:
            raise e

    @staticmethod
    def getUsers():
        return User.objects.select_related('djangoUser').prefetch_related('image').all()

    @staticmethod
    def updateUser(user, data):
        dataUtil.setObjectAttributes(user, data, {
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'birthDate': {'propFunc': lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE, allowNone=True)},
            'email': None,
            'userTypeBits': None,
            'employer_id': {'formName': 'employerId'}
        })
        user.save()

        dataUtil.setObjectAttributes(user.djangoUser, data, {
            'is_staff': {'formName': 'isStaff', 'isIgnoreExcluded': True},
            'is_active': {'formName': 'isActive', 'isIgnoreExcluded': True},
            'is_superuser': {'formName': 'isSuperUser', 'isIgnoreExcluded': True}
        })
        user.djangoUser.save()

    @staticmethod
    def createUser(data, isAdmin=False):
        password = data.get('password', None)
        djangoUserKwargs = dict(
            email=data['email'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            password=password or generatePassword()
        )
        if isAdmin and data.get('isSuperUser'):
            djangoUser = DjangoUser.objects.create_superuser(data['email'], **djangoUserKwargs)
        else:
            djangoUserKwargs['is_staff'] = data.get('isStaff', False) if isAdmin else False
            djangoUser = DjangoUser.objects.create_user(data['email'], **djangoUserKwargs)

        user = User(
            djangoUser=djangoUser,
            firstName=data['firstName'],
            middleName=data.get('middleName'),
            lastName=data['lastName'],
            birthDate=dateUtil.deserializeDateTime(data.get('birthDate'), dateUtil.FormatType.DATE, allowNone=True),
            email=data['email'],
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow()
        )
        user.save()

        return user, bool(password)


class UserProfileView(APIView):
    def get(self, request, profileId=None):
        pass

    @staticmethod
    def getUserProfile(profileId):
        try:
            return UserProfile.objects \
                .prefetch_related(
                    'section',
                    'section__sectionItem',
                    'section__sectionItem__contentObject',
                    'user__education',
                    'user__experience',
                    'user__contentItem',
                    'user__contentItem__section',
                    'user__video',
                    'user__file',
                    'user__image',
                    'user__tag'
                ) \
                .select_related(
                    'user'
                ) \
                .get(id=profileId)
        except UserProfile.DoesNotExist as e:
            raise e


class UserProjectView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, userId=None, userProjectId=None):
        userId = userId or request.data.get('userId')
        userProjectId = userProjectId or request.data.get('userProjectId')
        if not any([userId, userProjectId]):
            return Response('User ID or user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        if userId:
            if not security.isSelf(request, userId):
                return Response('You are not authorized to view this project', status=status.HTTP_401_UNAUTHORIZED)
            return Response([getSerializedUserProject(up) for up in self.getUserProjects(userId)], status=status.HTTP_200_OK)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(request, project.user_id):
            return Response('You are not authorized to view this project', status=status.HTTP_401_UNAUTHORIZED)
        return Response(getSerializedUserProject(project), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        project = self.createUserProject(request, request.data)
        # Return error response if something went wrong
        if isinstance(project, Response):
            return project

        return Response(status=status.HTTP_200_OK, data=getSerializedUserProject(self.getUserProjects(userProjectId=project.id)))

    @atomic
    def put(self, request, userProjectId=None):
        data = request.data
        userProjectId = userProjectId or data['id']
        if not userProjectId:
            return Response('A user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(request, project.user_id):
            return Response('You are not authorized to edit this project', status=status.HTTP_401_UNAUTHORIZED)

        isChanged = any([
            dataUtil.setObjectAttributes(project, data, {
                'projectNotes': None,
            }),
            self.addFiles(project, data, 'files', 'filesMetaData', self.getCreateFileFn(UserFile, 'file')),
            self.addFiles(project, data, 'videos', 'videosMetaData', self.getCreateFileFn(UserVideo, 'video')),
            self.addFiles(project, data, 'images', 'imagesMetaData', self.getCreateFileFn(UserImage, 'image')),
        ])

        if isChanged:
            project.modifiedDateTime = datetime.utcnow()
            project.save()

        return Response(
            status=status.HTTP_200_OK,
            data=getSerializedUserProject(self.getUserProjects(userProjectId=project.id))
        )

    def delete(self, request, userProjectId=None):
        userProjectId = userProjectId or request.data['id']
        if not userProjectId:
            return Response('A user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(request, project.user_id):
            return Response('You are not authorized to delete this project', status=status.HTTP_401_UNAUTHORIZED)

        try:
            project.delete()
        except ProtectedError:
            return Response(
                ('You cannot delete this project because it is used in one or more job applications. If you wish to '
                'delete the project, remove it from any job applications or withdraw your job applications.'),
                status=status.HTTP_409_CONFLICT
            )
        return Response(status=status.HTTP_200_OK, data=userProjectId)

    @staticmethod
    def getCreateFileFn(objClass, fileAttr):
        def createFileFn(userId, fileData, fileMetaData):
            file = objClass(
                user_id=userId,
                title=fileMetaData['title'],
                createdDateTime=datetime.utcnow(),
                modifiedDateTime=datetime.utcnow()
            )
            setattr(file, fileAttr, fileData)
            file.save()
            return file

        return createFileFn

    @staticmethod
    def addFiles(project, data, fileDataKey, fileMetaDataKey, createObjFn):
        isChanged = False
        filesDict = {f.name: f for f in data.getlist(fileDataKey, [])}
        usedFileIds = []
        existingFiles = getattr(project, fileDataKey)
        existingFilesDict = {f.id: f for f in existingFiles.all()}
        for fileMetaData in data.get(fileMetaDataKey, []):
            # Add new files
            if fileData := filesDict[fileMetaData['fileKey']] if fileMetaData['fileKey'] else None:
                file = createObjFn(project.user_id, fileData, fileMetaData)
                existingFiles.add(file)
                usedFileIds.append(file.id)
                isChanged = True
            else: # Update existing files
                fileId = fileMetaData['id']
                if not (file := existingFilesDict.get(fileId)):
                    return Response(f'No current file exists with ID={fileId}', status=status.HTTP_400_BAD_REQUEST)
                isChanged = isChanged or dataUtil.setObjectAttributes(file, fileMetaData, {
                    'title': None,
                })
                file.save()
                usedFileIds.append(file.id)

        # Remove files that are no longer included
        for file in existingFilesDict.values():
            if file.id not in usedFileIds:
                project.files.remove(file)
                isChanged = True

        return isChanged

    @staticmethod
    def createUserProject(request, data):
        if not security.isSelf(request, data['userId']):
            return Response('You are not authorized to post this project', status=status.HTTP_401_UNAUTHORIZED)

        existingProjects = {(up.user_id, up.customProject_id): up for up in UserProjectView.getUserProjects(userId=data['userId'])}
        if project := existingProjects.get((data['userId'], data['customProjectId'])):
            return Response(f'User project for {project.project.title} already exists', status=status.HTTP_409_CONFLICT)

        project = UserProject(
            user_id=data['userId'],
            customProject_id=data['customProjectId'],
            projectNotes=data.get('projectNotes'),
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow()
        )
        project.save()

        UserProjectView.addFiles(project, data, 'files', 'filesMetaData', UserProjectView.getCreateFileFn(UserFile, 'file'))
        UserProjectView.addFiles(project, data, 'videos', 'videosMetaData', UserProjectView.getCreateFileFn(UserVideo, 'video'))
        UserProjectView.addFiles(project, data, 'images', 'imagesMetaData', UserProjectView.getCreateFileFn(UserImage, 'image'))

        return project

    @staticmethod
    def getUserProjects(userProjectId=None, userId=None):
        if not any([userProjectId, userId]):
            return Response('An ID is required', status=status.HTTP_400_BAD_REQUEST)

        projectFilter = Q()
        if userProjectId:
            projectFilter &= Q(id=userProjectId)
        if userId:
            projectFilter &= Q(user_id=userId)
        projects = UserProject.objects\
            .select_related(
                'customProject',
                'customProject__project',
                'customProject__project__function',
                'user'
            )\
            .prefetch_related(
                'customProject__skills',
                'userProjectEvaluationCriterion',
                'userProjectEvaluationCriterion__employer',
                'userProjectEvaluationCriterion__evaluator',
                'files',
                'images',
                'videos'
            )\
            .filter(projectFilter)

        if userProjectId:
            if not projects:
                raise UserProject.DoesNotExist
            return projects[0]

        return projects


class UserJobApplicationView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, userJobApplicationId=None):
        userJobApplicationId = userJobApplicationId or request.data.get('id')
        if not userJobApplicationId:
            return Response('A job application ID is required', status=status.HTTP_400_BAD_REQUEST)

        jobApplication = self.getUserJobApplications(userJobApplicationId=userJobApplicationId)

        if not any([
            security.isSelf(request, jobApplication.userProject.user_id),
            security.isPermittedEmployer(request, jobApplication.employerProject.employer_id)
        ]):
            return Response('You do not have permission to view this job application', status=status.HTTP_401_UNAUTHORIZED)

        return Response(getSerializedJobApplication(jobApplication), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        data = request.data

        if userProjectId := data.get('userProjectId'):
            userProject = UserProjectView.getUserProjects(userProjectId=userProjectId)
            if not security.isSelf(request, userProject.user_id):
                return Response('You do not have permission to post this job application', status=status.HTTP_401_UNAUTHORIZED)
        else:
            userProject = UserProjectView.createUserProject(request, data)
            # Return error response if something went wrong
            if isinstance(userProject, Response):
                return userProject

        jobApplication = UserJobApplication(
            userProject_id=userProject.id,
            employerJob_id=data['employerJobId']
        )

        jobApplication.save()

        return Response(
            status=status.HTTP_200_OK,
            data=getSerializedJobApplication(self.getUserJobApplications(userJobApplicationId=jobApplication.id))
        )

    @atomic
    def put(self, request, userJobApplicationId=None):
        data = request.data
        userJobApplicationId = userJobApplicationId or data.get('id')
        if not userJobApplicationId:
            return Response('A job application ID is required', status=status.HTTP_400_BAD_REQUEST)

        jobApplication = self.getUserJobApplications(userJobApplicationId=userJobApplicationId)
        isSelf = security.isSelf(request, jobApplication.userProject.user_id)
        isEmployer = security.isPermittedEmployer(request, jobApplication.employerJob.employer_id)
        if not any([isSelf, isEmployer]):
            return Response('You do not have permission to update this job application', status=status.HTTP_401_UNAUTHORIZED)


        dtGetter = lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATETIME, allowNone=True)
        if isSelf and data.get('userProjectId'):
            dataUtil.setObjectAttributes(jobApplication, data, {
                'userProject_id': {'formName': 'userProjectId', 'isProtectExisting': True},
                'submissionDateTime': {'propFunc': dtGetter},
                'withdrawDateTime': {'propFunc': dtGetter}
            })

        if isEmployer:
            dataUtil.setObjectAttributes(jobApplication, data, {
                'approveDateTime': {'propFunc': dtGetter},
                'declineDateTime': {'propFunc': dtGetter},
            })

        jobApplication.save()
        return Response(
            status=status.HTTP_200_OK,
            data=getSerializedJobApplication(jobApplication)
        )

    @atomic
    def delete(self, request, userJobApplicationId=None):
        userJobApplicationId = userJobApplicationId or request.data.get('id')
        if not userJobApplicationId:
            return Response('A job application ID is required', status=status.HTTP_400_BAD_REQUEST)

        jobApplication = self.getUserJobApplications(userJobApplicationId=userJobApplicationId)
        if not security.isSelf(request, jobApplication.userProject.user_id):
            return Response('You do not have permission to delete this job application', status=status.HTTP_401_UNAUTHORIZED)

        jobApplication.delete()
        return Response(status=status.HTTP_200_OK, data=userJobApplicationId)

    @staticmethod
    def getUserJobApplications(userJobApplicationId=None, userId=None, userProjectId=None, employerJobId=None, employerId=None):
        if not any([userJobApplicationId, userId, userProjectId, employerJobId]):
            return Response('An ID is required', status=status.HTTP_400_BAD_REQUEST)

        applicationFilter = Q()
        if userJobApplicationId:
            applicationFilter &= Q(id=userJobApplicationId)
        if userId:
            applicationFilter &= Q(userProject__user_id=userId)
        if userProjectId:
            applicationFilter &= Q(userProject_id=userProjectId)
        if employerJobId:
            applicationFilter &= Q(employerJob_id=employerJobId)
        if employerId:
            applicationFilter &= Q(employerJob__employer_id=employerId)

        userJobApplications = UserJobApplication.objects\
            .select_related(
                'userProject',
                'userProject__user',
                'userProject__customProject',
                'userProject__customProject__project',
                'userProject__customProject__project__function',
                'employerJob'
            )\
            .prefetch_related(
                'userProject__files',
                'userProject__images',
                'userProject__videos',
                'userProject__customProject__skills',
                'employerJob__allowedProjects',
                'employerJob__allowedProjects__project',
                'employerJob__allowedProjects__project__function',
                'employerJob__allowedProjects__skills',
            )\
            .filter(applicationFilter)

        if userJobApplicationId:
            if not userJobApplications:
                raise UserJobApplication.DoesNotExist
            return userJobApplications[0]

        return userJobApplications


class UprovePasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.content_subtype = 'html'
        email_message.mixed_subtype = 'related'

        # Add Uprove logo
        imageName = 'logo.png'
        with open('up' + static(f'img/{imageName}'), 'rb') as logoFile:
            logo = MIMEImage(logoFile.read())
            logo.add_header('Content-ID', f'<logo>')
            logo.add_header('X-Attachment-Id', 'logo')
            logo.add_header('Content-Disposition', 'inline', filename=imageName)
            email_message.attach(logo)

        email_message.send()


def generatePassword():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS+'!@#$%^&*()-+=')
