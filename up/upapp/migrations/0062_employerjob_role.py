# Generated by Django 3.2.7 on 2022-04-01 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0061_auto_20220331_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerjob',
            name='role',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
