# Generated by Django 4.1 on 2022-10-04 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0002_project_stage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='client_org',
            new_name='clientOrg',
        ),
    ]
