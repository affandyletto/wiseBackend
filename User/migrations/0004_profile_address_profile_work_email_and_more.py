# Generated by Django 4.1 on 2022-09-27 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_alter_profile_company_delete_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_email',
            field=models.CharField(blank=True, max_length=199, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_phone_number',
            field=models.CharField(blank=True, max_length=199, null=True),
        ),
    ]
