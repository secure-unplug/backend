from django.urls import path
from .views import login, join, get_device_list, add_device, get_friends_list, get_friends_entries, get_user_info, update_userinfo_password, user_delete, update_userinfo_username

urlpatterns = [
    path('login', login),
    path('join', join),
    path('devices', get_device_list),
    path('add_device', add_device),
    path('get_user_info', get_user_info),
    path('friends_list', get_friends_list),
    path('friends_entries', get_friends_entries),
    path('update_userinfo_password', update_userinfo_password),
    path('update_userinfo_username', update_userinfo_username),
    path('user_delete', user_delete),



]