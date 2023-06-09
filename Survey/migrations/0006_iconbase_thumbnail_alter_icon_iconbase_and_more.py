# Generated by Django 4.1 on 2022-10-13 18:41

import Survey.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0005_category_iconbase_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='iconbase',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=Survey.models.upload_icon_base),
        ),
        migrations.AlterField(
            model_name='icon',
            name='iconBase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='icon', to='Survey.iconbase'),
        ),
        migrations.AlterField(
            model_name='iconbase',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iconBase', to='Survey.category'),
        ),
    ]
