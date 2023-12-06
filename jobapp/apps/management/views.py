from django.shortcuts import render


def index(request):
    return render(request, "management/dashboard.html")


def manage_users(request):
    return render(request, "management/manage_users.html")
