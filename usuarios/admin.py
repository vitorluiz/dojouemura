from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render
from .models import Usuario, Atleta, Modalidade, TipoMatricula, StatusMatricula, Matricula


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
	"""Configuração do admin para o modelo Usuario"""
	
	# Campos exibidos na listagem
	list_display = [
		'email', 'get_nome_completo', 'cpf', 'telefone', 
		'data_nascimento', 'email_verificado', 'is_active', 
		'date_joined', 'atletas_count'
	]
	
	# Campos para busca
	search_fields = ['email', 'first_name', 'last_name', 'cpf', 'telefone']
	
	# Filtros laterais
	list_filter = [
		'email_verificado', 'is_active', 'is_staff', 
		'date_joined', 'data_nascimento'
	]
	
	# Campos editáveis na listagem
	list_editable = ['email_verificado', 'is_active']
	
	# Ordenação padrão
	ordering = ['-date_joined']
	
	# Campos readonly
	readonly_fields = ['date_joined', 'last_login', 'atletas_count']
	
	# Configuração dos fieldsets para o formulário de edição
	fieldsets = (
		('Informações de Login', {
			'fields': ('email', 'password')
		}),
		('Dados Pessoais', {
			'fields': ('first_name', 'last_name', 'data_nascimento', 'cpf', 'telefone')
		}),
		('Permissões', {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
			'classes': ('collapse',)
		}),
		('Verificação', {
			'fields': ('email_verificado',)
		}),
		('Datas Importantes', {
			'fields': ('last_login', 'date_joined'),
			'classes': ('collapse',)
		}),
		('Estatísticas', {
			'fields': ('atletas_count',),
			'classes': ('collapse',)
		}),
	)
	
	# Campos para criação de novo usuário
	add_fieldsets = (
		('Informações Básicas', {
			'classes': ('wide',),
			'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
		}),
		('Dados Pessoais', {
			'fields': ('data_nascimento', 'cpf', 'telefone')
		}),
		('Permissões', {
			'fields': ('is_active', 'is_staff', 'email_verificado')
		}),
	)
	
	# Configurações do UserAdmin
	username_field = 'email'
	
	def get_nome_completo(self, obj):
		"""Retorna o nome completo do usuário"""
		return f"{obj.first_name} {obj.last_name}".strip() or obj.email
	get_nome_completo.short_description = 'Nome Completo'
	get_nome_completo.admin_order_field = 'first_name'
	
	def atletas_count(self, obj):
		"""Conta quantos atletas o usuário possui"""
		count = obj.atletas.count()
		if count > 0:
			url = reverse('admin:usuarios_atleta_changelist') + f'?usuario__id__exact={obj.id}'
			return format_html('<a href="{}">{} atleta(s)</a>', url, count)
		return '0 atletas'
	atletas_count.short_description = 'Atletas'
	
	def get_queryset(self, request):
		"""Otimiza consultas com prefetch_related"""
		queryset = super().get_queryset(request)
		return queryset.prefetch_related('atletas')


