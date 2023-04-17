# Generated by Django 4.1 on 2022-10-09 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0011_alter_project_nickname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.AddField(
            model_name='project',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='hibernate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='startDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
