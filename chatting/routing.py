from django.urls import re_path , path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<room_name>/<user_name>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/chat/<str:user_name>/', consumers.PersonalChatConsumer.as_asgi()),

]