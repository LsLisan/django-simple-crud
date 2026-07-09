from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import api_root, create_user, get_all_users, get_user, login_user, task_detail, task_list_create, update_user

urlpatterns = [
    path('', api_root, name='api_root'),
    path('user/<int:user_id>/', get_user, name='get_user'),
    path('user/create/', create_user, name='create_user'),
    path('all/users/', get_all_users, name='get_all_users'),
    path('user/update/<int:user_id>/', update_user, name='update_user'),
    path('delete/user/<int:user_id>/', update_user, name='delete_user'),
    path('login/', login_user, name='login_user'),
    path('tasks/', task_list_create, name='task_list_create'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]