# Generated by Django 3.2.7 on 2022-01-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0027_alter_projectevaluationcriterion_skilllevelbits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectevaluationcriterion',
            name='criterion',
            field=models.TextField(),
        ),
    ]
