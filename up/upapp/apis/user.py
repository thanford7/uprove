from datetime import datetime

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User as DjangoUser
from django.db import IntegrityError
from django.db.transaction import atomic
from django.utils import crypto
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from upapp import security
from upapp.models import *
from upapp.modelSerializers import getSerializedUser
from upapp.utils import dataUtil, dateUtil

__all__ = [
    'OrganizationView', 'UserVideoView', 'UserFileView', 'UserImageView', 'UserEducationItemView',
    'UserExperienceItemView', 'UserContentItemView', 'UserView', 'UserProfileView'
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


class UserView(APIView):

    def get(self, request, userId=None):
        return Response(getSerializedUser(self.getUser(userId)), status=status.HTTP_200_OK)

    @atomic
    def put(self, request, userId=None):
        userId = userId or request.data.get('id')
        if not userId:
            return Response('User ID is required to perform this operation', status=status.HTTP_400_BAD_REQUEST)
        if not (security.isPermittedAdmin(request) or security.isSelf(request, userId)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = self.getUser(userId)
        self.updateUser(user, request.data)
        return Response(getSerializedUser(user), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        if not security.isPermittedAdmin(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user, hasPassword = self.createUser(request.data)
        if not hasPassword:
            reset_form = PasswordResetForm({'email': user.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                subject_template_name='email/newUserPasswordEmailSubject.txt',
                email_template_name='email/newUserPasswordBody.html',
                html_email_template_name='email/newUserPassword.html',
                extra_email_context={
                    'supportEmail': 'community@uprove.co'
                }
            )

        return Response(status=status.HTTP_200_OK, data={'user': getSerializedUser(user), 'hasPassword': hasPassword})

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
    def getUser(userId):
        try:
            return User.objects.select_related('djangoUser').prefetch_related('image').get(id=userId)
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
            'userTypeBits': None
        })

        user.modifiedDateTime = datetime.utcnow()
        user.save()

    @staticmethod
    def createUser(data):
        password = data.get('password', None)
        djangoUserKwargs = dict(
            email=data['email'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            password=password or generatePassword()
        )
        try:
            if data.get('isSuperUser'):
                djangoUser = DjangoUser.objects.create_superuser(data['email'], **djangoUserKwargs)
            else:
                djangoUserKwargs['is_staff'] = data.get('isStaff', False)
                djangoUser = DjangoUser.objects.create_user(data['email'], **djangoUserKwargs)
        except IntegrityError:
            return Response(f'''
            User with email={data["email"]} already exists. If you forgot your password, please use the "reset password"
            link in the sign in menu.
            ''', status=status.HTTP_409_CONFLICT)

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


def generatePassword():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS+'!@#$%^&*()-+=')
