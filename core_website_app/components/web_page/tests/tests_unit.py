""" Web page models
"""
from unittest.case import TestCase
from ..api import *
from ..models import *
from mock import Mock, patch
from core_main_app.commons.exceptions import MDCSError


class TestsWebPageApiGet(TestCase):

    @patch('core_website_app.components.web_page.models.WebPage.get_by_type')
    def test_web_page_get_policy_privacy(self, mock_get_web_page_by_type):
        # Arrange
        mock_webpage_privacy = Mock(spec=WebPage)
        mock_webpage_privacy.type = WEB_PAGE_TYPES["privacy_policy"]
        mock_webpage_privacy.content = "content web page privacy"
        mock_get_web_page_by_type.return_value = mock_webpage_privacy
        # Act
        result = web_page_get("privacy_policy")
        # Assert
        self.assertEqual("content web page privacy", result)

    @patch('core_website_app.components.web_page.models.WebPage.get_by_type')
    def test_web_page_get_term_of_use(self, mock_get_web_page_by_type):
        # Arrange
        mock_webpage_termsof = Mock(spec=WebPage)
        mock_webpage_termsof.type = WEB_PAGE_TYPES["terms_of_use"]
        mock_webpage_termsof.content = "content web page terms"
        mock_get_web_page_by_type.return_value = mock_webpage_termsof
        # Act
        result = web_page_get("terms_of_use")
        # Assert
        self.assertEqual("content web page terms", result)

    @patch('core_website_app.components.web_page.models.WebPage.get_by_type')
    def test_web_page_get_help(self, mock_get_web_page_by_type):
        # Arrange
        mock_webpage_help = Mock(spec=WebPage)
        mock_webpage_help.type = WEB_PAGE_TYPES["help"]
        mock_webpage_help.content = "content web page help"
        mock_get_web_page_by_type.return_value = mock_webpage_help
        # Act
        result = web_page_get("help")
        # Assert
        self.assertEqual("content web page help", result)

    @patch('core_website_app.components.web_page.models.WebPage.get_by_type')
    def test_web_page_get_not_in_database_return_none(self, mock_get_web_page_by_type):
        # Arrange
        mock_get_web_page_by_type.side_effect = DoesNotExist()
        # Act
        result = web_page_get("help")
        # Assert
        self.assertEqual(None, result)

    def test_web_page_get_with_wrong_type_return_none(self):
        # Arrange
        # Act
        page = web_page_get("wrong_type")
        # Assert
        self.assertEqual(None, page)


class TestsWebPageApiPost(TestCase):

    def test_web_page_post_with_wrong_type_raise_mdcs_error(self):
        # Arrange
        # Act Assert
        with self.assertRaises(MDCSError):
            web_page_post("wrong_type", "content")

    @patch('core_website_app.components.web_page.models.WebPage.get_by_type')
    def test_web_page_post(self, mock_get_web_page_by_type):
        # Arrange
        type = WEB_PAGE_TYPES["help"]
        content = "content"
        mock_webpage = Mock(spec=WebPage)
        mock_webpage.type = type
        mock_webpage.content = content
        mock_get_web_page_by_type.return_value = mock_webpage
        # Act
        result = web_page_post(type, content)
        # Assert
        self.assertEquals(content, result)

    @patch('core_website_app.components.web_page.models.WebPage.get_by_type')
    def test_web_page_post_type_is_not_in_database(self, mock_get_web_page_by_type):
        # Arrange
        type = WEB_PAGE_TYPES["help"]
        content = "content"
        mock_get_web_page_by_type.side_effect = DoesNotExist()
        # Act
        result = web_page_post(type, content)
        # Assert
        self.assertEquals(content, result)
