from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from apps.accountapp.models import Education
from .forms import EducationForm, ProfileForm
from django.contrib import messages


def index(request):
    return render(request, "management/dashboard.html")


def manage_users(request):
    User = get_user_model()
    normal_users = User.objects.filter(is_superuser=False)

    return render(
        request, "management/manage_users.html", {"users": normal_users}
    )


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


def qualifications(request, id):
    User = get_user_model()
    user = get_object_or_404(User, pk=id)

    if request.method == "POST":
        print(request.POST)
        education_id = request.POST.get("education_id")
        education = Education.objects.get(pk=education_id)
        try:
            action = request.POST.get("action")
            if action == "delete":
                delete_education(request, education)
            else:
                edit_education(request, education)

            return redirect("managementapp:user_qualification", id=id)

        except Exception as e:
            messages.error(
                request, f"Education update failed. An error occurred. {e}"
            )
            return redirect("managementapp:user_qualification", id=id)

    education_form = EducationForm(instance=user)
    # get all the education of the user
    education_list = user.education_set.all()
    return render(
        request,
        "management/user_detail/qualification.html",
        {"education_form": education_form, "education_list": education_list},
    )


def action(request, id):
    return render(request, "management/user_detail/action.html")


def history(request, id):
    return render(request, "management/user_detail/history.html")
