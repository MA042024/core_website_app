""" Serializers used throughout the Rest API
################################################################################
#
# File Name: serializers.py
# Application: core_website_app
# Component: account_request
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
from rest_framework_mongoengine import serializers
from core_website_app.components.account_request.api import Request
from core_website_app.components.contact_message.api import Message


class RequestSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Request


class MessageSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = Message


class WebPageSerializer(serializers.MongoEngineModelSerializer):
    content = serializers.fields.CharField()
