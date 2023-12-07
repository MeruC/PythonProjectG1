from django.urls import path
from . import views

app_name = "accountapp"
urlpatterns = [
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]
