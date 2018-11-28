""" Rest views for the help page
"""
import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import core_website_app.components.help.api as help_api
from core_main_app.components.web_page.models import WebPage, WEB_PAGE_TYPES
from core_main_app.utils.decorators import api_staff_member_required
from core_website_app.rest.serializers import WebPageSerializer

logger = logging.getLogger("core_website_app.rest.help.views")


def get():
    """ Get the help page

    Returns:

        - code: 200
          content: Help page
        - code: 400
          content: Validation error
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
    """ Create the help page

    Parameters:
    
        {
            "content": "new_content"
        }

    Returns:

        - code: 200
          content: Help page
        - code: 400
          content: Validation error
    """
    try:
        # Get parameters
        help_content = request.DATA['content']
        help_page = help_api.get()

        if help_page is None:
            help_page = WebPage(WEB_PAGE_TYPES["help"], help_content)
        else:
            help_page.content = help_content

        try:
            help_page = help_api.upsert(help_page)

            # Serialize the request
            serializer = WebPageSerializer(help_page.content)

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
    """ Help redirect to POST or GET methods

    Args:

        request: HTTP request

    Returns:

        Response object
    """
    if request.method == 'GET':
        return get()
    elif request.method == 'POST':
        return post(request)
