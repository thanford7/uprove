import tempfile
import urllib.request
from email.mime.image import MIMEImage

import ffmpeg as ffmpeg
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User as DjangoUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import File
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.db.models import Q
from django.db.transaction import atomic
from django.template import loader
from django.templatetags.static import static
from django.utils import crypto, timezone
from moviepy.editor import clips_array, VideoFileClip
from rest_framework import status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

from upapp import security
from upapp.apis import UproveAPIView, saveActivity, ActivityKey
from upapp.apis.employer import JobPostingView, OrganizationView
from upapp.apis.project import SkillView
from upapp.apis.sendEmail import EmailView
from upapp.apis.tag import TagView
from upapp.models import *
from upapp.modelSerializers import ContentTypes, getSerializedUser, getSerializedJobApplication, \
    getSerializedUserProject, \
    getSerializedUserVideo, getSerializedUserProfile, getSerializedUserExperience, \
    getSerializedUserEducation, getSerializedUserCertification, getSerializedUserContentItem, getSerializedEmployerJob
from upapp.utils import dataUtil, dateUtil

CONTENT_TYPE_MODELS = {
    ContentTypes.EXPERIENCE.value: {'model': UserExperience, 'serializer': getSerializedUserExperience},
    ContentTypes.EDUCATION.value: {'model': UserEducation, 'serializer': getSerializedUserEducation},
    ContentTypes.CERTIFICATION.value: {'model': UserCertification, 'serializer': getSerializedUserCertification},
    ContentTypes.VIDEO.value: {'model': UserVideo, 'serializer': getSerializedUserVideo},
    ContentTypes.CUSTOM.value: {'model': UserContentItem, 'serializer': getSerializedUserContentItem},
    ContentTypes.PROJECT.value: {'model': UserProject, 'serializer': getSerializedUserProject}
}
PROJECT_COMPLETE_LOCK_DAYS = 30


def isUserProjectLocked(userProject):
    return (
        userProject.status == UserProject.Status.COMPLETE.value
        and getDaysUntilProjectUnlock(userProject) > 0
    )


def getDaysUntilProjectUnlock(userProject):
    statusChangeMinutes = (timezone.now() - userProject.statusChangeDateTime).total_seconds() / 60
    return round(PROJECT_COMPLETE_LOCK_DAYS - (statusChangeMinutes / dateUtil.MINUTES_IN_DAY), 1)


class UserVideoView(UproveAPIView):

    @atomic
    def post(self, request):
        rawAvVideo = self.data.get('avVideo')
        rawScreenVideo = self.data.get('screenVideo')
        if not any([rawAvVideo, rawScreenVideo]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='At least one video is required')

        userVideo = self.createCombinedUserVideo(self.user, self.data, rawAvVideo, rawScreenVideo)
        self.setUserProjectVideo(userVideo)
        # TODO: Send user an email if there is an error. Also send an email to Uprove support
        EmailView.sendEmail(
            'Uprove | Video processing complete',
            [self.user.email],
            djangoContext={
                'protocol': 'http' if settings.DEBUG else 'https',
                'domain': get_current_site(request).domain,
                'linkName': 'Dashboard page',
                'url': 'candidateDashboard/' if self.user.isCandidate else 'employerDashboard/'
            },
            djangoEmailBodyTemplate='email/videoProcessingComplete.html'
        )
        return Response(status=status.HTTP_200_OK, data=getSerializedUserVideo(userVideo))

    def delete(self, request):
        videoId = self.data.get('id')
        if not videoId:
            return Response('A video ID is required', status=status.HTTP_400_BAD_REQUEST)

        video = self.getVideo(videoId)
        if not security.isSelf(video.user_id, user=self.user):
            return Response('You are not permitted to delete this video', status=status.HTTP_401_UNAUTHORIZED)

        video.delete()
        return Response(status=status.HTTP_200_OK, data=videoId)

    def setUserProjectVideo(self, userVideo):
        if projectId := self.data.get('projectId'):
            project = UserProjectView.getUserProjects(userProjectId=projectId)
            project.videos.add(userVideo)

    @staticmethod
    def getVideo(videoId):
        try:
            return UserVideo.objects.get(id=videoId)
        except UserVideo.DoesNotExist as e:
            raise e

    @staticmethod
    @atomic
    def createUserVideo(user, data, videoKey='video'):
        video = UserVideo(
            user=user,
            video=data[videoKey],
            title=data.get('title') or data[videoKey].name,
            createdDateTime=timezone.now(),
            modifiedDateTime=timezone.now()
        )
        video.save()
        return video

    @staticmethod
    @atomic
    def createCombinedUserVideo(user, data, rawAvVideo, rawScreenVideo):
        # Write videos to temporary directory which gets deleted after exiting "with" statement
        with tempfile.TemporaryDirectory() as tmpDirectory:
            avVideo = None
            screenVideo = None
            if rawAvVideo:
                avVideo = open(f'{tmpDirectory}/avVideo.webm', 'wb+')
                for chunk in rawAvVideo.chunks():
                    avVideo.write(chunk)
                avVideo.seek(0)
                outputName = f'{tmpDirectory}/outputAvVideo.webm'
                (
                    ffmpeg
                        .input(avVideo.name)
                        .output(outputName, f='webm', video_bitrate='40M', r=25)
                        .run()
                )
                avClip = VideoFileClip(outputName)
                # avClip.resize(0.2)
                avVideo.close()

            if rawScreenVideo:
                screenVideo = open(f'{tmpDirectory}/screenVideo.webm', 'wb+')
                for chunk in rawScreenVideo.chunks():
                    screenVideo.write(chunk)
                screenVideo.seek(0)
                outputName = f'{tmpDirectory}/outputScreenVideo.webm'
                (
                    ffmpeg
                        .input(screenVideo.name)
                        .output(outputName, f='webm', video_bitrate='40M', r=25)
                        .run()
                )
                screenClip = VideoFileClip(outputName)
                screenVideo.close()

            if avVideo and screenVideo:
                combinedClip = clips_array([[screenClip, avClip]])
                outputName = f'outputCombinedVideo_{timezone.now().isoformat()}.webm'
                combinedClip.write_videofile(outputName)

            with open(outputName, 'rb') as video:
                userVideo = UserVideo(
                    user=user,
                    video=File(video),
                    title=data.get('title') or 'Combined video',
                    createdDateTime=timezone.now(),
                    modifiedDateTime=timezone.now()
                )
                userVideo.save()

        return userVideo


