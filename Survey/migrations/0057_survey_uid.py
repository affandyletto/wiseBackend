# Generated by Django 4.1 on 2023-03-26 15:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0056_remove_survey_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]
