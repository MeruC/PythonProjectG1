from django.utils import timezone
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
from apps.jobsapp.models import WorkExperience
from apps.accountapp.models import Education, User
from fpdf import FPDF

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
                company_form = CompanyDataForm(request.POST)
                if company_form.is_valid():
                    #add company based on the current user
                    company_instance = company_form.save(commit=False)
                    company_instance.user = current_user
                    company_instance.save()
                return redirect('companyapp:companyJobList')
            else:
                #open create company page with form included
                company = CompanyDataForm()
                context = {
                    "company":company
                }
                return render(request, "company/createCompany.html",context)
    
    return redirect('companyapp:companyJobList')
    

@login_required(login_url='/account/login/')
def companyProfile(request,company_id):
    try:
        company= Company.objects.get(id=company_id)
        
        if (company.user != request.user):
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
    
    user = request.user
    
    template = "company/companyJobList.html"
    context = {
        "job_list": job_list,
        "user": user,
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
        # Redirect to the current page with an error message
        messages.error(request, 'Invalid action')
        return redirect(request.META.get('HTTP_REFERER', 'companyapp:companyApplicants'))

    # Get the current user (assuming the user is authenticated)
    user = request.user

    # Update the status based on the action
    if action == 'check':
        applicant.status = 'approved'
        alert_message = 'Your application has been accepted for the job.'
        application_status = 'accepted'
    elif action == 'xmark':
        applicant.status = 'rejected'
        alert_message = 'Your application has been rejected for the job.'
        application_status = 'rejected'

    # Save the updated status
    applicant.save()

    # Create an alert notification
    alert = Alerts.objects.create(
        notification='ApplicationResult',
        message=alert_message,
        timestamp=timezone.now(),
        status='active',
        action_user=user.get_full_name(),
        user=applicant.user,
        job=applicant.job,
        application_status=application_status,
        is_read='unread',
    )

    # Redirect to the current page with a success message
    messages.success(request, 'Status updated successfully')
    return redirect(request.META.get('HTTP_REFERER', 'companyapp:companyApplicants'))

def resume(request, username):
    
    applicant = get_object_or_404(User, username=username)
    #VARIABLES
    userN = "_".join(applicant.last_name.split(" ")) + "_" + "_".join(applicant.first_name.split(" ")) + "_Resume"
    
    profile_img = applicant.profile_img
    first_name = applicant.first_name
    last_name = applicant.last_name
    email = applicant.email
    contact_no = applicant.contact_number
    profile_sum = applicant.profile_summary
    
    #GETS EVERY WORK EXPERIENCE
    work_experiences = WorkExperience.objects.filter(user=applicant)
    if(work_experiences):
        last_work = work_experiences[len(work_experiences)-1]
    
    #GETS EVERY EDUCATION
    education = Education.objects.filter(user=applicant)
    last_education = education[len(education)-1]
    
    skills = ', '.join(i for i in request.user.skills.split(','))
    
    #CREATES PDF
    pdf = FPDF('P', 'mm', 'A4')
    
    pdf.set_title(last_name + ", " + first_name + " Resume")
    pdf.set_author("WorkIt Job Portal")
    
    #HANDLES PAGE BREAKS
    pdf.set_auto_page_break(auto=True, margin= 15)
    #ADD PAGE
    pdf.add_page()
    
    ###HEADER
    #PROFILE PICTURE
    pdf.set_fill_color(56, 102, 65)
    pdf.rect(0,0,210,40,style="F")
    pdf.image(profile_img, 170, 8, 25)
    
    #NAME
    pdf.set_font("helvetica", "", 24)
    pdf.set_text_color(230,230,230)
    pdf.cell(0, 4, "", border=False, ln=1, align='L')
    pdf.cell(0, 7, first_name + " " + last_name, border=False, ln=1, align='L')
    
    #EMAIL
    pdf.set_text_color(180,180,180)
    pdf.set_font("helvetica", "", 14)
    pdf.cell(0, 7, email, ln=1, align='L')
    
    #PHONE NUMBER
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 4, "+63" + contact_no, ln=1, align='L')
    pdf.ln(20)
    
    ###PROFILE SUMMARY
    #TITLE
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(97,178,113)
    pdf.cell(0, 5, "Profile Summary", ln=True)

    #Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)

    ##SUMMARY CONTENT
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5, "\t\t\t\t\t\t\t\t\t" + profile_sum, align="J")

    ###WORK EXPERIENCE
    #TITLE
    pdf.cell(1,48,"")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(97,178,113)
    pdf.cell(0, 5, "Work Experience", ln=True)

    #Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)
    
    if (work_experiences):
        for work in work_experiences:
            #WORK TITLE
            pdf.cell(1,48,"")
            pdf.set_font('helvetica', '', 18)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 8, work.work_title, ln=True)
            
            #COMPANY NAME
            pdf.cell(10, 8, "")
            pdf.set_font('helvetica', '', 14)
            pdf.set_text_color(97,178,113)
            company_width = pdf.get_string_width(work.company_name)
            pdf.cell(company_width+1, 8, work.company_name)
            
            #DIVIDER
            pdf.set_font('helvetica', '', 12)
            pdf.set_text_color(75, 75, 75)
            pdf.cell(4, 8, "\t|\t")
            
            #START AND END DATES
            pdf.set_font('helvetica', '', 8)
            date = work.start_date + " to " + work.end_date
            pdf.cell(40, 9, date, ln=True)
            
            #JOB SUMMARY
            pdf.set_font('helvetica', '', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 5, "\t\t\t\t\t\t\t\t\t" + work.job_summary, align="J", ln=True)
            pdf.set_text_color(50, 50, 50)
            
            #MINI LINE BREAK
            if (work != last_work):
                pdf.cell(0, 8, "--------------------------------------------------------------------------------------------------------------------------------------", ln=True, align="C")
    else:
        pdf.cell(1,48,"")
        pdf.set_font('helvetica', '', 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "NO WORK EXPERIENCE", ln=True)
                
    ###EDUCATION
    #TITLE
    pdf.cell(1,48,"")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(97,178,113)
    pdf.cell(0, 5, "Education", ln=True)

    #Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)
    
    for edu in education:
        #SCHOOL NAME
        pdf.cell(1,48,"")
        pdf.set_font('helvetica', '', 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(100, 8, edu.school_name, ln=True)
        
        #EDUCATION LEVEL
        pdf.cell(10, 8, "")
        pdf.set_font('helvetica', '', 14)
        pdf.set_text_color(97,178,113)
        level_width = pdf.get_string_width(edu.get_education_level_display())
        pdf.cell(level_width+1, 8, edu.get_education_level_display())
        
        #DIVIDER
        pdf.set_font('helvetica', '', 12)
        pdf.set_text_color(75, 75, 75)
        pdf.cell(4, 8, "\t|\t")
        
        #START AND END DATES
        pdf.set_font('helvetica', '', 8)
        date = str(edu.started_year) + " to " + str(edu.ended_year)
        pdf.cell(40, 9, date, ln=True)
        
        #COURSE
        pdf.set_text_color(0,0,0)
        pdf.set_font('helvetica', '', 12)
        pdf.cell(10, 4, "")
        pdf.cell(40, 4, edu.course, ln=True)
        pdf.set_text_color(50, 50, 50)
        
        #MINI LINE BREAK
        if (edu != last_education):
            pdf.cell(0, 8, "--------------------------------------------------------------------------------------------------------------------------------------", ln=True, align="C")

    ###SKILLS
    pdf.cell(1, 30, "")
    pdf.cell(0, 8, "", ln=True)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(97,178,113)
    pdf.cell(0, 5, "Skills", ln=True)

    #Line Break
    pdf.cell(0, 4, "", ln=True)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(190, 0.5, "", ln=True, fill=True)
    pdf.cell(0, 4, "", ln=True)
    
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5, "\t\t\t\t\t\t\t\t\t\t" +  skills, align="J")
    
    #OUTPUT
    response = HttpResponse(bytes(pdf.output()), content_type="application/pdf", headers={"Content-Disposition": "inline; filename="+userN+".pdf"})
    if request.method == 'POST':
        return response
    else:
        return render(request, "accessDenied.html")
        

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