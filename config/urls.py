from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/portfolio/', include('portfolios.urls')),
    path('api/auth/', include('auth.urls')),
    path('api/users/', include('users.urls'))
]
