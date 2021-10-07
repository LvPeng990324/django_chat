# chat/routing.py
from django.conf.urls import re_path

from Chat.websockets.Chat import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>[^\s]*)/(?P<user_sig>[^\s]*)/$', ChatConsumer.as_asgi()),
]
