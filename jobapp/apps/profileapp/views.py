import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from .forms import EditForm, WorkHistoryForm, EducationForm, PasswordForm, SkillForm
from django.shortcuts import get_object_or_404, render, redirect
from apps.jobsapp.models import WorkExperience
from apps.accountapp.models import Education, User
from django.core.exceptions import ValidationError
from ..accountapp.views import hasUnreadNotif
from django.contrib.auth import logout

#retrieve current user data
def get_user_data(request):
    return {
        "email": request.user.email,
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "profile_summary": request.user.profile_summary,
        "profile_img": request.user.profile_img,
        "skills":formatted_skill(request.user.skills)
    }
   
# retrieve all the work experience of user
def get_user_work_experience(request):
    user = request.user.id
    work_experience = WorkExperience.objects.filter(user=user)
    return work_experience


#retrieve all the education
def get_user_education(request):
    user = request.user.id
    education = Education.objects.filter(user=user)
    return education

@login_required(login_url="login")
def index(request):
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES ,instance=request.user)  # instance of the current user
        work_history_form = WorkHistoryForm(request.POST)  # Pass request.POST here, not just request
        education_form = EducationForm(request.POST)
        password_form = PasswordForm(request.POST)
        skill_form = SkillForm(request.POST)
        if form.is_valid():  # checking if there's an error
            try:
                form.save()  # update the data of the current user     
                messages.success(request, 'Profile updated successfully.')
                return redirect('profileapp:index')  # direct only to the profile again
            except Exception as e:
                messages.error(request, 'Profile update failed. An error occurred.')
        else:
            messages.error(request, 'Profile update failed. Please check the form.')

    else:
        form = EditForm(instance=request.user)
        work_history_form = WorkHistoryForm()  # Create a blank instance for rendering in the template
        education_form = EducationForm()
        password_form = PasswordForm()
        skill_form = SkillForm()

    # data of the current user to be displayed on the profile section
    template = "profile.html"
    user_data = get_user_data(request)
    work_experiences = get_user_work_experience(request)
    education = get_user_education(request)

    context = {
        "user_data": user_data, 
        "form": form, 
        "work_form": work_history_form,
        "work_experiences": work_experiences,
        "education":education_form,
        "education_data":education,
        "password_form":password_form,
        "skill_form":skill_form,
        "hasUnreadNotif":hasUnreadNotif(request)
        }
    
    return render(request, template, context)
  

#user skill
def formatted_skill(skills):
    # separate each skill
    skills_arr = skills.split(',')
    return skills_arr
def retrieveEducation(request, id):
    education = Education.objects.filter(id=id).values()
    education_list = list(education)
    return JsonResponse({'status':200,'data':education_list}, safe=False)
    
def addWorkExp(request):
    if request.method == 'POST':
        work_history_form = WorkHistoryForm(request.POST)  # Pass request.POST here, not just request
        
        if work_history_form.is_valid():
            try:
                
                #work history form data field
                start_month = request.POST.get('started_month')
                start_year = request.POST.get('started_year')
                start_date = f"{start_month}, {start_year}"

                is_present = request.POST.get('present')
                    
                end_month = request.POST.get('end_month')
                end_year = request.POST.get('end_year')
                end_date = f"{end_month}, {end_year}"
                position = request.POST.get('position')
                company_name = request.POST.get('company_name')
                
                #add new data to the database
                work_experience = work_history_form.save(commit=False)
                #check if the present is clicked
                work_experience.end_date = "Present" if is_present else end_date
                work_experience.start_date = start_date
                work_experience.position = position
                work_experience.user = request.user
                work_experience.company_name = company_name
                work_experience.save() #add the new work experience
                
                messages.success(request, 'Work experience added successfully.')
                return redirect('profileapp:index')
            except ValidationError as e:
                 messages.error(request, 'Profile update failed. An error occurred.')
                 print(e)
                 
    else:
        work_history_form = WorkHistoryForm()  # Create a blank instance for rendering in the template
        
        
    # data of the current user to be displayed on the profile section
    user_data = get_user_data(request)
    template = "profile.html"
    context = {"user_data": user_data, "work_form": work_history_form}
    return render(request, template, context)

