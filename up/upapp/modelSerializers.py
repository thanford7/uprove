from datetime import date
from enum import Enum
from operator import itemgetter

from upapp.models import *
from upapp.utils.dataUtil import getFileNameFromUrl
from upapp.utils.htmlTruncate import truncate


# Keep in sync with CONTENT_TYPES in globalData.js
class ContentTypes(Enum):
    EXISTING = 'existing'
    EDUCATION = 'education'
    EXPERIENCE = 'experience'
    PROJECT = 'project'
    CUSTOM = 'custom'
    VIDEO = 'video'
    FILE = 'file'
    IMAGE = 'image'


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


def _addSerializedUserAssets(dataDict, user):
    dataDict[ContentTypes.EDUCATION.value] = [getSerializedUserEducation(e) for e in user.education.all()]
    dataDict[ContentTypes.EXPERIENCE.value] = [getSerializedUserExperience(e) for e in user.experience.all()]
    dataDict[ContentTypes.CUSTOM.value] = [getSerializedUserContentItem(ci) for ci in user.contentItem.all()]
    dataDict[ContentTypes.PROJECT.value] = [getSerializedUserProject(up) for up in user.userProject.all()]
    dataDict['videos'] = [getSerializedUserVideo(v) for v in user.video.all()]
    dataDict['files'] = [getSerializedUserFile(f) for f in user.file.all()]
    dataDict['images'] = [getSerializedUserImage(i) for i in user.image.all()]


def serializeGenericItem(item):
    if not item.contentObject:
        return None
    if isinstance(item.contentObject, UserVideo):
        return getSerializedUserVideo(item.contentObject)
    if isinstance(item.contentObject, UserFile):
        return getSerializedUserFile(item.contentObject)
    if isinstance(item.contentObject, UserImage):
        return getSerializedUserImage(item.contentObject)
    if isinstance(item.contentObject, UserEducation):
        return getSerializedUserEducation(item.contentObject)
    if isinstance(item.contentObject, UserExperience):
        return getSerializedUserExperience(item.contentObject)
    if isinstance(item.contentObject, UserContentItem):
        return getSerializedUserContentItem(item.contentObject)
    if isinstance(item.contentObject, UserProject):
        return getSerializedUserProject(item.contentObject)
    raise ValueError(f'Unknown content type: {item.contentType}')


def getSerializedUser(user: User, isIncludeAssets: bool=False):
    profileImage = next((i.image.url for i in user.image.all() if i.isDefault), None)
    serializedUser = {
        'id': user.id,
        'firstName': user.firstName,
        'middleName': user.middleName,
        'lastName': user.lastName,
        'birthDate': getDateTimeFormatOrNone(user.birthDate),
        'email': user.email,
        'profileImage': profileImage,
        'defaultProfileId': next((p.id for p in user.profile.all() if p.isPrimary), None),
        'employerId': user.employer_id,
        'inviteEmployerId': user.inviteEmployer_id,
        'userTypeBits': user.userTypeBits,
        'isStaff': user.djangoUser.is_staff,
        'isActive': user.djangoUser.is_active,
        'isSuperUser': user.djangoUser.is_superuser,
        'isDemo': user.isDemo,
        'isAuthenticated': user.djangoUser.is_authenticated,
        'skills': [getSerializedUserTag(t) for t in user.userTag.filter(tag__type=Tag.TYPE_SKILL)],
        'interests': [getSerializedUserTag(t) for t in user.userTag.filter(tag__type=Tag.TYPE_INTEREST)],
        **serializeAuditFields(user)
    }

    if isIncludeAssets:
        serializedUser['profiles'] = [getSerializedUserProfile(p) for p in user.profile.all()]
        _addSerializedUserAssets(serializedUser, user)

    return serializedUser


