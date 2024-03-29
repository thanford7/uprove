# Generated by Django 3.2.7 on 2022-05-06 18:16

from django.db import migrations, models
import django.db.models.deletion
from upapp.models import Role, RoleLevel

ROLE_MAP = {
    'Product management leader': {'level': 2, 'role': 'product management'},
    'Product manager': {'level': 1, 'role': 'product management'},
    'Product marketing management leader': {'level': 2, 'role': 'product marketing'},
    'Product marketing manager': {'level': 1, 'role': 'product marketing'},
    'Project management leader': {'level': 2, 'role': 'project management'},
    'Project manager': {'level': 1, 'role': 'project management'},
    'Account manager': {'level': 1, 'role': 'account management'},
    'Strategy and operations leader': {'level': 2, 'role': 'business analysis'},
    'Business analyst': {'level': 1, 'role': 'business analysis'},
    'Data analytics leader': {'level': 2, 'role': 'data analysis'},
    'Data analyst': {'level': 1, 'role': 'data analysis'},
    # 'Data engineering manager': {'level': 2, 'role': 'data analysis'},
    # 'Data engineer': {'level': 1, 'role': 'data analysis'},
    'Customer success leader': {'level': 2, 'role': 'customer success'},
    'Customer success manager': {'level': 1, 'role': 'customer success'},
    'Market research analyst': {'level': 1, 'role': 'market research'}
}


def updateRoleLevels(_x, _y):
    roles = {r.name.lower(): r for r in Role.objects.all()}
    for roleLevel in RoleLevel.objects.all():
        roleData = ROLE_MAP.get(roleLevel.roleTitle)
        if not roleData:
            continue
        if not (role := roles.get(roleData['role'])):
            roleName = ' '.join(word.capitalize() for word in roleData['role'].split(' '))
            role = Role(name=roleName)
            role.save()
            roles[role.name.lower()] = role
        roleLevel.role = role
        roleLevel.roleLevelBit = roleData['level']
        roleLevel.save()


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0084_auto_20220504_1605'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ('name',)},
        ),
        migrations.RenameModel('RoleTitle', 'RoleLevel'),
        migrations.AddField(
            model_name='rolelevel',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='upapp.role'),
        ),
        migrations.AddField(
            model_name='rolelevel',
            name='roleLevelBit',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterModelOptions(
            name='rolelevel',
            options={'ordering': ('roleTitle',)},
        ),
        migrations.AlterField(
            model_name='employerjob',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='upapp.rolelevel'),
        ),
        migrations.AlterField(
            model_name='user',
            name='preferenceRoles',
            field=models.ManyToManyField(to='upapp.RoleLevel'),
        ),
        migrations.RunPython(updateRoleLevels),
    ]
