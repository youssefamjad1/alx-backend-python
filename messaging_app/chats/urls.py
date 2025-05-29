from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, home

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', home, name='home'),              # Root of chats app (at '/')
    path('api/', include(router.urls)),       # API endpoints for viewsets
]