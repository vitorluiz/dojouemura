# backend/common/migrations/0002_popular_termos.py

from django.db import migrations

# Conteúdo dos seus ficheiros .md
TERMO_RESPONSABILIDADE = """
Eu, [NOME_DO_RESPONSAVEL], portador(a) do CPF nº [CPF_DO_RESPONSAVEL], RG nº [RG_DO_RESPONSAVEL], residente e domiciliado(a) à [ENDERECO_COMPLETO_DO_RESPONSAVEL], declaro, para os devidos fins, que sou responsável legal por [NOME_DO_DEPENDENTE], nascido(a) em [DATA_NASCIMENTO_DEPENDENTE], CPF nº [CPF_DEPENDENTE].

Autorizo a participação do(a) menor nas atividades físicas, esportivas e educacionais promovidas por [RAZAO_SOCIAL], denominado [NOME_FANTASIA], CNPJ nº [CNPJ], localizado na [LOGRADOURO], nº [NUMERO], [COMPLEMENTO], Bairro [BAIRRO], Município de [MUNICIPIO]/[UF], CEP [CEP], com atendimento pelo e-mail [EMAIL_EMPRESA] e telefone [TELEFONE_EMPRESA].

Declaro estar ciente de que todas as atividades seguem protocolos de segurança e orientação técnica profissional, e assumo integral responsabilidade pela conduta e bem-estar do(a) menor durante sua permanência no estabelecimento, isentando a instituição e seus colaboradores de quaisquer responsabilidades civis, penais ou médicas em decorrência de acidentes ou imprevistos resultantes de conduta inadequada, descumprimento de orientações, condições pré-existentes de saúde não informadas ou uso indevido das instalações.

Autorizo, ainda, em casos de emergência, que a equipe técnica da instituição tome todas as medidas necessárias à preservação da saúde e integridade física do(a) menor, inclusive acionando atendimento médico de urgência e informando-me por meio do telefone de contato [TELEFONE_EMERGENCIA].

[LOCALIDADE], [DATA_ATUAL]

Assinatura do(a) Responsável  
Nome: [NOME_DO_RESPONSAVEL]  
CPF: [CPF_DO_RESPONSAVEL]  RG: [RG_DO_RESPONSAVEL]
"""

TERMO_IMAGEM = """
TERMO DE CESSÃO DE DIREITO DE USO DE IMAGEM

Eu, [NOME_DO_RESPONSAVEL], portador(a) do CPF nº [CPF_DO_RESPONSAVEL], RG nº [RG_DO_RESPONSAVEL], residente à [ENDERECO_COMPLETO_DO_RESPONSAVEL], responsável legal por [NOME_DO_DEPENDENTE], nascido(a) em [DATA_NASCIMENTO_DEPENDENTE], AUTORIZO de forma gratuita, definitiva e irrevogável, o uso da imagem do(a) menor supracitado(a), captada durante aulas, eventos, treinamentos, campeonatos e demais atividades promovidas por [RAZAO_SOCIAL], denominado [NOME_FANTASIA], CNPJ nº [CNPJ], com sede na [LOGRADOURO], nº [NUMERO], [COMPLEMENTO], Bairro [BAIRRO], Município de [MUNICIPIO]/[UF], CEP [CEP].

A presente autorização abrange o uso da imagem e voz do(a) menor em vídeos, fotos, transmissões ao vivo, publicações em redes sociais, materiais promocionais, institucionais e educativos, sem limite de tempo ou número de vezes, sem qualquer compensação financeira, em território nacional ou internacional.

Declaro estar ciente de que o uso da imagem será feito de forma respeitosa, sem violar a moral, a ética ou os direitos do menor, e que tenho total ciência da possibilidade de revogação mediante solicitação formal enviada ao e-mail [EMAIL_EMPRESA].

[LOCALIDADE], [DATA_ATUAL]
  
Assinatura do(a) Responsável  
Nome: [NOME_DO_RESPONSAVEL]  
CPF: [CPF_DO_RESPONSAVEL]  
RG: [RG_DO_RESPONSAVEL]
"""

TERMO_MEDICO = """
TERMO DE CONDIÇÃO MÉDICA E AUTORIZAÇÃO PARA ATENDIMENTO DE URGÊNCIA

Eu, [NOME_DO_RESPONSAVEL], portador(a) do CPF nº [CPF_DO_RESPONSAVEL], RG nº [RG_DO_RESPONSAVEL], responsável legal pelo(a) menor [NOME_DO_DEPENDENTE], nascido(a) em [DATA_NASCIMENTO_DEPENDENTE], declaro para os devidos fins que:
1. O(a) menor encontra-se em boas condições de saúde física e psicológica para participar das atividades promovidas por [RAZAO_SOCIAL], denominado [NOME_FANTASIA], CNPJ nº [CNPJ], com sede na [LOGRADOURO], nº [NUMERO], [COMPLEMENTO], Bairro [BAIRRO], Município de [MUNICIPIO]/[UF], CEP [CEP].
2. Informo que o(a) menor possui as seguintes condições médicas, restrições ou alergias:  
[DESCREVER_CONDICOES_MEDICAS]  
3. Em caso de necessidade ou emergência médica, AUTORIZO a equipe da instituição a tomar as providências necessárias ao atendimento do(a) menor, inclusive acionando serviços de urgência e transporte até a unidade hospitalar mais próxima, isentando a instituição e seus representantes legais de qualquer ônus ou responsabilidade decorrente de tais medidas.
4. Autorizo o contato imediato ao número: [TELEFONE_EMERGENCIA], pertencente a [NOME_CONTATO_EMERGENCIA], com vínculo de [PARENTESCO_CONTATO_EMERGENCIA].
Declaro, por fim, que estou ciente e de pleno acordo com os termos deste documento, firmando-o para que produza seus devidos efeitos legais.
[LOCALIDADE], [DATA_ATUAL]
Assinatura do(a) Responsável  
Nome: [NOME_DO_RESPONSAVEL]  
CPF: [CPF_DO_RESPONSAVEL]  
RG: [RG_DO_RESPONSAVEL]
"""

def popular_termos(apps, schema_editor):
    TextoTermo = apps.get_model('common', 'TextoTermo')
    
    termos_a_criar = [
        {
            "identificador": "responsabilidade",
            "titulo": "Termo de Responsabilidade",
            "conteudo": TERMO_RESPONSABILIDADE.strip()
        },
        {
            "identificador": "imagem",
            "titulo": "Termo de Cessão de Direito de Uso de Imagem",
            "conteudo": TERMO_IMAGEM.strip()
        },
        {
            "identificador": "medica",
            "titulo": "Termo de Condição Médica e Atendimento de Urgência",
            "conteudo": TERMO_MEDICO.strip()
        },
    ]

    for termo_data in termos_a_criar:
        TextoTermo.objects.update_or_create(
            identificador=termo_data["identificador"],
            defaults=termo_data
        )

def remover_termos(apps, schema_editor):
    TextoTermo = apps.get_model('common', 'TextoTermo')
    TextoTermo.objects.filter(identificador__in=['responsabilidade', 'imagem', 'medica']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(popular_termos, reverse_code=remover_termos),
    ]
