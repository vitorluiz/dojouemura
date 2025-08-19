from django.contrib import admin
from django.utils.html import format_html
from .models import Empresa, MensagemContato, TermosCondicoes

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome_fantasia', 'municipio', 'uf', 'telefone1', 'email', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'uf', 'municipio', 'data_criacao']
    search_fields = ['nome_fantasia', 'nome_empresarial', 'municipio', 'email']
    readonly_fields = ['id', 'data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Identificação', {
            'fields': ('cnpj', 'nome_empresarial', 'nome_fantasia', 'situacao_cadastral')
        }),
        ('Endereço', {
            'fields': ('logradouro', 'numero', 'complemento', 'cep', 'bairro', 'municipio', 'uf')
        }),
        ('Contato', {
            'fields': ('email', 'telefone1', 'telefone2')
        }),
        ('Horários de Atendimento', {
            'fields': (
                'segunda_feira', 'terca_feira', 'quarta_feira', 'quinta_feira',
                'sexta_feira', 'sabado', 'domingo', 'horarios_atendimento'
            ),
            'description': 'Defina os horários de atendimento para cada dia da semana. Ex: "8h às 10h, 13h às 22h"'
        }),
        ('Redes Sociais', {
            'fields': ('instagram', 'facebook', 'youtube'),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('ativo', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Retorna apenas empresas ativas por padrão"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ativo=True)

class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'assunto', 'data_envio', 'lida', 'respondida']
    list_filter = ['lida', 'respondida', 'data_envio', 'assunto']
    search_fields = ['nome', 'email', 'assunto', 'mensagem']
    readonly_fields = ['id', 'data_envio']
    
    fieldsets = (
        ('Informações da Mensagem', {
            'fields': ('nome', 'email', 'telefone', 'assunto', 'mensagem')
        }),
        ('Status', {
            'fields': ('lida', 'respondida')
        }),
        ('Datas', {
            'fields': ('data_envio',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_como_lida', 'marcar_como_respondida']
    
    def marcar_como_lida(self, request, queryset):
        queryset.update(lida=True)
        self.message_user(request, f"{queryset.count()} mensagem(ns) marcada(s) como lida(s).")
    marcar_como_lida.short_description = "Marcar mensagens selecionadas como lidas"
    
    def marcar_como_respondida(self, request, queryset):
        queryset.update(respondida=True)
        self.message_user(request, f"{queryset.count()} mensagem(ns) marcada(s) como respondida(s).")
    marcar_como_respondida.short_description = "Marcar mensagens selecionadas como respondidas"

class TermosCondicoesAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'titulo', 'ativo', 'data_atualizacao']
    list_filter = ['tipo', 'ativo', 'data_criacao']
    search_fields = ['titulo', 'conteudo']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'titulo', 'ativo')
        }),
        ('Conteúdo', {
            'fields': ('conteudo',),
            'description': 'Use {{NOME_EMPRESA}}, {{DATA_ATUAL}}, {{RESPONSAVEL}} como variáveis'
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(MensagemContato, MensagemContatoAdmin)
admin.site.register(TermosCondicoes, TermosCondicoesAdmin)
