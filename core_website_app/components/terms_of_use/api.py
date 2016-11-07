"""
    terms of use api
"""
import core_website_app.components.web_page.api as web_page_api
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES

TERMOF_PAGE_TYPE = WEB_PAGE_TYPES["terms_of_use"]


def get():
    """
    Get the terms of use
    :return:
    """
    return web_page_api.get(TERMOF_PAGE_TYPE)


def save(terms_of_use_content):
    """
    Post the terms of use
    :param terms_of_use_content:
    :return:
    """
    return web_page_api.save(TERMOF_PAGE_TYPE, terms_of_use_content)
