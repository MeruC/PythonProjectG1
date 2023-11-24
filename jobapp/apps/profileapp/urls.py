from django.contrib import admin
from django.urls import path
from . import views


app_name = "profileapp"

urlpatterns = [
    path("", views.index, name="index"),
    # todo update this later since there's no view for logout yet
    path("logout/", views.index, name="logout"),
]
