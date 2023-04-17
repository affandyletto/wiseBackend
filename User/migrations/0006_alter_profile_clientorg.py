# Generated by Django 4.1 on 2022-10-03 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Organization', '0003_clientorganization_organization'),
        ('User', '0005_profile_clientorg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='clientOrg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='Organization.clientorganization'),
        ),
    ]
