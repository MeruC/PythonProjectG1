from django.shortcuts import render

def handler404(request, exception):
    print(exception)
    return render(request, "errorPage.html")