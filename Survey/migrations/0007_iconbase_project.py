# Generated by Django 4.1 on 2022-10-14 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Console', '0012_rename_first_name_project_firstname_and_more'),
        ('Survey', '0006_iconbase_thumbnail_alter_icon_iconbase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='iconbase',
            name='project',
            field=models.ManyToManyField(to='Console.project'),
        ),
    ]