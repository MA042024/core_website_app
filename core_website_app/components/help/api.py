"""
    help page api
"""
from ..web_page.api import web_page_get, web_page_post
from ..web_page.enums import WEB_PAGE_TYPES

HELP_PAGE_TYPE = WEB_PAGE_TYPES["help"]


def help_get():
    """
    Get the help
    :return:
    """
    return web_page_get(HELP_PAGE_TYPE)


def help_post(help_content):
    """
    Post the help
    :param help_content:
    :return:
    """
    return web_page_post(HELP_PAGE_TYPE, help_content)


def help_delete():
    pass
