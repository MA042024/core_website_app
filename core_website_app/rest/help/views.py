""" rest views for the help page
################################################################################
#
# File Name: rest.py
# Application: core_website_app
# Components: help
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
"""
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from mgi.permissions import api_staff_member_required
from ..serializers import WebPageSerializer
from core_website_app.components.help.api import help_get as api_help_get, help_post as api_help_post

import logging
# logger = logging.getLogger("core_website_app.rest.help")


def help_get():
    """
    Get the help
    :return:
    """
    help_page = api_help_get()
    serializer = WebPageSerializer(help_page)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization fail'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def help_post(request):
    """
    Post the help
    :param request:
    :return:
    """
    try:
        # Get parameters
        help_content = request.DATA['content']
        try:
            help_page_content = api_help_post(help_content)

            # Serialize the request
            serializer = WebPageSerializer(help_page_content)

            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                content = {'message': 'Serialization fail'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        # logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def help(request):
    """
    Help
    :param request:
    :return:
    """
    if request.method == 'GET':
        return help_get()
    elif request.method == 'POST':
        return help_post(request)
