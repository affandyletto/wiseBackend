# Generated by Django 4.1 on 2023-01-17 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proposal', '0004_section_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='proposCode',
            field=models.CharField(blank=True, default='', max_length=199, null=True),
        ),
    ]
