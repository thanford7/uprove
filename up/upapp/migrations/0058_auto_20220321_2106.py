# Generated by Django 3.2.7 on 2022-03-22 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0057_auto_20220310_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='file', to='upapp.user'),
        ),
        migrations.AlterField(
            model_name='userimage',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='upapp.user'),
        ),
        migrations.AlterField(
            model_name='uservideo',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='upapp.user'),
        ),
    ]
