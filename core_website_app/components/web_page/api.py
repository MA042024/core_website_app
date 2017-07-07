"""Web page API
"""
from core_website_app.commons.exceptions import WebsiteWebPageDoesNotExistError
from core_main_app.commons.exceptions import ApiError
from .models import WebPage
from .enums import WEB_PAGE_TYPES


def get(page_type):
    """Get the web page of a given type

        Parameters:
            page_type: type of the web page

        Returns: web page corresponding to the given id
    """
    if page_type not in WEB_PAGE_TYPES.keys():
        return None
    try:
        return WebPage.get_by_type(page_type)
    except WebsiteWebPageDoesNotExistError:
        return None


def upsert(web_page):
    """Post the page content

        Parameters:
            web_page (obj): web page object

        Returns: content of the web page
    """
    if web_page.type not in WEB_PAGE_TYPES.values():
        raise ApiError("Web page type does not exist")

    return web_page.save()
