from django.shortcuts import redirect, render
from ..jobsapp.models import Company

# Create your views here.
def index(request):
    return render(request, "index.html")
def createCompany(request):
    #check if logged in
    if request.user.is_authenticated and not request.user.is_superuser:
        #check if already has company
        current_user = request.user
        hasCompany = Company.objects.filter(user=current_user).count()>0
        
        if not hasCompany:
            if request.method == "POST": 
                addCompanyData(request)
            else:
                return render(request, "company/createCompany.html")
    
    return redirect("jobsapp:index")
    
def companyProfile(request):
    # TODO
    # - User must be logged in to view a company
    return render(request, "company/companyProfile.html")
def companyJobList(request):
    # TODO
    # - User must be the owner of the company to view this page
    return render(request, "company/companyJobList.html")

def companyApplicants(request):
    # TODO
    # - User must be the owner of the company to view this page
    return render(request, "company/companyApplications.html")
def companyProfileSettings(request):
    # TODO
    # - User must be the owner of the company to view this page
    # - If user doesn't have a company, redirect to createCompany
    return render(request, "company/companySettings.html")
def createJob(request):
    # TODO
    # - User must be the owner of the company to view this page
    # - If user doesn't have a company, redirect to createCompany
    return render(request, "company/createJob.html")



# ------------ Add new company ----------
def addCompanyData(request):
    Company.objects.create(
        user = request.user,
        company_name = request.POST.get('company_name'),
        description = request.POST.get('description'),
        city = request.POST.get('city'),
        country = request.POST.get('country'),
    ).save()
    
    return redirect('companyapp:companyProfileSettings')
    