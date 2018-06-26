"""
.. module:: urls
   :synopsis: URL routes for nanoms API functions.
"""

from django.conf.urls import url
from nanoms import views

urlpatterns = [
    url(r'things/$', views.things),
    url(r'add_building/$', views.add_building),
]
