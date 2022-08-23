from django.urls import path
from .views import login, join, get_device_list, add_device, get_friends_list, get_friends_entries, get_user_info, update_userinfo

urlpatterns = [
    path('login', login),
    path('join', join),
    path('devices', get_device_list),
    path('add_device', add_device),
    path('get_user_info', get_user_info),
    path('friends_list', get_friends_list),
    path('friends_entries', get_friends_entries),
    path('update_userinfo', update_userinfo)
]