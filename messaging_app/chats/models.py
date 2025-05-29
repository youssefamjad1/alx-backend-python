from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User model
class User(AbstractUser):
    # Add custom fields here if needed
    # For now we can use built-in fields like username, email, password, etc.
    pass

# 2. Conversation model
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

# 3. Message model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp}"
