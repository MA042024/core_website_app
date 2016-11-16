"""
    Serializers used throughout the Rest API
"""
from rest_framework_mongoengine import serializers
from core_website_app.components.account_request.api import AccountRequest
from core_website_app.components.contact_message.api import ContactMessage


class AccountRequestSerializer(serializers.MongoEngineModelSerializer):
    """
        Represents the account request serializer
    """
    class Meta:
        model = AccountRequest


class ContactMessageSerializer(serializers.MongoEngineModelSerializer):
    """
        Represents the contact message serializer
    """
    class Meta:
        model = ContactMessage


class WebPageSerializer(serializers.MongoEngineModelSerializer):
    """
        Represents the web page serializer
    """
    content = serializers.fields.CharField()
