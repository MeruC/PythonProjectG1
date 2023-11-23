from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditForm, WorkHistoryForm
from django.shortcuts import render, redirect


#retrieve current user data
def get_user_data(request):
    return {
        "email": request.user.email,
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "profile_summary": request.user.profile_summary
    }
    
@login_required(login_url="login")
def index(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)  # instance of the current user
        work_history_form = WorkHistoryForm(request.POST)  # Pass request.POST here, not just request
        if form.is_valid():  # checking if there's an error
            try:
                form.save()  # update the data of the current user
                messages.success(request, 'Profile updated successfully.')
                return redirect('index')  # direct only to the profile again
            except Exception as e:
                messages.error(request, 'Profile update failed. An error occurred.')
        else:
            messages.error(request, 'Profile update failed. Please check the form.')

    else:
        form = EditForm(instance=request.user)
        work_history_form = WorkHistoryForm()  # Create a blank instance for rendering in the template

    # data of the current user to be displayed on the profile section
    template = "profile.html"
    user_data = get_user_data(request)
    context = {"user_data": user_data, "form": form, "work_form": work_history_form}
    
    return render(request, template, context)



def addWorkExp(request):
    if request.method == 'POST':
        work_history_form = WorkHistoryForm(request.POST)  # Pass request.POST here, not just request
        
        if work_history_form.is_valid():
            try:
                
                #work history form data field
                start_month = request.POST.get('started_month')
                start_year = request.POST.get('started_year')
                start_date = f"{start_month}, {start_year}"

                end_month = request.POST.get('end_month')
                end_year = request.POST.get('end_year')
                end_date = f"{end_month}, {end_year}"
                position = request.POST.get('position')
                
                #add new data to the database
                work_experience = work_history_form.save(commit=False)
                work_experience.start_date = start_date
                work_experience.position = position
                work_experience.end_date = end_date
                work_experience.user = request.user
                
                work_experience.save() #add the new work experience
                
                messages.success(request, 'Work experience added successfully.')
                return redirect('index')
            except Exception as e:
                 messages.error(request, 'Profile update failed. An error occurred.')
                 
    else:
        work_history_form = WorkHistoryForm()  # Create a blank instance for rendering in the template
        
        
    # data of the current user to be displayed on the profile section
    user_data = get_user_data(request)
    template = "profile.html"
    context = {"user_data": user_data, "work_form": work_history_form}
    return render(request, template, context)