def getSerializedUserProfile(userProfile: UserProfile, isOwner=None):
    serializedProfile = {
        'id': userProfile.id,
        'profileName': userProfile.profileName,
        'makePublic': userProfile.makePublic,
        'isOwner': isOwner,
        'profilePicture': getSerializedUserImage(userProfile.profilePicture) if userProfile.profilePicture else None,
        'sections': sorted(
            [getSerializedUserProfileSection(ps) for ps in userProfile.section.all()],
            key=itemgetter('sectionOrder')
        ),
        'user': getSerializedUser(userProfile.user),
        **serializeAuditFields(userProfile)
    }

    if isOwner:
        serializedProfile['assets'] = {}
        _addSerializedUserAssets(serializedProfile['assets'], userProfile.user)

    return serializedProfile


def getSerializedUserProfileSection(userProfileSection: UserProfileSection):
    return {
        'id': userProfileSection.id,
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
        'type': ContentTypes.EDUCATION.value,
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
        'type': ContentTypes.EXPERIENCE.value,
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
        'type': ContentTypes.CUSTOM.value,
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
        'type': ContentTypes.VIDEO.value,
        'title': userVideo.title,
        'video': userVideo.video.url,
        **serializeAuditFields(userVideo)
    }


def getSerializedUserFile(userFile: UserFile):
    return {
        'id': userFile.id,
        'type': ContentTypes.FILE.value,
        'title': userFile.title,
        'file': userFile.file.url,
        'fileName': userFile.file.name.split('/')[-1],
        **serializeAuditFields(userFile)
    }


def getSerializedUserImage(userImage: UserImage):
    return {
        'id': userImage.id,
        'type': ContentTypes.IMAGE.value,
        'title': userImage.title,
        'image': userImage.image.url,
        **serializeAuditFields(userImage)
    }


def getSerializedUserTag(userTag: UserTag):
    return {
        'id': userTag.id,
        'tagType': userTag.tag.type,
        'tagId': userTag.tag.id,
        'title': userTag.tag.title,
        'description': userTag.description or userTag.tag.description,
        'skillLevelBit': userTag.skillLevelBit,
        **serializeAuditFields(userTag)
    }


def getSerializedTag(tag: Tag):
    return {
        'id': tag.id,
        'title': tag.title,
        'type': tag.type,
        'description': tag.description
    }


def getSerializedOrganization(organization: Organization):
    return {
        'id': organization.id,
        'name': organization.name,
        'orgType': organization.orgType,
        'logo': organization.logo.url if organization.logo else None,
    }


def getSerializedProject(project: Project, isIncludeDetails:bool=False, isAdmin=False, evaluationEmployerId=None):
    return {
        'id': project.id,
        'title': project.title,
        'image': project.image.url if project.image else None,
        'role': project.role.name,
        'roleId': project.role.id,
        'skills': [getSerializedSkill(s) for s in project.skills.all()],
        'skillLevelBits': project.skillLevelBits,
        'description': project.description,
        'background': project.background if isIncludeDetails else truncate(project.background, 250, ellipsis='...'),
        'instructions': [getSerializedProjectInstructions(pi) for pi in project.projectInstructions.all()],
        'evaluationCriteria': [
            getSerializedProjectEvaluationCriterion(ec)
            for ec in project.evaluationCriteria.all()
            if ec.employer_id is None or ec.employer_id == evaluationEmployerId
        ] if (evaluationEmployerId or isAdmin) else None,
        'employer': {
            'id': project.employer.id,
            'companyName': project.employer.companyName
        } if project.employer else None,
        'files': [getSerializedProjectFile(pf, isIncludeDetails) for pf in project.projectFile.all()],
        'isLimited': not isIncludeDetails
    }


def getSerializedProjectInstructions(projectInstructions: ProjectInstructions):
    return {
        'id': projectInstructions.id,
        'instructions': projectInstructions.instructions,
        'skillLevelBit': projectInstructions.skillLevelBit,
        **serializeAuditFields(projectInstructions)
    }


def getSerializedProjectEvaluationCriterion(evaluationCriterion: ProjectEvaluationCriterion):
    return {
        'id': evaluationCriterion.id,
        'criterion': evaluationCriterion.criterion,
        'category': evaluationCriterion.category,
        'skillLevelBits': evaluationCriterion.skillLevelBits,
        'employerId': evaluationCriterion.employer_id
    }


