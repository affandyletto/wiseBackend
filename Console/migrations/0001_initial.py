# Generated by Django 4.1 on 2022-10-03 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Organization', '0004_rename_organization_clientorganization_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=199, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('client_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='Organization.clientorganization')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='Organization.organization')),
            ],
        ),
    ]