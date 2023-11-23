from django.urls import path

from . import views


app_name = "jobsapp"
urlpatterns = [
    path("", views.index, name="index"),
]
