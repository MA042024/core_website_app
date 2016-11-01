"""
    web page model
"""
from django_mongoengine import fields, Document
from .enums import WEB_PAGE_TYPES


class WebPage(Document):
    type = fields.IntField(choices=WEB_PAGE_TYPES.values())
    content = fields.StringField()

    @staticmethod
    def get_by_type(page_type):
        return WebPage.objects.get(type=WEB_PAGE_TYPES[page_type])