class UserFileView(UproveAPIView):

    def delete(self, request):
        fileId = self.data.get('id')
        if not fileId:
            return Response('A file ID is required', status=status.HTTP_400_BAD_REQUEST)

        file = self.getFile(fileId)
        if not security.isSelf(file.user_id, user=self.user):
            return Response('You are not permitted to delete this file', status=status.HTTP_401_UNAUTHORIZED)

        file.delete()
        return Response(status=status.HTTP_200_OK, data=fileId)

    @staticmethod
    def getFile(fileId):
        try:
            return UserFile.objects.get(id=fileId)
        except UserFile.DoesNotExist as e:
            raise e

    @staticmethod
    @atomic
    def createUserFiles(user, data):
        files = data['file']
        if not isinstance(files, list):
            files = [files]

        savedFiles = []
        for fileData in files:
            file = UserFile(
                user=user,
                file=fileData,
                title=data.get('title') or fileData.name,
                createdDateTime=timezone.now(),
                modifiedDateTime=timezone.now()
            )
            file.save()
            savedFiles.append(file)

        return savedFiles


class UserImageView(UproveAPIView):

    def delete(self, request):
        imageId = self.data.get('id')
        if not imageId:
            return Response('An image ID is required', status=status.HTTP_400_BAD_REQUEST)

        image = self.getImage(imageId)
        if not security.isSelf(image.user_id, user=self.user):
            return Response('You are not permitted to delete this image', status=status.HTTP_401_UNAUTHORIZED)

        image.delete()
        return Response(status=status.HTTP_200_OK, data=imageId)

    @staticmethod
    def getImage(imageId):
        try:
            return UserImage.objects.get(id=imageId)
        except UserImage.DoesNotExist as e:
            raise e

    @staticmethod
    @atomic
    def createUserImage(user, data):
        image = UserImage(
            user=user,
            image=data['image'],
            title=data.get('title') or data['image'].name,
            createdDateTime=timezone.now(),
            modifiedDateTime=timezone.now()
        )
        image.save()
        return image


class UserEducationItemView(APIView):

    @staticmethod
    def getEducationItem(educationId):
        try:
            return UserEducation.objects.select_related('school').get(id=educationId)
        except UserEducation.DoesNotExist as e:
            raise e


class UserCertificationItemView(APIView):

    @staticmethod
    def getCertificationItem(certificationId):
        try:
            return UserCertification.objects.select_related('organization').get(id=certificationId)
        except UserCertification.DoesNotExist as e:
            raise e


class UserExperienceItemView(APIView):

    @staticmethod
    def getExperienceItem(experienceId):
        try:
            return UserExperience.objects.select_related('organization').get(id=experienceId)
        except UserExperience.DoesNotExist as e:
            raise e


class UserContentItemView(APIView):

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
        if not (security.isPermittedAdmin(request) or security.isSelf(userId, request=request)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = self.getUser(userId)
        self.updateUser(user, request.data)
        currentUproveUser = security.getSessionUser(request)
        if security.isSelf(userId, user=currentUproveUser) or not currentUproveUser:
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
                    'supportEmail': 'community@uprove.co',
                    'isNew': True,
                    'next': request.data.get('next')
                }
            })

        EmailView.sendFormattedEmail(request, contactType=EmailView.TYPE_CANDIDATE_SIGNUP)
        UserProfileView.createUserProfile(user.id, isPrimary=True)

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
            return User.objects \
                .select_related('djangoUser') \
                .prefetch_related(
                    'profile',
                    'profile__section',
                    'profile__section__sectionItem',
                    'profile__section__sectionItem__contentObject',
                    'education',
                    'education__school',
                    'certification',
                    'certification__organization',
                    'experience',
                    'experience__organization',
                    'contentItem',
                    'contentItem__section',
                    'video',
                    'file',
                    'image',
                    'userTag',
                    'userTag__tag',
                    'userProject',
                    'userProject__user',
                    'userProject__videos',
                    'userProject__images',
                    'userProject__files',
                    'userProject__customProject',
                    'userProject__customProject__skills',
                    'userProject__customProject__project',
                    'userProject__customProject__project__role',
                    'preferenceCompanySizes',
                    'preferenceRoles',
                    'preferenceState',
                    'preferenceCountry'
                ) \
                .get(id=userId)
        except User.DoesNotExist as e:
            raise e

    @staticmethod
    def getUserProfiles(userId):
        try:
            return User.objects \
                .select_related('djangoUser') \
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
            ) \
                .get(id=userId)
        except User.DoesNotExist as e:
            raise e

    @staticmethod
    def getUsers():
        return User.objects.select_related('djangoUser').prefetch_related('image', 'profile').all()

    @staticmethod
    def updateUser(user, data):
        dataUtil.setObjectAttributes(user, data, {
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'birthDate': {
                'propFunc': lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE, allowNone=True)},
            'email': None,
            'userTypeBits': None,
            'employer_id': {'formName': 'employerId'},
            'isDemo': {'isProtectExisting': True}
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
            employer_id=data.get('employerId'),
            inviteEmployer_id=data.get('inviteEmployerId'),
            isDemo=data.get('isDemo') or False,
            modifiedDateTime=timezone.now(),
            createdDateTime=timezone.now()
        )
        user.save()
        saveActivity(ActivityKey.CREATE_ACCOUNT, user.id)

        return user, bool(password)


