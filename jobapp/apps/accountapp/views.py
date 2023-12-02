from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

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
                "Registration successful. You can now login to your account.",
            )
            return redirect("accountapp:login")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form, "error": error})


# ------------------ Login ------------------
def Login(request):
    if request.user.is_authenticated:
        return redirect("jobsapp:index")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            user = User.objects.get(**{check_identifier(identifier): identifier})
            if user.is_active:
                login(request, user)
                return redirect("jobsapp:index")
            else:
                messages.error(request, "Your account has been disabled.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# ------------------ Logout ------------------
def Logout(request):
    logout(request)
    return redirect("accountapp:login")
