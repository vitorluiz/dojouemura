# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include # Adicione 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Adicione esta linha para criar o prefixo /api/v1/
    path('api/v1/', include('inscription.urls')),
    path('api/v1/manager/', include('manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)