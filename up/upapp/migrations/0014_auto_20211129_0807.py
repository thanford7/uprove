# Generated by Django 3.2.7 on 2021-11-29 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0013_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='instructions',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='projectfile',
            name='skillLevelBits',
            field=models.SmallIntegerField(default=1),
        ),
    ]
