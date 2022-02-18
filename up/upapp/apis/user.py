import urllib.request
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
from upapp.apis import UproveAPIView, saveActivity, ActivityKey
from upapp.apis.employer import JobPostingView, OrganizationView
from upapp.apis.project import SkillView
from upapp.apis.sendEmail import EmailView
from upapp.models import *
from upapp.modelSerializers import ContentTypes, getSerializedUser, getSerializedJobApplication, getSerializedUserProject, \
    getSerializedUserVideo, getSerializedUserProfile, getSerializedUserExperience, \
    getSerializedUserEducation, getSerializedUserContentItem
from upapp.utils import dataUtil, dateUtil


CONTENT_TYPE_MODELS = {
    ContentTypes.EXPERIENCE.value: {'model': UserExperience, 'serializer': getSerializedUserExperience},
    ContentTypes.EDUCATION.value: {'model': UserEducation, 'serializer': getSerializedUserEducation},
    ContentTypes.VIDEO.value: {'model': UserVideo, 'serializer': getSerializedUserVideo},
    ContentTypes.CUSTOM.value: {'model': UserContentItem, 'serializer': getSerializedUserContentItem},
    ContentTypes.PROJECT.value: {'model': UserProject, 'serializer': getSerializedUserProject}
}


class UserVideoView(UproveAPIView):
    def post(self, request):
        rawAvVideo = self.data.get('avVideo')
        rawScreenVideo = self.data.get('screenVideo')
        if not any([rawAvVideo, rawScreenVideo]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='At least one video is required')

        # TODO: Process video data
        userVideo = self.createUserVideo(self.user, self.data)

        return Response(status=status.HTTP_200_OK, data=getSerializedUserVideo(userVideo))

    def put(self, request, videoId):
        pass

    @staticmethod
    def getVideo(videoId):
        try:
            return UserVideo.objects.get(id=videoId)
        except UserVideo.DoesNotExist as e:
            raise e

    @staticmethod
    @atomic
    def createUserVideo(user, data):
        video = UserVideo(
            user=user,
            video=data['video'],
            title=data.get('title') or data['video'].name,
            createdDateTime=datetime.utcnow(),
            modifiedDateTime=datetime.utcnow()
        )
        video.save()
        return video


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
                createdDateTime=datetime.utcnow(),
                modifiedDateTime=datetime.utcnow()
            )
            file.save()
            savedFiles.append(file)

        return savedFiles


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

    @staticmethod
    @atomic
    def createUserImage(user, data):
        image = UserImage(
            user=user,
            image=data['image'],
            title=data.get('title') or data['image'].name,
            createdDateTime=datetime.utcnow(),
            modifiedDateTime=datetime.utcnow()
        )
        image.save()
        return image


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
        if not (security.isPermittedAdmin(request) or security.isSelf(userId, request=request)):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = self.getUser(userId)
        self.updateUser(user, request.data)
        currentUproveUser = security.getSessionUser(request)
        if security.isSelf(userId, user=user) or not currentUproveUser:
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
                    'tag',
                    'userProject',
                    'userProject__user',
                    'userProject__videos',
                    'userProject__images',
                    'userProject__files',
                    'userProject__customProject',
                    'userProject__customProject__skills',
                    'userProject__customProject__project',
                    'userProject__customProject__project__role'
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
        return User.objects.select_related('djangoUser').prefetch_related('image', 'profile').all()

    @staticmethod
    def updateUser(user, data):
        dataUtil.setObjectAttributes(user, data, {
            'firstName': None,
            'middleName': None,
            'lastName': None,
            'birthDate': {'propFunc': lambda val: dateUtil.deserializeDateTime(val, dateUtil.FormatType.DATE, allowNone=True)},
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
            modifiedDateTime=datetime.utcnow(),
            createdDateTime=datetime.utcnow()
        )
        user.save()
        saveActivity(ActivityKey.CREATE_ACCOUNT, user.id)

        return user, bool(password)


class UserProfileView(UproveAPIView):
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
        dataUtil.setObjectAttributes(profile, self.data, {
            'profileName': None
        })

        if profilePicture := self.data.get('newProfilePicture'):
            profile.profilePicture = UserImageView.createUserImage(self.user, {'image': profilePicture})

        profile.save()
        return self.getProfileOwnerResponse(profile.id)

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

    @staticmethod
    def getProfileOwnerResponse(profileId):
        return Response(
            status=status.HTTP_200_OK,
            data=getSerializedUserProfile(UserProfileView.getUserProfile(profileId), isOwner=True)
        )


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
                    s.sectionOrder -=1
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
            return UserProfileSection.objects\
                .select_related('userProfile')\
                .prefetch_related('sectionItem')\
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
            return Response(f'Content order must be between 1 and {sectionContentCount}', status=status.HTTP_400_BAD_REQUEST)

        contentItem = next((s for s in sectionItems if s.id == contentId), None)
        if not contentItem:
            return Response(f'Content item with ID={contentId} is not in the specified section', status=status.HTTP_400_BAD_REQUEST)

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

        sectionContentItem.delete()
        return UserProfileView.getProfileOwnerResponse(sectionContentItem.userProfileSection.userProfile.id)

    @staticmethod
    def getUserProfileSectionItem(contentId):
        return UserProfileSectionItem.objects\
            .select_related('userProfileSection', 'userProfileSection__userProfile')\
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
        # Note this endpoint will actually delete the content. To disassociate content from a section, use {TODO} endpoint
        pass

    @atomic
    def createOrUpdateContentItem(self, contentType, contentItem=None):
        # Save the content item depending on the type of content
        if contentType == ContentTypes.EXPERIENCE.value:
            contentItem = contentItem or UserExperience(
                createdDateTime=datetime.utcnow()
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
                createdDateTime=datetime.utcnow()
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
                'startDate': {'propFunc': lambda val: dateGetter(val, False)},
                'endDate': {'propFunc': lambda val: dateGetter(val, True)},
                'activities': None
            })
            contentItem.save()
            return contentItem
        elif contentType in [ContentTypes.CUSTOM.value, ContentTypes.VIDEO.value]:
            contentItem = contentItem or UserContentItem(createdDateTime=datetime.utcnow())
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
                        section['video'] = self.data[mediaKey]
                        contentItems = [UserVideoView.createUserVideo(self.user, section)]
                    else:
                        contentItems = [UserVideoView.getVideo(section['value'])]
                elif section['type'] == 'image':
                    if mediaKey:
                        section['image'] = self.data[mediaKey]
                        contentItems = [UserImageView.createUserImage(self.user, section)]
                    else:
                        contentItems = [UserImageView.getImage(section['value'])]
                elif section['type'] == 'file':
                    if mediaKey:
                        section['file'] = self.data[mediaKey]
                        contentItems = UserFileView.createUserFiles(self.user, section)
                    else:
                        if not isinstance(section['value'], list):
                            section['value'] = [section['value']]
                        contentItems = list(UserFile.objects.filter(id__in=section['value']))

                if contentItems:
                    for item in contentItems:
                        UserContentItemSection(
                            userContentItem=contentItem,
                            contentOrder=sectionIdx,
                            contentObject=item
                        ).save()
                        sectionIdx += 1
                else:
                    UserContentItemSection(
                        userContentItem=contentItem,
                        contentOrder=sectionIdx,
                        text=section['value']
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
            return Response([getSerializedUserProject(up) for up in self.getUserProjects(userId)], status=status.HTTP_200_OK)

        project = self.getUserProjects(userProjectId=userProjectId)
        if not security.isSelf(project.user_id, user=self.user):
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
        if not security.isSelf(project.user_id, user=self.user):
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
        if not security.isSelf(project.user_id, user=self.user):
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
            return Response(f'User project for {project.customProject.project.title} already exists', status=status.HTTP_409_CONFLICT)

        project = UserProject(
            user_id=data['userId'],
            customProject_id=customProjectId,
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
                'customProject__project__role',
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
            return Response('You do not have permission to view this job application', status=status.HTTP_401_UNAUTHORIZED)

        return Response(getSerializedJobApplication(jobApplication), status=status.HTTP_200_OK)

    @atomic
    def post(self, request):
        if userProjectId := self.data.get('userProjectId'):
            userProject = UserProjectView.getUserProjects(userProjectId=userProjectId)
            if not security.isSelf(userProject.user_id, user=self.user):
                return Response('You do not have permission to post this job application', status=status.HTTP_401_UNAUTHORIZED)
        else:
            userProject = UserProjectView.createUserProject(request, self.data)
            # Return error response if something went wrong
            if isinstance(userProject, Response):
                return userProject

        jobApplication = UserJobApplication(
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
        if not security.isSelf(jobApplication.userProject.user_id, user=self.user):
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
                'userProject__customProject__project__role',
                'employerJob'
            )\
            .prefetch_related(
                'userProject__files',
                'userProject__images',
                'userProject__videos',
                'userProject__customProject__skills',
                'employerJob__allowedProjects',
                'employerJob__allowedProjects__project',
                'employerJob__allowedProjects__project__role',
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
    return crypto.get_random_string(length=30, allowed_chars=crypto.RANDOM_STRING_CHARS+'!@#$%^&*()-+=')