@admin.register(Atleta)
class AtletaAdmin(admin.ModelAdmin):
	"""Configuração do admin para o modelo Atleta"""
	
	# Campos exibidos na listagem
	list_display = [
		'nome', 'usuario_link', 'idade_display', 
		'parentesco', 'escola', 'cidade_uf', 'foto_thumbnail', 'qr_code_preview',
		'termos_aceitos', 'data_cadastro'
	]
	
	# Campos para busca
	search_fields = [
		'nome', 'cpf', 'rg', 'usuario__first_name', 'usuario__last_name', 'usuario__email',
		'escola', 'cidade', 'estado'
	]
	
	# Filtros laterais
	list_filter = [
		'parentesco', 'sexo', 'estado_civil', 'escolaridade', 'turno', 'estado', 
		'tipo_sanguineo', 'termo_responsabilidade', 'termo_uso_imagem',
		'data_cadastro', 'usuario__email_verificado'
	]
	
	# Campos editáveis na listagem
	list_editable = ['parentesco']
	
	# Ordenação padrão
	ordering = ['-data_cadastro', 'usuario__first_name']
	
	# Campos readonly
	readonly_fields = ['data_cadastro', 'data_atualizacao', 'idade_display', 'endereco_completo', 'foto_preview', 'qr_code_preview', 'gerar_cartao_link']
	
	# Configuração dos fieldsets (tabs Jazzmin)
	fieldsets = (
		('Dados Pessoais', {
			'fields': (
				'usuario', 'nome', 'data_nascimento', 'idade_display', 
				'cpf', 'rg', 'sexo', 'estado_civil', 'parentesco'
			),
			'classes': ('tab',)
		}),
		('Foto e QR Code', {
			'fields': ('foto', 'foto_preview', 'qr_code_imagem', 'qr_code_preview', 'gerar_cartao_link'),
			'classes': ('tab',)
		}),
		('Endereco', {
			'fields': (
				('cep', 'endereco'), 
				('numero', 'complemento'),
				('bairro', 'cidade', 'estado'),
				'endereco_completo'
			),
			'classes': ('tab',)
		}),
		('Dados Escolares', {
			'fields': ('escolaridade', 'escola', 'serie', 'turno'),
			'classes': ('tab',)
		}),
		('Informacoes Medicas', {
			'fields': ('tipo_sanguineo', 'alergias', 'condicoes_medicas'),
			'classes': ('tab',)
		}),
		('Termos e Condicoes', {
			'fields': ('termo_responsabilidade', 'termo_uso_imagem'),
			'classes': ('tab',)
		}),
		('Informacoes do Sistema', {
			'fields': ('data_cadastro', 'data_atualizacao'),
			'classes': ('tab',)
		}),
	)
	
	# Ações
	actions = ['gerar_qr_codes', 'gerar_cartoes_lote']
	
	def usuario_link(self, obj):
		"""Link para o usuário responsável"""
		url = reverse('admin:usuarios_usuario_change', args=[obj.usuario.pk])
		nome_completo = f"{obj.usuario.first_name} {obj.usuario.last_name}".strip() or obj.usuario.email
		return format_html('<a href="{}">{}</a>', url, nome_completo)
	usuario_link.short_description = 'Responsável'
	usuario_link.admin_order_field = 'usuario__first_name'
	
	def idade_display(self, obj):
		"""Exibe a idade com formatação"""
		idade = obj.idade
		if idade < 6:
			return format_html('<span style="color: red;">{} anos (Muito novo)</span>', idade)
		elif idade > 18:
			return format_html('<span style="color: orange;">{} anos (Muito velho)</span>', idade)
		else:
			return format_html('<span style="color: green;">{} anos</span>', idade)
	idade_display.short_description = 'Idade'
	idade_display.admin_order_field = 'data_nascimento'
	
	def cidade_uf(self, obj):
		"""Exibe cidade e estado juntos"""
		return f"{obj.cidade}/{obj.estado}"
	cidade_uf.short_description = 'Cidade/Estado'
	cidade_uf.admin_order_field = 'cidade'
	
	def matriculas_count(self, obj):
		"""Conta quantas matrículas o atleta possui"""
		count = obj.matriculas.count()
		if count > 0:
			url = reverse('admin:usuarios_matricula_changelist') + f'?atleta__id__exact={obj.id}'
			return format_html('<a href="{}">{} matrícula(s)</a>', url, count)
		return '0 matrículas'
	matriculas_count.short_description = 'Matrículas'
	
	def foto_thumbnail(self, obj):
		"""Exibe miniatura da foto"""
		if obj.foto:
			return format_html(
				'<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />',
				obj.foto.url
			)
		# Placeholder
		nome = obj.nome_completo if hasattr(obj, 'nome_completo') else f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()
		primeira_letra = nome[0].upper() if nome else '?'
		return format_html('<div style="width: 40px; height: 40px; border-radius: 50%; background: #ddd; display: flex; align-items: center; justify-content: center; font-size: 12px;">{}</div>', primeira_letra)
	foto_thumbnail.short_description = 'Foto'
	
	def foto_preview(self, obj):
		"""Preview da foto no formulário"""
		if obj.foto:
			return format_html(
				'<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px;" />',
				obj.foto.url
			)
		return "Nenhuma foto enviada"
	foto_preview.short_description = 'Preview da Foto'

	def termos_aceitos(self, obj):
		"""Status dos termos aceitos"""
		if obj.termo_responsabilidade and obj.termo_uso_imagem:
			return format_html('<span style="color: green;">Todos aceitos</span>')
		elif obj.termo_responsabilidade or obj.termo_uso_imagem:
			return format_html('<span style="color: orange;">Parcialmente aceitos</span>')
		else:
			return format_html('<span style="color: red;">Não aceitos</span>')
	termos_aceitos.short_description = 'Termos'
	
	def qr_code_preview(self, obj):
		"""Mostra preview do QR Code"""
		if obj.qr_code_imagem:
			return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: contain; background: #fff; padding: 4px; border: 1px solid #eee; border-radius: 4px;" />', obj.qr_code_imagem.url)
		return '-'
	qr_code_preview.short_description = 'QR Code'

	def gerar_cartao_link(self, obj):
		"""Botão/link para abrir o cartão do atleta (site) em nova aba."""
		url = reverse('usuarios:cartao_atleta', args=[obj.id])
		return format_html('<a class="button" target="_blank" href="{}">Gerar Cartão</a>', url)
	gerar_cartao_link.short_description = 'Cartão do Atleta'
	
	def gerar_qr_codes(self, request, queryset):
		"""Ação para gerar/forçar regeneração de QR Codes para atletas selecionados"""
		count = 0
		for atleta in queryset:
			if atleta.gerar_qr_code(force=True):
				atleta.save(update_fields=['qr_code_imagem'])
				count += 1
		self.message_user(request, f'QR Code gerado/atualizado para {count} atleta(s).')
	gerar_qr_codes.short_description = 'Gerar/Atualizar QR Codes selecionados'
	
	def gerar_cartoes_lote(self, request, queryset):
		"""Gera QR Codes (se necessário) e redireciona para uma página de impressão em lote."""
		ids = []
		for atleta in queryset:
			if not atleta.qr_code_imagem:
				atleta.gerar_qr_code(force=True)
				atleta.save(update_fields=['qr_code_imagem'])
			ids.append(str(atleta.id))
		from django.http import HttpResponseRedirect
		url = reverse('admin:usuarios_atleta_imprimir_cartoes') + (f"?ids={','.join(ids)}" if ids else '')
		return HttpResponseRedirect(url)
	gerar_cartoes_lote.short_description = 'Gerar Cartões (lote) para impressão'
	
	def get_urls(self):
		from django.urls import path
		urls = super().get_urls()
		custom_urls = [
			path('imprimir-cartoes/', self.admin_site.admin_view(self.imprimir_cartoes_view), name='usuarios_atleta_imprimir_cartoes'),
		]
		return custom_urls + urls
	
	def imprimir_cartoes_view(self, request):
		"""Página de impressão em lote dos cartões de atletas selecionados via ação."""
		ids_param = request.GET.get('ids', '')
		ids = [i for i in ids_param.split(',') if i]
		queryset = self.get_queryset(request).filter(id__in=ids)
		# Garantir QR para todos
		for atleta in queryset:
			if not atleta.qr_code_imagem:
				atleta.gerar_qr_code(force=True)
				atleta.save(update_fields=['qr_code_imagem'])
		context = {
			'atletas': queryset,
			'title': 'Impressão de Cartões de Atleta',
		}
		return render(request, 'admin/usuarios/atleta/cartoes_impressao.html', context)


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
	"""Configuração do admin para o modelo Modalidade"""
	
	list_display = ['nome', 'imagem_preview', 'ativa', 'ordem', 'descricao_curta']
	list_editable = ['ativa', 'ordem']
	list_filter = ['ativa']
	search_fields = ['nome', 'descricao']
	ordering = ['ordem', 'nome']
	
	fieldsets = (
		('Informações Básicas', {
			'fields': ('nome', 'descricao', 'imagem', 'ativa', 'ordem')
		}),
	)
	
	def imagem_preview(self, obj):
		"""Exibe preview da imagem da modalidade"""
		if obj.imagem:
			return format_html(
				'<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
				obj.imagem.url
			)
		return '-'
	imagem_preview.short_description = 'Imagem'
	
	def descricao_curta(self, obj):
		"""Retorna descrição truncada para a listagem"""
		if obj.descricao:
			return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
		return '-'
	descricao_curta.short_description = 'Descrição'


