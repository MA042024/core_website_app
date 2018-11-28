""" rest views for the contact message API
"""
from core_main_app.utils.decorators import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import core_website_app.components.contact_message.api as contact_message_api
from core_website_app.components.contact_message.models import ContactMessage
from core_website_app.rest.serializers import ContactMessageSerializer

import logging
logger = logging.getLogger("core_website_app.rest.contact_message.views")


@api_view(['GET'])
@api_staff_member_required()
def get_all(request):
    """ Get all messages

    Args:

        request: HTTP request

    Returns:

        - code: 200
          content: List of contact messages
        - code: 400
          content: Validation error
    """
    messages = contact_message_api.get_all()
    serializer = ContactMessageSerializer(messages)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization failed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def get(request):
    """ Get a message

    Parameters:

        {
            "requestid": "request_id"
        }

    Args:

        request: HTTP request

    Returns:

        - code: 200
          content: List of contact messages
        - code: 400
          content: Validation error / missing parameters
    """
    try:
        # FIXME: requestid should be renamed to message_id
        # Get parameters
        message_id = request.DATA['requestid']

        try:
            messages = contact_message_api.get(message_id)
            serializer = ContactMessageSerializer(messages)

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
    """ Create a message

    Parameters:

        {
            "name": "name",
            "message": "message",
            "email": "email"
        }

    Args:

        request: HTTP request

    Returns:

        - code: 200
          content: Contact message
        - code: 400
          content: Validation error / missing parameters
    """
    try:
        # Get parameters
        message_name = request.DATA['name']
        message_email = request.DATA['email']
        message_content = request.DATA['message']

        try:
            # Create the message and insert it
            contact_message_object = ContactMessage(
                name=message_name,
                email=message_email,
                content=message_content
            )
            new_contact_message = contact_message_api.upsert(contact_message_object)

            # Serialize the message
            serializer = ContactMessageSerializer(new_contact_message)

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
def message(request):
    """ Message redirect to POST or GET methods

    Args:

        request: HTTP request

    Returns:

        Response object
    """
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)


@api_view(['POST'])
def delete(request):
    """ Delete a message

    Parameters:

        {
            "messageid": "message_id"
        }

    Args:

        request: HTTP request

    Returns:

        - code: 204
          content: {}
        - code: 400
          content: Missing parameters
    """
    try:
        # Get parameters
        message_id = request.DATA['messageid']

        try:
            contact_message = ContactMessage(pk=message_id)
            contact_message_api.delete(contact_message)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
