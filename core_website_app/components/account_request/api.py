""" The API contains the available function to access, create, edit and delete the account requests
"""

from core_main_app.utils.notifications.mail import send_mail as common_send_mail
from core_main_app.commons.exceptions import MDCSError
from core_website_app.settings import MDCS_URI
from .models import Request
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def request_list():
    """ List of opened account requests

    Returns:
        list: List of all requests
    """
    return Request.objects()


def request_get(request_id):
    """ Get an account request given its primary key

    Parameters:
        request_id (str): Primary key of the request

    Returns:
        :class:`~models.AccountRequest`: The corresponding request

    Raises:
        MDCSError: If no `request_id` does not correspond to any request.
    """
    try:
        return Request.get_by_id(request_id)
    except:
        raise MDCSError('No request could be found with the given id.')


def request_post(request_username, request_first_name, request_last_name, request_password, request_email):
    """ Create or modify a new request

    Parameters:
        request_username:
        request_first_name:
        request_last_name:
        request_password:
        request_email:

    Returns:

    """
    try:
        # check if a user with the same username exists
        _get_user_by_username(request_username)
        user_exits = True
    except ObjectDoesNotExist:
        user_exits = False

    if user_exits:
        raise MDCSError('A user with the same username already exists.')

    # Create the request
    new_request = Request(username=request_username,
                          first_name=request_first_name,
                          last_name=request_last_name,
                          password=request_password,
                          email=request_email).save()

    return new_request


def request_accept(request_id, send_mail=True):
    """ Accept an account request

    :param request_id:
    :param send_mail:
    :return:
    """

    user_request = request_get(request_id)
    can_return_user = False
    try:
        # check if a user with the same username exists
        _get_user_by_username(user_request.username)
    except ObjectDoesNotExist:
        # create the user
        user = _save_user(username=user_request.username,
                          password=user_request.password,
                          first_name=user_request.first_name,
                          last_name=user_request.last_name,
                          email=user_request.email)

        can_return_user = True

        if send_mail:
            # FIXME send_mail should use a User object
            context = {'lastname': user_request.last_name,
                       'firstname': user_request.first_name,
                       'URI': MDCS_URI}

            common_send_mail(subject='Account approved',
                             path_to_template='core_website_app/admin/email/request_account_approved.html',
                             context=context, recipient_list=[user_request.email])
    finally:
        # delete the user request
        user_request.delete()
        if can_return_user:
            return user
        else:
            raise MDCSError("User already exist")


def request_deny(request_id):
    """ Deny an account request

    :param request_id:
    :return:
    """
    user_request = request_get(request_id)
    # No exception possible for delete method
    user_request.delete()


def _get_user_by_username(username):
    """ Returns a user given its username

    :param username:
    :return:
    """
    return User.objects.get(username=username)


def _get_user_by_id(user_id):
    """ Returns a user given its primary key

    :param user_id:
    :return:
    """
    return User.objects.get(pk=user_id)


def _save_user(username, password, first_name, last_name, email):
    """ Save a user with the given parameters

    :param username:
    :param password:
    :param first_name:
    :param last_name:
    :param email:
    :return:
    """
    user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    # Have to be called separately because save from django object return nothing
    user.save()
    return user
