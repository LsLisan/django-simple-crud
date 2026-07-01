from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView  # 🔄 Added for refreshing expired tokens

from .views import create_user, get_all_users, get_user, login_user, update_user

urlpatterns = [
    path('user/<int:user_id>/', get_user, name='get_user'),
    path('user/create/', create_user, name='create_user'),
    path('all/users/', get_all_users, name='get_all_users'),
    path('user/update/<int:user_id>/', update_user, name='update_user'),
    path('delete/user/<int:user_id>/', update_user, name='delete_user'),
    path('login/', login_user, name='login_user'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]