
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return HttpResponse("Hello profile app")

# redirect the user to login page if not logged-in
@login_required(login_url="login")
def Profile(
    request,
):
    # Check if the user is logged-in
    if request.user.is_authenticated:
        # access logged-in user data using request.user.field_from_db
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

