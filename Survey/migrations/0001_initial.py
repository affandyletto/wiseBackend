# Generated by Django 4.1 on 2022-09-14 19:40

import Survey.models
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CCTV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cctvid', models.IntegerField(blank=True, default=1, null=True)),
                ('angle', models.IntegerField(blank=True, default=1, null=True)),
                ('depth', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('opacity', models.IntegerField(blank=True, default=1, null=True)),
                ('color', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('rotate', models.IntegerField(blank=True, default=45, null=True)),
                ('xposition', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('yposition', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cameraName', models.CharField(blank=True, default='', max_length=800, null=True)),
                ('cableName', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('location', models.TextField(blank=True, default='', null=True)),
                ('ceilingType', models.CharField(blank=True, default='', max_length=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('distance', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('pixelDistance', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('unit', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('project_id', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('project_address', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('survey_name', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=Survey.models.upload_picture_location)),
                ('degree', models.IntegerField(blank=True, default=0, null=True)),
                ('flip', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CCTVPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=Survey.models.upload_camera_pictures)),
                ('cctv', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cctvPicture', to='Survey.cctv')),
            ],
        ),
        migrations.AddField(
            model_name='cctv',
            name='survey',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cctv', to='Survey.survey'),
        ),
    ]
