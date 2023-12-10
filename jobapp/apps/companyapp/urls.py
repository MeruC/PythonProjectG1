from django.urls import path
from . import views

app_name = "companyapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("createCompany/", views.createCompany, name="createCompany"),
    # TODO: change this to dynamic url
    path("companyId/", views.companyProfile, name="companyProfile"),
    path("myCompany/jobListings", views.companyJobList, name="companyJobList"),
    path("myCompany/jobListings/createJob", views.createJob, name="createJob"),
    path("myCompany/applicants", views.companyApplicants, name="companyApplicants"),
    path("myCompany/", views.companyProfileSettings, name="companyProfileSettings"),
    path("myCompany/updatecompanylogo", views.AddCompanyLogo, name="UploadCompanyLogo"),
    path("myCompany/updatecompanycover", views.AddCompanyCoverPhoto, name="UploadCompanyCover"),
    path("myCompany/updatecompanydata", views.updateCompanyData, name="UploadCompanyData"),
]
