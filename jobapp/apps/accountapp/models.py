from django.db import models
import datetime as date
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# user table
class User(AbstractUser):
    # add additional fields here
    profile_summary = models.TextField(default="")
    profile_img = models.ImageField(null=True, blank=True,upload_to="images/")
    contact_number = models.CharField(max_length=12, default='')
    skills = models.TextField(null=True,blank=True,default='')
    is_deactivated = models.BooleanField(default=False)
    
# class User(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(max_length=255)
#     password = models.TextField()
#     isActivated = models.BooleanField(default=True)

#     last_login = models.DateTimeField(auto_now_add=True)


# class Person(models.Model):
#     # SEX_CHOICE = [('M','Male'),('F','Female')]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=70)
#     last_name = models.CharField(max_length=70)
#     # birthdate = models.DateField()
#     # sex = models.CharField(max_length=1, choices=SEX_CHOICE,blank=True)
#     # street_address = models.CharField(max_length=100)
#     # apartment_no = models.IntegerField(null=True)
#     # city = models.CharField(max_length=70)
#     # postal_code = models.IntegerField()


class Alerts(models.Model):
    
    # -----------Choices ---------------
    NOTIF_ACTION = [
        ("Applicant", "New Applicant Applied to your post"),
        ("MatchSkill", "Job matches your skill"),
        ("ApplicationResult","Application Result"),
    ]
    APPLICATION_STATUS = [('accepted','Accepted'),('rejected','Rejected'),]
    NOTIF_STATUS = [('read',"Read"),('unread','Unread'),]
    STATUS_CHOICES = [("active", "Active"), ("deleted", "Deleted")]
    
    # ------------fields ----------------
    notification = models.CharField(max_length=18,choices=NOTIF_ACTION,default='')
    timestamp = models.DateTimeField(default=datetime.today)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES,default='')
    action_user = models.CharField(max_length=220,default='',blank=True) #who trigger the action (fullname) can be person/company
    user = models.ForeignKey(User, on_delete=models.CASCADE) #the owner who will receive the notification
    job = models.ForeignKey('jobsapp.Job', on_delete=models.CASCADE, null=True, blank=True, default='')
    application_status = models.CharField(max_length=10,choices=APPLICATION_STATUS,blank=True,default='',null=True)
    is_read = models.CharField(max_length=7,choices=NOTIF_STATUS,default='')

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("signin", "Sign in"),
        ("logout", "Sign out"),
        ("applied", "Applied"),
        ("postJob", "Posted Job"),
        ("updatePost", "Update Post"),
        ("updateProfile", "Update Profile"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=14, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=date.datetime)  # automatic date today


class Education(models.Model):
    DEGREE_LEVEL_CHOICES = [
        ("HS", "High School"),
        ("UG", "Bachelors"),
        ("PG", "Masters"),
        ("CF", "Certificate"),
        ("AS", "Associates"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=4, choices=DEGREE_LEVEL_CHOICES)
    school_name = models.CharField(max_length=120)
    course = models.CharField(max_length=150, default="")
    started_year = models.IntegerField(default=2020)
    ended_year = models.IntegerField(default=2021)


class SocialMedia(models.Model):
    SOCMED_CHOICES = [
        ("FB", "Facebook"),
        ("IG", "Instagram"),
        ("GM", "Gmail"),
        ("LI", "LinkedIn"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_media = models.CharField(max_length=3, choices=SOCMED_CHOICES)
