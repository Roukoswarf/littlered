from django.conf.urls import include, url

urlpatterns = [
    #url(r'^nanoms-api/', include('apps.nanoms.urls')),
    url(r'^', include('littlered.urls')),
]
