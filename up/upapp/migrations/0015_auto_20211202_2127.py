# Generated by Django 3.2.7 on 2021-12-03 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0014_auto_20211129_0807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='instructions',
            new_name='background',
        ),
        migrations.CreateModel(
            name='ProjectInstructions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDateTime', models.DateTimeField()),
                ('modifiedDateTime', models.DateTimeField()),
                ('instructions', models.TextField()),
                ('skillLevelBit', models.SmallIntegerField(default=1)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projectInstructions', to='upapp.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
