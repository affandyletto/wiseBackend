# Generated by Django 4.1 on 2023-01-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proposal', '0003_proposal_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='no',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
