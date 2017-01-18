""" rest api views
"""
from core_main_app.utils.decorators import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import core_website_app.components.account_request.api as account_request_api
from core_website_app.components.account_request.models import AccountRequest
from core_website_app.rest.serializers import AccountRequestSerializer

import logging
logger = logging.getLogger("core_website_app.rest.account_request.views")


@api_view(['GET'])
@api_staff_member_required()
def get_all(request):
    """
        List all account requests

        Parameters:
            request (HttpRequest): request

        Returns:
            Response object
    """
    requests = account_request_api.get_all()
    serializer = AccountRequestSerializer(requests)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def get(request):
    """
        Get an account request

        Parameters:
            request (HttpRequest): request

        Returns:
            Response object
    """
    try:
        # Get parameters
        account_request_id = request.DATA['request_id']
        try:
            requests = account_request_api.get(account_request_id)
            serializer = AccountRequestSerializer(requests)

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

        Parameters:
            request (HttpRequest): request

        Returns:
            Response object
    """
    try:
        # Get parameters
        username = request.DATA['username']
        first_name = request.DATA['firstname']
        last_name = request.DATA['lastname']
        password = request.DATA['password']
        email = request.DATA['email']

        account_request_from_request = AccountRequest(username,
                                                      first_name,
                                                      last_name,
                                                      password,
                                                      email)
        try:
            # Create the request
            request_content = account_request_api.insert(account_request_from_request)
            # Serialize the request
            serializer = AccountRequestSerializer(request_content)
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
        Account request redirect to POST or GET methods

        Parameters:
            request (HttpRequest): request

        Returns:
            Response object
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

        Parameters:
            request (HttpRequest): request

        Returns:
            Response object
    """
    try:
        # Get parameters
        request_id = request.DATA['requestid']
        account_request_from_api = account_request_api.get(request_id)
        try:
            user_request = account_request_api.accept(account_request_from_api, send_mail=False)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the request
        serializer = AccountRequestSerializer(user_request)

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

        Parameters:
            request (HttpRequest): request

        Returns:
            Response object
    """
    try:
        # Get parameters
        request_id = request.DATA['requestid']
        account_request_from_api = account_request_api.get(request_id)
        try:
            account_request_api.deny(account_request_from_api)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
