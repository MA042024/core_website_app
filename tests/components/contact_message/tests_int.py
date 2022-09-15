"""  Test send mail
"""

from django.core import mail
from django.test import TestCase
from mock import patch

import core_website_app.components.contact_message.api as contact_message_api
from core_website_app.components.contact_message.models import ContactMessage


class TestSendEmailContactMessage(TestCase):
    """Test Send Email Contact Message"""

    def setUp(self):
        """setUp"""

        self.contact_message = _create_contact_message()

    @patch("core_website_app.components.contact_message.models.ContactMessage.save")
    def test_contact_message_send_mail(self, mock_save):
        """test_contact_message_send_mail"""

        # Arrange
        mock_save.return_value = self.contact_message

        # Act
        contact_message_api.upsert(self.contact_message)

        # Assert
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[Django] New Contact Message")

    @patch("core_website_app.components.contact_message.models.ContactMessage.save")
    def test_contact_message_send_mail_admins(self, mock_save):
        """test_contact_message_send_mail_admins"""

        # Arrange
        mock_save.return_value = self.contact_message

        # Act
        contact_message_api.upsert(self.contact_message)

        # Assert
        self.assertEqual(len(mail.outbox[0].to), 2)
        self.assertEqual(mail.outbox[0].to, ["admin1@test.com", "admin2@test.com"])


def _create_contact_message(
    name="name",
    email="email@test.com",
    content="message",
):
    """Create a contact message

    Args:
        name:
        email:
        content:

    Returns:
    """

    return ContactMessage(name=name, email=email, content=content)
