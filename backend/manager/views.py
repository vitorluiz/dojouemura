from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import InformacaoEmpresa
from .serializers import InformacaoEmpresaSerializer


@api_view(['GET'])
def informacao_empresa_view(request):
    """
    Endpoint para obter as informações da empresa.
    
    GET /api/v1/manager/info/
    
    Retorna as informações da empresa em formato JSON.
    Se não existir nenhum registro, cria um com dados padrão.
    """
    try:
        # Obtém a única instância das informações da empresa
        # Se não existir, cria uma com dados padrão
        informacao = InformacaoEmpresa.get_instance()
        
        # Serializa os dados para JSON
        serializer = InformacaoEmpresaSerializer(informacao)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Informações da empresa obtidas com sucesso.'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'data': None,
            'message': f'Erro ao obter informações da empresa: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
def atualizar_informacao_empresa_view(request):
    """
    Endpoint para atualizar as informações da empresa.
    
    PUT/PATCH /api/v1/manager/info/update/
    
    Atualiza as informações da empresa com os dados fornecidos.
    """
    try:
        # Obtém a única instância das informações da empresa
        informacao = InformacaoEmpresa.get_instance()
        
        # Atualiza os dados com base no request
        serializer = InformacaoEmpresaSerializer(
            informacao, 
            data=request.data, 
            partial=True  # Permite atualizações parciais
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Informações da empresa atualizadas com sucesso.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'data': None,
                'message': 'Dados inválidos.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'data': None,
            'message': f'Erro ao atualizar informações da empresa: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

