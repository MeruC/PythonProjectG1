from django.urls import path
from . import views

app_name = "jobsapp"
urlpatterns = [
    # render
    path("", views.index, name="index"),
    path("jobs/<int:jobId>/", views.jobDetails, name="jobDetails"),
    # asycn
    path(
        "getJobList",
        views.getJobList,
        name="getJobList",
    ),
    path("getJobDetails/<int:jobId>/", views.getJobDetails, name="getJobDetails"),
    path(
        "submitApplication/<int:job_id>/",
        views.submitApplication,
        name="submitApplication",
    ),
    path(
        "removeApplication/<int:job_id>/",
        views.removeApplication,
        name="removeApplication",
    ),
    path("searchJob", views.searchJob, name="searchJob"),
    path("getWhatSuggestion/", views.getWhatSuggestion, name="getWhatSuggestion"),
    path(
        "getWhereSuggestion/",
        views.getWhereSuggestion,
        name="getWhereSuggestion",
    ),
]
