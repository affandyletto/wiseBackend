# Generated by Django 4.1 on 2023-03-25 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_profile_isprevilagechange'),
        ('Survey', '0052_icon_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('mainSurveyID', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('editedProfile', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='savedSurvey', to='User.profile')),
                ('survey', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='savedSurvey', to='Survey.survey')),
            ],
        ),
    ]
