# Generated by Django 4.1 on 2022-12-06 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0029_cable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cable',
            name='xposition',
        ),
        migrations.RemoveField(
            model_name='cable',
            name='yposition',
        ),
        migrations.AddField(
            model_name='iconpicture',
            name='cable',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cablePicture', to='Survey.cable'),
        ),
    ]
