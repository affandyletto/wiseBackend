# Generated by Django 4.1 on 2023-03-26 15:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0053_savedsurvey'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]