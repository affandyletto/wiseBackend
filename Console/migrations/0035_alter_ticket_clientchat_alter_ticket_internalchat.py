# Generated by Django 4.1 on 2023-03-06 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0034_ticket_details_ticket_issuesfound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='clientChat',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='internalChat',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
    ]