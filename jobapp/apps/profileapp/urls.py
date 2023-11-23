from django.contrib import admin
from django.urls import path
from . import views


app_name = "profileapp"

urlpatterns = [
    path("", views.index, name="index"),
]
