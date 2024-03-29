# Generated by Django 3.2.7 on 2022-02-21 19:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0050_alter_usertag_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproject',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('hidden', 'hidden'), ('complete', 'complete')], default='draft', max_length=8),
        ),
        migrations.AddField(
            model_name='userproject',
            name='statusChangeDateTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
