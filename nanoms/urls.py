"""
.. module:: urls
   :synopsis: URL routes for nanoms API functions.
"""

from django.conf.urls import url
from nanoms.views import things

urlpatterns = [
    url(r'things/$', things),
]
