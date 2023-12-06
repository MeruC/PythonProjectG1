from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model


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

    return render(request, "management/user_detail.html", {"user": user})
