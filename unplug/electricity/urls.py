from django.urls import path
from .views import save_entries, view_entries, view_average_money, view_device_data, view_my_entries, view_average_kwatt

urlpatterns = [
    path('list', view_entries),
    path('save', save_entries),
    path('average_money', view_average_money),
    path('device_data', view_device_data),
    path('my_entries', view_my_entries),
    path('average_kwatt', view_average_kwatt)
]