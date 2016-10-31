""" Ajax views for the admin part
"""
from django.http import HttpResponse
import json

from core_main_app.commons.exceptions import MDCSError
from core_website_app.components.account_request.api import request_accept, request_deny
from core_website_app.components.contact_message.api import message_delete
from django.utils.importlib import import_module
import os
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MDCS_URI = settings.MDCS_URI


def accept_request(request):
    """
    Accepts a request and creates the user account
    :param request:
    :return:
    """
    try:
        request_id = request.POST['requestid']
        user = request_accept(request_id)

        message = "Request Accepted"
    except MDCSError as error:
        message = error.message
    except Exception as exception:
        message = exception.message

    return HttpResponse(json.dumps({"message": message}), content_type='application/json')


def deny_request(request):
    """
    Denies an account request
    :param request:
    :return:
    """

    try:
        request.DATA = request.POST
        request_id = request.POST['requestid']
        request_deny(request_id)
        message = "Request denied"
    except MDCSError as error:
        message = error.message
    except Exception as exception:
        message = exception.message

    return HttpResponse(json.dumps({"message": message}), content_type='application/json')


def remove_message(request):
    """
    Remove a message from the list of messages
    :param request:
    :return:
    """

    try:
        request.DATA = request.POST
        message_id = request.POST['messageid']
        message_delete(message_id)
        message = "Message deleted"
    except MDCSError as error:
        message = error.message
    except Exception as exception:
        message = exception.message

    return HttpResponse(json.dumps({"message": message}), content_type='application/json')
