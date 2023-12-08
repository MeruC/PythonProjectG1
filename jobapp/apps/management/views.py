from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login


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
