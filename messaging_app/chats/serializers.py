from django.contrib.auth import get_user_model
from .models import Conversation, Message
from rest_framework import serializers

CustomUser = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)  # read_only for display

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'users', 'messages']

    def get_messages(self, obj):
        # Return messages sorted by creation time
        messages = obj.messages.all().order_by('created_at')
        return MessageSerializer(messages, many=True).data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

    # Example of using field-level validation in the serializer:
    def validate_username(self, value):
        if 'admin' in value.lower():
            raise serializers.ValidationError("Username cannot contain 'admin'")
        return value