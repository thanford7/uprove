# Generated by Django 3.2.7 on 2022-03-01 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0055_usercertification'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('title', 'type')},
        ),
    ]
