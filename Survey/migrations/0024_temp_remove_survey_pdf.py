# Generated by Django 4.1 on 2022-11-09 21:26

import Survey.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0023_survey_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(blank=True, null=True, upload_to=Survey.models.upload_file_pdf)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=Survey.models.upload_temp_location)),
            ],
        ),
        migrations.RemoveField(
            model_name='survey',
            name='pdf',
        ),
    ]
