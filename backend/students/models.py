# backend/students/models.py

import random
import string
from django.db import models
from libs.uuid7 import uuid7
from users.models import Responsavel

def gerar_codigo_aluno():
    """Gera um código alfanumérico único de 9 dígitos para o aluno."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

class Dependente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    codigo_aluno = models.CharField(
        max_length=9,
        unique=True,
        default=gerar_codigo_aluno,
        help_text="Código único do aluno para identificação e QR Code"
    )
    status = models.CharField(
        max_length=20,
        default='Pendente',
        help_text="Status do aluno (Ex: Pendente, Ativo, Inativo)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        related_name='dependentes',
        help_text="O responsável por este dependente"
    )
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, help_text="CPF do dependente (opcional)")
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    escola = models.CharField(max_length=255, blank=True, null=True)
    serie_periodo = models.CharField(max_length=100, blank=True, null=True)
    condicoes_medicas = models.TextField(blank=True, null=True, help_text="Descrição de condições médicas, alergias, etc.")
    contato_emergencia_nome = models.CharField(max_length=255)
    contato_emergencia_telefone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Dependente"
        verbose_name_plural = "Dependentes"
        ordering = ['nome_completo']

    def __str__(self):
        return f"{self.nome_completo} ({self.codigo_aluno})"


class HistoricoEsportivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    dependente = models.ForeignKey(Dependente, on_delete=models.CASCADE, related_name='historico_esportivo')
    esporte_modalidade = models.CharField(max_length=100)
    faixa_graduacao = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Histórico Esportivo"
        verbose_name_plural = "Históricos Esportivos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.esporte_modalidade} - {self.faixa_graduacao}"


class TermoAceite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    dependente = models.ForeignKey(Dependente, on_delete=models.CASCADE, related_name='termos_aceitos')
    nome_termo = models.CharField(max_length=255, help_text="Identificação do termo assinado (Ex: Termo de Uso de Imagem)")
    pdf_gerado = models.FileField(upload_to='termos_assinados/', help_text="Arquivo PDF com a assinatura eletrônica")
    ip_assinatura = models.GenericIPAddressField()
    geolocalizacao = models.CharField(max_length=100, blank=True, null=True, help_text="Latitude e Longitude (opcional)")
    data_aceite = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Termo de Aceite"
        verbose_name_plural = "Termos de Aceite"
        ordering = ['-data_aceite']

    def __str__(self):
        return f"Termo '{self.nome_termo}' aceito por {self.dependente.nome_completo}"
