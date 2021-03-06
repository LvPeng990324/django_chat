# chat/routing.py
from django.conf.urls import re_path

from Chat.websockets.Chat import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/', ChatConsumer.as_asgi()),
]
