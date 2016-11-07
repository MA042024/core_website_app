"""
    privacy policy api
"""
import core_website_app.components.web_page.api as web_page_api
from core_website_app.components.web_page.enums import WEB_PAGE_TYPES

PRIVACY_PAGE_TYPE = WEB_PAGE_TYPES["privacy_policy"]


def get():
    """
    Get the privacy policy
    :return:
    """
    return web_page_api.get(PRIVACY_PAGE_TYPE)


def save(privacy_policy_content):
    """
    Post the privacy policy
    :param privacy_policy_content:
    :return:
    """
    return web_page_api.save(PRIVACY_PAGE_TYPE, privacy_policy_content)
