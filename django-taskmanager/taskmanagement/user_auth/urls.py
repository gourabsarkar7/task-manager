"""
Api end points for user_auth module
"""

from django.urls import path
from user_auth import views


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('change_password/', views.change_password, name="change_password"),
    path('signin/', views.signin, name="signin"),
    path('delete_profile/', views.delete_profile, name="delete_profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('add_user_role/', views.add_user_role, name="add_user_role"),
    path('update_user_role/', views.update_user_role, name="update_user_role"),
    path('delete_user_role/', views.delete_user_role, name="delete_user_role"),
    path('get_user_role/', views.get_user_role, name="get_user_role"),
    path('add_user_status/', views.add_user_status, name="add_user_status"),
    path('update_user_status/', views.update_user_status,
         name="update_user_status"),
    path('delete_user_status/', views.delete_user_status,
         name="delete_user_status"),
    path('get_user_status/', views.get_user_status, name="get_user_status"),
    path('refresh_token/', views.refresh_token, name="refresh_token"),
    path('logout/', views.logout, name="logout"),
    path('get_all_users/', views.get_all_users, name="get_all_users"),
]
