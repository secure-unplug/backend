from django.urls import path
from .views import save_entries, view_entries, view_average

urlpatterns = [
    path('list', view_entries),
    path('save', save_entries),
    path('average', view_average)
]