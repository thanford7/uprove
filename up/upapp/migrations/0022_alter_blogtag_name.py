# Generated by Django 3.2.7 on 2021-12-29 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0021_auto_20211228_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogtag',
            name='name',
            field=models.CharField(max_length=75, unique=True),
        ),
    ]
