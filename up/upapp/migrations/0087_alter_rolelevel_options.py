# Generated by Django 3.2.7 on 2022-05-06 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0086_rename_role_employerjob_rolelevel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rolelevel',
            options={'ordering': ('role__name', 'roleLevelBit')},
        ),
    ]
