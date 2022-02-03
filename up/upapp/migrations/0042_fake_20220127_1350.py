# Generated by Django 3.2.7 on 2022-01-27 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0041_auto_20220127_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('instruction', models.TextField(null=True)),
                ('isRequired', models.BooleanField(default=0)),
                ('isRecommended', models.BooleanField(default=1)),
                ('skillLevelBits', models.SmallIntegerField(null=True)),
                ('skillProject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='upapp.project')),
            ],
        ),
        # migrations.DeleteModel(
        #     name='ProjectSkill',
        # ),
        migrations.AlterField(
            model_name='customproject',
            name='skills',
            field=models.ManyToManyField(to='upapp.Skill'),
        ),
        migrations.AlterField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(to='upapp.Skill'),
        ),
    ]
