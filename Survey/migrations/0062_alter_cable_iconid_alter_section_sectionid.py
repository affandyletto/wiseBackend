# Generated by Django 4.1 on 2023-04-03 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0061_alter_icon_iconid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cable',
            name='iconid',
            field=models.CharField(blank=True, default='', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='sectionid',
            field=models.CharField(blank=True, default='', max_length=80, null=True),
        ),
    ]
