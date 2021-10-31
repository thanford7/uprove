from enum import IntEnum

from django.contrib.auth.models import User as DjangoUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models

__all__ = (
    'User', 'UserProfile', 'UserProfileSection', 'UserProfileSectionItem', 'UserEducation', 'UserExperience',
    'UserContentItem', 'UserContentItemSection', 'UserVideo', 'UserFile', 'UserImage', 'UserTag', 'Organization',
    'EmployerInterest', 'ProjectFunction', 'ProjectSkill'
)


ALLOWED_UPLOADS_VIDEO = ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg']
ALLOWED_UPLOADS_IMAGE = ['png', 'jpeg', 'jpg', 'gif']
ALLOWED_UPLOADS_FILE = ['doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx', 'twb', 'twbx', 'pages', 'numbers', 'key', 'gdoc', 'gslides', 'gsheet']


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
    djangoUser = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, editable=False)
    firstName = models.CharField(max_length=20)
    middleName = models.CharField(max_length=20, null=True)
    lastName = models.CharField(max_length=30)
    birthDate = models.DateTimeField(null=True)
    email = models.EmailField(unique=True)


class UserProfile(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    profileName = models.CharField(max_length=100)
    profilePicture = models.ForeignKey('UserImage', on_delete=models.SET_NULL, null=True)
    makePublic = models.BooleanField(default=False)
    password = models.CharField(max_length=20, null=True)  # Enables users to "lock" a profile to only users with a password


class UserProfileSection(models.Model):
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False, related_name='section')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    sectionOrder = models.SmallIntegerField()

    class Meta:
        unique_together = ('userProfile', 'sectionOrder')


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

    class Meta:
        unique_together = ('userProfileSection', 'contentOrder')


class UserEducation(AuditFields):
    # Keep in sync with globalData.js
    OPTIONS_DEGREE = [
        'Associate of Arts',
        'Associate of Science',
        'Associate of Applied Science',
        'Bachelor of Arts',
        'Bachelor of Science',
        'Master of Arts',
        'Master of Science',
        'Master of Business Administration',
        'Doctoral Degree',
        'Doctor of Medicine',
        'Juris Doctor',
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='education')
    school = models.ForeignKey('Organization', on_delete=models.PROTECT)
    degree = models.CharField(max_length=50, null=True, choices=[(o, o) for o in OPTIONS_DEGREE])
    degreeSubject = models.CharField(max_length=200, null=True)
    activities = models.TextField(null=True)
    startDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)


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
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(null=True)
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
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_VIDEO)]
    )
    title = models.CharField(max_length=100)


class UserFile(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='file')
    file = models.FileField(
        upload_to='files/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_FILE)]
    )
    title = models.CharField(max_length=100)


class UserImage(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='image')
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    isDefault = models.BooleanField(default=False)


class UserTag(AuditFields):
    # Keep in sync with globalData.js
    TYPE_INTEREST = 'interest'
    TYPE_SKILL = 'skill'
    TYPES_TAG = [(t, t) for t in (TYPE_INTEREST, TYPE_SKILL)]

    class SkillLevel(IntEnum):
        NOVICE = 1
        INTERMEDIATE = 2
        ADVANCED = 3
        EXPERT = 4

    SKILL_LEVELS = [(int(i), int(i)) for i in SkillLevel]

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='tag')
    tagType = models.CharField(max_length=25, choices=TYPES_TAG)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True)
    skillLevel = models.SmallIntegerField(choices=SKILL_LEVELS, null=True)


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
    logo = models.ImageField(upload_to='logos/', null=True)
    user = models.ForeignKey('User', null=True, on_delete=models.CASCADE, related_name='organization')

    class Meta:
        unique_together = ('name', 'orgType')


class EmployerInterest(AuditFields):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    companyName = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    companyEmployeeCount = models.CharField(max_length=10, null=True)
    hiringFunctions = models.ManyToManyField('ProjectFunction')
    hiringSkills = models.ManyToManyField('ProjectSkill')
    note = models.TextField(null=True)


class CandidateInterest(AuditFields):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    linkedInProfile = models.CharField(max_length=100)
    referrer = models.CharField(max_length=50, null=True)
    interestedFunctions = models.ManyToManyField('ProjectFunction')
    currentSkills = models.ManyToManyField('ProjectSkill')
    note = models.TextField(null=True)


class ProjectFunction(models.Model):
    functionName = models.CharField(max_length=100, unique=True)


class ProjectSkill(models.Model):
    skillName = models.CharField(max_length=100, unique=True)
