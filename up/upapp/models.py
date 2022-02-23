from enum import IntEnum, Enum

from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

__all__ = (
    'User', 'UserProfile', 'UserProfileSection', 'UserProfileSectionItem', 'UserEducation', 'UserExperience',
    'UserContentItem', 'UserContentItemSection', 'UserVideo', 'UserFile', 'UserImage', 'UserTag', 'Tag', 'Organization',
    'EmployerInterest', 'Role', 'Skill', 'Project', 'ProjectInstructions', 'ProjectEvaluationCriterion',
    'ProjectFile', 'Employer', 'CustomProject', 'EmployerCustomProjectCriterion', 'EmployerJob', 'JobTemplate',
    'UserJobApplication', 'UserProjectEvaluationCriterion', 'UserProject', 'BlogPost', 'BlogTag'
)


ALLOWED_UPLOADS_VIDEO = ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg']
ALLOWED_UPLOADS_IMAGE = ['png', 'jpeg', 'jpg', 'gif']
ALLOWED_UPLOADS_FILE = ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet']


def getUploadLocation(relPath):
    return f'{relPath}{"-test/" if settings.DEBUG else "/"}'


def getUserUploadLocation(instance, filename):
    if not instance.user:
        raise PermissionError('User must be logged in to modify uploads')
    return f'uploads-candidate{"-test/" if settings.DEBUG else "/"}user_{instance.user.id}/{filename}'


def getEmployerUploadLocation(instance, filename):
    if not instance.user:
        raise PermissionError('User must be logged in to modify uploads')
    uproveUser = User.objects.get(djangoUser_id=instance.user.id)
    if not uproveUser.employer_id:
        raise PermissionError('User must be associated with an employer to modify uploads')
    return f'uploads-employer{"-test/" if settings.DEBUG else "/"}employer_{uproveUser.employer_id}/{filename}'


# Create your models here.
class AuditFields(models.Model):
    createdDateTime = models.DateTimeField()
    modifiedDateTime = models.DateTimeField()

    class Meta:
        abstract = True


"""
Users will have content which can be used across multiple profiles. 
Users can have one or more profiles.
Each profile can have one or more sections. Sections are ordered vertically within the page.
Each section can have zero or more items. Items are ordered horizontally within the section.
Each content item can have one or more content sections. Content sections are ordered vertically within the item.
"""


class User(AuditFields):
    USER_TYPE_CANDIDATE = 0x1
    USER_TYPE_EMPLOYER = 0x2
    USER_TYPE_ADMIN = 0x4

    djangoUser = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, editable=False)
    firstName = models.CharField(max_length=20)
    middleName = models.CharField(max_length=20, null=True)
    lastName = models.CharField(max_length=30)
    birthDate = models.DateField(null=True)
    email = models.EmailField(unique=True)
    userTypeBits = models.SmallIntegerField(default=USER_TYPE_CANDIDATE)
    employer = models.ForeignKey('Employer', on_delete=models.SET_NULL, null=True)
    inviteEmployer = models.ForeignKey('Employer', on_delete=models.SET_NULL, null=True, related_name='inviteEmployer')
    isDemo = models.BooleanField(default=False)

    @property
    def isEmployer(self):
        return bool(self.employer_id)

    @property
    def isCandidate(self):
        return self.userTypeBits & self.USER_TYPE_CANDIDATE

    @property
    def isAdmin(self):
        return self.userTypeBits & self.USER_TYPE_ADMIN

    @property
    def isActive(self):
        return self.djangoUser.is_active

    @property
    def isSuperUser(self):
        return self.djangoUser.is_superuser


class UserProfile(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='profile')
    profileName = models.CharField(max_length=100, default='Default')
    profilePicture = models.ForeignKey('UserImage', on_delete=models.SET_NULL, null=True)
    makePublic = models.BooleanField(default=True)
    isPrimary = models.BooleanField(default=True)
    password = models.CharField(max_length=20, null=True)  # Enables users to "lock" a profile to only users with a password


class UserProfileSection(models.Model):
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False, related_name='section')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    sectionOrder = models.SmallIntegerField()


class UserProfileSectionItem(models.Model):
    """
    This model can point to any content type (e.g. education, experience, content, etc.)
    See https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/#generic-relations
    """
    userProfileSection = models.ForeignKey(UserProfileSection, on_delete=models.CASCADE, related_name='sectionItem')
    contentOrder = models.SmallIntegerField()

    # Generic relationship fields
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    contentItemId = models.PositiveIntegerField(null=True)
    contentObject = GenericForeignKey('contentType', 'contentItemId')


