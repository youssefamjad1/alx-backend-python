from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_instance.content != instance.content:
            instance.edited = True
            MessageHistory.objects.create(  
                message=instance,
                old_content=old_instance.content,
                edited_by=instance.sender  # you could use request.user if using views
            )
