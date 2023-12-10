from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from ..jobsapp.models import Company
from django.contrib import messages
from .forms import *

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
                return redirect('companyapp:companyJobList')
            else:
                return render(request, "company/createCompany.html")
    
    return redirect('companyapp:companyJobList')
    
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
    current_user = request.user
    hasCompany = Company.objects.filter(user=current_user).count()>0
    if hasCompany:
        company_instance = Company.objects.get(user=current_user)
        data = getCompanyData(request)
        company_logo_form = CompanyLogoForm()
        company_cover_form = CompanyCoverForm()
        company_data_form = CompanyDataForm(instance=company_instance)
        context = {
            'data':data,
            'company_logo_form': company_logo_form,
            'company_cover_form': company_cover_form,
            'company_data_form': company_data_form,
        }
        return render(request, "company/companySettings.html",context)
    return render(request, "company/createCompany.html")

def createJob(request):
    # TODO
    # - User must be the owner of the company to view this page
    # - If user doesn't have a company, redirect to createCompany
    return render(request, "company/createJob.html")


def getCompanyData(request):
    current_user = request.user
    company = Company.objects.filter(user=current_user).values().first()
    
    media_url = settings.MEDIA_URL
    return {
        "company_name": company['company_name'],
        "description": company['description'],
        "city": company['city'],
        "country": company['country'],
        "logo": f"{media_url}{company['logo']}" if company['logo'] else None,
        "cover_photo": f"{media_url}{company['cover_photo']}" if company['cover_photo'] else None,
    }

# ------------ Add new company ----------
def addCompanyData(request):
    Company.objects.create(
        user = request.user,
        company_name = request.POST.get('company_name'),
        description = request.POST.get('description'),
        city = request.POST.get('city'),
        country = request.POST.get('country'),
    ).save()
    
    
# Upload company logo
def AddCompanyLogo(request):
    current_user_id = request.user
    company = get_object_or_404(Company,user=current_user_id)
    
    if request.method == 'POST':
        logo_form = CompanyLogoForm(request.POST, request.FILES, instance=company)
        
        if logo_form.is_valid():
            logo_form.save()
            messages.success(request,'Company Logo Successfully updated!')
    return redirect('companyapp:companyProfileSettings')

# Upload company logo
def AddCompanyCoverPhoto(request):
    current_user_id = request.user
    company = get_object_or_404(Company,user=current_user_id)
    
    if request.method == 'POST':
        cover_form = CompanyCoverForm(request.POST, request.FILES, instance=company)
        
        if cover_form.is_valid():
            cover_form.save()
            messages.success(request,'Company Cover Successfully updated!')
    return redirect('companyapp:companyProfileSettings')



# ------- update company data ----------
def updateCompanyData(request):
    if request.method == 'POST':
        company_instance = Company.objects.get(user=request.user)
        company_data_form = CompanyDataForm(request.POST, instance=company_instance)
        
        try:   
            if company_data_form.is_valid():
                company_data_form.save()
                messages.success(request,'Company details successfully updated')
        except Exception as ex:
            print(ex)
            messages.error(request,ex)
            
    return redirect('companyapp:companyProfileSettings')