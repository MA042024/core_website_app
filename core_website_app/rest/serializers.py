"""
    Serializers used throughout the Rest API
"""
from rest_framework_mongoengine import serializers
from rest_framework import fields
from core_website_app.components.account_request.api import AccountRequest
from core_website_app.components.contact_message.api import ContactMessage


class AccountRequestSerializer(serializers.DocumentSerializer):
    """
        Represents the account request serializer
    """
    class Meta:
        model = AccountRequest


class ContactMessageSerializer(serializers.DocumentSerializer):
    """
        Represents the contact message serializer
    """
    class Meta:
        model = ContactMessage


class WebPageSerializer(serializers.DocumentSerializer):
    """
        Represents the web page serializer
    """
    content = fields.CharField()
