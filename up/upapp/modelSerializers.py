from datetime import date
from operator import itemgetter

from upapp.models import *
from upapp.utils.dataUtil import getFileNameFromUrl
from upapp.utils.htmlTruncate import truncate


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
    profileImage = next((i.image.url for i in user.image.all() if i.isDefault), None)
    serializedUser = {
        'id': user.id,
        'firstName': user.firstName,
        'middleName': user.middleName,
        'lastName': user.lastName,
        'birthDate': getDateTimeFormatOrNone(user.birthDate),
        'email': user.email,
        'profileImage': profileImage,
        'employerId': user.employer_id,
        'inviteEmployerId': user.inviteEmployer_id,
        'userTypeBits': user.userTypeBits,
        'isStaff': user.djangoUser.is_staff,
        'isActive': user.djangoUser.is_active,
        'isSuperUser': user.djangoUser.is_superuser,
        'isDemo': user.isDemo,
        'isAuthenticated': user.djangoUser.is_authenticated,
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
        'video': userVideo.video.url,
        **serializeAuditFields(userVideo)
    }


def getSerializedUserFile(userFile: UserFile):
    return {
        'id': userFile.id,
        'title': userFile.title,
        'file': userFile.file.url,
        **serializeAuditFields(userFile)
    }


def getSerializedUserImage(userImage: UserImage):
    return {
        'id': userImage.id,
        'title': userImage.title,
        'image': userImage.image.url,
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
        'logo': organization.logo.url if organization.logo else None
    }


def getSerializedProject(project: Project, isIncludeDetails:bool=False, isAdmin=False, evaluationEmployerId=None):
    return {
        'id': project.id,
        'title': project.title,
        'image': project.image.url if project.image else None,
        'function': project.function.functionName,
        'functionId': project.function.id,
        'skills': [getSerializedProjectSkill(s) for s in project.skills.all()],
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


def getSerializedProjectFunction(projectFunction: ProjectFunction):
    return {'id': projectFunction.id, 'functionName': projectFunction.functionName}


def getSerializedProjectSkill(projectSkill: ProjectSkill):
    return {
        'id': projectSkill.id,
        'skillName': projectSkill.skillName,
        'instruction': projectSkill.instruction
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
        'skills': [getSerializedProjectSkill(s) for s in customProject.skills.all()],
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
        'userProject': getSerializedUserProject(jobApplication.userProject, isEmployer=isEmployer),
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
    baseData = {
        'id': userProject.id,
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
            'skills': [getSerializedProjectSkill(s) for s in userProject.customProject.skills.all()],
            'projectId': userProject.customProject.project_id,
            'projectTitle': userProject.customProject.project.title,
            'function': userProject.customProject.project.function.functionName,
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
