# Generated by Django 3.2.7 on 2022-06-06 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0107_alter_userprofilesection_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='leverCompleteStageKey',
        ),
        migrations.RemoveField(
            model_name='employer',
            name='leverTriggerStageKey',
        ),
    ]
