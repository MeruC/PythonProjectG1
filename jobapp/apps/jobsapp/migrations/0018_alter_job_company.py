# Generated by Django 4.2.7 on 2023-12-09 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0017_remove_job_city_remove_job_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobsapp.company'),
        ),
    ]
