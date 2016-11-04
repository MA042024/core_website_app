"""
    Tests of contact message API
"""
from core_website_app.components.contact_message import api as contact_message_api
from ..models import *
from unittest.case import TestCase
from mock import Mock, patch
from core_main_app.commons.exceptions import MDCSError


class TestsContactMessageGet(TestCase):

    @patch('core_website_app.components.contact_message.models.Message.get_by_id')
    def test_contact_message_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        message_id = 1
        mock_message = Mock(spec=Message)
        mock_message.name = "my message name"
        mock_message.email = "mail@mail.com"
        mock_message.content = "content"
        mock_message.id = message_id
        mock_get_by_id.return_value = mock_message
        # Act
        result = contact_message_api.get(message_id)
        # Assert
        self.assertIsInstance(result, Message)

    @patch('core_website_app.components.contact_message.models.Message.get_by_id')
    def test_contact_message_get_raise_MDCSError_if_not_found(self, mock_get_by_id):
        # Arrange
        message_id = 1
        mock_get_by_id.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(MDCSError):
            contact_message_api.get(message_id)


class TestsContactMessageDelete(TestCase):

    @patch('core_website_app.components.contact_message.models.Message.get_by_id')
    def test_message_delete_raise_MDCSError_if_id_is_not_found(self, mock_get_by_id):
        # Arrange
        message_id = 1
        mock_get_by_id.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(MDCSError):
            contact_message_api.delete(message_id)


class TestsContactMessagePost(TestCase):

    @patch('core_website_app.components.contact_message.models.Message.save')
    def test_message_post_return_message_if_success(self, mock_save):
        # Arrange
        mock_message = Mock(spec=Message)
        mock_message.name = "name"
        mock_message.email = "mail@mail.com"
        mock_message.content = "content"
        mock_save.return_value = mock_message
        # Act
        result = contact_message_api.save("name", "mail@mail.com", "content")
        # Assert
        self.assertIsInstance(result, Message)

    @patch('core_website_app.components.contact_message.models.Message.save')
    def test_message_post_raise_MDCSError_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(MDCSError):
            contact_message_api.save("name", "mail@mail.com", "content")

