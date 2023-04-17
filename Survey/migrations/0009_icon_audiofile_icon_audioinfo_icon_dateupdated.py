# Generated by Django 4.1 on 2022-10-16 08:29

import Survey.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0008_icon_angle_icon_color_icon_depth_icon_iconid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='icon',
            name='audioFile',
            field=models.FileField(blank=True, null=True, upload_to=Survey.models.upload_audio),
        ),
        migrations.AddField(
            model_name='icon',
            name='audioInfo',
            field=models.CharField(blank=True, default='', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='icon',
            name='dateUpdated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
