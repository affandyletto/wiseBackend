# Generated by Django 4.1 on 2022-12-12 16:53

import Survey.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0038_section_cableid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cable',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=Survey.models.upload_icon),
        ),
    ]
