from django.urls import path
from django.urls import include

from api import admin
from .views import create_user, get_all_users, get_user, update_user

urlpatterns = [
    path('user/<int:user_id>/', get_user, name='get_user'),
    path('user/create/', create_user, name='create_user'),
    path('all/users/', get_all_users, name='get_all_users'),
    path('user/update/<int:user_id>/', update_user, name='update_user'),
    path('delete/user/<int:user_id>/', update_user, name='delete_user'),

]