# Generated by Django 3.2.7 on 2022-02-23 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0053_auto_20220223_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userjobapplication',
            name='userProject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobApplication', to='upapp.userproject'),
        ),
    ]
