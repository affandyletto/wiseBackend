# Generated by Django 4.1 on 2022-10-11 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0003_remove_survey_project_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='iconSize',
            field=models.IntegerField(blank=True, default=15, null=True),
        ),
    ]