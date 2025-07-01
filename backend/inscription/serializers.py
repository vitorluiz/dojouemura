# backend/inscription/serializers.py

from rest_framework import serializers
from users.models import Responsavel
from students.models import Dependente, HistoricoEsportivo

class HistoricoEsportivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoEsportivo
        fields = ['esporte', 'faixa', 'graduacao']

class DependenteSerializer(serializers.ModelSerializer):
    historico_esportivo = HistoricoEsportivoSerializer(many=True, required=False)

    class Meta:
        model = Dependente
        # Lista de campos que vêm do frontend para o dependente
        fields = [
            'nome_completo', 'cpf', 'data_nascimento', 'parentesco',
            'escola_nome', 'escola_serie', 'escola_periodo',
            'plano_saude_qual', 'alergias_quais', 'medicamentos_quais', 
            'condicoes_medicas', 'contato_emergencia_nome', 
            'contato_emergencia_telefone', 'historico_esportivo'
        ]

class InscricaoSerializer(serializers.Serializer):
    """
    Este é o serializer principal. Ele valida a estrutura completa do JSON
    que recebemos do frontend.
    """
    # Validação para o objeto 'responsavel'
    cpf = serializers.CharField(source='responsavel.cpf')
    rg = serializers.CharField(source='responsavel.rg')
    nome_completo_responsavel = serializers.CharField(source='responsavel.nome_completo')
    telefone = serializers.CharField(source='responsavel.telefone')
    email = serializers.EmailField(source='responsavel.email')

    # Validação para o objeto 'endereco'
    cep = serializers.CharField()
    logradouro = serializers.CharField(source='endereco.logradouro')
    numero = serializers.CharField(source='endereco.numero')
    complemento = serializers.CharField(source='endereco.complemento', required=False, allow_blank=True)
    bairro = serializers.CharField(source='endereco.bairro')
    cidade = serializers.CharField(source='endereco.localidade') # Note a correspondência de nomes
    estado = serializers.CharField(source='endereco.uf') # Note a correspondência de nomes

    # Validação para a lista de 'dependentes'
    dependentes = DependenteSerializer(many=True)

    def create(self, validated_data):
        # Esta é a lógica principal. Onde os dados são salvos.
        
        # 1. Cria ou atualiza o Responsável
        responsavel_data = validated_data.pop('responsavel')
        endereco_data = validated_data.pop('endereco')
        
        responsavel, created = Responsavel.objects.update_or_create(
            cpf=responsavel_data['cpf'],
            defaults={
                'nome_completo': responsavel_data['nome_completo'],
                'rg': responsavel_data['rg'],
                'email': responsavel_data['email'],
                'telefone': responsavel_data['telefone'],
                'cep': validated_data['cep'],
                'logradouro': endereco_data['logradouro'],
                'numero': endereco_data['numero'],
                'complemento': endereco_data.get('complemento', ''),
                'bairro': endereco_data['bairro'],
                'cidade': endereco_data['localidade'],
                'estado': endereco_data['uf'],
            }
        )

        # 2. Cria os Dependentes e o seu Histórico Esportivo
        dependentes_data = validated_data.pop('dependentes')
        for dependente_data in dependentes_data:
            historico_data = dependente_data.pop('historico_esportivo', [])
            
            dependente = Dependente.objects.create(
                responsavel=responsavel, 
                **dependente_data
            )

            for item_historico in historico_data:
                HistoricoEsportivo.objects.create(
                    dependente=dependente, 
                    **item_historico
                )
            
            # AQUI é onde chamamos a nossa tarefa Celery!
            from .tasks import gerar_e_salvar_termos_pdf_task
            gerar_e_salvar_termos_pdf_task.delay(str(dependente.id))

        return validated_data
