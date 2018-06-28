"""
.. module:: urls
   :synopsis: URL paths for main django-cms site.
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')
       ),
]

urlpatterns += [
    url(r'^passwordreset/$', auth_views.password_reset,
        {'post_reset_redirect': '/passwordreset/?email_sent=True'},
        name="password_reset"),
    url(r'^passwordreset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': '/login/?reset_success=True'},
        name="password_reset_confirm"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'login/loginpage.html'}, name='login'),
]

urlpatterns += [
    #url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    #url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^filer/', include('filer.urls')),
    url(r'^', include('filer.server.urls')),
    url(r'^', include('cms.urls')),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + staticfiles_urlpatterns() + urlpatterns