class PreferencesView(UproveAPIView):

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=self.getPreferenceOptions())

    @staticmethod
    def getPreferenceOptions():
        return {
            'companySizes': [{'id': s.id, 'companySize': s.companySize} for s in CompanySize.objects.all()],
            'roleTitles': sorted(
                [{'id': j.id, 'roleTitle': j.roleTitle} for j in RoleTitle.objects.all()],
                key=lambda x: x['roleTitle']
            ),
            'countries': sorted(
                [{'id': c.id, 'countryName': c.countryName} for c in Country.objects.filter(countryName__in=JobPostingView.permittedCountries)],
                key=lambda x: x['countryName']
            )
        }


class UserPreferenceView(UproveAPIView):

    @atomic
    def put(self, request):
        if not security.isPermittedSessionUser(user=self.user):
            return Response('You are not permitted to edit this user', status=status.HTTP_400_BAD_REQUEST)

        user = UserView.getUser(self.user.id)
        user.preferenceCompanySizes.clear()
        user.preferenceRoles.clear()
        user.preferenceCountry.clear()
        for v in self.data['companySizes']:
            user.preferenceCompanySizes.add(v)
        for v in self.data['roleTitles']:
            user.preferenceRoles.add(v)
        for v in self.data['countries']:
            user.preferenceCountry.add(v)

        isChanged = dataUtil.setObjectAttributes(user, self.data, {
            'preferenceRemoteBits': {'formName': 'remote', 'propFunc': lambda x: x or User.REMOTE_PREF_DEFAULT},
        })
        if isChanged:
            user.save()

        return Response(status=status.HTTP_200_OK, data=getSerializedUser(UserView.getUser(self.user.id)))


class UserProfileView(UproveAPIView):
    USER_SKILL_LIMIT = 5

    def get(self, request, profileId=None):
        pass

    @atomic
    def post(self, request):
        pass

    @atomic
    def put(self, request):
        if not self.data or not self.data.get('id'):
            return Response('A profile ID is required', status=status.HTTP_400_BAD_REQUEST)

        profile = self.getUserProfile(self.data['id'])

        if not security.isSelf(profile.user_id, user=self.user):
            return Response('You are not permitted to edit this profile', status=status.HTTP_401_UNAUTHORIZED)

        dataUtil.setObjectAttributes(profile, self.data, {
            'profileName': None
        })

        if profilePicture := self.data.get('newProfilePicture'):
            profile.profilePicture = UserImageView.createUserImage(self.user, {'image': profilePicture})

        profile.save()

        if userSkills := self.data.get('userSkills'):
            self.saveUserTags(self.user, Tag.TYPE_SKILL, userSkills)

        if userInterests := self.data.get('userInterests'):
            self.saveUserTags(self.user, Tag.TYPE_INTEREST, userInterests)

        return self.getProfileOwnerResponse(profile.id)

    @staticmethod
    def createUserProfile(userId, makePublic=True, isPrimary=False):
        profile = UserProfile(
            user_id=userId,
            makePublic=makePublic,
            isPrimary=isPrimary,
            createdDateTime=timezone.now(),
            modifiedDateTime=timezone.now()
        )
        profile.save()
        return profile

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
                    'user__userTag'
                ) \
                .select_related(
                    'user'
                ) \
                .get(id=profileId)
        except UserProfile.DoesNotExist as e:
            raise e

    @staticmethod
    def getProfileOwnerResponse(profileId):
        return Response(
            status=status.HTTP_200_OK,
            data=getSerializedUserProfile(UserProfileView.getUserProfile(profileId), isOwner=True)
        )

    @staticmethod
    def saveUserTags(user, tagType, tagData):
        user.userTag.filter(tag__type=tagType).delete()  # Clear existing skills before saving new ones
        if tagType == Tag.TYPE_SKILL:
            tagData = tagData[:UserProfileView.USER_SKILL_LIMIT]

        for userTagData in tagData:
            userTag = UserTag(
                user=user,
                createdDateTime=timezone.now(),
                modifiedDateTime=timezone.now()
            )
            if tagId := userTagData.get('id'):
                try:
                    userTag = UserTag.objects.get(tag_id=tagId, user_id=user.id)
                except UserTag.DoesNotExist:
                    pass

            userTag.tag = TagView.updateOrCreate(userTagData, tag=getattr(userTag, 'tag', None))

            # Update the user tag
            dataUtil.setObjectAttributes(userTag, userTagData, {
                'description': None,
                'skillLevelBit': None
            })
            userTag.save()


