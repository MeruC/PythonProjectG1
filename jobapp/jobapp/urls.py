from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from apps.accountapp import urls as account_urls
#from apps.core import urls as core_urls
from apps.jobsapp import urls as jobs_urls
from apps.management import urls as management_urls
from apps.profileapp import urls as profile_urls
from apps.companyapp import urls as company_urls
from django.conf.urls.static import static
from django.views.static import serve 

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    path("admin/", admin.site.urls),
    # homepage
    path("", include((jobs_urls), namespace='home')),
    path("account/", include(account_urls)),
    #path("core/", include(core_urls)),
    path("job/", include((jobs_urls), namespace='job')),
    path("management/", include(management_urls)),
    path("profile/", include(profile_urls)),
    path("company/", include(company_urls)),
    # EXTRAS / LIB
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'jobapp.views.handler404'