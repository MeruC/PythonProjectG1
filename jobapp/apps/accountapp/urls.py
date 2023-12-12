from django.urls import path
from . import views

app_name = "accountapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("notification/<int:offset>/",views.Notification, name="notification")
]
