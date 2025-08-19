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
    
    # Painel do Atleta (antigo dashboard)
    path('painel/', views.dashboard, name='dashboard'),
    
    # Gestão de Dependentes
    path('cadastrar-dependente/', views.cadastrar_dependente, name='cadastrar_dependente'),
    path('editar-dependente/<int:dependente_id>/', views.editar_dependente, name='editar_dependente'),
    path('excluir-dependente/<int:dependente_id>/', views.excluir_dependente, name='excluir_dependente'),
    
    # Matrículas
    path('matricula/projeto-social/', views.matricula_projeto_social, name='matricula_projeto_social'),
    path('matricula/modalidade-paga/', views.matricula_modalidade_paga, name='matricula_modalidade_paga'),
    
    # Recuperação de senha
    path('esqueceu-senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('reset-senha/<uidb64>/<token>/', views.reset_senha, name='reset_senha'),
    
    # Utilitários
    path('buscar-cep/', views.buscar_cep_ajax, name='buscar_cep'),
    path('galeria/', views.galeria_completa, name='galeria_completa'),
]