class UserEducation(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='education')
    school = models.ForeignKey('Organization', on_delete=models.PROTECT)
    degree = models.CharField(max_length=50, null=True)
    degreeSubject = models.CharField(max_length=200, null=True)
    activities = models.TextField(null=True)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)


class UserExperience(AuditFields):
    # Keep in sync with globalData.js
    OPTIONS_EMPLOYMENT_TYPE = [
        'Full-time',
        'Part-time',
        'Self-employed',
        'Contracted',
        'Internship'
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='experience')
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    positionTitle = models.CharField(max_length=100)
    employmentType = models.CharField(max_length=20, choices=[(o, o) for o in OPTIONS_EMPLOYMENT_TYPE])
    startDate = models.DateField()
    endDate = models.DateField(null=True)
    description = models.TextField(null=True)


class UserContentItem(AuditFields):
    """
    A generic model allowing for flexible construction of content. For example a content item can contain
    a video, followed by a description, followed by an image, followed by a list of supporting files.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='contentItem')
    title = models.CharField(max_length=100)


class UserContentItemSection(models.Model):
    userContentItem = models.ForeignKey(UserContentItem, on_delete=models.CASCADE, related_name='section')
    contentOrder = models.SmallIntegerField()
    text = models.TextField(null=True)

    # Generic relationship fields
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    contentItemId = models.PositiveIntegerField(null=True)
    contentObject = GenericForeignKey('contentType', 'contentItemId')

    class Meta:
        unique_together = ('userContentItem', 'contentOrder')


class UserVideo(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='video')
    video = models.FileField(
        upload_to=getUserUploadLocation,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_VIDEO)]
    )
    title = models.CharField(max_length=100)


class UserFile(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='file')
    file = models.FileField(
        upload_to=getUserUploadLocation,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_FILE)]
    )
    title = models.CharField(max_length=100)


class UserImage(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='image')
    image = models.ImageField(upload_to=getUserUploadLocation)
    title = models.CharField(max_length=100)
    isDefault = models.BooleanField(default=False)


class UserTag(AuditFields):

    class SkillLevel(IntEnum):
        ENTRY = 0x1
        INTERMEDIATE = 0x2
        ADVANCED = 0x4
        EXPERT = 0x8

    SKILL_LEVELS = [(int(i), int(i)) for i in SkillLevel]
    ALL_SKILL_LEVEL_BITS = SkillLevel.ENTRY | SkillLevel.INTERMEDIATE | SkillLevel.ADVANCED | SkillLevel.EXPERT

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='userTag')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)  # Override the description provided in the Tag model
    skillLevelBit = models.SmallIntegerField(choices=SKILL_LEVELS, null=True)

    class Meta:
        unique_together = ('user', 'tag')


class Tag(models.Model):
    # Keep in sync with globalData.js
    TYPE_INTEREST = 'interest'
    TYPE_SKILL = 'skill'
    TYPES_TAG = [(t, t) for t in (TYPE_INTEREST, TYPE_SKILL)]

    title = models.CharField(max_length=30)
    type = models.CharField(max_length=25, choices=TYPES_TAG)
    description = models.CharField(max_length=200, null=True)


class Organization(models.Model):
    """
    Items will be populated in database to allow users to quick select common organizations.
    Users will also be able to create entities if they are not pre-populated
    """
    TYPE_COMPANY = 'company'
    TYPE_SCHOOL = 'school'
    TYPES_ORG = [(o, o) for o in (TYPE_COMPANY, TYPE_SCHOOL)]

    name = models.CharField(max_length=100)
    orgType = models.CharField(max_length=30, choices=TYPES_ORG)
    logo = models.ImageField(upload_to=getUploadLocation('logos'), null=True)
    user = models.ForeignKey('User', null=True, on_delete=models.CASCADE, related_name='organization')

    class Meta:
        unique_together = ('name', 'orgType')


class EmployerInterest(AuditFields):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    companyName = models.CharField(max_length=100)
    note = models.TextField(null=True)


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Skill(models.Model):
    name = models.CharField(max_length=100)
    instruction = models.TextField(null=True)
    isRequired = models.BooleanField(default=0)
    isRecommended = models.BooleanField(default=1)
    skillProject = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)  # If not populated, it's the default skill
    skillLevelBits = models.SmallIntegerField(null=True)

    def isOverlap(self, otherSkill):
        """Uniqueness can't be enforced at DB level. This method checks for overlap issues.
        """
        return all([
            self.name == otherSkill.name,
            self.skillProject_id == otherSkill.skillProject_id,
            (self.skillLevelBits or UserTag.ALL_SKILL_LEVEL_BITS) & (otherSkill.skillLevelBits or UserTag.ALL_SKILL_LEVEL_BITS)
        ])


class Project(AuditFields):
    title = models.CharField(max_length=250)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    skills = models.ManyToManyField(Skill)
    skillLevelBits = models.SmallIntegerField(default=1)  # See UserTag.SKILL_LEVELS
    employer = models.ForeignKey('Employer', null=True, on_delete=models.PROTECT)  # Add employer if project should be private to this employer only
    description = models.TextField()
    background = models.TextField(null=True)
    image = models.ImageField(upload_to=getUploadLocation('uploads-project'), null=True)


class ProjectInstructions(AuditFields):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectInstructions')
    instructions = models.TextField()
    skillLevelBit = models.SmallIntegerField(default=1)  # See UserTag.SKILL_LEVELS

    class Meta:
        unique_together = ('project', 'skillLevelBit')


class ProjectEvaluationCriterion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='evaluationCriteria')
    criterion = models.TextField()
    category = models.CharField(max_length=100, null=True)
    skillLevelBits = models.SmallIntegerField(null=True)  # Null value indicates all skill levels
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True)


class ProjectFile(AuditFields):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='projectFile')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    file = models.FileField(upload_to=getUploadLocation('uploads-project'))
    skillLevelBits = models.SmallIntegerField(default=1)  # See UserTag.SKILL_LEVELS


class Employer(AuditFields):
    companyName = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to=getUploadLocation('logos'), null=True)
    description = models.TextField(null=True)
    isDemo = models.BooleanField(default=False)


class CustomProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='customProject')
    skillLevelBit = models.SmallIntegerField()
    skills = models.ManyToManyField(Skill)

    def isSame(self, otherProject):
        return (
            {s.id for s in self.skills.all()} == {s.id for s in otherProject.skills.all()}
            and self.project == otherProject.project
            and self.skillLevelBit == otherProject.skillLevelBit
        )


class EmployerCustomProjectCriterion(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    customProject = models.ForeignKey(CustomProject, on_delete=models.CASCADE)
    evaluationCriterion = models.ForeignKey(ProjectEvaluationCriterion, on_delete=models.CASCADE)


class EmployerJob(AuditFields):
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT, related_name='employerJob')
    jobTitle = models.CharField(max_length=100)
    jobDescription = models.TextField()
    allowedProjects = models.ManyToManyField(CustomProject, related_name='employerJobProjects')
    openDate = models.DateField(null=True)
    pauseDate = models.DateField(null=True)
    closeDate = models.DateField(null=True)
    salaryFloor = models.FloatField(null=True)
    salaryCeiling = models.FloatField(null=True)
    salaryUnit = models.CharField(max_length=25, null=True)  # per hour, month, year, project


class JobTemplate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class UserJobApplication(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    userProject = models.ForeignKey('UserProject', on_delete=models.SET_NULL, null=True, related_name='jobApplication')
    employerJob = models.ForeignKey(EmployerJob, on_delete=models.PROTECT, related_name='jobApplication')
    inviteDateTime = models.DateTimeField(null=True)
    submissionDateTime = models.DateTimeField(null=True)
    approveDateTime = models.DateTimeField(null=True)
    declineDateTime = models.DateTimeField(null=True)
    withdrawDateTime = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('user', 'employerJob')


class UserProjectEvaluationCriterion(AuditFields):
    userProject = models.ForeignKey('UserProject', on_delete=models.CASCADE, related_name='userProjectEvaluationCriterion')
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    evaluator = models.ForeignKey('User', on_delete=models.CASCADE)
    evaluationCriterion = models.ForeignKey(ProjectEvaluationCriterion, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('userProject', 'evaluator', 'evaluationCriterion')


class UserProject(AuditFields):
    class Status(Enum):
        DRAFT = 'draft'
        HIDDEN = 'hidden'
        COMPLETE = 'complete'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userProject')
    customProject = models.ForeignKey(CustomProject, on_delete=models.PROTECT)
    files = models.ManyToManyField(UserFile)
    videos = models.ManyToManyField(UserVideo)
    images = models.ManyToManyField(UserImage)
    projectNotes = models.TextField(null=True)
    status = models.CharField(max_length=8, default=Status.DRAFT.value)
    statusChangeDateTime = models.DateTimeField(default=timezone.now)
    isHidden = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'customProject')


class BlogPost(AuditFields):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=250)
    picture = models.ImageField(upload_to=getUploadLocation('uploads-blog'), null=True)
    post = models.TextField()
    publishDate = models.DateField(null=True)
    blogTags = models.ManyToManyField('BlogTag')


class BlogTag(models.Model):
    name = models.CharField(max_length=75, unique=True)


class Activity(models.Model):
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    notes = models.TextField(null=True)


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
