from rest_framework import serializers
from .models import InformacaoEmpresa


class InformacaoEmpresaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo InformacaoEmpresa.
    Usado para converter os dados do modelo em JSON para a API.
    """
    
    class Meta:
        model = InformacaoEmpresa
        fields = [
            'id',
            'razao_social',
            'nome_fantasia', 
            'cnpj',
            'logradouro',
            'numero',
            'complemento',
            'cep',
            'bairro',
            'municipio',
            'uf',
            'email',
            'telefone',
            'criado_em',
            'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

