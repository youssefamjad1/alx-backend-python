from rest_framework import permissions
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsParticipantInConversation(permissions.BasePermission):
    """
    Custom permission to check if user is participant in conversation
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False


class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission for message ownership
    """
    
    def has_object_permission(self, request, view, obj):
        # Users can only access their own messages
        return obj.sender == request.user


class CanAccessConversation(permissions.BasePermission):
    """
    Permission to check if user can access conversation and its messages
    """
    
    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check different object types
        if hasattr(obj, 'participants'):
            # This is a conversation object
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # This is a message object
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'sender'):
            # This is a message, check if user is sender or recipient
            return (obj.sender == request.user or 
                   request.user in obj.conversation.participants.all())
        
        return False


class IsAuthenticatedAndOwner(permissions.BasePermission):
    """
    Permission that combines authentication and ownership checks
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # For user objects
        if isinstance(obj, User):
            return obj == request.user
            
        # For objects with 'user' field
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # For objects with 'sender' field (messages)
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
            
        # For conversations, check if user is participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
            
        return False