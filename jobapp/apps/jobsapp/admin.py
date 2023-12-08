from django.contrib import admin

# Register your models here.
from .models import Company, Job


admin.site.register(Company)
admin.site.register(Job)
# WorkExperience is registered on account.models
# admin.site.register(WorkExperience)
