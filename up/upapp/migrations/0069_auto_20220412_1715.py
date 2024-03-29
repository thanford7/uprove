# Generated by Django 3.2.7 on 2022-04-12 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0068_rename_preferenceremote_user_preferenceremotebits'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='isLeverOn',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employer',
            name='leverHookArchive',
            field=models.CharField(max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='leverHookDeleted',
            field=models.CharField(max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='leverHookHired',
            field=models.CharField(max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='employer',
            name='leverHookStageChangeToken',
            field=models.CharField(max_length=75, null=True),
        ),
    ]
