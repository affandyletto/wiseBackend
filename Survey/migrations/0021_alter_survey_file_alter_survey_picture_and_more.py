# Generated by Django 4.1 on 2022-11-02 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0020_survey_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='survey',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='survey',
            name='surveyPicture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
