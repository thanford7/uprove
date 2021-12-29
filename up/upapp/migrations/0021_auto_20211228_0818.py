# Generated by Django 3.2.7 on 2021-12-28 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upapp', '0020_auto_20211219_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
            ],
        ),
        migrations.AlterField(
            model_name='projectinstructions',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectInstructions', to='upapp.project'),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDateTime', models.DateTimeField()),
                ('modifiedDateTime', models.DateTimeField()),
                ('title', models.CharField(max_length=250)),
                ('picture', models.ImageField(null=True, upload_to='uploads-blog-test/')),
                ('post', models.TextField()),
                ('publishDate', models.DateField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='upapp.user')),
                ('blogTags', models.ManyToManyField(to='upapp.BlogTag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
