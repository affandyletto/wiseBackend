# Generated by Django 4.1 on 2023-03-04 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_profile_isprevilagechange'),
        ('Console', '0024_remove_project_proposals'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticketID', models.CharField(max_length=499, unique=True)),
                ('dateCreated', models.DateTimeField(auto_now=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('clientChat', models.TextField(blank=True, null=True)),
                ('internalChat', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=499, unique=True)),
                ('subject', models.CharField(max_length=499, unique=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('client', models.ManyToManyField(related_name='ticket', to='User.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='Console.project')),
            ],
        ),
    ]