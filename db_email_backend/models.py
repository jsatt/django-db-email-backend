# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _


class Email(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation date"))
    subject = models.TextField(blank=True, verbose_name=_("Subject"))
    body = models.TextField(blank=True, verbose_name=_('Body'))
    content_subtype = models.CharField(max_length=254, verbose_name=_("content subtype"))
    from_email = models.CharField(max_length=254, blank=True, verbose_name=_('From'))
    to = models.TextField(blank=True, verbose_name=_('To'))
    cc = models.TextField(blank=True, verbose_name=_('CC'))
    bcc = models.TextField(blank=True, verbose_name=_('BCC'))
    headers = models.TextField(blank=True, verbose_name=_('Headers'))
    succeeded = models.BooleanField(default=True, verbose_name=_('Succeeded?'))
    error = models.TextField(blank=True, verbose_name=_('Errors'))

    def __str__(self):
        return '{} - {}, {}'.format(self.subject, self.to, self.create_date)

    class Meta:
        verbose_name = _('Email Log')
        verbose_name_plural = _('Emails Log')


class EmailAlternative(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='alternatives')
    content = models.TextField(blank=True)
    mimetype = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return '{}: alternative {}'.format(self.email, self.mimetype)


class EmailAttachment(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='attachments')
    filename = models.CharField(max_length=1000, blank=True)
    mimetype = models.CharField(max_length=254, blank=True)
    file = models.FileField(upload_to='db_email_backend')

    def __str__(self):
        return '{}: attachment {}'.format(self.email, self.filename)
