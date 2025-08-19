from django.urls import path
from . import views

app_name = 'publico'

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('projeto-social/', views.projeto_social, name='projeto_social'),
    path('galeria/', views.galeria, name='galeria'),
    path('contato/', views.contato, name='contato'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    
    # Páginas para usuários logados
    path('perfil/', views.perfil, name='perfil'),
]

