
from django.conf import settings
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from ..jobsapp.models import Company
from django.contrib.auth.decorators import login_required
from ..jobsapp.models import Job, jobApplicant,Company
from django.contrib.auth import get_user_model
from ..accountapp.models import Alerts
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

User = get_user_model()

# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required(login_url='/account/login/')
def createCompany(request):
    #check if logged in
    if not request.user.is_superuser:
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
    

@login_required(login_url='/account/login/')
def companyProfile(request,company_id):
    try:
        company= Company.objects.get(id=company_id)
        if (company.is_active == False):
            return redirect("jobsapp:index")
        jobs = Job.objects.filter(company_id=company_id, status="active")
        context = {
            "company":company,
            "jobs":jobs,
            
        }
    except Company.DoesNotExist:
        return redirect("jobsapp:index")

    return render(request, "company/companyProfile.html",context)


# -------- View all job listings of a company --------
@login_required(login_url='/account/login/')
def companyJobList(request):
    # TODO
    # - User must be the owner of the company to view this page
    
    try:
        # Try to get the company associated with the logged-in user
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # If the user doesn't have a company, redirect to the company creation page
        return redirect("/company/createCompany/")
    
    # If the user has a company, retrieve jobs owned by the company
    job_list = Job.objects.filter(company=company)
    
    template = "company/companyJobList.html"
    context = {
        "job_list": job_list,
    }
    return render(request, template, context)


# ------- For viewing applicants of a specific job -------
@login_required(login_url='/account/login/')
def jobApplicants(request, job_id):
    try:
        # Try to get the company associated with the logged-in user
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # If the user doesn't have a company, redirect to the company creation page
        return redirect("/company/createCompany/")
    
    job = get_object_or_404(Job, id=job_id)
    applicants = job.jobapplicant_set.all()  # Assuming you've set the related name in your Job model

    context = {
        'job': job,
        'applicants': applicants,
    }
    
    template = "company/jobApplications.html"
    
    return render(request, template, context)

# ------- For viewing applicants of a company -------
@login_required(login_url='/account/login/')
def companyApplicants(request):
    try:
        # Try to get the company associated with the logged-in user
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # If the user doesn't have a company, redirect to the company creation page
        return redirect("/company/createCompany/")
    
    # Retrieve all jobs associated with the company
    jobs = Job.objects.filter(company=company)

    # Retrieve all applicants for each job
    all_applicants = []
    for job in jobs:
        applicants = job.jobapplicant_set.all()  # Assuming you've set the related name in your Job model
        all_applicants.extend(applicants)

    context = {
        'company': company,
        'applicants': all_applicants,
    }
    
    template = "company/companyApplications.html"
    
    return render(request, template, context)

# ------ To update the application status ------
def updateStatus(request, applicant_id, action):
    # Get the job applicant
    applicant = get_object_or_404(jobApplicant, id=applicant_id)

    # Define valid actions (check or xmark)
    valid_actions = ['check', 'xmark']

    if action not in valid_actions:
        return HttpResponse("Invalid action")

    # Update the status based on the action
    if action == 'check':
        applicant.status = 'approved'
    elif action == 'xmark':
        applicant.status = 'rejected'

    # Save the updated status
    applicant.save()

    return redirect("companyapp:companyApplicants")


@login_required(login_url='/account/login/')
def companyProfileSettings(request):
    current_user = request.user
    hasCompany = Company.objects.filter(user=current_user).count()>0
    if hasCompany:
        company_instance = Company.objects.get(user=current_user)
        data = getCompanyData(request)
        
        initial_country_value = company_instance.country
        company_logo_form = CompanyLogoForm()
        company_cover_form = CompanyCoverForm()
        company_data_form = CompanyDataForm(instance=company_instance, initial={'country': initial_country_value})
        
        context = {
            'data':data,
            'company_logo_form': company_logo_form,
            'company_cover_form': company_cover_form,
            'company_data_form': company_data_form,
        }
        return render(request, "company/companySettings.html",context)
    return render(request, "company/createCompany.html")



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


# -------- Create and Edit a Job --------
@login_required(login_url='/account/login/')
def createJob(request, job_id=0):
    try:
        # Try to get the company associated with the logged-in user
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # If the user doesn't have a company, raise a 404 error
        return redirect("/company/createCompany/")

    if request.method == "GET":
        if job_id == 0:
            template = "company/createJob.html"
            form = JobForm()
            context = {
                "form": form,
                "company": company,
            }
        else:
            template = "company/createJob.html"
            job = Job.objects.get(pk=job_id)
            form = JobForm(instance=job)
            context = {
                "form": form,
                "company": company,
            }
    else:
        if job_id == 0:
            form = JobForm(request.POST)
        else:
            job = Job.objects.get(pk=job_id)
            form = JobForm(request.POST, instance=job)

        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.company = company  # Explicitly set the company field
            new_job.save()

            # Identify users whose skills have at least one partial match with the posted job
            job_skills = [skill.strip() for skill in new_job.skills.split(',')]
            user_skill_query = Q()
            for skill in job_skills:
                user_skill_query |= Q(skills__contains=skill)

            matching_users = User.objects.filter(user_skill_query)

            # Create a notification for each matching user, if it doesn't already exist
            for user in matching_users:
                existing_alert = Alerts.objects.filter(
                    notification="MatchSkill",
                    action_user=request.user.get_full_name(),
                    user=user,
                    is_read='unread',
                ).exists()

                if not existing_alert:
                    alert = Alerts(
                        notification="MatchSkill",
                        action_user=request.user.get_full_name(),
                        user=user,
                        is_read='unread',
                    )
                    alert.save()

            return redirect("/company/myCompany/jobListings")
        else:
            print(form.errors)
            template = "company/createJob.html"
            context = {
                "form": form,
                "company": company,
            }

    return render(request, template, context)


# ------------ Delete a Job ------------
@login_required(login_url='/account/login/')
def deleteJob(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.delete()
    return redirect("/company/myCompany/jobListings")


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
        
    return redirect('companyapp:createCompany')

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

    return redirect('companyapp:createCompany')


# ------- update company data ----------
def updateCompanyData(request):
    if request.method == 'POST':
        company_instance = Company.objects.get(user=request.user)
        company_data_form = CompanyDataForm(request.POST, instance=company_instance)
        
        try:   
            if company_data_form.is_valid():
                company_data_form.save()
                messages.success(request,'Company details successfully updated')
                return redirect('companyapp:companyProfileSettings')
        except Exception as ex:
            print(ex)
            messages.error(request,ex)
            
    return redirect('companyapp:createCompany')