from django.contrib import admin
from apps.accountapp.models import User
from apps.jobsapp.models import WorkExperience
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User, UserAdmin)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_staff",
        "is_active",
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


class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','work_title','position','start_date','end_date']
    
admin.site.register(WorkExperience,WorkHistoryAdmin)