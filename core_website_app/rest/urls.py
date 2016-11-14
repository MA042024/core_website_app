""" Url router for the Rest API
"""
from django.conf.urls import url
from .help import views as help_rest_views
from .privacy_policy import views as privace_policy_rest_views
from .terms_of_use import views as term_of_use_rest_views
from .account_request import views as account_request_views
from .contact_message import views as contact_message_views

urlpatterns = [
    url(r'^user-requests$', account_request_views.get_all, name='request_list_rest_views'),
    url(r'^user-request$', account_request_views.get, name='request_rest_views'),
    url(r'^user-request/accept$', account_request_views.accept, name='request_accept_rest_views'),
    url(r'^user-request/deny$', account_request_views.deny, name='request_deny_rest_views'),

    url(r'^messages$', contact_message_views.get_all, name='message_list_rest_views'),
    url(r'^message$', contact_message_views.message, name='message_rest_views'),
    url(r'^message/delete$', contact_message_views.delete, name='message_delete_rest_views'),

    url(r'^help$', help_rest_views.rest_help_page, name='help_rest_view'),
    url(r'^privacy_policy$', privace_policy_rest_views.privacy_policy, name='privacy_policy_rest_view'),
    url(r'^terms_of_use$', term_of_use_rest_views.terms_of_use, name='terms_of_use_rest_views'),
]
