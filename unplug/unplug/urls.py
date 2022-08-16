from django.contrib import admin
from django.urls import path, include
from electricity.views import save_entries

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/save/', save_entries)
]