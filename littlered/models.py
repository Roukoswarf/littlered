"""
.. module:: models
   :synopsis: Models for supporting CMS framework additions.
"""

from django.db import models
from cms.models import CMSPlugin

class AuthContent(CMSPlugin):
    """Adds structure to support :class:`brodasite.cms_plugins.AuthContentPlugin`
    """

    state_choices = (
        (True, 'Authenticated'),
        (False, 'Unauthenticated'),
    )

    state = models.BooleanField("Visible When", choices=state_choices)

    def __str__(self):
        if self.state:
            msg = "Authenticated"
        else:
            msg = "Unauthenticated"
        return msg
