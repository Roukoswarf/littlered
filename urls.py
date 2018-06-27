from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('littlered.urls')),
    url(r'^nanoms-api/', include('apps.nanoms.urls')),
]
