from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('verificar-email/<uidb64>/<token>/', views.verificar_email, name='verificar_email'),
    path('cadastrar-dependente/', views.cadastrar_dependente, name='cadastrar_dependente'),
    path('editar-dependente/<int:dependente_id>/', views.editar_dependente, name='editar_dependente'),
    path('excluir-dependente/<int:dependente_id>/', views.excluir_dependente, name='excluir_dependente'),
    path('buscar-cep/', views.buscar_cep_ajax, name='buscar_cep'),
    path('galeria/', views.galeria_completa, name='galeria_completa'),
]

