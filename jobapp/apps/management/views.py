from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from apps.accountapp.models import Education
from apps.profileapp.models import JobApplication
from apps.jobsapp.models import WorkExperience, Job
from .forms import EducationForm, ProfileForm, WorkHistoryForm
from django.contrib import messages
from django.db.models import F


def index(request):
    return render(request, "management/dashboard.html")


def manage_users(request):
    User = get_user_model()
    normal_users = User.objects.filter(is_superuser=False)

    return render(
        request, "management/manage_users.html", {"users": normal_users}
    )


def get_work_api(request, id):
    work = get_object_or_404(WorkExperience, pk=id)
    # return json api,
    if work:
        data = {
            "id": work.id,
            "work_title": work.work_title,
            "company_name": work.company_name,
            "position": work.position,
            "start_date": work.start_date,
            "end_date": work.end_date,
        }
        return JsonResponse({"status": 200, "data": data}, safe=False)
    else:
        return JsonResponse({"status": 404, "data": {}}, safe=False)


def user_detail(request, id):
    User = get_user_model()
    user = get_object_or_404(User, pk=id)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect(
                    "managementapp:manage_users"
                )  # direct only to the profile again

            except Exception as e:
                messages.error(
                    request, f"Profile update failed. An error occurred. {e}"
                )
        else:
            messages.error(
                request,
                f"Profile update failed. Please check the form. {form.errors}",
            )
        return redirect("managementapp:user_detail", id=id)

    else:
        profileForm = ProfileForm(instance=user)

        return render(
            request,
            "management/user_detail/profile.html",
            {"user": user, "profileForm": profileForm},
        )


def qualifications(request, id):
    User = get_user_model()
    user = get_object_or_404(User, pk=id)
    forms = {
        "education": {"edit": edit_education, "delete": delete_education},
        "work": {"edit": edit_work, "delete": delete_work},
    }

    if request.method == "POST":
        print(request.POST)

        try:
            form_name = request.POST.get("form_name")
            if form_name == "education":
                education_id = request.POST.get("education_id")
                education = Education.objects.get(pk=education_id)
                action = request.POST.get("action")
                method_function = forms["education"][action]
                method_function(request, education)

            elif form_name == "work":
                print("I ran")
                work_id = request.POST.get("work_id")
                work = WorkExperience.objects.get(pk=work_id)
                action = request.POST.get("action")
                method_function = forms["work"][action]
                method_function(request, work)

            return redirect("managementapp:user_qualification", id=id)

        except Exception as e:
            messages.error(
                request, f"Education update failed. An error occurred. {e}"
            )
            return redirect("managementapp:user_qualification", id=id)

    education_form = EducationForm()
    work_experience = WorkHistoryForm()
    # get all the education of the user
    education_list = user.education_set.all()
    work_list = user.workexperience_set.all()
    return render(
        request,
        "management/user_detail/qualification.html",
        {
            "education_list": education_list,
            "work_list": work_list,
            "work_form": work_experience,
            "education_form": education_form,
            "user": user,
        },
    )


def delete_education(request, education):
    try:
        education.delete()
        messages.success(request, "Education deleted successfully.")
    except Exception as e:
        messages.error(
            request, f"Education delete failed. An error occurred. {e}"
        )


def edit_education(request, education):
    education_form = EducationForm(request.POST, instance=education)
    if education_form.is_valid():
        education_form.save()
        messages.success(request, "Education added successfully.")
    else:
        messages.error(
            request,
            "Education update failed. Please check the form."
            f" {education_form.errors}",
        )
        return redirect("managementapp:user_qualification", id=id)


def edit_work(request, work):
    work_form = WorkHistoryForm(request.POST, instance=work)
    if work_form.is_valid():
        work_form.save()
        messages.success(request, "work added successfully.")
    else:
        messages.error(
            request,
            f"work update failed. Please check the form. {work_form.errors}",
        )
        return redirect("managementapp:user_qualification", id=id)


def delete_work(request, work):
    try:
        work.delete()
        messages.success(request, "work deleted successfully.")
    except Exception as e:
        messages.error(request, f"work delete failed. An error occurred. {e}")


def action(request, id):
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        User = get_user_model()
        # get the user
        user = get_object_or_404(User, pk=user_id)
        if not user:
            messages.error(request, "User not found.")
            return redirect("managementapp:manage_users")

        if action == "change_password":
            new_password = request.POST.get("new_password")
            change_user_password(user, new_password)
            messages.success(request, "Password changed successfully.")
            return redirect("managementapp:user_actions", id=id)
        elif action == "deactivate":
            deactivate_user_account(user)
            messages.success(request, "User deactivated successfully.")
            return redirect("managementapp:user_actions", id=id)
        elif action == "activate":
            activate_user_account(user)
            messages.success(request, "User activated successfully.")
            return redirect("managementapp:user_actions", id=id)
    User = get_user_model()
    user = get_object_or_404(User, pk=id)

    return render(request, "management/user_detail/action.html", {"user": user})


def change_user_password(user, new_password):
    # change the password of the user
    user.set_password(new_password)
    user.save()

def activate_user_account(user):
    # activate the user
    user.is_active = True
    user.save()

def deactivate_user_account(user):
    # deactivate the user
    user.is_active = False
    user.save()


def history(request, id):
    # get all the recent applications of the user.
    application_list = JobApplication.objects.filter(user_id=id).values(
        "id",
        "status",
        "user_id",
        company_name=F("job__company__company_name"),
        date_posted=F("job__date_posted"),
    )

    print(application_list)

    return render(
        request,
        "management/user_detail/history.html",
        {"applications": application_list},
    )
