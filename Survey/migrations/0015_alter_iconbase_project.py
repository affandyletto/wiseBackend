# Generated by Django 4.1 on 2022-10-24 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0015_project_address'),
        ('Survey', '0014_icon_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iconbase',
            name='project',
            field=models.ManyToManyField(to='Console.project'),
        ),
    ]
