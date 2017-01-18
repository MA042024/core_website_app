""" rest api for the privacy policy
"""
from core_main_app.utils.decorators import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from core_website_app.components.web_page.models import WebPage, WEB_PAGE_TYPES
import core_website_app.components.privacy_policy.api as privacy_policy_api
from core_website_app.rest.serializers import WebPageSerializer

import logging
logger = logging.getLogger("core_website_app.rest.privacy_policy.views")


def get():
    """
    Get the privacy policy
    :return:
    """
    privacy_policy_page = privacy_policy_api.get()
    serializer = WebPageSerializer(privacy_policy_page)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def post(request):
    """
    Post the privacy policy
    :param request:
    :return:
    """
    try:
        # Get parameters
        privacy_policy_content = request.DATA['content']
        privacy_policy_page = privacy_policy_api.get()

        if privacy_policy_page is None:
            privacy_policy_page = WebPage(WEB_PAGE_TYPES["privacy_policy"], privacy_policy_content)
        else:
            privacy_policy_page.content = privacy_policy_content

        try:
            privacy_policy_page = privacy_policy_api.upsert(privacy_policy_page)

            # Serialize the request
            serializer = WebPageSerializer(privacy_policy_page.content)

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
def privacy_policy(request):
    """
    Privacy Policy
    :param request:
    :return:
    """
    if request.method == 'GET':
        return get()
    elif request.method == 'POST':
        return post(request)
