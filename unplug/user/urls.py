from django.urls import path
from .views import login, join

urlpatterns = [
    path('login', login),
    path('join', join)
]