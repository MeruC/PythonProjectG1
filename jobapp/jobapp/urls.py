from django.contrib import admin
from django.urls import path, include
from apps.accountapp import urls as account_urls
from apps.core import urls as core_urls
from apps.jobsapp import urls as jobs_urls
from apps.management import urls as management_urls
from apps.profileapp import urls as profile_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account_urls)),
    path('core/', include(core_urls)),
    path('job/', include(jobs_urls)),
    path('management/', include(management_urls)),
    path('profile/', include(profile_urls)),
]
