"""
    privacy policy api
"""
import core_website_app.components.web_page.api as web_page_api
from core_website_app.components.web_page.models import WebPage
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES

PRIVACY_PAGE_TYPE = WEB_PAGE_TYPES["privacy_policy"]


def get():
    """
        Get the privacy policy if exist

        Returns: privacy policy web page
    """
    return web_page_api.get(PRIVACY_PAGE_TYPE)


def upsert(privacy_policy_content):
    """
        Post the privacy policy

        Parameters:
            privacy_policy_content (str): content of the web page

        Returns: privacy policy web page
    """
    return web_page_api.upsert(WebPage(PRIVACY_PAGE_TYPE, privacy_policy_content))
