from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('chatroom/<str:room_name>/', views.chatroom, name='chatroom'),
]
