from django.contrib import admin
from apps.accountapp.models import User, Education
from apps.jobsapp.models import WorkExperience
from django.contrib.auth.admin import UserAdmin
from apps.profileapp.models import JobSeeker

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_staff",
        "is_active",
        "profile_img",
        "contact_number",
    )
    list_filter = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                    "profile_summary",
                    "profile_img",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                    "profile_summary",
                    "profile_img",
                    "contact_number",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
    )
    ordering = (
        "email",
        "username",
    )

admin.site.register(User, CustomUserAdmin)

class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','work_title','position','start_date','end_date']
    
admin.site.register(WorkExperience,WorkHistoryAdmin)

class EducationAdmin(admin.ModelAdmin):
    list_display = ['user','education_level', 'school_name','course','started_year','ended_year']
    
admin.site.register(Education,EducationAdmin)


class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ['qualification','user','experience','skills']
    
admin.site.register(JobSeeker,JobSeekerAdmin)

