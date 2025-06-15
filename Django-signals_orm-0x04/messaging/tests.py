
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageNotificationTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create(username="sender")
        self.receiver = User.objects.create(username="receiver")

    def test_message_sends_notification(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello")
        self.assertEqual(Notification.objects.count(), 1)
