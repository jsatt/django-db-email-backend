# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.files.base import ContentFile
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

from .models import Email, EmailAlternative, EmailAttachment
from .app_settings import email_filter, db_email_filter

logger = logging.getLogger('db_mail_backend')


def record_email_message(msg, fail_silently):
    try:
        email = Email.objects.create(
            subject=msg.subject,
            body=msg.body,
            content_subtype=msg.content_subtype,
            from_email=msg.from_email,
            to='; '.join(msg.to),
            cc='; '.join(msg.cc),
            bcc='; '.join(msg.bcc),
            headers='\n'.join('{}: {}'.format(k, v)
                              for k, v in msg.extra_headers.items()),
        )
        # output.append(email)

        alternatives = getattr(msg, 'alternatives', [])
        for content, mimetype in alternatives:
            EmailAlternative.objects.create(
                email=email,
                content=content,
                mimetype=mimetype or '',
            )

        for filename, content, mimetype in msg.attachments:
            attachment = EmailAttachment.objects.create(
                email=email,
                filename=filename,
                mimetype=mimetype or '',
            )
            attachment.file.save(filename, ContentFile(content))
    except:
        email = None
        if not fail_silently:
            raise

    return email


class DBEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for msg in email_messages:
            if db_email_filter(msg):
                return record_email_message(msg, fail_silently=self.fail_silently)
        return len(email_messages)


class SMTPDBEmailBackend(SMTPEmailBackend):
    """
    This backend is mixture between SMTP and DB mail backend
    It writes to the database then send the email over smtp,
    if any errors happen while sending it is reflected in the email model
    """

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return 0
        with self._lock:
            new_conn_created = self.open()
            if not self.connection or new_conn_created is None:
                # We failed silently on open().
                # Trying to send would be pointless.
                return 0
            num_sent = 0
            for message in email_messages:
                try:
                    if db_email_filter(message):
                        email_inst = record_email_message(message, fail_silently=self.fail_silently)
                except Exception as e:
                    logger.error(e)
                try:
                    if email_filter(message):
                        sent = self._send(message)
                        if sent:
                            num_sent += 1
                except Exception as e:
                    if email_inst:
                        Email.objects.filter(pk=email_inst.pk).update(error=str(e), succeeded=False)
                    raise e
            if new_conn_created:
                self.close()
        return num_sent
