""" rest views for the help page
"""
from core_main_app.utils.permissions import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from core_website_app.rest.serializers import WebPageSerializer
import core_website_app.components.help.api as help_api

import logging
logger = logging.getLogger("core_website_app.rest.help.views")


def get():
    """
    Get the help
    :return:
    """
    help_page = help_api.get()
    serializer = WebPageSerializer(help_page)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def post(request):
    """
    Post the help
    :param request:
    :return:
    """
    try:
        # Get parameters
        help_content = request.DATA['content']
        try:
            help_page_content = help_api.save(help_content)

            # Serialize the request
            serializer = WebPageSerializer(help_page_content)

            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                content = {'message': 'Serialization failed'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def rest_help_page(request):
    """
    Help
    :param request:
    :return:
    """
    if request.method == 'GET':
        return get()
    elif request.method == 'POST':
        return post(request)
