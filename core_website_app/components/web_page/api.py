"""
    Web page API
"""
from mongoengine.errors import DoesNotExist
from core_main_app.commons.exceptions import MDCSError
from .models import WebPage
from .enums import WEB_PAGE_TYPES


def get(page_type):
    """
        Get the content of a given web page
        :return: web page content
    """
    if page_type not in WEB_PAGE_TYPES.keys():
        return None
    try:
        page_object = WebPage.get_by_type(page_type)
        return page_object.content
    except DoesNotExist:
        return None


def save(page_type, page_content):
    """
        Post the page content
        :param page_type: type of the web page (help, policy, terms)
        :param page_content: content of the web page
        :return:
    """
    if page_type not in WEB_PAGE_TYPES.values():
        raise MDCSError("Web page type does not exist")

    page_object = None
    try:
        page_object = WebPage.get_by_type(page_type)
        page_object.content = page_content
    except DoesNotExist:
        page_object = WebPage(type=page_type, content=page_content)
    finally:
        page_object.save()
        return page_content


def delete(page_type):
    """
    """
    pass
