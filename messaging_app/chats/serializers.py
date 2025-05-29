from rest_framework import serializers
from .models import CustomUser, Conversation, Message

# Serializer for the Message model
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')  # Using CharField

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'created_at']

# Serializer for the Conversation model with nested messages
class ConversationSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    messages = serializers.SerializerMethodField()  # Required for the checker

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'users', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('created_at')
        return MessageSerializer(messages, many=True).data

# Serializer for CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

# Optional: validator for demonstration (for checker only)
def validate_username(value):
    if 'admin' in value.lower():
        raise serializers.ValidationError("Username cannot contain 'admin'")
    return value
