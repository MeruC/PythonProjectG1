from django.db import models

# user table
class User(models.Model):
    email = models.EmailField(max_length=255)
    password = models.TextField()
    isActivated = models.BooleanField(default=True)
    

class Person(models.Model):
    SEX_CHOICE = [('M','Male'),('F','Female')]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICE,blank=True)
    street_address = models.CharField(max_length=100)
    apartment_no = models.IntegerField(null=True)
    city = models.CharField(max_length=70)
    postal_code = models.IntegerField()
    
    
class Alerts(models.Model):
    NOTIF_ACTION = [('Applicant','New Applicant Applied to your post'),('MatchSkill','Job matches your skill')]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('signin', 'Sign in'),
        ('logout','Sign out'),
        ('applied','Applied'),
        ('postJob','Posted Job'),
        ('updatePost','Update Post'),
        ('updateProfile','Update Profile')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    action = models.CharField(max_length=14,choices=ACTION_CHOICES)
    timestamp = models.DateTimeField()
    
    
    
    