# Generated by Django 4.1 on 2023-01-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proposal', '0005_proposal_proposcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='sender',
            field=models.CharField(blank=True, default='', max_length=199, null=True),
        ),
    ]
