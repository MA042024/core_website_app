""" Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^login', RedirectView.as_view(url=reverse_lazy("core_website_login"))),

    url(r'^user-requests$', admin_views.user_requests, name='user_requests'),
    url(r'^accept_request', admin_ajax.accept_request),
    url(r'^deny_request', admin_ajax.deny_request),
    url(r'^contact-messages$', admin_views.contact_messages, name='contact_messages'),
    url(r'^remove_message', admin_ajax.remove_message),

    url(r'^website/privacy-policy$', admin_views.privacy_policy_admin, name='core_website_app_privacy'),
    url(r'^website/terms-of-use$', admin_views.terms_of_use_admin, name='core_website_app_terms'),
    url(r'^website/help$', admin_views.help_admin, name='core_website_app_help'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls

