# Generated by Django 4.1 on 2023-01-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proposal', '0002_proposal_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
