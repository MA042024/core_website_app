"""Web page model
"""
from django_mongoengine import fields, Document
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES
from core_website_app.commons.exceptions import WebsiteWebPageDoesNotExistError


class WebPage(Document):
    """Represents a WebPage
    """
    type = fields.IntField(choices=WEB_PAGE_TYPES.values())
    content = fields.StringField()

    @staticmethod
    def get_by_type(page_type):
        """Get a WebPage given its type

            Parameters:
                page_type (str): page type of the page

            Returns:
                Web Page corresponding to the given type
        """
        try:
            return WebPage.objects.get(type=WEB_PAGE_TYPES[page_type])
        except:
            raise WebsiteWebPageDoesNotExistError("Web page does not exist")

