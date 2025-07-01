# backend/users/admin.py

from django.contrib import admin
from .models import Responsavel

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    """
    Configuração para a exibição do modelo Responsavel na área de administração.
    """
    # Colunas a serem exibidas na lista de responsáveis
    list_display = ('nome_completo', 'email', 'cpf', 'telefone', 'status')
    
    # Campos que podem ser usados para pesquisar
    search_fields = ('nome_completo', 'cpf', 'email')
    
    # Filtros que aparecerão na barra lateral direita
    list_filter = ('status', 'estado')
    
    # Agrupamento de campos no formulário de edição
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'email', 'cpf', 'rg', 'telefone', 'status')
        }),
        ('Endereço', {
            'fields': ('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Datas Importantes', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Começa recolhido para não poluir a tela
        }),
    )
    
    # Campos que são apenas para leitura
    readonly_fields = ('created_at', 'updated_at')

