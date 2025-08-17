from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from utils.get_alphanumeric import get_alphanumeric
import re
from utils.valicacaos import validar_cpf, validar_idade_usuario, validar_idade_dependente




class Usuario(AbstractUser):

    class TipoConta(models.TextChoices):
        RESPONSAVEL = 'RESPONSAVEL', 'Responsável'
        PROFESSOR = 'PROFESSOR', 'Professor'
        GESTOR = 'GESTOR', 'Gestor'
        FUNCIONARIO = 'FUNCIONARIO', 'Funcionário'

    
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
        )

    email_verificado = models.BooleanField(
        default=False,
        verbose_name='Email Verificado',
        help_text='Indica se o email foi verificado pelo usuário'
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF',
        validators=[validar_cpf]
    )
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
        validators=[validar_idade_usuario]
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name='Telefone',
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Telefone deve estar no formato (XX) XXXXX-XXXX'
        )]
    )

    tipo_conta = models.CharField(
        max_length=20,
        choices=TipoConta.choices,
        default=TipoConta.RESPONSAVEL,
        verbose_name='Tipo de Conta'
    )

   
    # Usar email como username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.nome_completo


class Dependente(models.Model):
    """Modelo para dependentes dos usuários"""
    
    PARENTESCO_CHOICES = [
        ('filho', 'Filho(a)'),
        ('enteado', 'Enteado(a)'),
        ('neto', 'Neto(a)'),
        ('sobrinho', 'Sobrinho(a)'),
        ('outro', 'Outro'),
    ]
    
    ESCOLARIDADE_CHOICES = [
        ('fundamental_1', 'Ensino Fundamental I (1º ao 5º ano)'),
        ('fundamental_2', 'Ensino Fundamental II (6º ao 9º ano)'),
        ('medio', 'Ensino Médio'),
        ('tecnico', 'Ensino Técnico'),
    ]
    
    TURNO_CHOICES = [
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
        ('noturno', 'Noturno'),
        ('integral', 'Integral'),
    ]
    
    # Relacionamento com usuário
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='dependentes',
        verbose_name='Usuário Responsável'
    )
    codigo_alfanumerico = models.CharField(max_length=9, unique=True, editable=False)

    # Dados pessoais
    
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
        validators=[validar_idade_dependente]
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF',
        validators=[validar_cpf]
    )
    parentesco = models.CharField(
        max_length=20,
        choices=PARENTESCO_CHOICES,
        verbose_name='Parentesco'
    )
    
    # Foto
    foto = models.ImageField(
        upload_to='dependentes/fotos/',
        verbose_name='Foto',
        help_text='Foto do dependente (opcional)'
    )
    
    # Endereço
    cep = models.CharField(
        max_length=9,
        verbose_name='CEP',
        validators=[RegexValidator(
            regex=r'^\d{5}-\d{3}$',
            message='CEP deve estar no formato XXXXX-XXX'
        )]
    )
    
    logradouro = models.CharField(
        max_length=200,
        verbose_name='Logradouro'
        )

    numero = models.CharField(
        max_length=10,
        verbose_name='Número'
        )

    complemento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Complemento'
        )

    bairro = models.CharField(
        max_length=100,
        verbose_name='Bairro'
        )

    cidade = models.CharField(
        max_length=100,
        verbose_name='Cidade'
        )

    uf = models.CharField(
        max_length=2,
        verbose_name='UF',
        validators=[RegexValidator(
            regex=r'^[A-Z]{2}$',
            message='UF deve ter 2 letras maiúsculas'
        )]
        )
    
    # Dados escolares
    escolaridade = models.CharField(
        max_length=20,
        choices=ESCOLARIDADE_CHOICES,
        verbose_name='Escolaridade'
        )

    escola = models.CharField(
        max_length=200,
        verbose_name='Escola'
        )
    
    turno = models.CharField(
        max_length=15,
        choices=TURNO_CHOICES,
        verbose_name='Turno'
        )
    
    # Dados médicos e termos
    condicoes_medicas = models.TextField(
        blank=True,
        verbose_name='Condições Médicas para Prática de Esportes',
        help_text='Descreva qualquer condição médica relevante para a prática de esportes'
    )
    termo_responsabilidade = models.BooleanField(
        default=False,
        verbose_name='Aceito os Termos de Responsabilidade'
    )
    termo_uso_imagem = models.BooleanField(
        default=False,
        verbose_name='Autorizo o Uso de Imagem'
    )
    
    # NOVOS CAMPOS DE MATRÍCULA
    tipo_matricula = models.ForeignKey(
        'TipoMatricula',
        on_delete=models.PROTECT,
        verbose_name='Tipo de Matrícula',
        help_text='Projeto Social (gratuito) ou Modalidade Paga'
    )
    
    modalidade = models.ForeignKey(
        'Modalidade',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Modalidade',
        help_text='Modalidade escolhida (apenas para matrícula paga)'
    )
    
    status_matricula = models.ForeignKey(
        'StatusMatricula',
        on_delete=models.PROTECT,
        default=1,  # ID do status 'pendente'
        verbose_name='Status da Matrícula'
    )
    
    data_matricula = models.DateField(
        auto_now_add=True,
        verbose_name='Data da Matrícula'
    )
    
    # Metadados
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
        )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'nome_completo', 'cpf'],
                name='unique_dependente_por_usuario'
            )
        ]
        verbose_name = 'Dependente'
        verbose_name_plural = 'Dependentes'
        ordering = ['nome_completo']
   
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Validar se os termos foram aceitos
        if not self.termo_responsabilidade:
            raise ValidationError('É obrigatório aceitar os termos de responsabilidade')
        
        if not self.termo_uso_imagem:
            raise ValidationError('É obrigatório autorizar o uso de imagem')
    
    # Dentro da classe Usuario(AbstractUser)
    @property
    def nome_completo(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def idade(self):
        """Calcula a idade do dependente"""
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
    
    @property
    def endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.logradouro}, {self.numero}"
        if self.complemento:
            endereco += f", {self.complemento}"
        endereco += f" - {self.bairro}, {self.cidade}/{self.uf} - CEP: {self.cep}"
        return endereco
    
    def save(self, *args, **kwargs):
        """Gera um código alfanumérico único antes de salvar o dependente se ele não existir."""
        if not self.codigo_alfanumerico:
            # Loop para garantir que o código gerado seja único
            while True:
                codigo = get_alphanumeric()
                # Verifica se já existe um dependente com este código
                if not Dependente.objects.filter(codigo_alfanumerico=codigo).exists():
                    self.codigo_alfanumerico = codigo
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} ({self.usuario.nome_completo})"


# MODELOS PARA CHOICES - Permitem gerenciar opções via admin
class Modalidade(models.Model):
    """Modelo para modalidades esportivas disponíveis"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome da Modalidade')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    ativa = models.BooleanField(default=True, verbose_name='Modalidade Ativa')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class TipoMatricula(models.Model):
    """Modelo para tipos de matrícula disponíveis"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome do Tipo')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    gratuito = models.BooleanField(default=False, verbose_name='Matrícula Gratuita')
    taxa_inscricao = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00,
        verbose_name='Taxa de Inscrição'
    )
    ativo = models.BooleanField(default=True, verbose_name='Tipo Ativo')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Tipo de Matrícula'
        verbose_name_plural = 'Tipos de Matrícula'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class StatusMatricula(models.Model):
    """Modelo para status de matrícula disponíveis"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome do Status')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    cor = models.CharField(
        max_length=7, 
        default='#007bff',
        verbose_name='Cor do Status',
        help_text='Código hexadecimal da cor (ex: #007bff)'
    )
    ativo = models.BooleanField(default=True, verbose_name='Status Ativo')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Status de Matrícula'
        verbose_name_plural = 'Status de Matrícula'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome