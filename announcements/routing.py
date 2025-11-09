"""
WebSocket URL routing for announcements
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/display-board/$', consumers.DisplayBoardConsumer.as_asgi()),
]

