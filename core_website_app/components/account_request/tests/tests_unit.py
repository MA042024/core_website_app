"""
    Tests of the account request API
"""
from ..api import *
from ..models import *
from mock import Mock, patch
from unittest.case import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from core_main_app.commons.exceptions import MDCSError


class TestsAccountRequestGet(TestCase):

    @patch('core_website_app.components.account_request.models.Request.get_by_id')
    def test_account_request_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        request_id = 1
        mock_request = Mock(spec=Request)
        mock_request.username = "my message name"
        mock_request.first_name = "mail@mail.com"
        mock_request.last_name = "content"
        mock_request.email = request_id
        mock_get_by_id.return_value = mock_request
        # Act
        result = request_get(request_id)
        # Assert
        self.assertIsInstance(result, Request)

    @patch('core_website_app.components.account_request.models.Request.get_by_id')
    def test_account_request_get_raise_MDCSError_if_request_not_found(self, mock_get_by_id):
        # Arrange
        request_id = 1
        mock_get_by_id.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(MDCSError):
            request_get(request_id)


class TestsAccountRequestAccept(TestCase):

    @patch('core_website_app.components.account_request.api._get_user_by_username')
    @patch('core_website_app.components.account_request.api.request_get')
    def test_account_request_accept_raise_MDCSError_if_user_already_exist(self, mock_request_get, mock_get_user_by_username):
        # Arrange
        mock_request = Mock(spec=Request)
        mock_request.username = "username"
        mock_request_get.return_value = mock_request
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.return_value = mock_user
        # Act # Assert
        with self.assertRaises(MDCSError):
            request_accept(1, False)

    @patch('core_website_app.components.account_request.api._save_user')
    @patch('core_website_app.components.account_request.api._get_user_by_username')
    @patch('core_website_app.components.account_request.api.request_get')
    def test_account_request_accept_return_user_if_user_doesnt_exist(self, mock_request_get, mock_get_by_username,
                                                                     mock_save):
        # Arrange
        mock_request = Mock(spec=Request)
        mock_request.username = "username"
        mock_request_get.return_value = mock_request
        mock_get_by_username.side_effect = ObjectDoesNotExist()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_save.return_value = mock_user
        # Act
        result = request_accept(1, False)
        #  Assert
        self.assertIsInstance(result, User)


class TestsAccountRequestPost(TestCase):

    @patch('core_website_app.components.account_request.api._get_user_by_username')
    def test_account_request_post_raise_MDCSError_if_username_already_exist(self, mock_get_user_by_username):
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.return_value = mock_user
        # Act # Assert
        with self.assertRaises(MDCSError):
            request_post("username", "firestname", "lastname", "password", "mail@mail.com")

    @patch('core_website_app.components.account_request.models.Request.save')
    @patch('core_website_app.components.account_request.api._get_user_by_username')
    def test_account_request_post_return_request_if_username_doesnt_exist(self, mock_get_user_by_username, mock_save):
        # Arrange
        mock_get_user_by_username.side_effect = ObjectDoesNotExist()
        mock_request = Mock(spec=Request)
        mock_save.return_value = mock_request
        # Act
        result = request_post("username", "firestname", "lastname", "password", "mail@mail.com")
        # Assert
        self.assertIsInstance(result, Request)


class TestsAccountRequestDeny(TestCase):

    @patch('core_website_app.components.account_request.models.Request.get_by_id')
    def test_account_request_deny_raise_MDCSError_if_request_not_found(self, mock_get_by_id):
        # Arrange
        request_id = 1
        mock_get_by_id.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(MDCSError):
            request_deny(request_id)
