# Generated by Django 4.2.7 on 2023-12-08 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0012_alter_job_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
