# Generated by Django 3.2.7 on 2022-04-20 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0077_userjobapplication_hiredatetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='leverUserKey',
            field=models.CharField(max_length=75, null=True),
        ),
    ]
