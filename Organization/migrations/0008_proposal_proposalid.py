# Generated by Django 4.1 on 2023-01-09 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0007_proposal_section_page_element'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='proposalid',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
