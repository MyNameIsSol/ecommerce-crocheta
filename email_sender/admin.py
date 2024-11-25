# email_sender/admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import EmailLog
from .views import send_email_view

# Register your models here.

class SendEmailAdmin(admin.ModelAdmin):
    change_list_template = "email_sender/send_email_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-email/', self.admin_site.admin_view(send_email_view), name='send-email'),
        ]
        return custom_urls + urls

admin.site.register(EmailLog,SendEmailAdmin)

