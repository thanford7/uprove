from datetime import date
from enum import Enum
from operator import itemgetter

from django.db.models import Q

from upapp.models import *
from upapp.utils.dataUtil import getFileNameFromUrl, groupBy, capitalizeAllWords
from upapp.utils.htmlTruncate import truncate


# Keep in sync with CONTENT_TYPES in globalData.js
class ContentTypes(Enum):
    EXISTING = 'existing'
    EDUCATION = 'education'
    CERTIFICATION = 'certification'
    EXPERIENCE = 'experience'
    PROJECT = 'project'
    CUSTOM = 'custom'
    VIDEO = 'video'
    FILE = 'file'
    IMAGE = 'image'

csRoleFilter = Q()
for csRole in ('customer success', 'customer experience', 'account management'):
    csRoleFilter |= Q(name__icontains=csRole)
CUSTOMER_SUCCESS_ROLE_IDS = [r.id for r in Role.objects.filter(csRoleFilter)]


def getDateTimeFormatOrNone(val):
    """Serialize a date or datetime value if it exists, otherwise return None"""
    if val:
        return val.isoformat()
    return None


def getAnonymizedEmployerData(text, employerName):
    text = text.replace(capitalizeAllWords(employerName), '<code>Employer</code>')
    text = text.replace(employerName.lower(), '<code>employer</code>')
    return text.replace(employerName, '<code>employer</code>')


def serializeAuditFields(obj):
    return {
        'createdDateTime': obj.createdDateTime.isoformat(),
        'modifiedDateTime': obj.modifiedDateTime.isoformat()
    }


def _addSerializedUserAssets(dataDict, user):
    dataDict[ContentTypes.EDUCATION.value] = [getSerializedUserEducation(e) for e in user.education.all()]
    dataDict[ContentTypes.CERTIFICATION.value] = [getSerializedUserCertification(e) for e in user.certification.all()]
    dataDict[ContentTypes.EXPERIENCE.value] = [getSerializedUserExperience(e) for e in user.experience.all()]
    dataDict[ContentTypes.CUSTOM.value] = [getSerializedUserContentItem(ci) for ci in user.contentItem.all()]
    dataDict[ContentTypes.PROJECT.value] = [getSerializedUserProject(up) for up in user.userProject.all()]
    dataDict['videos'] = [getSerializedUserVideo(v) for v in user.video.all()]
    dataDict['files'] = [getSerializedUserFile(f) for f in user.file.all()]
    dataDict['images'] = [getSerializedUserImage(i) for i in user.image.all()]


def getAllowedProjects(customProjects, job):
    return [
        cp for cp
        in customProjects
        if cp.project.role_id == job.roleLevel.role_id or (cp.project.role_id in CUSTOMER_SUCCESS_ROLE_IDS and job.roleLevel.role_id in CUSTOMER_SUCCESS_ROLE_IDS)
    ] if job.roleLevel else []


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
    if isinstance(item.contentObject, UserCertification):
        return getSerializedUserCertification(item.contentObject)
    if isinstance(item.contentObject, UserExperience):
        return getSerializedUserExperience(item.contentObject)
    if isinstance(item.contentObject, UserContentItem):
        return getSerializedUserContentItem(item.contentObject)
    if isinstance(item.contentObject, UserProject):
        return getSerializedUserProject(item.contentObject)
    raise ValueError(f'Unknown content type: {item.contentType}')


def getItemPrimarySort(item):
    if not item.contentObject:
        return None
    if (
        isinstance(item.contentObject, UserVideo)
        or isinstance(item.contentObject, UserFile)
        or isinstance(item.contentObject, UserImage)
        or isinstance(item.contentObject, UserContentItem)
        or isinstance(item.contentObject, UserProject)
    ):
        return item.contentObject.modifiedDateTime
    if isinstance(item.contentObject, UserEducation) or isinstance(item.contentObject, UserExperience):
        return item.contentObject.endDate or date.today()
    if isinstance(item.contentObject, UserCertification):
        return item.contentObject.expirationDate or date.today()
    raise ValueError(f'Unknown content type: {item.contentType}')


