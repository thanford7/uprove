# Generated by Django 3.2.7 on 2022-06-10 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0109_remove_employerjob_salaryunit'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('shortDescription', models.TextField()),
                ('urlSalesPage', models.CharField(max_length=50)),
                ('urlCoursePage', models.CharField(max_length=50)),
                ('priceBasic', models.FloatField()),
                ('pricePremium', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completionPct', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upapp.trainingcourse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTraining', to='upapp.user')),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]
