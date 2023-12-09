from django.contrib import admin
from django.urls import path
from . import views

app_name = "profileapp"
urlpatterns = [
    path("", views.index, name="index"),
    path('addWorkExp/', views.addWorkExp, name="addWorkExp"), #add work experience
    path('addEducation/',views.addEducation, name="addEducation"),
    path('delWork/<int:id>/',views.delete_work,name="deleteWork"),
    path('updatePassword/<int:id>/',views.updatePassword,name="updatePass"),
    path('delEducation/<int:id>/',views.delete_education,name="deleteEducation"),
    path('education/<int:id>/',views.retrieveEducation,name='education'),
    path('addskill',views.addSkill,name="addSkill"),
    path('updateEducation/<int:id>/',views.updateEducation,name="updateEducation"),
    path('deleteskill/<str:skill>/',views.delete_skill,name="deleteSkill"),
    path('checkskill/<str:skill>/',views.isSkillAvailable,name="checkSkill"),
    path('deactivate/',views.DeactivateAccount, name="deactAccount")
    # todo update this later since there's no view for logout yet
    # path("logout/", views.index, name="logout"),
]
