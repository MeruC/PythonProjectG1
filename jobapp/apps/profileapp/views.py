from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
@login_required(login_url="login")
def Profile(
    request,
):
    if request.user.is_authenticated:
        print("user_email", request.user.email)
        print("user_id", request.user.id)
        user_data = None

        user_data = {
            "email": request.user.email,
            "id": request.user.id,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

    return render(request, "profile.html", {"user_data": user_data})
