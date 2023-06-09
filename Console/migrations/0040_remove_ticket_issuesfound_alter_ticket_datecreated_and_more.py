# Generated by Django 4.1 on 2023-03-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0039_remove_ticket_icons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='issuesFound',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dateCreated',
            field=models.CharField(blank=True, default='', max_length=499, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dateUpdated',
            field=models.CharField(blank=True, default='', max_length=499, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seenByAdmin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seenByClient',
            field=models.BooleanField(default=True),
        ),
    ]
