"""
    Account requests model
"""
from django_mongoengine import fields, Document
import datetime


class AccountRequest(Document):
    """
        Represents a request sent by an user to get an account
    """
    username = fields.StringField(blank=False)  #: Username associated with the request
    date = fields.DateTimeField(default=datetime.datetime.now, blank=False)

    @staticmethod
    def get_by_id(request_id):
        """
            Get a request given its primary key

            Parameters:
                request_id (str): Primary key of the request

            Returns:
                Request object corresponding to the given id
        """
        return AccountRequest.objects().get(pk=str(request_id))
