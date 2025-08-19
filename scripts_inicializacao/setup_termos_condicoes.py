#!/usr/bin/env python
"""
Script para configurar os termos e condições iniciais do sistema
"""
import os
import sys
import django

# Adicionar o diretório do projeto ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from empresa.models import TermosCondicoes

def criar_termos_responsabilidade():
    """Cria os termos de responsabilidade"""
    conteudo = """TERMOS DE RESPONSABILIDADE

Eu, {{RESPONSAVEL}}, responsável legal pelo(a) atleta {{NOME_ATLETA}}, declaro que:

1. Li e compreendi todas as informações sobre as atividades esportivas oferecidas pela {{NOME_EMPRESA}}.

2. Estou ciente de que a prática de artes marciais envolve riscos inerentes à atividade física e esportiva.

3. Autorizo a participação do(a) atleta nas atividades, treinos e eventos promovidos pela {{NOME_EMPRESA}}.

4. Comprometo-me a informar imediatamente sobre qualquer mudança no estado de saúde do(a) atleta.

5. Assumo total responsabilidade pela integridade física e bem-estar do(a) atleta durante as atividades.

6. Concordo em cumprir todas as normas e regulamentos estabelecidos pela {{NOME_EMPRESA}}.

7. Estou ciente de que a {{NOME_EMPRESA}} não se responsabiliza por acidentes decorrentes da prática esportiva.

Data: {{DATA_ATUAL}}
Local: {{MUNICIPIO}}/{{UF}}

Assinatura do Responsável: _____________________________
CPF: _____________________________"""

    TermosCondicoes.objects.update_or_create(
        tipo='responsabilidade',
        defaults={
            'titulo': 'Termos de Responsabilidade para Participação em Atividades Esportivas',
            'conteudo': conteudo,
            'ativo': True
        }
    )
    print("✓ Termos de responsabilidade criados/atualizados")

def criar_termos_medicas():
    """Cria os termos de condições médicas"""
    conteudo = """TERMOS DE CONDIÇÕES MÉDICAS

Eu, {{RESPONSAVEL}}, responsável legal pelo(a) atleta {{NOME_ATLETA}}, declaro que:

1. O(A) atleta está em condições físicas adequadas para participar das atividades esportivas.

2. Informei todas as condições médicas, alergias e limitações físicas do(a) atleta.

3. Estou ciente de que a prática de artes marciais requer boa condição física e mental.

4. Comprometo-me a informar imediatamente sobre qualquer mudança no estado de saúde.

5. Autorizo a equipe da {{NOME_EMPRESA}} a tomar medidas de emergência se necessário.

6. Assumo responsabilidade por qualquer consequência relacionada a informações médicas não fornecidas.

7. Estou ciente de que a {{NOME_EMPRESA}} pode solicitar atestado médico quando necessário.

CONDIÇÕES MÉDICAS DECLARADAS:
- Tipo sanguíneo: {{TIPO_SANGUINEO}}
- Alergias: {{ALERGIAS}}
- Condições médicas: {{CONDICOES_MEDICAS}}

Data: {{DATA_ATUAL}}
Local: {{MUNICIPIO}}/{{UF}}

Assinatura do Responsável: _____________________________
CPF: _____________________________"""

    TermosCondicoes.objects.update_or_create(
        tipo='medicas',
        defaults={
            'titulo': 'Termos de Condições Médicas e Autorização',
            'conteudo': conteudo,
            'ativo': True
        }
    )
    print("✓ Termos de condições médicas criados/atualizados")

def criar_termos_imagem():
    """Cria os termos de direito de uso de imagem"""
    conteudo = """DIREITO DE USO DE IMAGEM

Eu, {{RESPONSAVEL}}, responsável legal pelo(a) atleta {{NOME_ATLETA}}, autorizo a {{NOME_EMPRESA}} a:

1. Capturar imagens (fotos e vídeos) do(a) atleta durante atividades esportivas.

2. Utilizar essas imagens para fins promocionais, educativos e de divulgação.

3. Publicar as imagens em redes sociais, site oficial e materiais de marketing.

4. Compartilhar as imagens com parceiros e patrocinadores para fins promocionais.

5. Utilizar as imagens em campanhas publicitárias da {{NOME_EMPRESA}}.

LIMITAÇÕES:
- As imagens serão utilizadas de forma respeitosa e profissional
- Não serão utilizadas para fins comerciais sem autorização adicional
- O atleta pode solicitar a remoção de imagens específicas a qualquer momento

DURAÇÃO:
Esta autorização é válida durante todo o período de matrícula do(a) atleta na {{NOME_EMPRESA}}.

Data: {{DATA_ATUAL}}
Local: {{MUNICIPIO}}/{{UF}}

Assinatura do Responsável: _____________________________
CPF: _____________________________"""

    TermosCondicoes.objects.update_or_create(
        tipo='imagem',
        defaults={
            'titulo': 'Autorização para Uso de Imagem',
            'conteudo': conteudo,
            'ativo': True
        }
    )
    print("✓ Termos de uso de imagem criados/atualizados")

def main():
    """Função principal"""
    print("Configurando termos e condições iniciais...")
    print("=" * 50)
    
    try:
        criar_termos_responsabilidade()
        criar_termos_medicas()
        criar_termos_imagem()
        
        print("=" * 50)
        print("✓ Todos os termos e condições foram configurados com sucesso!")
        print("\nPróximos passos:")
        print("1. Acesse o admin do Django")
        print("2. Vá para 'Termos e Condições'")
        print("3. Personalize os textos conforme necessário")
        print("4. Use as variáveis {{NOME_EMPRESA}}, {{DATA_ATUAL}}, {{RESPONSAVEL}}, etc.")
        
    except Exception as e:
        print(f"❌ Erro ao configurar termos e condições: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
