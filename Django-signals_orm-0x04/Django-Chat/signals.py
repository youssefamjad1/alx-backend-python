from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, not an edit

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_instance.content
        )
        instance.edited = True