class UserProfileSectionView(UproveAPIView):

    @atomic
    def post(self, request):
        if not self.data or not self.data.get('profileId'):
            return Response('A profile ID is required', status=status.HTTP_400_BAD_REQUEST)

        profile = UserProfileView.getUserProfile(self.data['profileId'])

        if not security.isSelf(profile.user_id, user=self.user):
            return Response('You are not permitted to edit this profile', status=status.HTTP_401_UNAUTHORIZED)

        newProfileSection = UserProfileSection(
            userProfile_id=profile.id
        )
        sectionCount = profile.section.all().count()
        dataUtil.setObjectAttributes(newProfileSection, self.data, {
            'title': None,
            'description': None,
            'sectionOrder': {'propFunc': lambda val: val or sectionCount}
        })
        newProfileSection.save()
        return UserProfileView.getProfileOwnerResponse(profile.id)

    @atomic
    def put(self, request):
        if not self.data or not self.data.get('id'):
            return Response('A profile section ID is required', status=status.HTTP_400_BAD_REQUEST)

        profileSection = self.getUserProfileSection(self.data['id'])

        if not security.isSelf(profileSection.userProfile.user_id, user=self.user):
            return Response('You are not permitted to edit this profile', status=status.HTTP_401_UNAUTHORIZED)

        previousSectionOrder = profileSection.sectionOrder
        dataUtil.setObjectAttributes(profileSection, self.data, {
            'title': None,
            'description': None,
            'sectionOrder': None
        })
        profileSection.save()

        # Check if the section order has changed and rearrange all sections if it has
        if (sectionMove := profileSection.sectionOrder - previousSectionOrder) != 0:
            profileSections = UserProfileSection.objects.filter(userProfile=profileSection.userProfile)
            for s in profileSections:
                if s.id == profileSection.id:
                    continue
                if sectionMove < 0 and s.sectionOrder >= profileSection.sectionOrder:
                    s.sectionOrder += 1
                    s.save()
                if sectionMove > 0 and s.sectionOrder <= profileSection.sectionOrder:
                    s.sectionOrder -= 1
                    s.save()

        return UserProfileView.getProfileOwnerResponse(profileSection.userProfile_id)

    @atomic
    def delete(self, request):
        if not self.data.get('id'):
            return Response('A profile section ID is required', status=status.HTTP_400_BAD_REQUEST)

        profileSection = self.getUserProfileSection(self.data['id'])

        if not security.isSelf(profileSection.userProfile.user_id, user=self.user):
            return Response('You are not permitted to edit this profile', status=status.HTTP_401_UNAUTHORIZED)

        profileSection.delete()
        return UserProfileView.getProfileOwnerResponse(profileSection.userProfile_id)

    @staticmethod
    def getUserProfileSection(profileSectionId):
        try:
            return UserProfileSection.objects \
                .select_related('userProfile') \
                .prefetch_related('sectionItem') \
                .get(id=profileSectionId)
        except UserProfileSection.DoesNotExist as e:
            raise e


class UserProfileSectionContentItemView(UproveAPIView):

    def put(self, request):
        if not (sectionId := self.data.get('sectionId')):
            return Response('Section ID is required', status=status.HTTP_400_BAD_REQUEST)
        if not (contentId := self.data.get('id')):
            return Response('Content ID is required', status=status.HTTP_400_BAD_REQUEST)
        if not (newContentOrder := self.data.get('contentOrder')):
            return Response('Content order is required', status=status.HTTP_400_BAD_REQUEST)

        section = UserProfileSectionView.getUserProfileSection(sectionId)
        if not security.isSelf(section.userProfile.user_id, request=request):
            return Response('You are not permitted to edit this profile', status=status.HTTP_401_UNAUTHORIZED)
        sectionItems = [s for s in section.sectionItem.all()]
        sectionContentCount = len(sectionItems)

        if newContentOrder < 1 or newContentOrder > sectionContentCount:
            return Response(f'Content order must be between 1 and {sectionContentCount}',
                            status=status.HTTP_400_BAD_REQUEST)

        contentItem = next((s for s in sectionItems if s.id == contentId), None)
        if not contentItem:
            return Response(f'Content item with ID={contentId} is not in the specified section',
                            status=status.HTTP_400_BAD_REQUEST)

        if contentItem.contentOrder == newContentOrder:
            return UserProfileView.getProfileOwnerResponse(section.userProfile.id)

        isMovingUp = contentItem.contentOrder > newContentOrder
        # TODO: Bulk update instead of saving individually
        for item in sectionItems:
            if item.id == contentId:
                item.contentOrder = newContentOrder
                item.save()
            elif isMovingUp and item.contentOrder >= newContentOrder:
                item.contentOrder += 1
                item.save()
            elif not isMovingUp and item.contentOrder <= newContentOrder:
                item.contentOrder -= 1
                item.save()

        return UserProfileView.getProfileOwnerResponse(section.userProfile.id)

    def delete(self, request):
        if not (contentId := self.data.get('id')):
            return Response('Content ID is required', status=status.HTTP_400_BAD_REQUEST)

        sectionContentItem = self.getUserProfileSectionItem(contentId)
        if not security.isSelf(sectionContentItem.userProfileSection.userProfile.user_id, request=request):
            return Response('You are not permitted to edit this profile', status=status.HTTP_401_UNAUTHORIZED)

        sectionId = sectionContentItem.userProfileSection_id
        sectionContentItem.delete()

        # Update the section ordering to make sure there aren't any gaps
        section = UserProfileSectionView.getUserProfileSection(sectionId)
        for idx, contentItem in enumerate(sorted(section.sectionItem.all(), key=lambda val: val.contentOrder)):
            contentOrder = idx + 1
            if contentItem.contentOrder != contentOrder:
                contentItem.contentOrder = contentOrder
                contentItem.save()

        return UserProfileView.getProfileOwnerResponse(sectionContentItem.userProfileSection.userProfile.id)

    @staticmethod
    def getUserProfileSectionItem(contentId):
        return UserProfileSectionItem.objects \
            .select_related('userProfileSection', 'userProfileSection__userProfile') \
            .get(id=contentId)