def getItemSecondarySort(item):
    if isinstance(item.contentObject, UserEducation) or isinstance(item.contentObject, UserExperience):
        return item.contentObject.startDate or date.today()
    if isinstance(item.contentObject, UserCertification):
        return item.contentObject.issueDate
    return None


def getGenericItemSort(item):
    return (getItemPrimarySort(item), getItemSecondarySort(item))


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
        'city': user.city,
        'state': user.state.stateName if user.state else None,
        'stateId': user.state.id if user.state else None,
        'country': user.country.countryName if user.country else None,
        'countryId': user.country.id if user.country else None,
        'userTypeBits': user.userTypeBits,
        'resume': user.resume.url if user.resume else None,
        'isStaff': user.djangoUser.is_staff,
        'isActive': user.djangoUser.is_active,
        'isSuperUser': user.djangoUser.is_superuser,
        'isDemo': user.isDemo,
        'isAuthenticated': user.djangoUser.is_authenticated,
        'leverUserKey': user.leverUserKey,
        'skills': [getSerializedUserTag(t) for t in user.userTag.filter(tag__type=Tag.TYPE_SKILL)],
        'interests': [getSerializedUserTag(t) for t in user.userTag.filter(tag__type=Tag.TYPE_INTEREST)],
        'preferences': {
            'companySizes': [{'id': p.id, 'companySize': p.companySize} for p in user.preferenceCompanySizes.all()],
            'roles': [{
                    'id': p.id,
                    'roleTitle': p.roleTitle,
                    'roleId': p.role_id,
                    'roleLevelBit': p.roleLevelBit
                } for p in user.preferenceRoles.all()
            ],
            'countries': [{'id': p.id, 'countryName': p.countryName} for p in user.preferenceCountry.all()],
            'remoteBits': user.preferenceRemoteBits,
            'salary': user.preferenceSalary
        },
        **serializeAuditFields(user)
    }

    if isIncludeAssets:
        serializedUser['profiles'] = [getSerializedUserProfile(p) for p in user.profile.all()]
        _addSerializedUserAssets(serializedUser, user)

    return serializedUser


