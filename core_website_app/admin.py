""" Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url

from views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^user-requests$', admin_views.user_requests, name='user_requests'),
    url(r'^accept_request', admin_ajax.accept_request),
    url(r'^deny_request', admin_ajax.deny_request),
    url(r'^contact-messages$', admin_views.contact_messages, name='contact_messages'),
    url(r'^remove_message', admin_ajax.remove_message),
    url(r'^website$', admin_views.website, name='website'),
    url(r'^website/privacy-policy$', admin_views.privacy_policy_admin, name='privacy_policy_admin'),
    url(r'^website/terms-of-use$', admin_views.terms_of_use_admin, name='terms_of_use_admin'),
    url(r'^website/help$', admin_views.help_admin, name='help_admin'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls

