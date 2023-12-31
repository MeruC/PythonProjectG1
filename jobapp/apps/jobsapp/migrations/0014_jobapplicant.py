# Generated by Django 4.2.7 on 2023-12-09 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobsapp', '0013_alter_job_date_posted'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobApplicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_applied', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobsapp.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
