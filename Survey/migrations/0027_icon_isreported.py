# Generated by Django 4.1 on 2022-11-29 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0026_alter_survey_iconsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='icon',
            name='isReported',
            field=models.BooleanField(default=False),
        ),
    ]