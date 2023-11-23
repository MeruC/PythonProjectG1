from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('addWorkExp/', views.addWorkExp, name="addWorkExp") #add work experience
]
