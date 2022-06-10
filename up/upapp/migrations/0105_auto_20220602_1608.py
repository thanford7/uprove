# Generated by Django 3.2.7 on 2022-06-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0104_remove_userjobapplication_userproject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userjobapplication',
            old_name='submissionDateTime',
            new_name='applicationDateTime',
        ),
        migrations.AddField(
            model_name='userjobapplication',
            name='interviewDateTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userjobapplication',
            name='offerDateTime',
            field=models.DateTimeField(null=True),
        ),
    ]
