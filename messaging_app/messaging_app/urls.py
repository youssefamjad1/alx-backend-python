from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chats.urls')),          # Forward root URLs to chats app
    path('api-auth/', include('rest_framework.urls')),  # DRF auth
]
