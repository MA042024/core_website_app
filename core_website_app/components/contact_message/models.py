""" Contact messages models
################################################################################
#
# File Name: models.py
# Application: core_website_app
# Component: contact_message
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
"""

from django_mongoengine import fields, Document


class Message(Document):
    """Represents a message sent via the Contact form"""
    name = fields.StringField(max_length=100)
    email = fields.EmailField()
    content = fields.StringField()

    @staticmethod
    def get_by_id(message_id):
        return Message.objects().get(message_id)
