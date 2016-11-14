"""contact message API
"""
import logging
from core_main_app.commons.exceptions import ApiError
from core_website_app.components.contact_message.models import Message

logger = logging.getLogger("core_website_app.components.contact_message.api")


def get_all():
    """
        List all messages
        :return:
    """
    return Message.get_all()


def get(message_id):
    """
        Get a message
        :param message_id:
        :return:
    """
    try:
        return Message.get_by_id(message_id)
    except Exception as e:
        logger.error(e.message)
        raise ApiError('No message could be found with the given id.')


def save(message_name, message_email, message_content):
    """
        Post a message
        :param message_name:
        :param message_email:
        :param message_content:
        :return: message's pk
    """
    try:
        # save method return self
        return_value = Message.create(message_name, message_email, message_content)
        return return_value
    except Exception as e:
        logger.error(e.message)
        raise ApiError('Save message failed')


def delete(message_id):
    """
        Delete a message
        :param message_id:
        :return:
    """
    message = get(message_id)
    # No exception possible for delete method
    message.delete()
