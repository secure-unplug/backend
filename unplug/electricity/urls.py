from django.urls import path
from .views import save_entries, view_entries, view_average, view_device_data, view_my_entries

urlpatterns = [
    path('list', view_entries),
    path('save', save_entries),
    path('average', view_average),
    path('view_device_data', view_device_data),
    path('view_my_entries',view_my_entries)
]