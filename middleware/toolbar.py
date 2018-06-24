"""
.. module:: cms_plugins
   :synopsis: Edit Toolbar middleware
"""
from django import forms
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve
from django.utils.cache import add_never_cache_headers

from cms.toolbar.toolbar import CMSToolbar
from cms.toolbar.utils import get_toolbar_from_request
from cms.utils.conf import get_cms_setting
from cms.utils.compat.dj import MiddlewareMixin
from cms.utils.request_ip_resolvers import get_request_ip_resolver

GET_REQUEST_IP = get_request_ip_resolver()

class ToolbarMiddleware(MiddlewareMixin):
    """
    Middleware to set up CMS Toolbar.
    """

    @staticmethod
    def is_cms_request(request):
        """Determines using a varety of methods if the request should be shown a toolbar.
        Via configured source IPs, cookies, and url.
        """

        toolbar_hide = get_cms_setting('TOOLBAR_HIDE')
        internal_ips = get_cms_setting('INTERNAL_IPS')

        if internal_ips:
            client_ip = GET_REQUEST_IP(request)
            try:
                client_ip = forms.GenericIPAddressField().clean(client_ip)
            except ValidationError:
                return False
            else:
                if client_ip not in internal_ips:
                    return False

        if not toolbar_hide:
            return True

        match = resolve(request.path_info)
        if not match:
            return False

        return match.url_name in ('pages-root', 'pages-details-by-slug')

    def process_request(self, request):
        """
        If we should show the toolbar for this request, put it on
        request.toolbar. Then call the request_hook on the toolbar.
        """

        # if user has no permissions, stop wasting cpu time
        if not request.user.get_all_permissions():
            return
        if not self.is_cms_request(request):
            return

        edit_on = get_cms_setting('CMS_TOOLBAR_URL__EDIT_ON')
        edit_off = get_cms_setting('CMS_TOOLBAR_URL__EDIT_OFF')
        disable = get_cms_setting('CMS_TOOLBAR_URL__DISABLE')
        anonymous_on = get_cms_setting('TOOLBAR_ANONYMOUS_ON')
        edit_enabled = edit_on in request.GET and 'preview' not in request.GET
        edit_disabled = edit_off in request.GET or 'preview' in request.GET

        if request.session.get('cms_toolbar_disabled', None) is None:
            request.session['cms_toolbar_disabled'] = True

        if disable in request.GET:
            request.session['cms_toolbar_disabled'] = True

        if edit_enabled:
            # If we actively enter edit mode, we should show the toolbar in any case
            request.session['cms_toolbar_disabled'] = False

        if request.session.get('cms_toolbar_disabled'):
            return

        toolbar_enabled = not request.session.get('cms_toolbar_disabled', False)
        can_see_toolbar = request.user.is_staff or (anonymous_on and request.user.is_anonymous())
        show_toolbar = (toolbar_enabled and can_see_toolbar)

        if edit_enabled and show_toolbar and not request.session.get('cms_edit'):
            # User has explicitly enabled mode
            # AND can see the toolbar
            request.session['cms_edit'] = True
            request.session['cms_preview'] = False

        if edit_disabled or not show_toolbar and request.session.get('cms_edit'):
            # User has explicitly disabled the toolbar
            # OR user has explicitly turned off edit mode
            # OR user can't see toolbar
            request.session['cms_edit'] = False

        if 'preview' in request.GET and not request.session.get('cms_preview'):
            # User has explicitly requested a preview of the live page.
            request.session['cms_preview'] = True

        if request.user.is_staff:
            try:
                request.cms_latest_entry = LogEntry.objects.filter(
                    user=request.user,
                    action_flag__in=(ADDITION, CHANGE)
                ).only('pk').order_by('-pk')[0].pk
            except IndexError:
                request.cms_latest_entry = -1
        request.toolbar = CMSToolbar(request)

    def process_response(self, request, response):
        """Modifies response on it's way out, mostly useless stuff, probably could chuck it"""

        if not self.is_cms_request(request):
            return response

        toolbar = get_toolbar_from_request(request)

        if toolbar:
            add_never_cache_headers(response)

        if hasattr(request, 'user') and request.user.is_staff and response.status_code != 500:
            try:
                if hasattr(request, 'cms_latest_entry'):
                    log_entries = LogEntry.objects.filter(
                        user=request.user,
                        action_flag__in=(ADDITION, CHANGE)
                    ).only('pk').order_by('-pk')[0].pk

                    if request.cms_latest_entry != log_entries:
                        request.session['cms_log_latest'] = log_entries
            # If there were no LogEntries, just don't touch the session.
            # Note that in the case of a user logging-in as another user,
            # request may have a cms_latest_entry attribute, but there are no
            # LogEntries for request.user.
            except IndexError:
                pass
        return response
