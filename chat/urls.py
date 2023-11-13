from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.CreateChatRoomView.as_view(), name='home'),
    path('<str:slug>/', views.room, name='room'),
]