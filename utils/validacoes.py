import re
import requests
from django.core.exceptions import ValidationError
from datetime import date

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


def buscar_cep(cep):
    """
    Busca informações do CEP usando a API ViaCEP
    Retorna um dicionário com os dados do endereço ou None se não encontrar
    """
    # Limpar CEP (remover caracteres especiais)
    cep_limpo = re.sub(r'[^0-9]', '', cep)
    
    if len(cep_limpo) != 8:
        return None
    
    try:
        # Fazer requisição para a API ViaCEP
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            
            # Verificar se o CEP foi encontrado
            if not dados.get('erro'):
                return {
                    'cep': dados.get('cep'),
                    'logradouro': dados.get('logradouro'),
                    'bairro': dados.get('bairro'),
                    'cidade': dados.get('localidade'),
                    'uf': dados.get('uf'),
                    'complemento': dados.get('complemento')
                }
        
        return None
        
    except requests.RequestException:
        # Em caso de erro na requisição, retornar None
        return None


def validar_cep(cep):
    """
    Valida se o CEP é válido e existe
    Retorna os dados do endereço se válido
    """
    dados = buscar_cep(cep)
    if dados is None:
        raise ValidationError('CEP inválido ou não encontrado')
    return dados