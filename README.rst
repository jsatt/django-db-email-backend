Django DB Email Backend
=======================

Record Email Messages Sent to database , with the ability to also send them via SMTP.


Usage
-----

Install ::

    pip install kn-django-db-email-backend

In settings.py::

    INSTALLED_APPS += ['db_email_backend']

    EMAIL_BACKEND = 'db_email_backend.backend.DBEmailBackend'
    # record the email message to database

    # OR
    EMAIL_BACKEND = 'db_email_backend.backend.SMTPDBEmailBackend'
    # Record to database and send via SMTP.
    # IF errors happened you can see it in the Admin and resend it again.

Migrate::

    $ python manage.py migrate


Configuration
=============

SMTP_EMAIL_FILTER_FUNCTION_PATH default to `db_email_backend.utils.smtp_filter_email_function`. a dotted path to the smtp email filter function.
A filter function for the smtp email, takes the email_message (django.core.mail.message.EmailMessage) as a parameter, and return False if this message should be filter out out and not sent via the backend.

Example::

    def only_allow_emails_to_mahad(message):
        return True if 'mahad@kuwaitnet.com' in message.to else False


DB_EMAIL_FILTER_FUNCTION_PATH default to `db_email_backend.utils.db_filter_email_function`. a dotted path to the db email filter function. same as the SMTP one but for the Database.

Example::

    def dont_record_error_emails(message):
        return False if settings.EMAIL_SUBJECT_PREFIX in message.subject else True

Admin
-----

Package have and admin integration ready where you can send the email SMTP even if the EMAIL_HOST = "db_email_backend.backend.DBEmailBackend"
