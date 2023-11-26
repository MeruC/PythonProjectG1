from django.urls import path
from . import views


app_name = "jobsapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("searchJob", views.searchJob, name="searchJob"),
    path("applyNow", views.applyNow, name="applyNow"),
    path("jobDetails", views.jobDetails, name="jobDetails"),
]
