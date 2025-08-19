from django.contrib import admin
from django.utils.html import format_html
from .models import Professor, Turma, Frequencia


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = [
        'usuario_link', 'graduacao', 'modalidades_display', 
        'ativo', 'data_cadastro'
    ]
    list_filter = ['ativo', 'graduacao', 'modalidades', 'data_cadastro']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'graduacao']
    readonly_fields = ['id', 'data_cadastro', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'graduacao', 'modalidades')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('id', 'data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def usuario_link(self, obj):
        """Exibe link para o usuário"""
        if obj.usuario:
            return format_html(
                '<a href="{}">{}</a>',
                f'/admin/usuarios/usuario/{obj.usuario.id}/change/',
                obj.usuario.nome_completo
            )
        return '-'
    usuario_link.short_description = 'Usuário'
    usuario_link.admin_order_field = 'usuario__first_name'
    
    def modalidades_display(self, obj):
        """Exibe as modalidades de forma legível"""
        return ', '.join([modalidade.nome for modalidade in obj.modalidades.all()])
    modalidades_display.short_description = 'Modalidades'


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'modalidade', 'professor_link', 'dias_semana_display',
        'horario_display', 'capacidade_maxima', 'ativa'
    ]
    list_filter = ['ativa', 'modalidade', 'professor', 'dias_semana', 'data_criacao']
    search_fields = ['nome', 'modalidade__nome', 'professor__usuario__first_name']
    readonly_fields = ['id', 'data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'modalidade', 'professor')
        }),
        ('Horários', {
            'fields': ('dias_semana', 'horario_inicio', 'horario_fim')
        }),
        ('Configurações', {
            'fields': ('capacidade_maxima', 'ativa')
        }),
        ('Metadados', {
            'fields': ('id', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def professor_link(self, obj):
        """Exibe link para o professor"""
        if obj.professor:
            return format_html(
                '<a href="{}">{}</a>',
                f'/admin/frequencia/professor/{obj.professor.id}/change/',
                obj.professor.usuario.nome_completo
            )
        return '-'
    professor_link.short_description = 'Professor'
    professor_link.admin_order_field = 'professor__usuario__first_name'
    
    def dias_semana_display(self, obj):
        """Exibe os dias da semana de forma legível"""
        dias_map = {
            'segunda': 'Seg',
            'terca': 'Ter',
            'quarta': 'Qua',
            'quinta': 'Qui',
            'sexta': 'Sex',
            'sabado': 'Sáb',
            'domingo': 'Dom'
        }
        dias = [dias_map.get(dia, dia) for dia in obj.dias_semana]
        return ', '.join(dias)
    dias_semana_display.short_description = 'Dias da Semana'
    
    def horario_display(self, obj):
        """Exibe o horário de forma legível"""
        return f"{obj.horario_inicio.strftime('%H:%M')} - {obj.horario_fim.strftime('%H:%M')}"
    horario_display.short_description = 'Horário'


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = [
        'atleta_link', 'turma_link', 'data_aula', 'horario_entrada',
        'horario_saida', 'status', 'duracao_display', 'atraso_display'
    ]
    list_filter = [
        'status', 'turma__modalidade', 'turma__professor', 
        'data_aula', 'data_registro'
    ]
    search_fields = [
        'atleta__nome', 'turma__nome', 'qr_code_utilizado'
    ]
    readonly_fields = [
        'id', 'data_registro', 'data_atualizacao', 'duracao_aula', 'atraso_minutos'
    ]
    date_hierarchy = 'data_aula'
    
    fieldsets = (
        ('Informações da Aula', {
            'fields': ('atleta', 'turma', 'professor', 'data_aula')
        }),
        ('Controle de Entrada/Saída', {
            'fields': ('data_entrada', 'data_saida', 'status', 'qr_code_utilizado')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Metadados', {
            'fields': ('id', 'data_registro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
        ('Cálculos', {
            'fields': ('duracao_aula', 'atraso_minutos'),
            'classes': ('collapse',)
        }),
    )
    
    def atleta_link(self, obj):
        """Exibe link para o atleta"""
        if obj.atleta:
            return format_html(
                '<a href="{}">{}</a>',
                f'/admin/usuarios/atleta/{obj.atleta.id}/change/',
                obj.atleta.nome
            )
        return '-'
    atleta_link.short_description = 'Atleta'
    atleta_link.admin_order_field = 'atleta__nome'
    
    def turma_link(self, obj):
        """Exibe link para a turma"""
        if obj.turma:
            return format_html(
                '<a href="{}">{}</a>',
                f'/admin/frequencia/turma/{obj.turma.id}/change/',
                obj.turma.nome
            )
        return '-'
    turma_link.short_description = 'Turma'
    turma_link.admin_order_field = 'turma__nome'
    
    def horario_entrada(self, obj):
        """Exibe o horário de entrada"""
        return obj.data_entrada.strftime('%H:%M')
    horario_entrada.short_description = 'Entrada'
    horario_entrada.admin_order_field = 'data_entrada'
    
    def horario_saida(self, obj):
        """Exibe o horário de saída"""
        if obj.data_saida:
            return obj.data_saida.strftime('%H:%M')
        return '-'
    horario_saida.short_description = 'Saída'
    horario_saida.admin_order_field = 'data_saida'
    
    def duracao_display(self, obj):
        """Exibe a duração da aula"""
        duracao = obj.duracao_aula
        if duracao:
            return f"{duracao} min"
        return '-'
    duracao_display.short_description = 'Duração'
    
    def atraso_display(self, obj):
        """Exibe o atraso (se houver)"""
        atraso = obj.atraso_minutos
        if atraso > 0:
            return format_html(
                '<span style="color: red;">{} min</span>',
                atraso
            )
        return '-'
    atraso_display.short_description = 'Atraso'
