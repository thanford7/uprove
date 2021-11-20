from operator import itemgetter

from upapp.models import *


def getDateTimeFormatOrNone(val):
    """Serialize a date or datetime value if it exists, otherwise return None"""
    if val:
        return val.isoformat()
    return None


def serializeAuditFields(obj):
    return {
        'createdDateTime': obj.createdDateTime.isoformat(),
        'modifiedDateTime': obj.modifiedDateTime.isoformat()
    }


def serializeGenericItem(item):
    if item.contentType == 'UserVideo':
        return getSerializedUserVideo(item.contentObject)
    if item.contentType == 'UserFile':
        return getSerializedUserFile(item.contentObject)
    if item.contentType == 'UserImage':
        return getSerializedUserImage(item.contentObject)
    if item.contentType == 'UserEducation':
        return getSerializedUserEducation(item.contentObject)
    if item.contentType == 'UserExperience':
        return getSerializedUserExperience(item.contentObject)
    raise ValueError(f'Unknown content type: {item.contentType}')


def getSerializedUser(user: User, isIncludeAssets: bool=False):
    serializedUser = {
        'id': user.id,
        'firstName': user.firstName,
        'middleName': user.middleName,
        'lastName': user.lastName,
        'birthDate': user.birthDate.isoformat(),
        'email': user.email,
        'userTypeBits': user.userTypeBits,
        'isStaff': user.djangoUser.is_staff,
        'isActive': user.djangoUser.is_active,
        'isSuperUser': user.djangoUser.is_superuser,
        **serializeAuditFields(user)
    }

    if isIncludeAssets:
        serializedUser['profiles'] = [getSerializedUserProfile(p) for p in user.profile.all()]
        serializedUser['education'] = [getSerializedUserEducation(e) for e in user.education.all()]
        serializedUser['experience'] = [getSerializedUserExperience(e) for e in user.experience.all()]
        serializedUser['content'] = [getSerializedUserContentItem(ci) for ci in user.contentItem.all()]
        serializedUser['videos'] = [getSerializedUserVideo(v) for v in user.video.all()]
        serializedUser['files'] = [getSerializedUserFile(f) for f in user.file.all()]
        serializedUser['images'] = [getSerializedUserImage(i) for i in user.image.all()]
        serializedUser['tags'] = [getSerializedUserTag(t) for t in user.tag.all()]

    return serializedUser


def getSerializedUserProfile(userProfile: UserProfile):
    return {
        'profileName': userProfile.profileName,
        'makePublic': userProfile.makePublic,
        'profilePicture': getSerializedUserImage(userProfile.profilePicture),
        'sections': [getSerializedUserProfileSection(ps) for ps in userProfile.section.all()],
        **getSerializedUser(userProfile.user),
        **serializeAuditFields(userProfile)
    }


def getSerializedUserProfileSection(userProfileSection: UserProfileSection):
    return {
        'title': userProfileSection.title,
        'description': userProfileSection.description,
        'sectionOrder': userProfileSection.sectionOrder,
        'sectionItems': sorted(
            [getSerializedUserProfileSectionItem(psi) for psi in userProfileSection.sectionItem.all()],
            key=itemgetter('contentOrder')
        )
    }


def getSerializedUserProfileSectionItem(userProfileSectionItem: UserProfileSectionItem):
    return {
        'id': userProfileSectionItem.id,
        'contentOrder': userProfileSectionItem.contentOrder,
        'item': serializeGenericItem(userProfileSectionItem)
    }


def getSerializedUserEducation(userEducation: UserEducation):
    return {
        'id': userEducation.id,
        'school': getSerializedOrganization(userEducation.school),
        'degree': userEducation.degree,
        'degreeSubject': userEducation.degreeSubject,
        'activities': userEducation.activities,
        'startDate': getDateTimeFormatOrNone(userEducation.startDate),
        'endDate': getDateTimeFormatOrNone(userEducation.endDate),
        **serializeAuditFields(userEducation)
    }


def getSerializedUserExperience(userExperience: UserExperience):
    return {
        'id': userExperience.id,
        'organization': getSerializedOrganization(userExperience.organization),
        'positionTitle': userExperience.positionTitle,
        'employmentType': userExperience.employmentType,
        'startDate': userExperience.startDate.isoformat(),
        'endDate': getDateTimeFormatOrNone(userExperience.endDate),
        'description': userExperience.description,
        **serializeAuditFields(userExperience)
    }


def getSerializedUserContentItem(userContentItem: UserContentItem):
    return {
        'id': userContentItem.id,
        'title': userContentItem.title,
        'sections': sorted([getSerializedUserContentItemSection(cis) for cis in userContentItem.section.all()], key=itemgetter('contentOrder')),
        **serializeAuditFields(userContentItem)
    }


def getSerializedUserContentItemSection(userContentItemSection: UserContentItemSection):
    return {
        'id': userContentItemSection.id,
        'contentOrder': userContentItemSection.contentOrder,
        'text': userContentItemSection.text,
        'item': serializeGenericItem(userContentItemSection)
    }


def getSerializedUserVideo(userVideo: UserVideo):
    return {
        'id': userVideo.id,
        'title': userVideo.title,
        'video': userVideo.video,
        **serializeAuditFields(userVideo)
    }


def getSerializedUserFile(userFile: UserFile):
    return {
        'id': userFile.id,
        'title': userFile.title,
        'file': userFile.file,
        **serializeAuditFields(userFile)
    }


def getSerializedUserImage(userImage: UserImage):
    return {
        'id': userImage.id,
        'title': userImage.title,
        'file': userImage.image,
        **serializeAuditFields(userImage)
    }


def getSerializedUserTag(userTag: UserTag):
    return {
        'id': userTag.id,
        'tagType': userTag.tagType,
        'title': userTag.title,
        'description': userTag.description,
        'skillLevelNum': userTag.skillLevel,
        **serializeAuditFields(userTag)
    }


def getSerializedOrganization(organization: Organization):
    return {
        'id': organization.id,
        'name': organization.name,
        'orgType': organization.orgType,
        'logo': organization.logo
    }


def getSerializedProject(project: Project):
    return {
        'id': project.id,
        'title': project.title,
        'function': project.function.functionName,
        'functionId': project.function.id,
        'skills': [{'name': s.skillName, 'id': s.id} for s in project.skills.all()],
        'skillLevel': project.skillLevel,
        'description': project.description,
        'employer': getSerializedEmployer(project.employer),
        'files': [getSerializedProjectFile(pf) for pf in project.projectFile.all()]
    }


def getSerializedProjectFile(projectFile: ProjectFile):
    return {
        'id': projectFile.id,
        'title': projectFile.title,
        'description': projectFile.description,
        'file': projectFile.file,
        **serializeAuditFields(projectFile)
    }


def getSerializedEmployer(employer: Employer):
    return {
        'id': employer.id,
        'companyName': employer.companyName,
        'logo': employer.logo,
        **serializeAuditFields(employer)
    }
