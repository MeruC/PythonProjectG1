# Generated by Django 4.2.7 on 2023-12-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0007_alter_job_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.CharField(default='', max_length=100),
        ),
    ]