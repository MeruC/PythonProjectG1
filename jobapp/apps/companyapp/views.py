from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")
def createCompany(request):
    # TODO
    # - User must be logged in to create a company
    # - User must not have a company already
    return render(request, "company/createCompany.html")
def companyProfile(request):
    # TODO
    # - User must be logged in to view a company
    return render(request, "company/companyProfile.html")
