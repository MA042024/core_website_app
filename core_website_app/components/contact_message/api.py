"""
    contact message API
"""
from core_main_app.commons.exceptions import MDCSError
from .models import Message

# import logging
# logger = logging.getLogger('core_website_app')
# hdlr = logging.FileHandler('core_website_app.components.contact_message.api.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.WARNING)


def get_all():
    """
        List all messages
        :return:
    """
    return Message.objects.all()


def get(message_id):
    """
        Get a message
        :param message_id:
        :return:
    """
    try:
        return Message.get_by_id(message_id)
    except Exception as e:
        # logger.error(e.message)
        raise MDCSError('No message could be found with the given id.')


def save(message_name, message_email, message_content):
    """
        Post a message
        :param message_name:
        :param message_email:
        :param message_content:
        :return: message's pk
    """
    message_to_save = Message(name=message_name, email=message_email, content=message_content)
    try:
        # save method return self
        return_value = message_to_save.save()
        return return_value
    except Exception as e:
        # logger.error(e.message)
        raise MDCSError('Save message failed')


def delete(message_id):
    """
        Delete a message
        :param message_id:
        :return:
    """
    message = get(message_id)
    # No exception possible for delete method
    message.delete()
