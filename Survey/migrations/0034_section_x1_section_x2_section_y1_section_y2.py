# Generated by Django 4.1 on 2022-12-09 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0033_remove_cable_answer_remove_cable_audiofile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='x1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='section',
            name='x2',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='section',
            name='y1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='section',
            name='y2',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
