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
    path("postJob/", views.postJob, name="postJob"),                       # get and post req. for job posting operation
    path("editJob/<int:job_id>/", views.postJob, name="editJob"),          # get and post req. for job editing operation
    path("deleteJob/<int:job_id>/", views.deleteJob, name="deleteJob"),    # get and post req. for job deleting operation
    path("jobListings/", views.listJob, name="jobListings"),                   # for company (viewing of listed jobs - active and inactive)
]
