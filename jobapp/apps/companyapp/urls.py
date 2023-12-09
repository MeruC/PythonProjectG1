from django.urls import path
from . import views

app_name = "companyapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("createCompany/", views.createCompany, name="createCompany"),
    # TODO: change this to dynamic url
    path("companyId/", views.companyProfile, name="companyProfile"),
    path("myCompany/settings", views.companyProfileSettings, name="companyProfileSettings")
]