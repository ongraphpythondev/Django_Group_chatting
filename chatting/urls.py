from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/<str:user_name>', views.room, name='room'),
    path('users', views.all_users, name='users'),
    path('<str:user_name>', views.chat, name='chat'),
]