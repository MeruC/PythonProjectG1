from django.db import models
from apps.accountapp.models import User


# company
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user id in account model
    company_name = models.CharField(max_length=80)
    description = models.TextField()


# job
class Job(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("deleted", "Deleted")]
    TYPE_CHOICES = [("fulltime", "Full-time"), ("parttime", "Part-time")]
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    type = models.CharField(max_length=9, choices=TYPE_CHOICES)
    type = models.CharField(max_length=9, choices=TYPE_CHOICES)

    skills = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)

    max_salary = models.IntegerField(null=True)
    min_salary = models.IntegerField(null=True)


# work experience
class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, default="")
    position = models.CharField(max_length=150)
    start_date = models.CharField(max_length=70)
    end_date = models.CharField(max_length=70)
