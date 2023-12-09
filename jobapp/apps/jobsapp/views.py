import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from ..accountapp.views import hasUnreadNotif
from ..profileapp.models import JobApplication
from .models import Job
from django.contrib import messages
from .forms import JobForm
from django.contrib.auth import get_user_model
from apps.jobsapp.models import Job, Company
from apps.accountapp.models import Alerts
from django.utils import timezone as django_timezone
from django.contrib.auth.decorators import login_required

User = get_user_model()


# render
def index(request):
    if request.user.is_authenticated:
        user = request.user
        if user.contact_number and user.skills and user.profile_summary:
            hasInfo = True
        else:
            hasInfo = False
    else:
        hasInfo = False
        
        
    context = {
        "hasInfo":hasInfo,
        "hasUnreadNotif":hasUnreadNotif(request),
    }
    return render(request, "index/base.html", context)


def jobDetails(request, jobId):
    if not request.user.is_authenticated:
        hasInfo = False
        return redirect("jobsapp:index")
    else:
        user = request.user
        if user.contact_number and user.skills and user.profile_summary:
            hasInfo = True
        else:
            hasInfo = False

        if not Job.objects.filter(id=jobId).exists():
            return redirect("jobsapp:index")
    return render(request, "jobDetails.html", {"hasInfo": hasInfo})

# async (views used in ajax call )
def getJobList(request):
    if request.user.is_authenticated:
        appliedJobs = JobApplication.objects.filter(
            user=request.user.id, status="active"
        )
        appliedJobsId = appliedJobs.values_list("job_id", flat=True)
        jobs = (
            Job.objects.filter(status="active")
            .select_related("company")
            .values(
                "id",
                "job_title",
                "description",
                "status",
                "type",
                "skills",
                "city",
                "country",
                "max_salary",
                "min_salary",
                "date_posted",
                "company_id",
                "company__company_name",
            )
        )

        return JsonResponse(
            {
                "success": True,
                "jobs": list(jobs),
                "appliedJobsId": list(appliedJobsId),
            }
        )
    else:
        return JsonResponse(
            {
                "success": False,
            }
        )


def getJobDetails(request, jobId):
    user = request.user

    if user.contact_number and user.skills and user.profile_summary:
        hasInfo = True
    else:
        hasInfo = False

    if not request.user.is_authenticated:
        return redirect("jobsapp:index")

    hasApplied = JobApplication.objects.filter(
        job_id=jobId, user_id=request.user.id, status="active"
    ).exists()

    try:
        job = (
            Job.objects.filter(id=jobId, status="active")
            .select_related("company")
            .values()
            .values(
                "id",
                "job_title",
                "description",
                "status",
                "type",
                "skills",
                "city",
                "country",
                "max_salary",
                "min_salary",
                "date_posted",
                "company_id",
                "company__company_name",
            )
            .first()
        )

    except Job.DoesNotExist:
        return redirect("jobsapp:index")
    return JsonResponse(
        {"success": True, "job": job, "hasApplied": hasApplied, "hasInfo": hasInfo}
    )


def manageApplication(request, jobId):
    if request.method == "POST":
        job = Job.objects.get(id=jobId)

        # job_seeker = JobSeeker.objects.get(user=request.user)
        existing_application = JobApplication.objects.filter(
            job=job, user=request.user.id
        ).first()

        if existing_application:
            if existing_application.status == "deleted":
                existing_application.status = "active"
            elif existing_application.status == "active":
                existing_application.status = "deleted"
            else:
                pass
            existing_application.save()
        else:
            JobApplication.objects.create(
                job_id=job.id, user_id=request.user.id, status="active"
            )
        return JsonResponse({"success": True})


def searchJob(request):
    what = request.GET.get("what", "")
    where = request.GET.get("where", "")
    type = request.GET.get("type", "all")
    base_query = Q(status="active")
    appliedJobs = JobApplication.objects.filter(user=request.user.id, status="active")
    appliedJobsId = appliedJobs.values_list("job_id", flat=True)
    if what:
        skills_list = re.split(r"\W+", what)
        for part in skills_list:
            base_query &= Q(skills__icontains=part) | Q(job_title__icontains=what)

    if where:
        cleaned_parts = re.split(r"\W+", where)
        for part in cleaned_parts:
            base_query &= Q(city__icontains=part) | Q(country__icontains=part)

    if type and type != "all":
        base_query &= Q(type=type)
    jobs = (
        Job.objects.filter(base_query)
        .select_related("company")
        .values(
            "id",
            "job_title",
            "description",
            "status",
            "type",
            "skills",
            "city",
            "country",
            "max_salary",
            "min_salary",
            "date_posted",
            "company_id",
            "company__company_name",
        )
    )

    return JsonResponse(
        {
            "success": True,
            "jobs": list(jobs),
            "appliedJobsId": list(appliedJobsId),
        }
    )


def getWhatSuggestion(request):
    query = request.GET.get("query", "")
    suggestions = set()

    if query:
        base_query = Q(job_title__icontains=query) | Q(skills__icontains=query)
        jobs = Job.objects.filter(base_query).values("job_title", "skills").distinct()

        for job in jobs:
            suggestions.add(job["job_title"])
            skills_list = re.split(r"\W+", job["skills"])
            suggestions.update(skill for skill in skills_list if skill)

    return JsonResponse({"success": True, "suggestions": list(suggestions)})


def getWhereSuggestion(request):
    query = request.GET.get("query", "")
    suggestions = set()

    if query:
        city_query = Q(city__icontains=query)
        country_query = Q(country__icontains=query)
        jobs = (
            Job.objects.filter(city_query | country_query)
            .values("city", "country")
            .distinct()
        )

        for job in jobs:
            suggestion = f"{job['city']}, {job['country']}"
            suggestions.add(suggestion)

    return JsonResponse({"success": True, "suggestions": list(suggestions)})



# For adding or editing a job
@login_required(login_url='/account/login/')
def postJob(request, job_id=0):
    if request.method == "GET":
        if job_id == 0:
            template = "job_form.html"
            form = JobForm()
            context = {
                "form": form
            }
        else:
            template = "job_form.html"
            job = Job.objects.get(pk=job_id)
            form = JobForm(instance=job)
            context = {
                "form": form
            }
    else:
        if job_id == 0:
            form = JobForm(request.POST)
        else:
            job = Job.objects.get(pk=job_id)
            form = JobForm(request.POST, instance=job)
        if form.is_valid():
            new_job = form.save()
            
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
            
            return redirect("../../company/jobListings")
        else:
            print(form.errors)
            template = "job_form.html"
            context = {
                "form": form
            }
        
    return render(request, template, context)

# For Job Deletion
@login_required(login_url='/account/login/')
def deleteJob(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.delete()
    return redirect("../../company/jobListings")

# For displying all jobs listed by the company
@login_required(login_url='/account/login/')
def listJob(request):
    template = "job_listings.html"
    context = {
        "job_list": Job.objects.all()
    }
    return render(request, template, context)

