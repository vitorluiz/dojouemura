# backend/common/models.py
from django.db import models
from libs.uuid7 import uuid7

class TextoTermo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    identificador = models.SlugField(max_length=50, unique=True, help_text="Identificador único para a API (ex: 'responsabilidade')")
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField(help_text="Conteúdo do termo em formato Markdown")
    versao = models.PositiveIntegerField(default=1)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Texto de Termo"
        verbose_name_plural = "Textos de Termos"
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} (v{self.versao})"