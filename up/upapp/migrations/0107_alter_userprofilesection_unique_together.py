# Generated by Django 3.2.7 on 2022-06-05 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0106_remove_userprofilesectionitem_contentorder'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userprofilesection',
            unique_together={('userProfile', 'sectionOrder')},
        ),
    ]