class UserProfileContentItemView(UproveAPIView):

    def post(self, request):
        if not (contentType := self.data.get('type')):
            return Response('Content type is required', status=status.HTTP_400_BAD_REQUEST)

        if not security.isSelf(self.data['userId'], user=self.user):
            return Response('You are not permitted to edit this content', status=status.HTTP_401_UNAUTHORIZED)

        contentItem = self.createOrUpdateContentItem(contentType)
        if isinstance(contentItem, Response):
            return contentItem

        # Associate the content
        if sectiondId := self.data.get('sectionId'):
            with atomic():
                profileSection = UserProfileSectionView.getUserProfileSection(sectiondId)
                sectionItemCount = profileSection.sectionItem.all().count()
                sectionItem = UserProfileSectionItem(
                    userProfileSection=profileSection,
                    contentOrder=sectionItemCount + 1,
                    contentObject=contentItem
                )
                sectionItem.save()
            return UserProfileView.getProfileOwnerResponse(profileSection.userProfile_id)

        serializer = CONTENT_TYPE_MODELS[contentType]['serializer']
        return Response(
            status=status.HTTP_200_OK,
            data=serializer(contentItem)
        )

    def put(self, request):
        if not (contentId := self.data.get('id')):
            return Response('An ID is required', status=status.HTTP_400_BAD_REQUEST)

        if not (contentType := self.data.get('type')):
            return Response('Content type is required', status=status.HTTP_400_BAD_REQUEST)

        if not security.isSelf(self.data['userId'], user=self.user):
            return Response('You are not permitted to edit this content', status=status.HTTP_401_UNAUTHORIZED)

        contentItem = self.createOrUpdateContentItem(
            contentType,
            contentItem=self.getContentItem(contentId, contentType)
        )
        if isinstance(contentItem, Response):
            return contentItem

        if profileId := self.data.get('profileId'):
            return UserProfileView.getProfileOwnerResponse(profileId)

        serializer = CONTENT_TYPE_MODELS[contentType]['serializer']
        return Response(
            status=status.HTTP_200_OK,
            data=serializer(contentItem)
        )

    def delete(self, request):
        # Note this endpoint will actually delete the content.
        # To disassociate content from a section, use the UserProfileSectionContentItemView
        pass

    @atomic
    def createOrUpdateContentItem(self, contentType, contentItem=None):
        # Save the content item depending on the type of content
        if contentType == ContentTypes.EXPERIENCE.value:
            contentItem = contentItem or UserExperience(
                createdDateTime=timezone.now()
            )
            if (orgId := self.data.get('organizationId')) and not self.data.get('organizationNewLogo'):
                contentItem.organization_id = orgId
            else:
                self.data['organization']['newLogo'] = self.data.get('organizationNewLogo')
                org = OrganizationView.updateOrCreateOrg(self.data['organization'])
                contentItem.organization = org

            dateGetter = lambda val, allowNone: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE,
                                                                             allowNone=allowNone)
            dataUtil.setObjectAttributes(contentItem, self.data, {
                'user_id': {'formName': 'userId'},
                'positionTitle': None,
                'employmentType': None,
                'startDate': {'propFunc': lambda val: dateGetter(val, False)},
                'endDate': {'propFunc': lambda val: dateGetter(val, True)},
                'description': None
            })
            contentItem.save()
            return contentItem
        elif contentType == ContentTypes.EDUCATION.value:
            contentItem = contentItem or UserEducation(
                createdDateTime=timezone.now()
            )
            if (schoolId := self.data.get('schoolId')) and not self.data.get('schoolNewLogo'):
                contentItem.school_id = schoolId
            else:
                self.data['school']['newLogo'] = self.data.get('schoolNewLogo')
                org = OrganizationView.updateOrCreateOrg(self.data['school'])
                contentItem.school = org

            dateGetter = lambda val, allowNone: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE,
                                                                             allowNone=allowNone)
            dataUtil.setObjectAttributes(contentItem, self.data, {
                'user_id': {'formName': 'userId'},
                'degree': None,
                'degreeSubject': None,
                'startDate': {'propFunc': lambda val: dateGetter(val, True)},
                'endDate': {'propFunc': lambda val: dateGetter(val, True)},
                'activities': None
            })
            contentItem.save()
            return contentItem
        elif contentType == ContentTypes.CERTIFICATION.value:
            contentItem = contentItem or UserCertification(
                createdDateTime=timezone.now()
            )
            if (organizationId := self.data.get('organizationId')) and not self.data.get('organizationNewLogo'):
                contentItem.organization_id = organizationId
            else:
                self.data['organization']['newLogo'] = self.data.get('organizationNewLogo')
                org = OrganizationView.updateOrCreateOrg(self.data['organization'])
                contentItem.organization = org

            dateGetter = lambda val, allowNone: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE,
                                                                             allowNone=allowNone)
            dataUtil.setObjectAttributes(contentItem, self.data, {
                'user_id': {'formName': 'userId'},
                'hasExpiration': None,
                'title': None,
                'issueDate': {'propFunc': lambda val: dateGetter(val, False)},
                'expirationDate': {'propFunc': lambda val: dateGetter(val, True)},
            })
            contentItem.save()
            return contentItem
        elif contentType == ContentTypes.CUSTOM.value:
            contentItem = contentItem or UserContentItem(createdDateTime=timezone.now())
            dataUtil.setObjectAttributes(contentItem, self.data, {
                'user_id': {'formName': 'userId'},
                'title': None
            })
            contentItem.save()
            contentItem.section.all().delete()  # Clear existing content before saving new content

            sectionIdx = 1
            for section in self.data['sections']:
                contentItems = None
                mediaKey = section.get('mediaKey')
                if section['type'] == 'video':
                    if mediaKey:
                        section['video'] = self.files[mediaKey][0]
                        contentItems = [UserVideoView.createUserVideo(self.user, section)]
                    else:
                        contentItems = [UserVideoView.getVideo(section['value'])]
                elif section['type'] == 'image':
                    if mediaKey:
                        section['image'] = self.files[mediaKey][0]
                        contentItems = [UserImageView.createUserImage(self.user, section)]
                    else:
                        contentItems = [UserImageView.getImage(section['value'])]
                elif section['type'] == 'file':
                    if mediaKey:
                        section['file'] = self.files[mediaKey]
                        contentItems = UserFileView.createUserFiles(self.user, section)
                    elif fileVal := section['value']:
                        if not isinstance(fileVal, list):
                            section['value'] = [fileVal]
                        contentItems = list(UserFile.objects.filter(id__in=section['value']))

                if contentItems:
                    for item in contentItems:
                        UserContentItemSection(
                            userContentItem=contentItem,
                            contentOrder=sectionIdx,
                            contentObject=item
                        ).save()
                        sectionIdx += 1
                elif contentItem and (text := section['value']):
                    UserContentItemSection(
                        userContentItem=contentItem,
                        contentOrder=sectionIdx,
                        text=text
                    ).save()
                    sectionIdx += 1
            return contentItem
        elif contentType == ContentTypes.EXISTING.value:
            contentModel = CONTENT_TYPE_MODELS[self.data['existingContentType']]['model']
            try:
                return contentModel.objects.get(id=self.data['existingContentId'])
            except contentModel.DoesNotExist as e:
                raise e
        else:
            return Response(f'Unrecognized content type of {contentType}', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def getContentItem(contentId, contentType):
        if contentType == ContentTypes.EXPERIENCE.value:
            return UserExperience.objects.select_related('organization').get(id=contentId)
        if contentType == ContentTypes.EDUCATION.value:
            return UserEducation.objects.select_related('school').get(id=contentId)
        if contentType == ContentTypes.CUSTOM.value:
            return UserContentItem.objects.prefetch_related('section').get(id=contentId)
        return CONTENT_TYPE_MODELS[contentType]['model'].objects.get(id=contentId)


class UserProjectView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, userId=None, userProjectId=None):
        userId = userId or request.data.get('userId')
        userProjectId = userProjectId or self.data.get('userProjectId')
        if not any([userId, userProjectId]):
            return Response('User ID or user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        if userId:
            if not security.isSelf(userId, user=self.user):
                return Response('You are not authorized to view this project', status=status.HTTP_401_UNAUTHORIZED)
            return Response([getSerializedUserProject(up) for up in self.getUserProjects(userId)],
                            status=status.HTTP_200_OK)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(project.user_id, user=self.user):
            return Response('You are not authorized to view this project', status=status.HTTP_401_UNAUTHORIZED)
        return Response(getSerializedUserProject(project), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        project = self.createUserProject(request, self.data, self.files)
        # Return error response if something went wrong
        if isinstance(project, Response):
            return project

        return Response(status=status.HTTP_200_OK,
                        data=getSerializedUserProject(self.getUserProjects(userProjectId=project.id)))

    @atomic
    def put(self, request, userProjectId=None):
        userProjectId = userProjectId or self.data['id']
        if not userProjectId:
            return Response('A user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(project.user_id, user=self.user):
            return Response('You are not authorized to edit this project', status=status.HTTP_401_UNAUTHORIZED)

        if isUserProjectLocked(project):
            return Response(f'Project is locked for another {dataUtil.pluralize("day", getDaysUntilProjectUnlock(project))}', status=status.HTTP_401_UNAUTHORIZED)

        user = UserView.getUser(self.user.id)  # Grab the user with all associated data so we can get files without extra DB query
        isChanged = any([
            dataUtil.setObjectAttributes(project, self.data, {
                'projectNotes': None,
            }),
            self.addFiles(project, user, self.data, self.files, 'file', 'filesMetaData', self.getCreateFileFn(UserFile, 'file')),
            self.addFiles(project, user, self.data, self.files, 'video', 'videosMetaData', self.getCreateFileFn(UserVideo, 'video')),
            self.addFiles(project, user, self.data, self.files, 'image', 'imagesMetaData', self.getCreateFileFn(UserImage, 'image')),
        ])

        if isChanged:
            project.modifiedDateTime = timezone.now()
            project.save()

        return Response(
            status=status.HTTP_200_OK,
            data=getSerializedUserProject(UserProjectView.getUserProjects(userProjectId=userProjectId))
        )

    def delete(self, request, userProjectId=None):
        userProjectId = userProjectId or self.data['id']
        if not userProjectId:
            return Response('A user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(project.user_id, user=self.user):
            return Response('You are not authorized to delete this project', status=status.HTTP_401_UNAUTHORIZED)

        for jobApplication in project.jobApplication.all():
            jobApplication.withdrawDateTime = timezone.now()
            jobApplication.save()

        project.delete()
        return Response(status=status.HTTP_200_OK, data=userProjectId)

    @staticmethod
    def getCreateFileFn(objClass, fileAttr):
        def createFileFn(userId, fileData, fileMetaData):
            file = objClass(
                user_id=userId,
                title=fileMetaData['title'],
                createdDateTime=timezone.now(),
                modifiedDateTime=timezone.now()
            )
            setattr(file, fileAttr, fileData)
            file.save()
            return file

        return createFileFn

    @staticmethod
    def addFiles(project, user, data, fileData, fileDataKey, fileMetaDataKey, createObjFn):
        isChanged = False
        filesDict = {f.name: f for f in fileData.get(fileDataKey, [])}
        usedFileIds = []
        existingProjectFiles = getattr(project, fileDataKey + 's')   # Need to pluralize the data key
        existingProjectFilesDict = {f.id: f for f in existingProjectFiles.all()}
        allFiles = getattr(user, fileDataKey)
        allFilesDict = {f.id: f for f in allFiles.all()}
        for fileMetaData in data.get(fileMetaDataKey, []):
            # Add new files
            if fileData := filesDict[fileMetaData['fileKey']] if fileMetaData['fileKey'] else None:
                file = createObjFn(project.user_id, fileData, fileMetaData)
                existingProjectFiles.add(file)
                usedFileIds.append(file.id)
                isChanged = True
            else:  # Update existing files
                fileId = fileMetaData['id']

                # User selected an existing file that is not currently associated with this project
                if not (file := existingProjectFilesDict.get(fileId)):
                    file = allFilesDict.get(fileId)
                    existingProjectFiles.add(file)
                isChanged = isChanged or dataUtil.setObjectAttributes(file, fileMetaData, {
                    'title': None,
                })
                file.save()
                usedFileIds.append(file.id)

        # Remove files that are no longer included
        for file in existingProjectFilesDict.values():
            if file.id not in usedFileIds:
                project.files.remove(file)
                isChanged = True

        return isChanged

    @staticmethod
    def createUserProject(request, data, fileData):
        if not security.isSelf(data['userId'], request=request):
            return Response('You are not authorized to post this project', status=status.HTTP_401_UNAUTHORIZED)

        if not (customProjectId := data.get('customProjectId')):
            existingCustomProjects = JobPostingView.getCustomProjects()
            customProject = CustomProject(
                project_id=data['projectId'],
                skillLevelBit=data['skillLevelBit']
            )

            if not (existingCustomProject := existingCustomProjects.get(
                    JobPostingView.generateUniqueCustomProjectKey(customProject, skillIds=data['skillIds'])
            )
            ):
                customProject.save()
                SkillView.setSkillIds(customProject, data['skillIds'])

            customProjectId = existingCustomProject.id if existingCustomProject else customProject.id

        existingProjects = {
            (up.user_id, up.customProject_id): up
            for up in UserProjectView.getUserProjects(userId=data['userId'])
        }
        if project := existingProjects.get((data['userId'], customProjectId)):
            return Response(f'User project for {project.customProject.project.title} already exists',
                            status=status.HTTP_409_CONFLICT)

        project = UserProject(
            user_id=data['userId'],
            customProject_id=customProjectId,
            projectNotes=data.get('projectNotes'),
            modifiedDateTime=timezone.now(),
            createdDateTime=timezone.now()
        )
        project.save()

        user = UserView.getUser(data['userId'])  # Grab the user with all associated data so we can get files without extra DB query
        UserProjectView.addFiles(project, user, data, fileData, 'file', 'filesMetaData',
                                 UserProjectView.getCreateFileFn(UserFile, 'file'))
        UserProjectView.addFiles(project, user, data, fileData, 'video', 'videosMetaData',
                                 UserProjectView.getCreateFileFn(UserVideo, 'video'))
        UserProjectView.addFiles(project, user, data, fileData, 'image', 'imagesMetaData',
                                 UserProjectView.getCreateFileFn(UserImage, 'image'))

        saveActivity(ActivityKey.CANDIDATE_CREATE_PROJECT, project.user_id)

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
        projects = UserProject.objects \
            .select_related(
            'customProject',
            'customProject__project',
            'customProject__project__role',
            'user'
        ) \
            .prefetch_related(
            'jobApplication',
            'customProject__skills',
            'userProjectEvaluationCriterion',
            'userProjectEvaluationCriterion__employer',
            'userProjectEvaluationCriterion__evaluator',
            'files',
            'images',
            'videos',
            'customProject__project__projectInstructions'
        ) \
            .filter(projectFilter)

        if userProjectId:
            if not projects:
                raise UserProject.DoesNotExist
            return projects[0]

        return projects


class UserProjectStatusView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def put(self, request):
        userProjectId = self.data['id']
        if not userProjectId:
            return Response('A user project ID is required', status=status.HTTP_400_BAD_REQUEST)

        project = UserProjectView.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(project.user_id, user=self.user):
            return Response('You are not authorized to edit this project', status=status.HTTP_401_UNAUTHORIZED)

        projectStatus = self.data.get('status')
        if projectStatus and isUserProjectLocked(project):
            return Response(f'Project is locked for another {dataUtil.pluralize("day", getDaysUntilProjectUnlock(project))}', status=status.HTTP_401_UNAUTHORIZED)

        dataUtil.setObjectAttributes(project, self.data, {
            'status': {'isProtectExisting': True},
            'isHidden': {'isProtectExisting': True},
        })

        if self.data.get('isSubmitApplications'):
            for application in project.jobApplication.all():
                application.withdrawDateTime = None
                application.submissionDateTime = timezone.now()
                application.save()

        if projectStatus:
            project.statusChangeDateTime = timezone.now()
            if projectStatus == UserProject.Status.COMPLETE.value:
                saveActivity(ActivityKey.CANDIDATE_COMPLETE_PROJECT, project.user_id)

        project.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                'userProjects': [getSerializedUserProject(up) for up in
                                 UserProjectView.getUserProjects(userId=self.user.id)],
                'jobApplications': [getSerializedJobApplication(ja, includeJob=True) for ja in
                                    UserJobApplicationView.getUserJobApplications(userId=self.user.id)]
            }
        )


class UserJobApplicationView(UproveAPIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, userJobApplicationId=None):
        userJobApplicationId = userJobApplicationId or self.data.get('id')
        if not userJobApplicationId:
            return Response('A job application ID is required', status=status.HTTP_400_BAD_REQUEST)

        jobApplication = self.getUserJobApplications(userJobApplicationId=userJobApplicationId)

        if not any([
            security.isSelf(jobApplication.userProject.user_id, user=self.user),
            security.isPermittedEmployer(request, jobApplication.employerProject.employer_id)
        ]):
            return Response('You do not have permission to view this job application',
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(getSerializedJobApplication(jobApplication), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        if userProjectId := self.data.get('userProjectId'):
            userProject = UserProjectView.getUserProjects(userProjectId=userProjectId)
            if not security.isSelf(userProject.user_id, user=self.user):
                return Response('You do not have permission to post this job application',
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            userProject = UserProjectView.createUserProject(request, self.data, self.files)
            # Return error response if something went wrong
            if isinstance(userProject, Response):
                return userProject

        try:
            # Check if the candidate has submitted a past application which was withdrawn (and is now reapplying)
            jobApplication = UserJobApplication.objects.get(user_id=self.data['userId'], employerJob_id=self.data['employerJobId'])
            jobApplication.userProject_id = userProject.id
            jobApplication.withdrawDateTime = None
        except UserJobApplication.DoesNotExist:
            # User application is new
            jobApplication = UserJobApplication(
                user_id=self.data['userId'],
                userProject_id=userProject.id,
                employerJob_id=self.data['employerJobId']
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
        isSelf = security.isSelf(jobApplication.userProject.user_id, user=self.user)
        isEmployer = security.isPermittedEmployer(request, jobApplication.employerJob.employer_id)
        if not any([isSelf, isEmployer]):
            return Response('You do not have permission to update this job application',
                            status=status.HTTP_401_UNAUTHORIZED)

        dtGetter = lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATETIME, allowNone=True)
        if isSelf and data.get('userProjectId'):
            dataUtil.setObjectAttributes(jobApplication, data, {
                'user_id': {'formName': 'userId'},
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
        if not security.isSelf(jobApplication.userProject.user_id, user=self.user):
            return Response('You do not have permission to delete this job application',
                            status=status.HTTP_401_UNAUTHORIZED)

        jobApplication.delete()
        return Response(status=status.HTTP_200_OK, data=userJobApplicationId)

    @staticmethod
    def getUserJobApplications(userJobApplicationId=None, userId=None, userProjectId=None, employerJobId=None,
                               employerId=None):
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

        userJobApplications = UserJobApplication.objects \
            .select_related(
            'user',
            'userProject',
            'userProject__user',
            'userProject__customProject',
            'userProject__customProject__project',
            'userProject__customProject__project__role',
            'employerJob'
        ) \
            .prefetch_related(
            'userProject__files',
            'userProject__images',
            'userProject__videos',
            'userProject__customProject__skills',
            'employerJob__allowedProjects',
            'employerJob__allowedProjects__project',
            'employerJob__allowedProjects__project__role',
            'employerJob__allowedProjects__skills',
        ) \
            .filter(applicationFilter)

        if userJobApplicationId:
            if not userJobApplications:
                raise UserJobApplication.DoesNotExist
            return userJobApplications[0]

        return userJobApplications


class UserJobSuggestions(UproveAPIView):

    def get(self, request):
        if not self.user:
            return Response('You do not have permission to view this data', status=status.HTTP_401_UNAUTHORIZED)

        user = UserView.getUser(self.user.id)
        jobSuggestions = self.getUserSuggestedJobs(user)
        projectIdsByRole, projectRoleIdsByRole = JobPostingView.getProjectRoleMaps()
        return Response(status=status.HTTP_200_OK, data=[{
                **getSerializedEmployerJob(job),
                'projectIds': projectIdsByRole[job.role.roleTitle],
                'projectRoleIds': list(projectRoleIdsByRole[job.role.roleTitle])
            } for job in jobSuggestions])

    @staticmethod
    def getUserSuggestedJobs(user, jobLimit=10):
        if not user.hasPreferences:
            return []
        filter = JobPostingView.getEmployerJobFilter()
        countryIds = [c.id for c in user.preferenceCountry.all()]
        if not (user.preferenceRemoteBits & user.REMOTE_PREF_YES):
            filter &= Q(country_id__in=countryIds)
        else:
            filter &= (
                    Q(country_id__in=countryIds) |
                    Q(country_id__isnull=True)
            )

        if user.preferenceRemoteBits == user.REMOTE_PREF_YES:
            filter &= Q(isRemote=True)

        companySizeIds = [c.id for c in user.preferenceCompanySizes.all()]
        filter &= Q(employer__companySize_id__in=companySizeIds)

        roleIds = [r.id for r in user.preferenceRoles.all()]
        filter &= Q(role_id__in=roleIds)
        return JobPostingView.getEmployerJobs(jobFilter=filter)[:jobLimit]


class WaitlistView(UproveAPIView):

    def post(self, request):
        if not (email := self.data.get('email')):
            return Response('An email is required', status=status.HTTP_400_BAD_REQUEST)

        Waitlist(
            email=email,
            signUpDateTime=timezone.now(),
            waitlistType=Waitlist.WaitlistType.MENTOR.value
        ).save()

        EmailView.sendEmail(
            'Uprove | Thanks for your interest in a hiring coach',
            [email],
            djangoContext={
                'supportEmail': EmailView.EMAIL_ROUTES[EmailView.TYPE_CANDIDATE_SIGNUP]
            },
            djangoEmailBodyTemplate='email/waitlistEmail.html'
        )

        EmailView.sendEmail(
            'New waitlist signup!',
            EmailView.EMAIL_ROUTES[EmailView.TYPE_CANDIDATE_SIGNUP],
            djangoContext={
                'bodyContent': email,
                'isInternal': True
            },
            djangoEmailBodyTemplate='email/generalEmail.html'
        )

        return Response(status=status.HTTP_200_OK)


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
        imageUrl = static(f'img/{imageName}')
        fileOpenner = lambda url: urllib.request.urlopen(url)
        if settings.DEBUG:
            imageUrl = f'up{imageUrl}'
            fileOpenner = lambda url: open(url, 'rb')
        with fileOpenner(imageUrl) as logoFile:
            logo = MIMEImage(logoFile.read())
            logo.add_header('Content-ID', f'<logo>')
            logo.add_header('X-Attachment-Id', 'logo')
            logo.add_header('Content-Disposition', 'inline', filename=imageName)
            email_message.attach(logo)

        email_message.send()


def generatePassword():
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS + '!@#$%^&*()-+=')
