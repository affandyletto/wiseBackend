# Generated by Django 4.1 on 2022-12-12 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0039_cable_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='label',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='pathType',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]