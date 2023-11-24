from django.contrib import admin
from django.urls import path
from . import views


app_name = "profileapp"

urlpatterns = [
    path("", views.index, name="index"),
    path('addWorkExp/', views.addWorkExp, name="addWorkExp"), #add work experience
    path('addEducation/',views.addEducation, name="addEducation"),
    # todo update this later since there's no view for logout yet
    path("logout/", views.index, name="logout"),
]
