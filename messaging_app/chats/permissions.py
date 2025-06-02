# chats/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages in that conversation.
    """

    def has_permission(self, request, view):
        # Require authentication for any request
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed only to participants of the conversation.

        # For a Conversation object:
        if hasattr(obj, 'users'):
            return request.user in obj.users.all()

        # For a Message object:
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.users.all()

        return False
