from django.urls import path
from .views import login, join, get_device_list, add_device

urlpatterns = [
    path('login', login),
    path('join', join),
    path('devices', get_device_list),
    path('add_device', add_device)
]