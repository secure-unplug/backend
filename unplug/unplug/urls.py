from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('electricities/', include('electricity.urls')),
    path('users/', include('user.urls'))
]