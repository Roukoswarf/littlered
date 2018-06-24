"""
.. module:: cms_apps
   :synopsis: Apphooks for attaching nanoms API functions to an arbitrary url
"""

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

@apphook_pool.register
class NanomsApphook(CMSApp):
    """Apphook to attach nanoms API"""
    name = _("nanoms API")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["nanoms.urls"]
