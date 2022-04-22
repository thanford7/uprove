# Generated by Django 3.2.7 on 2022-04-21 23:54

from django.db import migrations, models

from upapp.models import UserProfileSection, UserProfile, UserEducation, UserCertification, UserExperience, UserProject


def addProfileSections(apps, schema_editor):
    for profile in UserProfile.objects.prefetch_related('section').all():
        profileSections = {s.sectionType for s in profile.section.all()}
        for sectionOrder, defaultSection in enumerate(('PROJECTS', 'EXPERIENCE', 'EDUCATION')):
            if defaultSection not in profileSections:
                newSection = UserProfileSection(
                    userProfile=profile,
                    title=defaultSection,
                    sectionType=defaultSection,
                    sectionOrder=sectionOrder
                )
                newSection.save()


def moveProfileContent(apps, schema_editor):
    for profile in UserProfile.objects.prefetch_related('section', 'section__sectionItem', 'section__sectionItem__contentType').all():
        profileSections = {s.sectionType: s for s in profile.section.all()}
        for section in profileSections.values():
            for sectionItem in section.sectionItem.all():
                if (
                    (isinstance(sectionItem.contentObject, UserEducation) or isinstance(sectionItem.contentObject, UserCertification))
                    and section.sectionType != 'EDUCATION'
                ):
                    sectionItem.userProfileSection = profileSections['EDUCATION']
                    sectionItem.save()
                if (
                    isinstance(sectionItem.contentObject, UserExperience)
                    and section.sectionType != 'EXPERIENCE'
                ):
                    sectionItem.userProfileSection = profileSections['EXPERIENCE']
                    sectionItem.save()
                if (
                    isinstance(sectionItem.contentObject, UserProject)
                    and section.sectionType != 'PROJECTS'
                ):
                    sectionItem.userProfileSection = profileSections['PROJECTS']
                    sectionItem.save()


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0080_auto_20220421_1954'),
    ]

    operations = [
        migrations.RunSQL('''
                UPDATE upapp_userprofilesection
                SET "sectionType" = CASE
                    WHEN title = 'Projects' THEN 'PROJECTS'
                    WHEN title like 'Experience%' THEN 'EXPERIENCE'
                END;
            '''),
        migrations.RunSQL('''
                UPDATE upapp_userprofilesection
                SET "sectionOrder" = CASE
                    WHEN "sectionType" = 'PROJECTS' THEN 0
                    WHEN "sectionType" = 'EXPERIENCE' THEN 1
                END;
            '''),
        migrations.RunPython(addProfileSections),
        migrations.RunPython(moveProfileContent)
    ]
