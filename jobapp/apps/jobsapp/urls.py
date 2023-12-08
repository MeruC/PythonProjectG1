from django.urls import path
from . import views

app_name = "jobsapp"
urlpatterns = [
    # render
    path("", views.index, name="index"),
    path("jobs/<int:jobId>/", views.jobDetails, name="jobDetails"),
    # asycn (url used in ajax call )
    path(
        "getJobList",
        views.getJobList,
        name="getJobList",
    ),
    path("getJobDetails/<int:jobId>/", views.getJobDetails, name="getJobDetails"),
    path(
        "manageApplication/<int:jobId>/",
        views.manageApplication,
        name="manageApplication",
    ),
    path("searchJob", views.searchJob, name="searchJob"),
    path("getWhatSuggestion/", views.getWhatSuggestion, name="getWhatSuggestion"),
    path(
        "getWhereSuggestion/",
        views.getWhereSuggestion,
        name="getWhereSuggestion",
    ),
]
