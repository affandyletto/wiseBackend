# Generated by Django 4.1 on 2023-03-06 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_profile_isprevilagechange'),
        ('Console', '0027_alter_ticket_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='technician',
            field=models.ManyToManyField(related_name='ticket_technician', to='User.profile'),
        ),
    ]
