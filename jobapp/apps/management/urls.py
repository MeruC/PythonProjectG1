from django.urls import path

from . import views

app_name = "managementapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.manage_users, name="manage_users"),
    path("users/<int:id>/profile", views.user_detail, name="user_detail"),
]
