from django import template
from django.urls import reverse
from ...jobsapp.models import Company

register = template.Library()

@register.simple_tag
def navbar_link_url(user):
    has_company = Company.objects.filter(user=user).exists()

    create_company_url = reverse('companyapp:createCompany')
    my_company_url = reverse('companyapp:companyJobList')

    return my_company_url if has_company else create_company_url

@register.simple_tag
def navbar_content(user):
    has_company = Company.objects.filter(user=user).exists()
    
    company_name = "Recruit"
    company_img = None
    
    if has_company:
        company = Company.objects.filter(user=user).get()
        company_name = company.company_name
        company_img = company.logo

    context = {
        "company_name":company_name,
        "company_img":company_img,
    }

    
    return context