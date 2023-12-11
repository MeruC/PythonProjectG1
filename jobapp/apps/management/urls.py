from django.urls import path

from . import views

app_name = "managementapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/job_posts/", views.get_job_post_data, name="job_posts"),
    path("users/", views.manage_users, name="manage_users"),
    path("users/<int:id>/profile", views.user_detail, name="user_detail"),
    path(
        "users/<int:id>/qualification",
        views.qualifications,
        name="user_qualification",
    ),
    path("job_history/<int:id>", views.get_work_api, name="job_history"),
    path("users/<int:id>/history", views.history, name="user_history"),
    path("users/<int:id>/actions", views.action, name="user_actions"),
    path("users/<int:id>/logs", views.get_logs, name="user_logs"),
    path("jobs/", views.manage_jobs, name="manage_jobs"),
    path("jobs/delete/<int:job_id>/", views.delete_job, name="delete_job"),
    path("jobs/edit/<int:job_id>/", views.edit_job, name="edit_job"),
    path("jobs/action/<int:job_id>/", views.action_job, name="action_job"),
    path("companies/", views.manage_companies, name="manage_companies"),
    path(
        "companies/delete/<int:company_id>/",
        views.delete_company,
        name="delete_company",
    ),
    path(
        "companies/edit/<int:company_id>/",
        views.edit_company,
        name="edit_company",
    ),
    path(
        "companies/action/<int:company_id>/",
        views.action_company,
        name="action_company",
    ),
]
