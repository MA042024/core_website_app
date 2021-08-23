""" Account requests model
"""
import datetime

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class AccountRequest(Document):
    """Represents a request sent by an user to get an account"""

    meta = {"allow_inheritance": True}

    username = fields.StringField(blank=False)  #: Username associated with the request
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    email = fields.StringField(blank=False)
    date = fields.DateTimeField(default=datetime.datetime.now, blank=False)

    @staticmethod
    def get_by_id(request_id):
        """Get a request given its primary key

        Parameters:
            request_id (str): Primary key of the request

        Returns:
            Request object corresponding to the given id
        """
        try:
            return AccountRequest.objects().get(pk=str(request_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Get all Account Request

        Returns:

        """
        return AccountRequest.objects.all()
