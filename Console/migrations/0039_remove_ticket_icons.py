# Generated by Django 4.1 on 2023-03-09 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0038_ticket_seenbyadmin_ticket_seenbyclient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='icons',
        ),
    ]
