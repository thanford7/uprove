# Generated by Django 3.2.7 on 2022-02-19 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0049_rename_skilllevel_usertag_skilllevelbit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertag',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='userTag', to='upapp.user'),
        ),
    ]
