"""
    help page api
"""
import core_website_app.components.web_page.api as web_page_api
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES

HELP_PAGE_TYPE = WEB_PAGE_TYPES["help"]


def get():
    """
    Get the help
    :return:
    """
    return web_page_api.get(HELP_PAGE_TYPE)


def save(help_content):
    """
    Post the help
    :param help_content:
    :return:
    """
    return web_page_api.save(HELP_PAGE_TYPE, help_content)


def delete():
    pass
