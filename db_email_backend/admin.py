# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.core.mail import EmailMessage
from django.test import override_settings
from django.utils.translation import gettext_lazy as _

from .models import Email, EmailAlternative, EmailAttachment


class EmailAlternativeInline(admin.StackedInline):
    model = EmailAlternative
    readonly_fields = ('mimetype', 'content')
    extra = 0
    max_num = 0
    can_delete = False


class EmailAttachmentInline(admin.StackedInline):
    model = EmailAttachment
    readonly_fields = ('filename', 'mimetype', 'file')
    extra = 0
    max_num = 0
    can_delete = False


class EmailAdmin(admin.ModelAdmin):
    fields = (
        ('from_email', 'create_date', 'content_subtype'),
        ('to', 'cc', 'bcc'),
        'subject', 'body', 'headers', 'succeeded', 'error')
    readonly_fields = (
        'create_date', 'from_email', 'to', 'cc', 'bcc', 'subject', 'body', 'content_subtype', 'headers', 'succeeded',
        'error')
    list_display = (
        'subject', 'to', 'from_email', 'create_date', 'attachment_count', 'alternative_count', 'succeeded', 'error')
    list_filter = ('succeeded', 'content_subtype',)
    date_hierarchy = 'create_date'
    search_fields = ('to', 'from_email', 'cc', 'bcc', 'subject', 'body')
    inlines = (EmailAlternativeInline, EmailAttachmentInline)

    actions = ['send_mail']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not self.has_change_permission(request):
            actions.pop('send_mail')
        return actions

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = list(fields)
            fields.remove('body')
        return fields

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def send_mail(self, request, queryset):
        for row in queryset:
            msg = EmailMessage()
            msg.subject = row.subject
            msg.body = row.body
            msg.content_subtype = row.content_subtype
            msg.from_email = row.from_email
            msg.to = [x for x in row.to.split('; ') if x]
            msg.cc = [x for x in row.cc.split('; ') if x]
            msg.bcc = [x for x in row.bcc.split('; ') if x]

            msg.send(fail_silently=False)

        self.message_user(request, f'{queryset.count()} Emails sent', 25)

    send_mail.short_description = _("Send Email")

    def attachment_count(self, instance):
        return instance.attachments.count()

    attachment_count.short_description = _('Attachments')

    def alternative_count(self, instance):
        return instance.alternatives.count()

    alternative_count.short_description = _('Alternatives')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Email, EmailAdmin)
