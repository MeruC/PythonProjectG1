from django.db import models
from django.contrib.auth.models import AbstractUser


# user table
class User(AbstractUser):
    # add additional fields here
    pass


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
    NOTIF_ACTION = [
        ("Applicant", "New Applicant Applied to your post"),
        ("MatchSkill", "Job matches your skill"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
