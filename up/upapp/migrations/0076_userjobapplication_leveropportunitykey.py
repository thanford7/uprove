# Generated by Django 3.2.7 on 2022-04-19 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0075_employerjob_isinternal'),
    ]

    operations = [
        migrations.AddField(
            model_name='userjobapplication',
            name='leverOpportunityKey',
            field=models.CharField(max_length=75, null=True),
        ),
    ]
