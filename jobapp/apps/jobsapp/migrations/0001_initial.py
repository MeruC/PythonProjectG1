# Generated by Django 4.2.7 on 2023-11-18 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accountapp', '0002_activitylog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('deleted', 'Deleted')], max_length=8)),
                ('type', models.CharField(choices=[('fulltime', 'Full-time'), ('parttime', 'Part-time')], max_length=9)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobsapp.company')),
            ],
        ),
    ]
