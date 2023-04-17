# Generated by Django 4.1 on 2022-10-29 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_profile_isfreeuser'),
        ('Console', '0021_attachment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='deliverableManager',
        ),
        migrations.RemoveField(
            model_name='project',
            name='estimator',
        ),
        migrations.RemoveField(
            model_name='project',
            name='fieldManager',
        ),
        migrations.AddField(
            model_name='project',
            name='designer',
            field=models.ManyToManyField(related_name='project_designer', to='User.profile'),
        ),
        migrations.AddField(
            model_name='project',
            name='proposal',
            field=models.ManyToManyField(related_name='project_proposal', to='User.profile'),
        ),
        migrations.AddField(
            model_name='project',
            name='technician',
            field=models.ManyToManyField(related_name='project_technician', to='User.profile'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='accountManager',
        ),
        migrations.RemoveField(
            model_name='project',
            name='surveyer',
        ),
        migrations.AddField(
            model_name='project',
            name='accountManager',
            field=models.ManyToManyField(related_name='project_account', to='User.profile'),
        ),
        migrations.AddField(
            model_name='project',
            name='surveyer',
            field=models.ManyToManyField(related_name='project_surveyer', to='User.profile'),
        ),
    ]