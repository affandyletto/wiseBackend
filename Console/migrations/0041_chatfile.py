# Generated by Django 4.1 on 2023-03-13 07:41

import Console.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0040_remove_ticket_issuesfound_alter_ticket_datecreated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatID', models.CharField(default='', max_length=100)),
                ('picture', models.FileField(blank=True, null=True, upload_to=Console.models.upload_chat_file)),
            ],
        ),
    ]