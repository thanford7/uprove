# Generated by Django 3.2.7 on 2022-06-12 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0113_waitlist_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingcourse',
            name='urlCoursePage',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trainingcourse',
            name='urlSalesPage',
            field=models.CharField(max_length=100),
        ),
    ]
