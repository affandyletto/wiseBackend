# Generated by Django 4.1 on 2022-10-10 15:37

import Survey.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0012_rename_first_name_project_firstname_and_more'),
        ('Survey', '0002_rename_survey_name_survey_project_nickname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='project_address',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='project_nickname',
        ),
        migrations.AddField(
            model_name='cctv',
            name='dateUpdated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='dateUpdated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='name',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey', to='Console.project'),
        ),
        migrations.AddField(
            model_name='survey',
            name='surveyPicture',
            field=models.ImageField(blank=True, null=True, upload_to=Survey.models.upload_picture_location),
        ),
    ]