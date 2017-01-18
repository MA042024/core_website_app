""" rest api for the terms of use
"""
from core_main_app.utils.decorators import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from core_website_app.components.web_page.models import WebPage, WEB_PAGE_TYPES
import core_website_app.components.terms_of_use.api as terms_of_use_api
from core_website_app.rest.serializers import WebPageSerializer

import logging
logger = logging.getLogger("core_website_app.rest.terms_of_use.views")


def get():
    """
    Get the terms of use
    :return:
    """
    help_page = terms_of_use_api.get()
    serializer = WebPageSerializer(help_page)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def post(request):
    """
    Post the terms of use
    :param request:
    :return:
    """
    try:
        # Get parameters
        terms_of_use_content = request.DATA['content']
        terms_of_use_page = terms_of_use_api.get()

        if terms_of_use_page is None:
            terms_of_use_page = WebPage(WEB_PAGE_TYPES["privacy_policy"], terms_of_use_content)
        else:
            terms_of_use_page.content = terms_of_use_content

        try:
            terms_of_use_page = terms_of_use_api.upsert(terms_of_use_page)

            # Serialize the request
            serializer = WebPageSerializer(terms_of_use_page.content)

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
def terms_of_use(request):
    """
    Terms of Use
    :param request:
    :return:
    """
    if request.method == 'GET':
        return get()
    elif request.method == 'POST':
        return post(request)
