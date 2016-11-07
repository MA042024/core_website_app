""" Contact messages models
"""
from django_mongoengine import fields, Document


class Message(Document):
    """Represents a message sent via the Contact form"""
    name = fields.StringField(max_length=100)
    email = fields.EmailField()
    content = fields.StringField()

    @staticmethod
    def get_by_id(message_id):
        return Message.objects().get(message_id)

    @staticmethod
    def get_all():
        return Message.objects.all()

    @staticmethod
    def create(message_name, message_email, message_content):
        new_message = Message(name=message_name, email=message_email, content=message_content).save()
        return new_message
