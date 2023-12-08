from django.urls import path
from . import views


app_name = "jobsapp"
urlpatterns = [
    path("", views.displayJobs, name="displayJobs"),                        # for homepage (viewing of active jobs)
    path("post-job/", views.postJob, name="postJob"),                       # get and post req. for job posting operation
    path("edit-job/<int:job_id>/", views.postJob, name="editJob"),          # get and post req. for job editing operation
    path("delete-job/<int:job_id>/", views.deleteJob, name="deleteJob"),    # get and post req. for job deleting operation
    path("job-listings/", views.listJob, name="listJob"),                   # for company (viewing of listed jobs - active and inactive)
]
