from django.urls import path, re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
    # path('', ChatConsumer.as_asgi()),

]
