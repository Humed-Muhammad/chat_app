from django.urls import path
from .views.login import login_view
from .views.getUsers import get_users

urlpatterns = [
    path('login/', login_view, name='login'),
    path('users/', get_users, name='users'),
]