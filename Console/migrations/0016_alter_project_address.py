# Generated by Django 4.1 on 2022-10-24 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0015_project_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]