# Generated by Django 4.2.7 on 2023-11-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0002_workexperience'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='company_name',
            field=models.CharField(default='', max_length=150),
        ),
    ]