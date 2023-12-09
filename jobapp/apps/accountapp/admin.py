from django.contrib import admin
from apps.accountapp.models import User, Education,Alerts
from apps.jobsapp.models import WorkExperience
from django.contrib.auth.admin import UserAdmin

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
                    "skills",
                    "is_deactivated",
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
                    "skills",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
    )


admin.site.register(User, CustomUserAdmin)


class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "work_title", "position", "start_date", "end_date"]


admin.site.register(WorkExperience, WorkHistoryAdmin)


class EducationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "education_level",
        "school_name",
        "course",
        "started_year",
        "ended_year",
    ]
admin.site.register(Education, EducationAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'notification','timestamp','status','action_user',
            'user','application_status','is_read'
    ]
    
admin.site.register(Alerts,NotificationAdmin)
