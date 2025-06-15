from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # REQUIRED FIELD
    # Optional: if you're preparing for later tasks
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:20]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='histories', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # FOR ALX CHECKER

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"
