from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import JobForm
from django.contrib.auth import get_user_model
from apps.jobsapp.models import Job, Company
from django.utils import timezone as django_timezone


User = get_user_model()

# For displying active jobs in the homepage
def displayJobs(request):
    template = "job_list.html"
    active_jobs = Job.objects.filter(status='active')
    context = {
        "job_list":active_jobs,
        'now': django_timezone.now(),
    }
    return render(request, template, context)

# For adding or editing a job
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
            form.save()
            
            # generate a success message when registration is successful
            messages.success(
                request,
                "Job has been posted successfully.",
            )
            return redirect("../../company/job-listings")
        else:
            template = "job_form.html"
            context = {
                "form": form
            }
        
    return render(request, template, context)

# For deleting a job
def deleteJob(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.delete()
    return redirect("../../company/job-listings")

# For displying all jobs listed by the company
def listJob(request):
    template = "job_listings.html"
    context = {
        "job_list": Job.objects.all()
    }
    return render(request, template, context)
