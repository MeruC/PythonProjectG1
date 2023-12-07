from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login

from apps.jobsapp.models import Job


from django.contrib import messages

from .forms import EditJobForm

# todo to be used when they logged in as admin. should move this to account
def my_login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.is_staff:
            redirect("managementapp:index")

        else:
            # Redirect to a success page.
            ...
    else:
        # Return an 'invalid login' error message.
        ...


def index(request):
    return render(request, "management/dashboard.html")


def manage_users(request):
    return render(request, "management/manage_users.html")

# manage jobs ------------------------------

def manage_jobs(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, "management/manage-jobs/manage_jobs.html", context)


def edit_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return redirect("managementapp:manage_jobs")
    
    if request.method == 'POST':
        form = EditJobForm(request.POST)
        if form.is_valid():
            try:
                job.job_title = form.cleaned_data['job_title']
                job.description = form.cleaned_data['description']
                job.type = form.cleaned_data['type']
                job.skills = form.cleaned_data['skills']

                job.save()
                messages.success(
                    request,
                    "Job updated successfully",
                ) 
            except Exception as e:
                messages.error(request, "Internal Server Error")
                print(e)
    else:
        form = EditJobForm(initial={
            'type': job.type,
            'skills': job.skills,
            'job_title': job.job_title,
            'description': job.description,
            
        })

    context = {'job': job, 'form': form}
    return render(request, 'management/manage-jobs/job_edit.html', context)



def action_job(request, job_id):

    try:
        job = Job.objects.get( id=job_id)
    except Job.DoesNotExist:
        return redirect("managementapp:manage_jobs")
    
    if request.method == 'POST':
        try :
            if job.status == 'active':
                job.status = 'deleted'
            else:
                job.status = 'active'
            job.save()
            messages.success(
                    request,
                    "Job  deleted successfully" if job.status == 'active' else "Job activated successfully",
                ) 
        except Exception as e:
            messages.error(request, "Internal Server Error")
            print(e)
  
    context = {'job': job}
    return render(request, 'management/manage-jobs/job_action.html', context)



def delete_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.delete()
        messages.success(
                    request,
                    "Job  deleted successfully" ,
                )
    except Job.DoesNotExist:
        return redirect("managementapp:manage_jobs")
    except Exception as e:
            messages.error(request, "Internal Server Error")
            print(e)
    return redirect("managementapp:manage_jobs")
    