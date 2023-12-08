from django.urls import path
from . import views

app_name = "companyapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("createCompany/", views.createCompany, name="createCompany"),
]