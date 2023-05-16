from django.conf import settings
from django.utils.module_loading import import_string

SMTP_EMAIL_FILTER_FUNCTION_PATH = getattr(settings, 'SMTP_EMAIL_FILTER_FUNCTION_PATH',
                                          'db_email_backend.utils.smtp_filter_email_function')
DB_EMAIL_FILTER_FUNCTION_PATH = getattr(settings, 'SMTP_EMAIL_FILTER_FUNCTION_PATH',
                                          'db_email_backend.utils.db_filter_email_function')

try:
    email_filter = import_string(SMTP_EMAIL_FILTER_FUNCTION_PATH)
except Exception as e:
    raise e
try:
    db_email_filter = import_string(DB_EMAIL_FILTER_FUNCTION_PATH)
except Exception as e:
    raise e
