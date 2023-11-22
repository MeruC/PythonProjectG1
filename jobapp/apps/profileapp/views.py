from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditForm
from django.shortcuts import render, redirect

@login_required(login_url="login")
def index(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user) #instance of the current user
        if form.is_valid(): #checking if there's an error
            try:
                form.save() #update the data of the current user
                messages.success(request, 'Profile updated successfully.')
                return redirect('index') #direct only to the profile again
            except Exception as e:
                messages.error(request, 'Profile update failed. An error occurred.')
        else:
            messages.error(request, 'Profile update failed. Please check the form.')

    else:
        form = EditForm(instance=request.user)

    #data of the current user to be displayed on the profile section
    user_data = {
        "email": request.user.email,
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "profile_summary": request.user.profile_summary
    }

    return render(request, "profile.html", {"user_data": user_data, "form": form})
