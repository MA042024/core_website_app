""" Url router for the main application
"""
from django.conf.urls import include, url
from .views.user import views as public_views

urlpatterns = [
    url(r'^request-new-account', public_views.request_new_account, name='request-new-account'),
    url(r'^contact', public_views.contact, name='contact'),
    url(r'^help', public_views.help, name='help'),
    url(r'^privacy-policy', public_views.privacy_policy, name='privacy-policy'),
    url(r'^terms-of-use', public_views.terms_of_use, name='terms-of-use'),

    url(r'^api/', include('core_website_app.rest.urls')),
]




