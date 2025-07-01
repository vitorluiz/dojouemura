# backend/users/models.py

from django.db import models
from django.core.validators import RegexValidator
from libs.uuid7 import uuid7 
# --- Validações ---
cpf_validator = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    message='CPF deve estar no formato 000.000.000-00'
)

telefone_validator = RegexValidator(
    regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
    message='Telefone deve estar no formato (11) 91234-5678'
)

# --- Choices para o campo estado ---
ESTADOS = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

class Responsavel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        help_text="ID único no formato UUIDv7"
    )
    status = models.CharField(
        max_length=20,
        default='Ativo',
        help_text="Status do cadastro do responsável (Ex: Ativo, Inativo)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora de criação do registro"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última atualização do registro"
    )
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[cpf_validator],
        help_text="CPF no formato 123.456.789-00"
    )
    rg = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="RG (opcional)"
    )
    email = models.EmailField(unique=True)
    telefone = models.CharField(
        max_length=20,
        validators=[telefone_validator],
        help_text="Telefone no formato (11) 98765-4321"
    )
    cep = models.CharField(
        max_length=9,
        help_text="CEP no formato 12345-678"
    )
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS,
        help_text="Sigla do estado (Ex: SP)"
    )

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo
