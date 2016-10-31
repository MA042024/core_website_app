""" rest views for the contact message API

# File Name: rest.py
# Application: core_website_app
# Component: contact_message
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
"""

# API
from core_main_app.utils.permissions import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# Permissions
# Models
from core_website_app.components.contact_message.api import \
    message_list as api_message_list, \
    message_delete as api_message_delete, \
    message_get as api_message_get, \
    message_post as api_message_post
# Serializers
from ..serializers import MessageSerializer

# import logging
# logger = logging.getLogger("core_website_app.rest.contact_message")


@api_view(['GET'])
@api_staff_member_required()
def message_list(request):
    """
    List all messages
    :param request:
    :return:
    """
    messages = api_message_list()
    serializer = MessageSerializer(messages)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def message_get(request):
    """
    Get a message
    :param request:
    :return:
    """
    try:
        # Get parameters
        message_id = request.DATA['requestid']

        try:
            messages = api_message_get(message_id)
            serializer = MessageSerializer(messages)

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


def message_post(request):
    """
    Post a message
    :param request:
    :return:
    """
    try:
        # Get parameters
        message_name = request.DATA['name']
        message_email = request.DATA['email']
        message_content = request.DATA['message']

        try:
            # Create the message
            new_message = api_message_post(message_name=message_name, message_email=message_email,
                                           message_content=message_content)

            # Serialize the message
            serializer = MessageSerializer(new_message)

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
def message(request):
    """
    Create a message
    :param request:
    :return:
    """
    if request.method == 'GET':
        return message_get(request)
    elif request.method == 'POST':
        return message_post(request)


@api_view(['POST'])
def message_delete(request):
    """
    Delete a message
    :param request:
    :return:
    """
    try:
        # Get parameters
        message_id = request.DATA['messageid']

        try:
            api_message_delete(message_id)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        # logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
