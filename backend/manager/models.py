from django.db import models
from django.core.exceptions import ValidationError


class InformacaoEmpresa(models.Model):
    """
    Modelo Singleton para armazenar informações da empresa.
    Só pode existir um único registro desta tabela na base de dados.
    """
    razao_social = models.CharField(
        max_length=255,
        verbose_name="Razão Social",
        help_text="Razão social da empresa"
    )
    nome_fantasia = models.CharField(
        max_length=255,
        verbose_name="Nome Fantasia",
        help_text="Nome fantasia da empresa"
    )
    cnpj = models.CharField(
        max_length=18,
        verbose_name="CNPJ",
        help_text="CNPJ da empresa (formato: XX.XXX.XXX/XXXX-XX)"
    )
    logradouro = models.CharField(
        max_length=255,
        verbose_name="Logradouro",
        help_text="Endereço da empresa"
    )
    numero = models.CharField(
        max_length=20,
        verbose_name="Número",
        help_text="Número do endereço"
    )
    complemento = models.CharField(
        max_length=100,
        verbose_name="Complemento",
        blank=True,
        null=True,
        help_text="Complemento do endereço"
    )
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP",
        help_text="CEP (formato: XXXXX-XXX)"
    )
    bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro",
        help_text="Bairro da empresa"
    )
    municipio = models.CharField(
        max_length=100,
        verbose_name="Município",
        help_text="Município da empresa"
    )
    uf = models.CharField(
        max_length=2,
        verbose_name="UF",
        help_text="Estado (UF) da empresa"
    )
    email = models.EmailField(
        verbose_name="E-mail",
        help_text="E-mail de contato da empresa"
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        help_text="Telefone de contato da empresa"
    )
    
    # Campos de controle
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Informação da Empresa"
        verbose_name_plural = "Informações da Empresa"

    def __str__(self):
        return f"{self.nome_fantasia} - {self.razao_social}"

    def save(self, *args, **kwargs):
        """
        Garante que só pode existir um único registro desta tabela.
        """
        if not self.pk and InformacaoEmpresa.objects.exists():
            raise ValidationError(
                "Só pode existir um único registro de informações da empresa. "
                "Edite o registro existente em vez de criar um novo."
            )
        return super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """
        Método de classe para obter a única instância das informações da empresa.
        Se não existir, cria uma com dados padrão.
        """
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            # Cria uma instância com dados padrão se não existir
            return cls.objects.create(
                razao_social="UEMURA CENTRO DE TREINAMENTO ESPORTIVO LTDA",
                nome_fantasia="DOJÔ UEMURA",
                cnpj="59.002.265/0001-71",
                logradouro="Rod. Emanuel Pinheiro",
                numero="S/N",
                complemento="KM 60",
                cep="78195-000",
                bairro="Centro",
                municipio="Chapada dos Guimarães",
                uf="MT",
                email="contato@dojouemura.com.br",
                telefone="(65) 98111-1125"
            )

