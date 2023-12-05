from django.db import models
from apps.accountapp.models import User
from apps.jobsapp.models import Job

# class JobSeeker(models.Model):
#     qualification = models.TextField()
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     experience = models.TextField()
#     skills = models.TextField()
    
    
    
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deleted','Deleted')
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    # foreign keys
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    
    
