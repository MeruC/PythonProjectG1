from django.shortcuts import redirect


class SuperuserRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # redirects if the user is not superuser
        if not request.user.is_superuser and request.path_info.startswith(
            "/management/"
        ):
            # Redirect non-superusers to login
            return redirect("accountapp:login")
        return self.get_response(request)
