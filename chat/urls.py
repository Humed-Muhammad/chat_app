from django.urls import path
from .views import consumer, getUsers, login, getChatsByUser, uploadFileToS3

urlpatterns = [
    path('login', login.login_view, name='login'),
    path('users', getUsers.get_users, name='users'),
    path('chats', getChatsByUser.get_chats, name='chats'),
    path('upload', uploadFileToS3.uploadFileToS3, name='upload'),
    
    
]