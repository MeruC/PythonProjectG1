from django.shortcuts import render


def index(request):
    return render(request, "index/base.html")


def applyNow(request):
    return render(request, "index/base.html")


def searchJob(request):
    return render(request, "index/base.html")


def jobDetails(request):
    return render(request, "index/base.html")
