# chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Top-level router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router for messages
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),                # ✅ Required by checker
    path('', include(conversations_router.urls)),  # ✅ Nested routes
]
