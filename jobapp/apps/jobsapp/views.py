import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q

from ..accountapp.models import ActivityLog, Alerts, Education
from ..accountapp.views import hasUnreadNotif
# from ..profileapp.models import JobApplication
from .models import Job, WorkExperience, jobApplicant
from django.contrib.auth import get_user_model
from apps.jobsapp.models import Job, Company
from django.utils  import timezone
User = get_user_model()


# render
def index(request):
    if request.user.is_authenticated:
        user = request.user
        if user.contact_number and user.skills and user.profile_summary:
            hasInfo = True
        else:
            hasInfo = False
            
        if not Education.objects.filter(user_id=request.user).exists():
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
            
        if  not Education.objects.filter(user_id=request.user).exists():
            hasInfo = False

        if not Job.objects.filter(id=jobId, status="active",company__is_active=True).select_related("company").values("company__is_active").exists():
            return redirect("jobsapp:index")
      
        
        company = Company.objects.get(id=Job.objects.get(id=jobId).company_id)
        
        if company.user_id == request.user.id:
            isOwned = True
        else:
            isOwned = False
    return render(request, "jobDetails.html", {"hasInfo": hasInfo, "company": company, "isOwned": isOwned})


# async (views used in ajax call )
def getJobList(request):
    if request.user.is_authenticated:
        appliedJobs = jobApplicant.objects.filter(
            user=request.user.id, status__in=["pending", "approved"]
        )
        appliedJobsId = appliedJobs.values_list("job_id", flat=True)
        approvedJobs = jobApplicant.objects.filter(
            user=request.user.id, status__in=[ "approved"]
        )
        approvedJobsId = approvedJobs.values_list("job_id", flat=True)
        jobs = (
            Job.objects.filter(status="active", company__is_active=True)
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
                "company__is_active",
                "company__user_id"
            )
        )
        #print(jobs)
        return JsonResponse(
            {
                "success": True,
                "jobs": list(jobs),
                "appliedJobsId": list(appliedJobsId),
                "userId": request.user.id,
                "approvedJobsId": list(approvedJobsId),
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
    
    if not Education.objects.filter(user_id=request.user).exists():
            hasInfo = False

    if not request.user.is_authenticated:
        return redirect("jobsapp:index")

    hasApplied = jobApplicant.objects.filter(
        job_id=jobId, user_id=request.user.id, status__in=["pending", "approved"]
    ).exists()
    isApproved = jobApplicant.objects.filter(
        job_id=jobId, user_id=request.user.id, status__in=["approved"]
    ).exists()

    try:
        job = (
            Job.objects.filter(id=jobId, status="active", company__is_active=True)
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
                "company__description",
                "company__city",
                "company__country",
                "company__logo",
                "company__cover_photo",
                "company__is_active",
                "company__user_id"
            )
            .first()
        )
        if job is None:
            #print(job)
            return redirect("jobsapp:index")
    except Job.DoesNotExist:
        return redirect("jobsapp:index")
    return JsonResponse(
        {"success": True, "job": job, "hasApplied": hasApplied, "hasInfo": hasInfo,  "userId": request.user.id, "isApproved": isApproved}
    )


def manageApplication(request, jobId):
    if request.method == "POST":
        job = Job.objects.get(id=jobId)

        # job_seeker = JobSeeker.objects.get(user=request.user)
        existing_application = jobApplicant.objects.filter(
            job=job, user=request.user.id, status__in=["pending", "approved"]
        ).last()

        if existing_application:
            existing_application.delete()
        else:
            jobApplicant.objects.create(
                job_id=job.id, user_id=request.user.id, status="pending", date_applied=timezone.now()
            )
            # Alerts.objects.create(
            #     notification="Applicant",
            #     message=f"New applicant applied to your post ({user.username} for {job.job_title}).",
            #     user=request.user.id,
            #     job=job,
            #     action_user= request.user.firstname  + " " + request.user.lastname,
            #     application_status="",
            #     is_read="unread"
            # )
            ActivityLog.objects.create(user=request.user, action="Applied")
        return JsonResponse({"success": True})


def searchJob(request):
    what = request.GET.get("what", "")
    where = request.GET.get("where", "")
    type = request.GET.get("type", "all")
    base_query = Q(status="active")
    appliedJobs = jobApplicant.objects.filter(user=request.user.id, status__in=["pending", "approved"])
    appliedJobsId = appliedJobs.values_list("job_id", flat=True)
    
    
    approvedJobs = jobApplicant.objects.filter(
            user=request.user.id, status__in=[ "approved"]
        )
    approvedJobsId = approvedJobs.values_list("job_id", flat=True)
        
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
        Job.objects.filter(base_query & Q(company__is_active=True))
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
            "company__is_active",
            "company__user_id"
            
            
        )
    )

    return JsonResponse(
        {
            "success": True,
            "jobs": list(jobs),
            "appliedJobsId": list(appliedJobsId),
            "userId": request.user.id,
            "approvedJobsId": list(approvedJobsId),
        }
    )



def getWhatSuggestion(request):
    query = request.GET.get("query", "")
    suggestions = set()

    if query:
  
        job_title_matches = Job.objects.filter(job_title__icontains=query, status="active",company__is_active=True).values("job_title",  "company__is_active").distinct()

        skills_matches = Job.objects.filter(skills__icontains=query, status="active",company__is_active=True).values("skills",  "company__is_active").distinct()

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
        city_query = Q(company__city__icontains=query)
        country_query = Q(company__country__icontains=query)
        active_query = Q(status="active")
        company_active_query = Q(company__is_active=True)
        jobs = (
            Job.objects.filter(city_query | country_query, active_query, company_active_query)
            .values("company__city", "company__country","company__is_active","status")
            .distinct()
        )
        for job in jobs:
            suggestion = f"{job['company__city']}, {job['company__country']}"
            suggestions.add(suggestion)

        print ("list(suggestions)")
        print (list(suggestions))
    return JsonResponse({"success": True, "suggestions": list(suggestions)})


