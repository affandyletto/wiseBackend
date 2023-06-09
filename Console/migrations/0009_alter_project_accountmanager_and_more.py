# Generated by Django 4.1 on 2022-10-07 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_alter_profile_clientorg'),
        ('Console', '0008_remove_project_enddate_remove_project_hibernate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='accountManager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_account', to='User.profile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='deliverableManager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_deliverable', to='User.profile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='estimator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_estimator', to='User.profile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='fieldManager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_field', to='User.profile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='surveyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_surveyer', to='User.profile'),
        ),
    ]
