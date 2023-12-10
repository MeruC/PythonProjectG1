from django.db import models
from apps.accountapp.models import User
import datetime as date


# company
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user id in account model
    company_name = models.CharField(max_length=80)
    description = models.TextField()
    city = models.CharField(max_length=95,default='')
    country = models.CharField(max_length=95,default='')
    logo = models.ImageField(null=True, blank=True,upload_to="images/company/")
    cover_photo= models.ImageField(null=True, blank=True,upload_to="images/company/")


# job
class Job(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("deleted", "Deleted")]
    TYPE_CHOICES = [("fulltime", "Full-time"), ("parttime", "Part-time")]
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    # details = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    type = models.CharField(max_length=9, choices=TYPE_CHOICES)

    # temporarily set fields to null=True
    skills = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)

    max_salary = models.IntegerField(null=True)
    min_salary = models.IntegerField(null=True)
    date_posted = models.DateTimeField(default=date.datetime.today)


# work experience
class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, default="")
    position = models.CharField(max_length=150)
    start_date = models.CharField(max_length=70)
    end_date = models.CharField(max_length=70)
