""" rest api views
################################################################################
#
# File Name: rest.py
# Application: core_website_app
# Component: account_request
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
from mgi.permissions import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from core_website_app.components.account_request.api import \
    request_list as api_request_list, \
    request_post as api_request_post, \
    request_accept as api_request_accept, \
    request_deny as api_request_deny, \
    request_get as api_request_get
from ..serializers import RequestSerializer

# import logging
# logger = logging.getLogger("core_website_app.rest.account_request")


@api_view(['GET'])
@api_staff_member_required()
def request_list(request):
    """
    List all account requests
    :param request:
    :return:
    """
    requests = api_request_list()
    serializer = RequestSerializer(requests)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization fail'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def request_get(request):
    """
    Get an account request
    :param request:
    :return:
    """

    try:
        # Get parameters
        request_id = request.DATA['requestid']

        try:
            requests = api_request_get(request_id)
            serializer = RequestSerializer(requests)

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


def request_post(request):
    """
    Post a new account request
    :param request:
    :return:
    """
    try:
        # Get parameters
        request_username = request.DATA['username']
        request_first_name = request.DATA['firstname']
        request_last_name = request.DATA['lastname']
        request_password = request.DATA['password']
        request_email = request.DATA['email']

        try:
            # Create the request
            request_content = api_request_post(username=request_username,
                                               first_name=request_first_name,
                                               last_name=request_last_name,
                                               password=request_password,
                                               email=request_email)

            # Serialize the request
            serializer = RequestSerializer(request_content)

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
def request(request):
    """
    Account Request
    :param request:
    :return:
    """
    if request.method == 'GET':
        return request_get(request)
    elif request.method == 'POST':
        return request_post(request)


@api_view(['POST'])
def request_accept(request):
    """
    Accept an account request
    :param request:
    :return:
    """
    try:
        # Get parameters
        request_id = request.DATA['requestid']

        try:
            user_request = api_request_accept(request_id, send_mail=False)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the request
        serializer = RequestSerializer(user_request)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            content = {'message': 'Serialization fail'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        # logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_deny(request):
    """
    Deny an account request
    :param request:
    :return:
    """

    try:
        # Get parameters
        request_id = request.DATA['requestid']

        try:
            api_request_deny(request_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        # logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
