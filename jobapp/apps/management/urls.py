from django.urls import path

from . import views

app_name = "managementapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.manage_users, name="manage_users"),

    path("jobs/", views.manage_jobs, name="manage_jobs"),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobs/action/<int:job_id>/', views.action_job, name='action_job'),
    
    
    
    path("companies/", views.manage_companies, name="manage_companies"),
    path('companies/delete/<int:company_id>/', views.delete_company, name='delete_company'),
    path('companies/edit/<int:company_id>/', views.edit_company, name='edit_company'),
    path('companies/action/<int:company_id>/', views.action_company, name='action_company'),

    
]
