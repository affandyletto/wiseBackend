# Generated by Django 4.1 on 2022-10-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0017_project_stagehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='stageHistory',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
