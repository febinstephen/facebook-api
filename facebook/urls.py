from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('applications.api.v1.urls')),
    url(r'^social-accounts/', include('allauth.urls')),
]
