from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import InformacaoEmpresa


@admin.register(InformacaoEmpresa)
class InformacaoEmpresaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo InformacaoEmpresa.
    Garante que só pode existir um único registro.
    """
    list_display = [
        'nome_fantasia', 
        'razao_social', 
        'cnpj', 
        'email', 
        'telefone',
        'atualizado_em'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('razao_social', 'nome_fantasia', 'cnpj')
        }),
        ('Endereço', {
            'fields': ('logradouro', 'numero', 'complemento', 'cep', 'bairro', 'municipio', 'uf')
        }),
        ('Contato', {
            'fields': ('email', 'telefone')
        }),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def has_add_permission(self, request):
        """
        Permite adicionar apenas se não existir nenhum registro.
        """
        return not InformacaoEmpresa.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """
        Não permite deletar o registro das informações da empresa.
        """
        return False
    
    def changelist_view(self, request, extra_context=None):
        """
        Redireciona diretamente para a edição se já existir um registro.
        """
        if InformacaoEmpresa.objects.exists():
            obj = InformacaoEmpresa.objects.first()
            return HttpResponseRedirect(
                reverse('admin:manager_informacaoempresa_change', args=[obj.pk])
            )
        return super().changelist_view(request, extra_context)
    
    def response_add(self, request, obj, post_url_override=None):
        """
        Customiza a resposta após adicionar um registro.
        """
        messages.success(request, 'Informações da empresa criadas com sucesso!')
        return HttpResponseRedirect(
            reverse('admin:manager_informacaoempresa_change', args=[obj.pk])
        )
    
    def response_change(self, request, obj):
        """
        Customiza a resposta após alterar um registro.
        """
        messages.success(request, 'Informações da empresa atualizadas com sucesso!')
        return HttpResponseRedirect(
            reverse('admin:manager_informacaoempresa_change', args=[obj.pk])
        )

