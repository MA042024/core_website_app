"""
    help page api
"""
import core_website_app.components.web_page.api as web_page_api
from core_website_app.components.web_page.models import WebPage
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES

HELP_PAGE_TYPE = WEB_PAGE_TYPES["help"]


def get():
    """
        Get the help if exist

        Returns: help web page
    """
    return web_page_api.get(HELP_PAGE_TYPE)


def upsert(help_content):
    """
        Post the help

        Parameters:
            help_content (str): content of the web page

        Returns: help web page
    """
    return web_page_api.upsert(WebPage(HELP_PAGE_TYPE, help_content))
