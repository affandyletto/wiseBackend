# Generated by Django 4.1 on 2023-03-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0033_remove_ticket_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='details',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='issuesFound',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
