from rest_framework import status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
# TODO create an IsOwnerOrReadOnly wrapper
from ..models import *
from ..utils.dateUtil import serializeDatetime

__all__ = [
    'OrganizationView', 'UserVideoView', 'UserFileView', 'UserImageView', 'UserEducationItemView',
    'UserExperienceItemView', 'UserContentItemView', 'UserProfileSectionView', 'UserView', 'UserProfileView'
]


def serializeAuditFields(obj):
    createdDateTime = getattr(obj, 'createdDateTime', None)
    modifiedDateTime = getattr(obj, 'modifiedDateTime', None)
    return {
        'createdDateTime': serializeDatetime(createdDateTime) if createdDateTime else None,
        'modifiedDateTime': serializeDatetime(modifiedDateTime) if modifiedDateTime else None
    }


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

    @staticmethod
    def serializeOrganization(org):
        return {
            'orgId': org.id,
            'name': org.name,
            'orgType': org.orgType,
            'logo': org.logo,
        }


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

    @staticmethod
    def serializeVideo(video):
        return {
            'videoId': video.id,
            'title': video.title,
            'video': video.video,
            **serializeAuditFields(video)
        }


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
    def serializeFile(file):
        return {
            'fileId': file.id,
            'title': file.title,
            'file': file.file,
            **serializeAuditFields(file)
        }


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
    def serializeImage(image):
        return {
            'imageId': image.id,
            'title': image.title,
            'image': image.image,
            'isDefault': image.isDefault,
            **serializeAuditFields(image)
        }


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

    @staticmethod
    def serializeEducationItem(educationItem):
        return {
            'educationId': educationItem.id,
            'school': OrganizationView.serializeOrganization(educationItem.school),
            'degree': educationItem.degree,
            'degreeSubject': educationItem.degreeSubject,
            'activities': educationItem.activities,
            'startDate': serializeDatetime(educationItem.startDate, allowNone=True),
            'endDate': serializeDatetime(educationItem.endDate, allowNone=True),
            **serializeAuditFields(educationItem)
        }


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

    @staticmethod
    def serializeExperienceItem(experienceItem):
        return {
            'experienceId': experienceItem.id,
            'organization': OrganizationView.serializeOrganization(experienceItem.organization),
            'positionTitle': experienceItem.positionTitle,
            'employmentType': experienceItem.employmentType,
            'startDate': serializeDatetime(experienceItem.startDate),
            'endDate': serializeDatetime(experienceItem.endDate, allowNone=True),
            'description': experienceItem.description,
            **serializeAuditFields(experienceItem)
        }


class UserContentItemView(APIView):
    CONTENT_ITEM_SERIALIZERS = {
        'UserVideo': UserVideoView.serializeVideo,
        'UserFile': UserFileView.serializeFile,
        'UserImage': UserImageView.serializeImage
    }

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

    @staticmethod
    def serializeContentItem(contentItem):
        return {
            'contentId': contentItem.id,
            'title': contentItem.title,
            'sections': [
                {
                    'contentOrder': section.contentOrder,
                    'text': section.text,
                    'content': UserContentItemView.serializeContentSection(section)
                } for section in contentItem.section.all()
            ],
            **serializeAuditFields(contentItem)
        }

    @staticmethod
    def serializeContentSection(section):
        if not section.contentType:
            return None

        serializer = UserContentItemView.CONTENT_ITEM_SERIALIZERS[section.contentType.model]
        return serializer(section.contentObject)


class UserProfileSectionView(APIView):
    CONTENT_ITEM_SERIALIZERS = {
        'UserEducation': UserEducationItemView.serializeEducationItem,
        'UserExperience': UserExperienceItemView.serializeExperienceItem,
        'UserContentItem': UserContentItemView.serializeContentItem
    }

    def post(self, request):
        pass

    def put(self, request, sectionId):
        pass

    @staticmethod
    def getProfileSection(sectionId):
        try:
            return UserProfileSection.objects.prefetch_related('sectionItem', 'sectionItem__contentObject').get(id=sectionId)
        except UserProfileSection.DoesNotExist as e:
            raise e

    @staticmethod
    def serializeProfileSection(section):
        return {
            'sectionId': section.id,
            'title': section.title,
            'description': section.description,
            'sectionOrder': section.sectionOrder,
            'items': [
                {
                    'contentOrder': item.contentOrder,
                    'content': UserProfileSectionView.serializeItemContent(item)
                } for item in section.sectionItem
            ]
        }

    @staticmethod
    def serializeItemContent(item):
        if not item.contentType:
            return None

        serializer = UserProfileSectionView.CONTENT_ITEM_SERIALIZERS[item.contentType.model]
        return serializer(item.contentObject)


class UserView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def get(self, request, userId=None):
        return Response(self.serializeUser(self.getUser(userId)), status=status.HTTP_200_OK)

    def put(self, request, userId=None):
        user = self.getUser(userId)
        # TODO: get data and add to model

    @staticmethod
    def getUser(userId):
        try:
            return User.objects.prefetch_related('image').get(id=userId)
        except User.DoesNotExist as e:
            raise e

    @staticmethod
    def serializeUser(user):
        return {
            'userId': user.id,
            'firstName': user.firstName,
            'middleName': user.middleName,
            'lastName': user.lastName,
            'birthDate': serializeDatetime(user.birthDate),
            'profilePicture': next((image.image for image in user.image.all() if image.isDefault), None),
            **serializeAuditFields(user)
        }


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

    @staticmethod
    def serializeUserProfile(profile):
        # TODO: only add password if the user owns the profile
        # 'password': profile.password
        return {
            'user': UserView.serializeUser(profile.user),
            'profileId': profile.id,
            'profileName': profile.profileName,
            'profilePicture': profile.profilePicture,
            'makePublic': profile.makePublic,
            **serializeAuditFields(profile),
            'sections': [
                UserProfileSectionView.serializeProfileSection(section) for section in profile.section.all()
            ]
        }
