import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q

from ..profileapp.models import JobApplication, JobSeeker
from .models import Job


# render
def index(request):
    return render(request, "index/base.html")


def jobDetails(request, jobId):
    if not request.user.is_authenticated:
        return redirect("jobsapp:index")

    return render(request, "jobDetails.html")


# async (views used in ajax call )
def getJobList(request):
    seekerId = JobSeeker.objects.get(user_id=request.user.id)
    appliedJobs = JobApplication.objects.filter(job_seeker_id=seekerId, status="active")
    appliedJobsId = appliedJobs.values_list("job_id", flat=True)
    # jobs = Job.objects.select_related("company").filter(status="active")
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


def getJobDetails(request, jobId):
    if not request.user.is_authenticated:
        return redirect("jobsapp:index")

    hasApplied = JobApplication.objects.filter(
        job_id=jobId, job_seeker_id=request.user.id, status="active"
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
    return JsonResponse({"success": True, "job": job, "hasApplied": hasApplied})


def manageApplication(request, jobId):
    if request.method == "POST":
        job = Job.objects.get(id=jobId)
        job_seeker = JobSeeker.objects.get(user=request.user)
        existing_application = JobApplication.objects.filter(
            job=job, job_seeker=job_seeker
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
                job=job, job_seeker=job_seeker, status="active"
            )
        return JsonResponse({"success": True})


def searchJob(request):
    what = request.GET.get("what", "")
    where = request.GET.get("where", "")
    type = request.GET.get("type", "all")
    base_query = Q()

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

    return JsonResponse({"success": True, "jobs": list(jobs)})


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
