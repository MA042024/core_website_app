""" privacy policy api
#################################################################################
# File Name: views.py
# Application: api
# Purpose:
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
"""

from ..web_page.api import web_page_get, web_page_post
from ..web_page.enums import WEB_PAGE_TYPES

PRIVACY_PAGE_TYPE = WEB_PAGE_TYPES["privacy_policy"]


def privacy_policy_get():
    """
    Get the privacy policy
    :return:
    """
    return web_page_get(PRIVACY_PAGE_TYPE)


def privacy_policy_post(privacy_policy_content):
    """
    Post the privacy policy
    :param privacy_policy_content:
    :return:
    """
    return web_page_post(PRIVACY_PAGE_TYPE, privacy_policy_content)