def getSerializedProjectFile(projectFile: ProjectFile, isIncludeDetails:bool=False):
    return {
        'id': projectFile.id,
        'title': projectFile.title,
        'description': projectFile.description,
        'file': projectFile.file.url if isIncludeDetails else None,
        'fileName': getFileNameFromUrl(projectFile.file.url),
        'skillLevelBits': projectFile.skillLevelBits,
        **serializeAuditFields(projectFile)
    }


def getSerializedRole(role: Role):
    return {'id': role.id, 'name': role.name}


def getSerializedSkill(skill: Skill):
    return {
        'id': skill.id,
        'name': skill.name,
        'instruction': skill.instruction,
        'isRequired': skill.isRequired,
        'isRecommended': skill.isRecommended,
        'projectId': skill.skillProject_id,
        'skillLevelBits': skill.skillLevelBits
    }


def getSerializedEmployer(employer: Employer, isEmployer=False):
    baseFields = {
        'id': employer.id,
        'companyName': employer.companyName,
        'logo': employer.logo.url if employer.logo else None,
        'description': employer.description,
        'isDemo': employer.isDemo,
        'jobs': [getSerializedEmployerJob(ej, isEmployer=isEmployer) for ej in employer.employerJob.all()],
    }
    employerFields = {
        **serializeAuditFields(employer)
    }
    return baseFields if not isEmployer else {**baseFields, **employerFields}


def getSerializedCustomProject(customProject: CustomProject):
    return {
        'id': customProject.id,
        'skillLevelBit': customProject.skillLevelBit,
        'skills': [getSerializedSkill(s) for s in customProject.skills.all()],
        'projectId': customProject.project_id,
        'projectTitle': customProject.project.title
    }


def getSerializedEmployerCustomProjectCriterion(criterion: EmployerCustomProjectCriterion):
    return {
        'id': criterion.id,
        'employerId': criterion.employer_id,
        'customProjectId': criterion.customProject_id,
        'evaluationCriterionId': criterion.evaluationCriterion_id
    }


def getSerializedEmployerJob(employerJob: EmployerJob, isEmployer=False):
    baseFields = {
        'id': employerJob.id,
        'jobTitle': employerJob.jobTitle,
        'jobDescription': employerJob.jobDescription,
        'allowedProjects': [getSerializedCustomProject(ep) for ep in employerJob.allowedProjects.all()],
        'salaryFloor': employerJob.salaryFloor,
        'salaryCeiling': employerJob.salaryCeiling,
        'salaryUnit': employerJob.salaryUnit,
        'openDate': employerJob.openDate.isoformat() if employerJob.openDate else None,
        'pauseDate': employerJob.pauseDate.isoformat() if employerJob.pauseDate else None,
        'closeDate': employerJob.closeDate.isoformat() if employerJob.closeDate else None,
    }
    employerFields = {
        'applications': [getSerializedJobApplication(app, isEmployer=True) for app in employerJob.jobApplication.all()],
        **serializeAuditFields(employerJob)
    }

    return baseFields if not isEmployer else {**baseFields, **employerFields}


def getSerializedJobTemplate(template: JobTemplate):
    return {
        'id': template.id,
        'title': template.title,
        'description': template.description
    }


def getSerializedJobApplication(jobApplication: UserJobApplication, includeJob=False, isEmployer=False):
    val = {
        'id': jobApplication.id,
        'user': {
            'id': jobApplication.user.id,
            'firstName': jobApplication.user.firstName,
            'middleName': jobApplication.user.middleName,
            'lastName': jobApplication.user.lastName,
            'email': jobApplication.user.email
        },
        'userProject': getSerializedUserProject(jobApplication.userProject, isEmployer=isEmployer) if jobApplication.userProject else None,
        'inviteDateTime': getDateTimeFormatOrNone(jobApplication.inviteDateTime),
        'submissionDateTime': getDateTimeFormatOrNone(jobApplication.submissionDateTime),
        'approveDateTime': getDateTimeFormatOrNone(jobApplication.approveDateTime),
        'declineDateTime': getDateTimeFormatOrNone(jobApplication.declineDateTime),
        'withdrawDateTime': getDateTimeFormatOrNone(jobApplication.withdrawDateTime),
    }

    if includeJob:
        val['job'] = {
            'id': jobApplication.employerJob.id,
            'jobTitle': jobApplication.employerJob.jobTitle,
            'employer': jobApplication.employerJob.employer.companyName,
            'employerLogo': jobApplication.employerJob.employer.logo.url if jobApplication.employerJob.employer.logo else None,
            'allowedProjects': [getSerializedCustomProject(ep) for ep in jobApplication.employerJob.allowedProjects.all()]
        }

    return val


