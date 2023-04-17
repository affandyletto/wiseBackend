# Generated by Django 4.1 on 2022-09-24 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=199, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=799, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=199, null=True)),
                ('last_name', models.CharField(blank=True, max_length=199, null=True)),
                ('username', models.CharField(blank=True, max_length=99, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('isSuperAdmin', models.BooleanField(blank=True, default=False, null=True)),
                ('isCompanyAdmin', models.BooleanField(blank=True, default=False, null=True)),
                ('isAccountManager', models.BooleanField(blank=True, default=False, null=True)),
                ('isSurveyor', models.BooleanField(blank=True, default=False, null=True)),
                ('isDesigner', models.BooleanField(blank=True, default=False, null=True)),
                ('isProposal', models.BooleanField(blank=True, default=False, null=True)),
                ('isTechnician', models.BooleanField(blank=True, default=False, null=True)),
                ('isClient', models.BooleanField(blank=True, default=False, null=True)),
                ('User', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='User.organization')),
            ],
        ),
    ]
