# Generated by Django 3.2.7 on 2022-01-03 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0024_auto_20220103_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectskill',
            name='instruction',
            field=models.TextField(null=True),
        ),
    ]
