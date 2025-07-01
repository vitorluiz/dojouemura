# backend/common/admin.py
from django.contrib import admin
from .models import TextoTermo

@admin.register(TextoTermo)
class TextoTermoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'identificador', 'versao', 'ativo', 'updated_at')
    search_fields = ('titulo', 'identificador', 'conteudo')
    list_filter = ('ativo',)