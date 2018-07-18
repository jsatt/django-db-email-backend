# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.test.utils import override_settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import django

from .models import Email


@override_settings(EMAIL_BACKEND='db_email_backend.backend.DBEmailBackend')
class DBEmailBackendTest(TestCase):
    def test_send_mail(self):
        self.assertEqual(Email.objects.count(), 0)

        send_mail('test mail', 'this is just a test', 'jim@bob.com',
                  ['frank@example.com', 'joe@test.com'])

        email = Email.objects.get()
        self.assertEqual(email.subject, 'test mail')
        self.assertEqual(email.body, 'this is just a test')
        self.assertEqual(email.content_subtype, 'plain')
        self.assertEqual(email.from_email, 'jim@bob.com')
        self.assertEqual(email.to, 'frank@example.com; joe@test.com')
        self.assertEqual(email.cc, '')
        self.assertEqual(email.bcc, '')
        self.assertEqual(email.headers, '')

        self.assertEqual(email.attachments.count(), 0)
        self.assertEqual(email.alternatives.count(), 0)

    def test_send_attachments(self):
        self.assertEqual(Email.objects.count(), 0)

        e = EmailMessage('test mail', 'this is just a test', 'jim@bob.com',
                         ['frank@example.com', 'joe@test.com'])
        e.attach_file('README.md')
        e.send()

        email = Email.objects.get()
        self.assertEqual(email.subject, 'test mail')
        self.assertEqual(email.body, 'this is just a test')
        self.assertEqual(email.content_subtype, 'plain')
        self.assertEqual(email.from_email, 'jim@bob.com')
        self.assertEqual(email.to, 'frank@example.com; joe@test.com')
        self.assertEqual(email.cc, '')
        self.assertEqual(email.bcc, '')
        self.assertEqual(email.headers, '')

        attachment = email.attachments.get()
        self.assertEqual(attachment.filename, 'README.md')
        with open('README.md') as f:
            self.assertEqual(attachment.file.read().decode('utf8'), f.read())
        if django.VERSION >= (1, 9):
            self.assertIn(attachment.mimetype, ('application/octet-stream', 'text/markdown'))
        else:
            self.assertEqual(attachment.mimetype, '')

        self.assertEqual(email.alternatives.count(), 0)

    def test_send_alternatives(self):
        self.assertEqual(Email.objects.count(), 0)

        e = EmailMultiAlternatives('test mail', 'this is just a test', 'jim@bob.com',
                                   ['frank@example.com', 'joe@test.com'])
        e.attach_alternative('<h1>Testing stuff</h1>', 'text/html')
        e.send()

        email = Email.objects.get()
        self.assertEqual(email.subject, 'test mail')
        self.assertEqual(email.body, 'this is just a test')
        self.assertEqual(email.content_subtype, 'plain')
        self.assertEqual(email.from_email, 'jim@bob.com')
        self.assertEqual(email.to, 'frank@example.com; joe@test.com')
        self.assertEqual(email.cc, '')
        self.assertEqual(email.bcc, '')
        self.assertEqual(email.headers, '')

        alternative = email.alternatives.get()
        self.assertEqual(alternative.mimetype, 'text/html')
        self.assertEqual(alternative.content, '<h1>Testing stuff</h1>')

        self.assertEqual(email.attachments.count(), 0)
