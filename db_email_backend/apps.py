from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DBEmailBackendConfig(AppConfig):
    name = 'db_email_backend'
    verbose_name = _('Email Backend')
