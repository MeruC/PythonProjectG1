from django.urls import path

from . import views

app_name = "managementapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.manage_users, name="manage_users"),
    path("users/<int:id>/profile", views.user_detail, name="user_detail"),
    path(
        "users/<int:id>/qualification",
        views.qualifications,
        name="user_qualification",
    ),
    path("users/<int:id>/history", views.history, name="user_history"),
    path("users/<int:id>/actions", views.action, name="user_actions"),
]
