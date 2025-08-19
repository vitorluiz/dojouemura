from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Usuario, Atleta, Modalidade
from utils.uuid7 import uuid7


class Professor(models.Model):
    """Modelo para professores do Dojô"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='professor',
        verbose_name='Usuário'
    )
    
    graduacao = models.CharField(
        max_length=50,
        verbose_name='Graduação',
        help_text='Ex: Faixa Preta 1º Dan, Faixa Marrom, etc.'
    )
    
    modalidades = models.ManyToManyField(
        Modalidade,
        verbose_name='Modalidades que ensina',
        help_text='Selecione as modalidades que este professor pode ensinar'
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name='Professor Ativo'
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )
    
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
        ordering = ['usuario__first_name', 'graduacao']
    
    def __str__(self):
        return f"{self.usuario.nome_completo} - {self.graduacao}"
    
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Verificar se o usuário é do tipo PROFESSOR
        if self.usuario.tipo_conta != 'PROFESSOR':
            raise ValidationError('Apenas usuários do tipo Professor podem ser cadastrados como professores')


class Turma(models.Model):
    """Modelo para turmas do Dojô"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    
    DIAS_SEMANA_CHOICES = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome da Turma',
        help_text='Ex: Turma A - Jiu-Jitsu Iniciante'
    )
    
    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        verbose_name='Modalidade'
    )
    
    professor = models.ForeignKey(
        Professor,
        on_delete=models.PROTECT,
        verbose_name='Professor Responsável'
    )
    
    dias_semana = models.JSONField(
        verbose_name='Dias da Semana',
        help_text='Lista dos dias da semana que a turma funciona',
        default=list
    )
    
    horario_inicio = models.TimeField(
        verbose_name='Horário de Início'
    )
    
    horario_fim = models.TimeField(
        verbose_name='Horário de Término'
    )
    
    capacidade_maxima = models.PositiveIntegerField(
        default=20,
        verbose_name='Capacidade Máxima',
        help_text='Número máximo de alunos por turma'
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name='Turma Ativa'
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['modalidade__nome', 'nome', 'horario_inicio']
        unique_together = ['modalidade', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.modalidade.nome} ({self.horario_inicio.strftime('%H:%M')})"
    
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Verificar se o horário de fim é maior que o de início
        if self.horario_fim <= self.horario_inicio:
            raise ValidationError('O horário de término deve ser maior que o horário de início')
        
        # Verificar se pelo menos um dia da semana foi selecionado
        if not self.dias_semana or len(self.dias_semana) == 0:
            raise ValidationError('Selecione pelo menos um dia da semana')
        
        # Verificar se o professor ensina a modalidade da turma
        if self.modalidade not in self.professor.modalidades.all():
            raise ValidationError('O professor selecionado não ensina esta modalidade')


class Frequencia(models.Model):
    """Modelo para controle de frequência dos atletas"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        verbose_name='ID'
    )
    
    STATUS_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('justificado', 'Justificado'),
        ('atrasado', 'Atrasado'),
    ]
    
    atleta = models.ForeignKey(
        Atleta,
        on_delete=models.CASCADE,
        related_name='frequencias',
        verbose_name='Atleta'
    )
    
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        verbose_name='Turma'
    )
    
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        verbose_name='Professor'
    )
    
    data_aula = models.DateField(
        verbose_name='Data da Aula'
    )
    
    data_entrada = models.DateTimeField(
        verbose_name='Data e Hora de Entrada'
    )
    
    data_saida = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data e Hora de Saída'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='presente',
        verbose_name='Status'
    )
    
    qr_code_utilizado = models.CharField(
        max_length=10,
        verbose_name='QR Code Utilizado',
        help_text='Código alfanumérico usado para o check-in/check-out'
    )
    
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Observações sobre a presença do atleta'
    )
    
    data_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Registro'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )
    
    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'
        ordering = ['-data_aula', '-data_entrada', 'atleta__nome']
        unique_together = ['atleta', 'turma', 'data_aula']
    
    def __str__(self):
        return f"{self.atleta.nome} - {self.turma.nome} - {self.data_aula.strftime('%d/%m/%Y')}"
    
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Verificar se o QR Code corresponde ao atleta
        if self.qr_code_utilizado != self.atleta.codigo_alfanumerico:
            raise ValidationError('QR Code não corresponde ao atleta')
        
        # Verificar se a data de saída é posterior à data de entrada
        if self.data_saida and self.data_saida <= self.data_entrada:
            raise ValidationError('A data de saída deve ser posterior à data de entrada')
        
        # Verificar se o atleta está matriculado na turma
        from usuarios.models import Matricula
        if not Matricula.objects.filter(
            atleta=self.atleta,
            modalidade=self.turma.modalidade,
            ativa=True
        ).exists():
            raise ValidationError('O atleta não está matriculado nesta modalidade')
    
    @property
    def duracao_aula(self):
        """Retorna a duração da aula em minutos"""
        if self.data_saida:
            duracao = self.data_saida - self.data_entrada
            return int(duracao.total_seconds() / 60)
        return None
    
    @property
    def atraso_minutos(self):
        """Retorna o atraso em minutos (se houver)"""
        if self.data_entrada:
            horario_previsto = self.turma.horario_inicio
            horario_real = self.data_entrada.time()
            if horario_real > horario_previsto:
                atraso = horario_real.hour * 60 + horario_real.minute - (horario_previsto.hour * 60 + horario_previsto.minute)
                return atraso
        return 0
