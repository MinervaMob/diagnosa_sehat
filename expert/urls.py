from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('diagnosa/', views.diagnosa, name='diagnosa'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/start/', views.chatbot_start, name='chatbot_start'),
]
