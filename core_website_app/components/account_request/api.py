"""
    The API contains the available function to access, create, edit and delete the account requests
"""
from core_main_app.utils.notifications.mail import send_mail as common_send_mail
from core_main_app.commons.exceptions import ApiError
from core_website_app.settings import SERVER_URI
from core_website_app.components.account_request.models import AccountRequest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def get_all():
    """
        List of opened account requests

        Returns:
            list: List of all requests
    """
    return AccountRequest.objects()


def get_count():
    """ Count number of account request currently in the database.

    Returns:
        int: number of account requests
    """
    return len(get_all())


def get(account_request_id):
    """
        Get an account request given its primary key

        Parameters:
            account_request_id (str): Primary key of the request

        Returns:
            :class:`~models.AccountRequest`: The corresponding account request

        Raises:
            MDCSError: If no `request_id` does not correspond to any request.
    """
    try:
        return AccountRequest.get_by_id(account_request_id)
    except:
        raise ApiError('No request could be found with the given id.')


def insert(user):
    """
        Create a new request

        Parameters:
            user:

        Returns: new account request
    """
    try:
        # check if a user with the same username exists
        _get_user_by_username(user.username)
        raise ApiError('A user with the same username already exists.')
    except ObjectDoesNotExist:
        user.save()

        # Create the account request and save it
        account_request = AccountRequest(username=user.username)
        return account_request.save()


def accept(account_request, send_mail=True):
    """
        Accept an account request

        Parameters:
            account_request (obj): Primary key of the request
            send_mail (bool): send email

        Returns:
            User object

        Raises:
            ApiError: If user already exists
    """
    user = None
    try:
        # check if a user with the same username exists
        user = _get_user_by_username(account_request.username)
        user.is_active = True
        user.save()

        if send_mail:
            # FIXME send_mail should use a User object
            context = {'lastname': account_request.last_name,
                       'firstname': account_request.first_name,
                       'URI': SERVER_URI}

            common_send_mail(subject='Account approved',
                             path_to_template='core_website_app/admin/email/request_account_approved.html',
                             context=context, recipient_list=[account_request.email])
    finally:
        # delete the user request
        account_request.delete()
        if user is not None:
            return user
        else:
            raise ApiError("User does not exist")


def deny(account_request):
    """
        Delete an account request

        Parameters:
            account_request (obj): Primary key of the request
    """
    user = None
    try:
        # check if a user with the same username exists
        user = _get_user_by_username(account_request.username)
        user.delete()
    finally:
        # delete the user request
        account_request.delete()
        if user is not None:
            return
        else:
            raise ApiError("User does not exist")


def _get_user_by_username(username):
    """
        Returns a user given its username

        Parameters:
            username (str): Given username

        Returns:
            User object
    """
    return User.objects.get(username=username)


def _get_user_by_id(user_id):
    """
        Returns a user given its primary key

        Parameters:
            user_id (str): Given user id

        Returns:
            User object
    """
    return User.objects.get(pk=user_id)


def _create_and_save_user(username, password, first_name, last_name, email):
    """
        Save a user with the given parameters

        Parameters:
            username (str): Given user name
            password (str): Given password
            first_name (str): Given first name
            last_name (str): Given last name
            email (str): Given email

        Returns:
            User object
    """
    user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    # Have to be called separately because save from django object return nothing
    user.save()
    return user
