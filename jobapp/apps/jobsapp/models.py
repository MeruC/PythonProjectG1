from django.db import models
from apps.accountapp.models import User
import datetime as date
from django.utils import timezone


# company
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user id in account model
    company_name = models.CharField(max_length=80)
    description = models.TextField()
    city = models.CharField(max_length=95,default='')
    country = models.CharField(max_length=95,default='')
    logo = models.ImageField(null=True, blank=True,upload_to="images/company/")
    cover_photo= models.ImageField(null=True, blank=True,upload_to="images/company/")
    is_active = models.BooleanField(default=True)
    email_address = models.EmailField(default='')



# job
class Job(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    TYPE_CHOICES = [("fulltime", "Full-time"), ("parttime", "Part-time")]
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) # attributes null=True and blank=True are temporary
    description = models.TextField()
    # details = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    type = models.CharField(max_length=9, choices=TYPE_CHOICES)

    # temporarily set fields to null=True
    skills = models.TextField(null=True)
    max_salary = models.IntegerField(null=True)
    min_salary = models.IntegerField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)


# work experience
class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, default="")
    job_summary = models.TextField(default='')
    start_date = models.CharField(max_length=70)
    end_date = models.CharField(max_length=70)

#
class jobApplicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default="pending")