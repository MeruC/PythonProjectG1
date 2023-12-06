from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .forms import ProfileForm
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
