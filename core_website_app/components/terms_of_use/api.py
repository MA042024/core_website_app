"""
    terms of use api
"""
import core_website_app.components.web_page.api as web_page_api
from core_website_app.components.web_page.models import WebPage
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES

TERMOF_PAGE_TYPE = WEB_PAGE_TYPES["terms_of_use"]


def get():
    """
        Get the terms of use if exist

        Returns: Terms of use web page
    """
    return web_page_api.get(TERMOF_PAGE_TYPE)


def upsert(terms_of_use_content):
    """
        Post the terms of use

        Parameters:
            terms_of_use_content (str): content of the web page

        Returns: Terms of use web page
    """
    return web_page_api.upsert(WebPage(TERMOF_PAGE_TYPE, terms_of_use_content))
