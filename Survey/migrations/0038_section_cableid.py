# Generated by Django 4.1 on 2022-12-11 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0037_section_comment_section_enddate_section_startdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='cableID',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
