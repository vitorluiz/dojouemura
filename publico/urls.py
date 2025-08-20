from django.urls import path, include
from . import views


app_name = 'publico'

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('projeto-social/', views.projeto_social, name='projeto_social'),
    path('galeria/', views.galeria, name='galeria'),
    path('contato/', views.contato, name='contato'),
    # URLs de usuários incluídas no arquivo principal
    
    
    # Páginas para usuários logados
    path('perfil/', views.perfil, name='perfil'),
]

