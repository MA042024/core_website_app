""" Serializers used throughout the Rest API
"""
from rest_framework_mongoengine import serializers
from core_website_app.components.account_request.api import AccountRequest
from core_website_app.components.contact_message.api import ContactMessage


class AccountRequestSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = AccountRequest


class ContactMessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = ContactMessage


class WebPageSerializer(serializers.MongoEngineModelSerializer):
    content = serializers.fields.CharField()
