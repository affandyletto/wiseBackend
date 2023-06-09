# Generated by Django 4.1 on 2022-11-10 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0024_temp_remove_survey_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='icon',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='icon',
            name='endDate',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='icon',
            name='startDate',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='icon',
            name='techName',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='icon',
            name='test',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
