""" terms of use api
################################################################################
#
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

TERMOF_PAGE_TYPE = WEB_PAGE_TYPES["terms_of_use"]


def terms_of_use_get():
    """
    Get the terms of use
    :return:
    """
    return web_page_get(TERMOF_PAGE_TYPE)


def terms_of_use_post(terms_of_use_content):
    """
    Post the terms of use
    :param terms_of_use_content:
    :return:
    """
    return web_page_post(TERMOF_PAGE_TYPE, terms_of_use_content)