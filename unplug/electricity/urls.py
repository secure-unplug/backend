from django.urls import path
from .views import save_entries, view_entries, view_average_money, view_device_data, view_average_kwatt, get_kwatt_level, view_period_average, view_device_fee

urlpatterns = [
    path('list', view_entries),
    path('save', save_entries),
    path('average_money', view_average_money),
    path('device_data', view_device_data),
    #path('my_entries', view_my_entries),
    path('average_kwatt', view_average_kwatt),
    path('kwatt_level', get_kwatt_level),
    path('period_average',view_period_average),
    path('device_fee', view_device_fee)
]