def getSerializedUserProjectEvaluationCriterion(criterion: UserProjectEvaluationCriterion):
    return {
        'id': criterion.id,
        'userProjectId': criterion.userProject_id,
        'employer': {
            'id': criterion.employer_id,
            'companyName': criterion.employer.companyName
        },
        'evaluator': {
            'id': criterion.evaluator_id,
            'firstName': criterion.evaluator.firstName,
            'lastName': criterion.evaluator.lastName,
            'isFromEmployer': criterion.evaluator.employer_id == criterion.employer_id if criterion.evaluator.employer_id else False
        },
        'evaluationCriterionId': criterion.evaluationCriterion_id,
        'value': criterion.value,
        **serializeAuditFields(criterion)
    }


def getSerializedUserProject(userProject: UserProject, isEmployer=False):
    from upapp.apis.user import isUserProjectLocked, getDaysUntilProjectUnlock

    isLocked = isUserProjectLocked(userProject)
    baseData = {
        'id': userProject.id,
        'type': ContentTypes.PROJECT.value,
        'status': userProject.status,
        'statusChangeDateTime': getDateTimeFormatOrNone(userProject.statusChangeDateTime),
        'isLocked': isLocked,
        'isHidden': userProject.isHidden,
        'daysUntilUnlock': getDaysUntilProjectUnlock(userProject) if isLocked else None,
        'jobApplicationCount': userProject.jobApplication.all().count(),
        'user': {
            'id': userProject.user.id,
            'firstName': userProject.user.firstName,
            'middleName': userProject.user.middleName,
            'lastName': userProject.user.lastName,
            'email': userProject.user.email
        },
        'customProject': {
            'id': userProject.customProject.id,
            'skillLevelBit': userProject.customProject.skillLevelBit,
            'skills': [getSerializedSkill(s) for s in userProject.customProject.skills.all()],
            'projectId': userProject.customProject.project_id,
            'projectTitle': userProject.customProject.project.title,
            'projectImage': getattr(userProject.customProject.project.image, 'url', None),
            'projectDescription': userProject.customProject.project.description,
            'projectBackground': userProject.customProject.project.background,
            'role': userProject.customProject.project.role.name,
        },
        'projectNotes': userProject.projectNotes,
        'files': [getSerializedUserFile(f) for f in userProject.files.all()],
        'videos': [getSerializedUserVideo(v) for v in userProject.videos.all()],
        'images': [getSerializedUserImage(i) for i in userProject.images.all()]
    }

    if isEmployer:
        baseData['evaluationCriteria'] = [getSerializedUserProjectEvaluationCriterion(upec) for upec in userProject.userProjectEvaluationCriterion.all()]

    return baseData


def getSerializedBlog(blogPost: BlogPost):
    return {
        'id': blogPost.id,
        'author': {
            'id': blogPost.author.id,
            'firstName': blogPost.author.firstName,
            'lastName': blogPost.author.lastName,
        },
        'title': blogPost.title,
        'picture': blogPost.picture.url if blogPost.picture else None,
        'post': blogPost.post,
        'publishDate': getDateTimeFormatOrNone(blogPost.publishDate),
        'isPublished': blogPost.publishDate and blogPost.publishDate <= date.today(),
        'blogTags': [getSerializedBlogTag(bt) for bt in blogPost.blogTags.all()],
        **serializeAuditFields(blogPost)
    }


def getSerializedBlogTag(blogTag: BlogTag):
    return {
        'id': blogTag.id,
        'name': blogTag.name
    }
