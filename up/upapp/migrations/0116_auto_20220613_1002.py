# Generated by Django 3.2.7 on 2022-06-13 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0115_auto_20220612_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeachableUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('teachableUserId', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='usertraining',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userTraining', to='upapp.user'),
        ),
        migrations.AddField(
            model_name='usertraining',
            name='teachableUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='upapp.teachableuser'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='usertraining',
            unique_together={('teachableUser', 'course')},
        ),
    ]
