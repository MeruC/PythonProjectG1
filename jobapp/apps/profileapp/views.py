from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse("Hello profile app")
