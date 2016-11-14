""" Url router for the main application
"""
from django.conf.urls import url, include
from views.user import views as public_views

urlpatterns = [
    url(r'^$', public_views.homepage, name='core_website_homepage'),
    url(r'^account-request', public_views.request_new_account, name='core_website_account_request'),
    url(r'^contact', public_views.contact, name='core_website_contact'),
    url(r'^help', public_views.help_page, name='core_website_help'),
    url(r'^privacy', public_views.privacy_policy, name='core_website_privacy'),
    url(r'^terms', public_views.terms_of_use, name='core_website_terms'),

    url(r'^login', public_views.custom_login, name='core_website_login'),
    url(r'^logout', public_views.custom_logout, name='core_website_logout'),

    url(r'^api/', include('core_website_app.rest.urls')),
]
