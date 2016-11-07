""" rest api views
"""
from core_main_app.utils.permissions import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import core_website_app.components.account_request.api as account_request_api
from core_website_app.rest.serializers import RequestSerializer

import logging
logger = logging.getLogger("core_website_app.rest.account_request.views")


@api_view(['GET'])
@api_staff_member_required()
def get_all(request):
    """
    List all account requests
    :param request:
    :return:
    """
    requests = account_request_api.get_all()
    serializer = RequestSerializer(requests)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def get(request):
    """
    Get an account request
    :param request:
    :return:
    """

    try:
        # Get parameters
        request_id = request.DATA['requestid']

        try:
            requests = account_request_api.get(request_id)
            serializer = RequestSerializer(requests)

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


def post(request):
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
            request_content = account_request_api.save(request_username=request_username,
                                                       request_first_name=request_first_name,
                                                       request_last_name=request_last_name,
                                                       request_password=request_password,
                                                       request_email=request_email)

            # Serialize the request
            serializer = RequestSerializer(request_content)

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
def account_request(request):
    """
    Account Request
    :param request:
    :return:
    """
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)


@api_view(['POST'])
@api_staff_member_required()
def accept(request):
    """
    Accept an account request
    :param request:
    :return:
    """
    try:
        # Get parameters
        request_id = request.DATA['requestid']

        try:
            user_request = account_request_api.accept(request_id, send_mail=False)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the request
        serializer = RequestSerializer(user_request)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            content = {'message': 'Serialization failed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@api_staff_member_required()
def deny(request):
    """
    Deny an account request
    :param request:
    :return:
    """

    try:
        # Get parameters
        request_id = request.DATA['requestid']

        try:
            account_request_api.deny(request_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