@admin.register(TipoMatricula)
class TipoMatriculaAdmin(admin.ModelAdmin):
	"""Configuração do admin para o modelo TipoMatricula"""
	
	list_display = ['nome', 'gratuito', 'taxa_inscricao', 'ativo', 'ordem']
	list_editable = ['gratuito', 'taxa_inscricao', 'ativo', 'ordem']
	list_filter = ['gratuito', 'ativo']
	search_fields = ['nome', 'descricao']
	ordering = ['ordem', 'nome']
	
	fieldsets = (
		('Informações Básicas', {
			'fields': ('nome', 'descricao', 'ativo', 'ordem')
		}),
		('Configurações Financeiras', {
			'fields': ('gratuito', 'taxa_inscricao'),
			'classes': ('collapse',)
		}),
	)


@admin.register(StatusMatricula)
class StatusMatriculaAdmin(admin.ModelAdmin):
	"""Configuração do admin para o modelo StatusMatricula"""
	
	list_display = ['nome', 'cor_display', 'ativo', 'ordem']
	list_editable = ['ativo', 'ordem']
	list_filter = ['ativo']
	search_fields = ['nome', 'descricao']
	ordering = ['ordem', 'nome']
	
	def cor_display(self, obj):
		"""Exibe a cor como um quadrado colorido"""
		return format_html(
			'<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
			obj.cor
		)
	cor_display.short_description = 'Cor'


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
	"""Configuração do admin para o modelo Matricula"""
	
	list_display = [
		'atleta', 'modalidade', 'tipo_matricula', 'status_matricula', 
		'data_matricula', 'ativa', 'duracao_dias_display'
	]
	list_filter = [
		'tipo_matricula', 'modalidade', 'status_matricula', 'ativa', 
		'data_matricula', 'data_inicio', 'data_fim'
	]
	search_fields = [
		'atleta__nome', 'atleta__usuario__first_name', 'atleta__usuario__last_name',
		'modalidade__nome', 'tipo_matricula__nome', 'status_matricula__nome'
	]
	list_editable = ['status_matricula', 'ativa']
	ordering = ['-data_matricula', 'atleta__nome']
	
	fieldsets = (
		('Informações do Atleta', {
			'fields': ('atleta',)
		}),
		('Detalhes da Matrícula', {
			'fields': ('tipo_matricula', 'modalidade', 'status_matricula', 'data_matricula')
		}),
		('Período de Aulas', {
			'fields': ('data_inicio', 'data_fim'),
			'classes': ('collapse',)
		}),
		('Controle', {
			'fields': ('ativa', 'observacoes'),
			'classes': ('collapse',)
		}),
	)
	
	def duracao_dias_display(self, obj):
		"""Exibe a duração da matrícula em dias"""
		duracao = obj.duracao_dias
		if duracao is not None:
			return f"{duracao} dias"
		return "-"
	duracao_dias_display.short_description = 'Duração'
	
	def get_queryset(self, request):
		"""Otimiza consultas com select_related"""
		queryset = super().get_queryset(request)
		return queryset.select_related(
			'atleta', 'atleta__usuario', 'modalidade', 'tipo_matricula', 'status_matricula'
		)

# Configurações globais do admin
admin.site.site_header = "Administração - Cadastro de Pessoas"
admin.site.site_title = "Admin Cadastro"
admin.site.index_title = "Painel de Administração"

