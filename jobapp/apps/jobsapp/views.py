import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from ..accountapp.views import hasUnreadNotif
from ..profileapp.models import JobApplication
from .models import Job
from django.contrib.auth import get_user_model
from apps.jobsapp.models import Job, Company

User = get_user_model()


# render
def index(request):
    if request.user.is_authenticated:
        user = request.user
        if user.contact_number and user.skills and user.profile_summary:
            hasInfo = True
        else:
            hasInfo = False
        context = {
        "hasInfo":hasInfo,
        "hasUnreadNotif":hasUnreadNotif(request),
    }
    else:
        hasInfo = False
        context = {
        "hasInfo":hasInfo,
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
        company = Company.objects.get(id=Job.objects.get(id=jobId).company_id)
    return render(request, "jobDetails.html", {"hasInfo": hasInfo, "company": company})

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
                "max_salary",
                "min_salary",
                "date_posted",
                "company_id",
                "company__company_name",
                "company__city",
                "company__country",
            )
        )
        print(jobs)
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
                "max_salary",
                "min_salary",
                "date_posted",
                "company_id",
                "company__company_name",
                "company__city",
                "company__country",
                "company__logo",
                "company__cover_photo",
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
            base_query &= Q(company__city__icontains=part) | Q(company__country__icontains=part)

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
            "max_salary",
            "min_salary",
            "date_posted",
            "company_id",
            "company__company_name",
            "company__city",
            "company__country",
            
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
  
        job_title_matches = Job.objects.filter(job_title__icontains=query).values("job_title").distinct()

        skills_matches = Job.objects.filter(skills__icontains=query).values("skills").distinct()

        for job_title_match in job_title_matches:
            suggestions.add(job_title_match["job_title"])

        for skills_match in skills_matches:
            skills_list = re.split(r"\W+", skills_match["skills"])
            suggestions.update(skill for skill in skills_list if  query.lower() in skill.lower() )

    return JsonResponse({"success": True, "suggestions": list(suggestions)})

def getWhereSuggestion(request):
    query = request.GET.get("query", "")
    suggestions = set()

    if query:
        city_query = Q(city__icontains=query)
        country_query = Q(country__icontains=query)
        jobs = (
            Company.objects.filter(city_query | country_query)
            .values("city", "country")
            .distinct()
        )

        for job in jobs:
            suggestion = f"{job['city']}, {job['country']}"
            suggestions.add(suggestion)

    return JsonResponse({"success": True, "suggestions": list(suggestions)})
