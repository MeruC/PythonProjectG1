from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import ActivityLog, Alerts
from django.contrib.auth import login, logout

from django.contrib import messages

from .forms import LoginForm, RegisterForm
from .utils import (
    check_identifier,
)

from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

User = get_user_model()


# ------------------ Register ------------------
def Register(request):
    error = {}

    if request.user.is_authenticated:
        return redirect("jobsapp:index")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        # check if all inputs are valid
        if form.is_valid():
            try:
                # check if username already exists
                new_user = User.objects.create_user(
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                new_user.save()

                # generate a success message when registration is successful
                messages.success(
                    request,
                    "Registration successful. You can now login to your"
                    " account.",
                )
                return redirect("accountapp:login")
            except Exception as e:
                # messages.error(
                # request,
                # "Internal Server Error.",)
                print("Internal Server Error", e)

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form, "error": error})


# ------------------ Login ------------------
def Login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("managementapp:index")
    elif request.user.is_authenticated:
        return redirect("jobsapp:index")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            user = User.objects.get(
                **{check_identifier(identifier): identifier}
            )
            if not user.is_deactivated:
                login(request, user)
                ActivityLog.objects.create(
                    user=user, action="Sign in", timestamp=timezone.now()
                )
                if user.is_superuser:  # user is an admin
                    return redirect("managementapp:index")
                return redirect("jobsapp:index")
            else:
                messages.error(request, "Your account has been disabled.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def index(request):
    return redirect("accountapp:login")


# ------------------ Logout ------------------
def Logout(request):
    ActivityLog.objects.create(
        user=request.user, action="Sign out", timestamp=timezone.now()
    )
    logout(request)
    return redirect("accountapp:login")


# ----------------- notification -----------
MAX_LIMIT = 20


def Notification(request, offset):
    user_id = request.user.id  # current user

    # offset with max to 20 notif
    limit = offset + MAX_LIMIT
    notifications = (
        Alerts.objects.filter(user_id=user_id)
        .order_by("-timestamp")[offset:limit]
        .values()
    )
    notification_list = list(notifications)
    return JsonResponse(notification_list, safe=False)


# ------------------ check user notification unread ---------
def hasUnreadNotif(request):
    # check for unread notification
    query = Alerts.objects.filter(user=request.user, is_read="unread").count()

    hasUnread = query > 0  # check if it has unread
    return hasUnread
