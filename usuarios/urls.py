from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('verificar-email/<uidb64>/<token>/', views.verificar_email, name='verificar_email'),
    
    # Painel do Atleta (antigo painel-atleta)
    path('painel/', views.painel-atleta, name='painel-atleta'),
    
    # Gestão de Atletas
    path('cadastrar-atleta/', views.cadastrar_atleta, name='cadastrar_atleta'),
    path('editar-atleta/<uuid:atleta_id>/', views.editar_atleta, name='editar_atleta'),
    path('excluir-atleta/<uuid:atleta_id>/', views.excluir_atleta, name='excluir_atleta'),
    
    # Matrículas
    path('matricula/projeto-social/', views.matricula_projeto_social, name='matricula_projeto_social'),
    path('matricula/modalidade-paga/', views.matricula_modalidade_paga, name='matricula_modalidade_paga'),
    
    # Recuperação de senha
    path('esqueceu-senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('reenviar-verificacao/', views.reenviar_verificacao, name='reenviar_verificacao'),
    path('reset-senha/<uidb64>/<token>/', views.reset_senha, name='reset_senha'),
    
    # Utilitários
    path('buscar-cep/', views.buscar_cep_ajax, name='buscar_cep'),
    path('galeria/', views.galeria_completa, name='galeria_completa'),
]

