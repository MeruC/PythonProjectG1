from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login

from apps.jobsapp.models import Job, Company


from django.contrib import messages

from .forms import  EditCompanyForm, EditCompanyImageForm, EditJobForm

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
                    "Job Updated Successfully",
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
                    "Job Activated Successfully" if job.status == 'active' else "Job Deleted Successfully",
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
    
    
# manage companies ------------------------------

def manage_companies(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, "management/manage-companies/manage_companies.html", context)


def edit_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return redirect("managementapp:manage_companies")
    
    if request.method == 'POST':
        form = EditCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                company.company_name = form.cleaned_data['company_name']
                company.description = form.cleaned_data['description']
                company.location = form.cleaned_data['location']
                if form.cleaned_data['company_img']:
                    company.company_img = form.cleaned_data['company_img']

                company.save()
                messages.success(
                    request,
                    "Company Updated Successfully",
                ) 
            except Exception as e:
                messages.error(request, "Internal Server Error")
                print(e)
    else:
        form = EditCompanyForm(initial={
            'company_name': company.company_name,
            'description': company.description,
            'location': company.location,
            'company_img': company.company_img,
            
        })
        

    context = {'company': company, 'form': form, 

               }
    return render(request, 'management/manage-companies/company_edit.html', context)

def edit_company_image(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return redirect("managementapp:manage_companies")
    
    if request.method == 'POST':
        form = EditCompanyImageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                company.company_img = form.cleaned_data['company_img']
                company.save()
            except Exception as e:
                print(e)
    
    return redirect(request, 'managementapp:edit_company', company_id=company_id)



def action_company(request, company_id):

    try:
        company = Company.objects.get( id=company_id)
    except Company.DoesNotExist:
        return redirect("managementapp:manage_companies")
    
    if request.method == 'POST':
        try :
            if company.is_active == True:
                company.is_active = False
            else:
                company.is_active = True
            company.save()
            messages.success(
                    request,
                    "Company Activated Successfully" if company.is_active == True else "Company  Deleted Successfully", 
                ) 
        except Exception as e:
            messages.error(request, "Internal Server Error")
            print(e)
  
    context = {'company': company}
    return render(request, 'management/manage-companies/company_action.html', context)



def delete_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
        company.delete()
        messages.success(
                    request,
                    "Company  Deleted Successfully" ,
                )
    except Company.DoesNotExist:
        return redirect("managementapp:manage_companies")
    except Exception as e:
            messages.error(request, "Internal Server Error")
            print(e)
    return redirect("managementapp:manage_companies")
    