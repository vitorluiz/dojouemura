from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('publico.urls')),  # Site público como página principal
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),  # Sistema de usuários
]
# Servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
