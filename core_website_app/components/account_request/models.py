"""
    Account requests model
"""
from django_mongoengine import fields, Document


class AccountRequest(Document):
    """
        Represents a request sent by an user to get an account
    """
    username = fields.StringField(blank=False)  #: Username associated with the request
    password = fields.StringField(blank=False, min_length=8)  #: User password associated with the request
    first_name = fields.StringField(blank=False)  #: First name of the user issuing the request
    last_name = fields.StringField(blank=False)  #: Last name of the user issuing the request
    email = fields.StringField(blank=False)  #: Email address of the user issuing the request

    @staticmethod
    def get_by_id(request_id):
        """
            Get a request given its primary key

            Parameters:
                request_id (str): Primary key of the request

            Returns:
                Request object corresponding to the given id
        """
        return AccountRequest.objects().get(pk=request_id)
