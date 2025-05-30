from django.urls import path, include
import rest_framework.routers as routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Top-level router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router for messages
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
