# chat/urls.py
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [

    path('<str:room_name>/', views.room, name='room'),
]