""" rest api for the privacy policy
################################################################################
#
# File Name: views.py
# Application: api
# Purpose:
#
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
"""

# API
from core_main_app.utils.permissions import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# Models
from core_website_app.components.privacy_policy.api import \
    privacy_policy_get as api_privacy_policy_get, \
    privacy_policy_post as api_privacy_policy_post
# Serializers
from ..serializers import WebPageSerializer

import logging
# logger = logging.getLogger("core_website_app.rest.privacy_policy")


def privacy_policy_get():
    """
    Get the privacy policy
    :return:
    """
    privacy_policy_page = api_privacy_policy_get()
    serializer = WebPageSerializer(privacy_policy_page)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def privacy_policy(request):
    """
    Post the privacy policy
    :param request:
    :return:
    """
    try:
        # Get parameters
        privacy_policy_content = request.DATA['content']
        try:
            privacy_policy_page_content = api_privacy_policy_post(privacy_policy_content)

            # Serialize the request
            serializer = WebPageSerializer(privacy_policy_page_content)

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
        # logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def privacy_policy(request):
    """
    Privacy Policy
    :param request:
    :return:
    """
    if request.method == 'GET':
        return privacy_policy(request)
    elif request.method == 'POST':
        return privacy_policy(request)
