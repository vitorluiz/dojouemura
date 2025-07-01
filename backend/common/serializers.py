# backend/common/serializers.py
from rest_framework import serializers
from .models import TextoTermo

class TextoTermoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextoTermo
        fields = ['titulo', 'conteudo']