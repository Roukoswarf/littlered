"""
.. module:: cms_plugins
   :synopsis: Plugins for core django-cms, independent of other apps.
"""

from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.models import Text
from .models import AuthContent

@plugin_pool.register_plugin
class AuthContentPlugin(CMSPluginBase):
    """Uses data from :class:`brodasite.models.AuthContent` to create an cms plugin
    which can be toggled to show content only to authenticated user, or guests.
    """
    model = AuthContent
    name = _('Auth Content')
    render_template = 'cmsplugin_auth_content/content.html'
    cache = False
    allow_children = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class HtmlPlugin(CMSPluginBase):
    """Plugin which is functionally identical to the standard text module, but does
    not use the WYSIWYG editor in the frontend, and instead allows only raw HTML.
    """
    model = Text
    name = _("HTML")
    render_template = "html.html"

@plugin_pool.register_plugin
class LoginMenuPlugin(CMSPluginBase):
    """Plugin to display a login menu at any location on a cms page.
    """
    name = _("Login Menu")
    render_template = "login/loginmenu.html"
    cache = True