def getSerializedUserProfile(userProfile: UserProfile, isOwner=None):
    serializedProfile = {
        'id': userProfile.id,
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
        'sectionType': userProfileSection.sectionType,
        'sectionOrder': userProfileSection.sectionOrder,
        'sectionItems': [
            getSerializedUserProfileSectionItem(psi)
            for psi in sorted(userProfileSection.sectionItem.all(), key=getGenericItemSort, reverse=True)
        ],
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


def getSerializedUserCertification(userCertification: UserCertification):
    return {
        'id': userCertification.id,
        'type': ContentTypes.CERTIFICATION.value,
        'organization': getSerializedOrganization(userCertification.organization),
        'hasExpiration': userCertification.hasExpiration,
        'title': userCertification.title,
        'issueDate': getDateTimeFormatOrNone(userCertification.issueDate),
        'expirationDate': getDateTimeFormatOrNone(userCertification.expirationDate),
        **serializeAuditFields(userCertification)
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
        'thumbnail': userFile.thumbnail.url if userFile.thumbnail else None,
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
        'description': project.description,
        'background': project.background if isIncludeDetails else truncate(project.background, 250, ellipsis='...'),
        'instructions': project.instructions,
        'evaluationCriteria': [
            getSerializedProjectEvaluationCriterion(ec)
            for ec in project.evaluationCriteria.all()
        ] if (evaluationEmployerId or isAdmin) else None,
        'files': [getSerializedProjectFile(pf, isIncludeDetails) for pf in project.projectFile.all()],
        'isLimited': not isIncludeDetails
    }


def getSerializedProjectEvaluationCriterion(evaluationCriterion: ProjectEvaluationCriterion):
    return {
        'id': evaluationCriterion.id,
        'criterion': evaluationCriterion.criterion,
        'category': evaluationCriterion.category
    }


def getSerializedProjectFile(projectFile: ProjectFile, isIncludeDetails:bool=False):
    return {
        'id': projectFile.id,
        'title': projectFile.title,
        'description': projectFile.description,
        'file': projectFile.file.url if isIncludeDetails else None,
        'fileName': getFileNameFromUrl(projectFile.file.url),
        **serializeAuditFields(projectFile)
    }


def getSerializedRole(role: Role):
    return {
        'id': role.id,
        'name': role.name,
    }


def getSerializedRoleLevel(roleLevel: RoleLevel):
    return {
        'id': roleLevel.id,
        'roleLevelBit': roleLevel.roleLevelBit,
        'roleId': roleLevel.role.id,
        'roleName': roleLevel.role.name,
        'roleTitle': f'{roleLevel.role.name} ({RoleLevel.LABELS[roleLevel.roleLevelBit]})'
    }


def getSerializedSkill(skill: Skill):
    return {
        'id': skill.id,
        'name': skill.name,
        'instruction': skill.instruction,
        'projectId': skill.skillProject_id,
    }


def getSerializedEmployer(employer: Employer, employerId=None):
    from upapp.apis.employer import JobPostingView  # Avoid circular import
    customProjects = CustomProject.objects.select_related('project').all()
    baseFields = {
        'id': employer.id,
        'companyName': employer.companyName,
        'logo': employer.logo.url if employer.logo else None,
        'description': employer.description,
        'companySize': employer.companySize.companySize if employer.companySize else None,
        'companySizeId': employer.companySize.id if employer.companySize else None,
        'glassDoorUrl': employer.glassDoorUrl,
        'isDemo': employer.isDemo,
        'isClient': employer.isClient,
        'jobs': [
            getSerializedEmployerJob(ej, employerId=employerId, customProjects=customProjects)
            for ej in employer.employerJob.filter(JobPostingView.getEmployerJobFilter(isIncludeClosed=True, isEmployer=bool(employerId)))
        ],
    }
    employerFields = {
        **serializeAuditFields(employer),
        'isLeverOn': employer.isLeverOn,
        'leverTriggerStageKey': employer.leverTriggerStageKey,
        'leverCompleteStageKey': employer.leverCompleteStageKey,
        'leverHookStageChangeToken': employer.leverHookStageChangeToken,
        'leverHookArchive': employer.leverHookArchive,
        'leverHookHired': employer.leverHookHired,
        'leverHookDeleted': employer.leverHookDeleted
    }
    return baseFields if not employerId else {**baseFields, **employerFields}


def getSerializedCustomProject(customProject: CustomProject):
    return {
        'id': customProject.id,
        'skillLevelBit': customProject.skillLevelBit,
        'skills': [getSerializedSkill(s) for s in customProject.skills.all()],
        'projectId': customProject.project_id,
        'projectTitle': customProject.project.title
    }


def getSerializedEmployerJob(employerJob: EmployerJob, employerId=None, customProjects=None, isAnonymous=False):
    customProjects = customProjects or CustomProject.objects.select_related('project').all()
    allowedProjects = getAllowedProjects(customProjects, employerJob)
    companyName = employerJob.employer.companyName

    baseFields = {
        'id': employerJob.id,
        'employerId': employerJob.employer_id,
        'isClient': employerJob.employer.isClient,
        'jobTitle': employerJob.jobTitle,
        'roleLevelId': employerJob.roleLevel_id,
        'roleName': employerJob.roleLevel.role.name if employerJob.roleLevel else None,
        'roleId': employerJob.roleLevel.role.id if employerJob.roleLevel else None,
        'roleLevelBit': employerJob.roleLevel.roleLevelBit if employerJob.roleLevel else None,
        'allowedProjects': [getSerializedCustomProject(ap) for ap in allowedProjects],
        'salaryFloor': employerJob.salaryFloor,
        'salaryCeiling': employerJob.salaryCeiling,
        'salaryUnit': employerJob.salaryUnit,
        'openDate': getDateTimeFormatOrNone(employerJob.openDate),
        'pauseDate': getDateTimeFormatOrNone(employerJob.pauseDate),
        'closeDate': getDateTimeFormatOrNone(employerJob.closeDate),
        'isRemote': employerJob.isRemote,
        'state': employerJob.state.stateName if employerJob.state else None,
        'stateId': employerJob.state.id if employerJob.state else None,
        'country': employerJob.country.countryName if employerJob.country else None,
        'countryId': employerJob.country.id if employerJob.country else None,
        'region': employerJob.region,
    }

    anonymousFields = {
        'jobDescription': getAnonymizedEmployerData(employerJob.jobDescription, companyName),
    }

    nonAnonymousFields = {
        'companyName': companyName,
        'employerLogo': employerJob.employer.logo.url if employerJob.employer.logo else None,
        'companySize': employerJob.employer.companySize.companySize if employerJob.employer.companySize else None,
        'companySizeId': employerJob.employer.companySize.id if employerJob.employer.companySize else None,
        'jobDescription': employerJob.jobDescription,
        'location': employerJob.location,
        'city': employerJob.city,
        'applicationUrl': employerJob.applicationUrl,
        'isInternal': employerJob.isInternal,
        'leverPostingKey': employerJob.leverPostingKey,
    }

    if not isAnonymous:
        baseFields = {**baseFields, **nonAnonymousFields}
        if employerId:
            baseFields['applications'] = [getSerializedJobApplication(app) for app in employerJob.jobApplication.all()]
            baseFields = {**baseFields, **serializeAuditFields(employerJob)}
    else:
        baseFields = {**baseFields, **anonymousFields}

    return baseFields


def getSerializedJobApplication(jobApplication: UserJobApplication, includeJob=False):

    val = {
        'id': jobApplication.id,
        'user': {
            'id': jobApplication.user.id,
            'firstName': jobApplication.user.firstName,
            'middleName': jobApplication.user.middleName,
            'lastName': jobApplication.user.lastName,
            'email': jobApplication.user.email,
            'profileId': jobApplication.user.primaryProfile.id if jobApplication.user.primaryProfile else None
        },
        'jobId': jobApplication.employerJob_id,
        'jobTitle': jobApplication.employerJob.jobTitle,
        'employer': jobApplication.employerJob.employer.companyName,
        'employerLogo': jobApplication.employerJob.employer.logo.url if jobApplication.employerJob.employer.logo else None,
        'status': jobApplication.status,
        'statusUpdateDateTime': getDateTimeFormatOrNone(jobApplication.statusUpdateDateTime),
    }

    if includeJob:
        customProjects = CustomProject.objects.select_related('project').all()
        allowedProjects = getAllowedProjects(customProjects, jobApplication.employerJob)
        val['job'] = {
            'id': jobApplication.employerJob.id,
            'jobTitle': jobApplication.employerJob.jobTitle,
            'allowedProjects': [getSerializedCustomProject(ep) for ep in allowedProjects]
        }

    return val


def getSerializedUserProjectEvaluationCriterion(criterion: UserProjectEvaluationCriterion):
    return {
        'id': criterion.id,
        'userProjectId': criterion.userProject_id,
        'employer': {
            'id': criterion.employer_id,
            'companyName': criterion.employer.companyName
        } if criterion.employer_id else None,
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


def getSerializedUserProject(userProject: UserProject, isIncludeEvaluation=False, employerId=None):
    from upapp.apis.user import UserProjectView

    baseData = {
        'id': userProject.id,
        'type': ContentTypes.PROJECT.value,
        'status': userProject.status,
        'statusChangeDateTime': getDateTimeFormatOrNone(userProject.statusChangeDateTime),
        'isHidden': userProject.isHidden,
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
            'projectInstructions': userProject.customProject.project.instructions,
            'role': userProject.customProject.project.role.name,
        },
        'projectNotes': userProject.projectNotes,
        'projectEvalScorePct': UserProjectView.getUserProjectScorePct(userProject, employerId=employerId),
        'files': [getSerializedUserFile(f) for f in userProject.files.all()],
        'videos': [getSerializedUserVideo(v) for v in userProject.videos.all()],
        'images': [getSerializedUserImage(i) for i in userProject.images.all()]
    }

    if isIncludeEvaluation:
        evaluationCriteria = [
            getSerializedProjectEvaluationCriterion(ec)
            for ec in userProject.customProject.project.evaluationCriteria.all()
        ]

        baseData['evaluationCriteria'] = evaluationCriteria

        evaluationFilter = Q()
        if employerId:
            evaluationFilter = Q(employer_id__isnull=True) | Q(employer_id=employerId)
        baseData['evaluations'] = groupBy(
            userProject.userProjectEvaluationCriterion.filter(evaluationFilter),
            lambda x: x.evaluator_id,
            valTransformFn=getSerializedUserProjectEvaluationCriterion
        )

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