def addEducation(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)  # instance of the current user
        work_history_form = WorkHistoryForm(request.POST)  # Pass request.POST here, not just request
        education_form = EducationForm(request.POST)
        
        if education_form.is_valid():
            try:
                #add new record of education
                new_education = education_form.save(commit=False)
                new_education.user = request.user
                new_education.save()

                messages.success(request, 'Education added successfully.')
                return redirect('profileapp:index')  # Redirect to the profile again
            except Exception as e:
                messages.error(request,'Education update failed')
            
    user_data = get_user_data(request)
    template = 'profile.html'
    work_experiences = get_user_work_experience(request)
    context = {
        "user_data": user_data, 
        "form": form, 
        "work_form": work_history_form,
        "work_experiences": work_experiences,
        "education":education_form,
        }
    
    return render(request,template,context)

def addSkill(request):
    
    if request.method == 'POST':
        current_skill = request.user.skills #skill of the user
        added_skill = request.POST.get('skills')    
        
        # concatenating the skills already available (if any) in the newly added skill
        new_skill = f"{current_skill},{added_skill}" if current_skill !="" else added_skill
        
        User.objects.filter(username = request.user.username).update(skills=new_skill)# update skill data
    return redirect('profileapp:index')


def updatePassword(request, id):
    if(request.method == 'POST'):
        user = get_object_or_404(User,id=id)
        
        try:
            # load body to get the data sent
            data = json.loads(request.body)
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            user_auth = authenticate(request, username=user.username, password=current_password)
            
            
            # check current password for validation
            if user_auth is not None:
                user.set_password(new_password)
                user.save()
                return JsonResponse({'status':200,'message':'Successfully updated'})
            else : return JsonResponse({'status':200,'message':'Password unmatched'})
            
        except Exception: 
            return redirect('profileapp:index')  # Redirect to the profile again
        
    return redirect('profileapp:index')

def updateEducation(request,id):
    if(request.method == 'POST'):
        
        try:
            data = json.loads(request.body)
        
            educationlvl = data.get('educationlvl')
            school_name = data.get('school_name')
            course = data.get('course')
            started_year = data.get('started_year')
            ended_year = data.get('ended_year')
            
            # update the data 
            Education.objects.filter(id=id).update(
                education_level=educationlvl,
                school_name=school_name,
                course=course,
                started_year=started_year,
                ended_year=ended_year
                
            )
            return JsonResponse({'status':200,'message':'Successfully updated'})
        except Exception:
            pass
    
        
        return redirect('profileapp:index')
    
#deleting record

# ------ work deletion
def delete_work(request,id):
    del_work = get_object_or_404(WorkExperience, id=id)
    try:
        del_work.delete() #delete the selected data in the record
        messages.success(request,'Deletetion of work Success')
        return JsonResponse({'status':200,'message':'Success Deletion'})
    except Exception:
        messages.error(request,'Deletion of work failed')
        
    return redirect('profileapp:index')

# -----------education deletion
def delete_education(request,id):
    del_education = get_object_or_404(Education,id=id)
    try:
        del_education.delete() #delete education record
        messages.success(request,'Deletion of education success')
        return JsonResponse({'status':200,'message':'Success Deletion'})
    except Exception:
        messages.error(request,'Deletion of education failed')
        
    return redirect('profileapp:index')


# ===== Skill Deletion
def delete_skill(request,skill):
    current_ID = request.user.id
    user_skill = User.objects.get(id=current_ID)
    skills_arr = formatted_skill(user_skill.skills) # format the string into array
    
    skills_arr.remove(skill) # remove specific item in the list
    updated_skill = ",".join(skills_arr)
    
    User.objects.filter(id=current_ID).update(skills=updated_skill) #update the skill data
    return redirect('profileapp:index')


#===========Check if the newly added skill is already existing
def isSkillAvailable(request,skill):
    if request.method == 'POST':
        try:
            user_obj = User.objects.get(id=request.user.id)
            current_skill = formatted_skill(user_obj.skills) #format into list
            isAvailable = True if skill in current_skill else False
                
            return JsonResponse({'status':200,'isAvailable':isAvailable})
        except:
            messages.error(request,'Education update failed')
            return redirect('profileapp:index')
        
    
    return redirect('profileapp:index')


# deactivate account
def DeactivateAccount(request):
    if request.method == "POST":
        current_id = request.user.id
        User.objects.filter(id=current_id).update(is_deactivated = True)
        messages.success(request,"Account successfully deactivated")
        
        #direct logout
        logout(request)
        return redirect("accountapp:login")
    
    return redirect("profileapp:index")
