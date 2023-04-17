# Generated by Django 4.1 on 2022-10-19 19:24

import User.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_alter_profile_clientorg'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('username', models.CharField(blank=True, max_length=199, null=True)),
                ('first_name', models.CharField(blank=True, max_length=199, null=True)),
                ('last_name', models.CharField(blank=True, max_length=199, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('company_name', models.CharField(blank=True, max_length=399, null=True)),
                ('work_number', models.CharField(blank=True, max_length=199, null=True)),
                ('work_email', models.CharField(blank=True, max_length=199, null=True)),
                ('work_address', models.CharField(blank=True, max_length=1999, null=True)),
                ('file', models.ImageField(blank=True, null=True, upload_to=User.models.upload_free_company)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=1999, null=True),
        ),
    ]