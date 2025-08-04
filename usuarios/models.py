from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from utils.get_alphanumeric import get_alphanumeric
import re


def validar_cpf(cpf):
    """Valida CPF brasileiro"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')
    
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        raise ValidationError('CPF inválido')
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        raise ValidationError('CPF inválido')


def validar_idade_usuario(data_nascimento):
    """Valida se o usuário é maior de idade"""
    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    
    if idade < 18:
        raise ValidationError('Usuário deve ser maior de idade (18 anos ou mais)')


def validar_idade_dependente(data_nascimento):
    """Valida se o dependente tem entre 6 e 18 anos"""
    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    
    if idade < 6 or idade > 18:
        raise ValidationError('Dependente deve ter entre 6 e 18 anos')


class Usuario(AbstractUser):
    """Modelo customizado de usuário"""
    nome_completo = models.CharField(max_length=200, verbose_name='Nome Completo')
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
        validators=[validar_idade_usuario]
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF',
        validators=[validar_cpf]
    )
    telefone = models.CharField(
        max_length=15,
        verbose_name='Telefone',
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Telefone deve estar no formato (XX) XXXXX-XXXX'
        )]
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    email_verificado = models.BooleanField(default=False, verbose_name='Email Verificado')
    
    # Usar email como username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'data_nascimento', 'cpf', 'telefone']
    
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
    nome_completo = models.CharField(max_length=200, verbose_name='Nome Completo')
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
    logradouro = models.CharField(max_length=200, verbose_name='Logradouro')
    numero = models.CharField(max_length=10, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
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
    escola = models.CharField(max_length=200, verbose_name='Escola')
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
    
    # Metadados
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')
    
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