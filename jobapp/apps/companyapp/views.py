from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from ..jobsapp.models import Company
from django.contrib.auth.decorators import login_required
from ..jobsapp.models import Job, jobApplicant
from django.contrib.auth import get_user_model
from ..accountapp.models import Alerts
from .forms import JobForm
from django.http import JsonResponse
from django.template.loader import render_to_string

User = get_user_model()

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

def companyApplicants(request):
    # TODO
    # - User must be the owner of the company to view this page
    return render(request, "company/companyApplications.html")


@login_required(login_url='/account/login/')
def companyProfileSettings(request):
    # TODO
    # - User must be the owner of the company to view this page
    # - If user doesn't have a company, redirect to createCompany
    
    try:
        # Try to get the company associated with the logged-in user
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        # If the user doesn't have a company, redirect to the company creation page
        return redirect("/company/createCompany/")
    
    return render(request, "company/companySettings.html")


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
    
    return redirect('companyapp:companyProfileSettings')
    