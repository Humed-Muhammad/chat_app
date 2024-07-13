from django.urls import path, re_path
from .views import consumer, getUsers, login

urlpatterns = [
    path('login', login.login_view, name='login'),
    path('users', getUsers.get_users, name='users'),
    re_path(r'wss/chat/$', consumer.ChatConsumer.as_asgi()),
]