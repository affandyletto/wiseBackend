# Generated by Django 4.1 on 2022-09-22 21:16

import Survey.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='survey_name',
            new_name='project_nickname',
        ),
        migrations.AddField(
            model_name='cctv',
            name='audioFile',
            field=models.FileField(blank=True, null=True, upload_to=Survey.models.upload_audio),
        ),
        migrations.AddField(
            model_name='cctv',
            name='audioInfo',
            field=models.CharField(blank=True, default='', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='cctv',
            name='isLocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cctv',
            name='unit',
            field=models.CharField(blank=True, default='', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='project_name',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='cctv',
            name='survey',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cctv', to='Survey.survey'),
        ),
        migrations.AlterField(
            model_name='cctvpicture',
            name='cctv',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cctvPicture', to='Survey.cctv'),
        ),
    ]