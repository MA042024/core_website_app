""" Serializers used throughout the Rest API
"""
from rest_framework_mongoengine import serializers
from core_website_app.components.account_request.api import Request
from core_website_app.components.contact_message.api import ContactMessage


class RequestSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Request


class ContactMessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = ContactMessage


class WebPageSerializer(serializers.MongoEngineModelSerializer):
    content = serializers.fields.CharField()
