from django.contrib import admin
from django.urls import path, include
from electricity.views import save_entries, view_entries, view_average

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/save/', save_entries),
    path('api/view/', view_entries),
    path('api/average/', view_average),
]