# backend/students/admin.py

from django.contrib import admin
from .models import Dependente, HistoricoEsportivo, TermoAceite

class HistoricoEsportivoInline(admin.TabularInline):
    """
    Permite editar o Histórico Esportivo diretamente na página do Dependente.
    'TabularInline' mostra os campos em formato de tabela.
    """
    model = HistoricoEsportivo
    extra = 1 # Quantos formulários em branco mostrar por padrão

class TermoAceiteInline(admin.StackedInline):
    """
    Permite visualizar os Termos de Aceite na página do Dependente.
    'StackedInline' mostra os campos empilhados.
    """
    model = TermoAceite
    extra = 0 # Não mostrar formulários em branco, pois são criados pelo sistema
    readonly_fields = ('nome_termo', 'pdf_gerado', 'ip_assinatura', 'geolocalizacao', 'data_aceite')
    can_delete = False # Não permitir apagar a prova da assinatura

@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    """
    Configuração para a exibição do modelo Dependente.
    """
    list_display = ('nome_completo', 'codigo_aluno', 'responsavel', 'data_nascimento', 'status')
    search_fields = ('nome_completo', 'codigo_aluno', 'responsavel__nome_completo', 'responsavel__cpf')
    list_filter = ('status', 'responsavel__cidade', 'responsavel__estado')
    readonly_fields = ('codigo_aluno', 'created_at', 'updated_at')
    
    # Adiciona os inlines que criamos acima à página de detalhes do Dependente
    inlines = [HistoricoEsportivoInline, TermoAceiteInline]

    fieldsets = (
        ('Informações do Aluno', {
            'fields': ('responsavel', 'nome_completo', 'codigo_aluno', 'status', 'data_nascimento', 'cpf', 'foto_perfil', 'parentesco')
        }),
        ('Dados Escolares', {
            'fields': ('escola_nome', 'escola_serie_periodo'),
            'classes': ('collapse',)
        }),
        ('Saúde e Emergência', {
            'fields': ('plano_saude_qual', 'alergias_quais', 'medicamentos_quais', 'condicoes_medicas', 'contato_emergencia_nome', 'contato_emergencia_telefone')
        }),
        ('Datas Importantes', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Também registamos os modelos sozinhos para o caso de querermos vê-los separadamente
@admin.register(HistoricoEsportivo)
class HistoricoEsportivoAdmin(admin.ModelAdmin):
    # --- CORREÇÃO AQUI ---
    # Usamos os nomes de campo corretos do modelo: 'esporte', 'faixa', 'graduacao'
    list_display = ('dependente', 'esporte', 'faixa', 'graduacao')

@admin.register(TermoAceite)
class TermoAceiteAdmin(admin.ModelAdmin):
    list_display = ('dependente', 'nome_termo', 'data_aceite')
