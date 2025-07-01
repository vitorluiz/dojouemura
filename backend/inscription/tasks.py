# backend/inscription/tasks.py

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML

from users.models import Responsavel
from students.models import Dependente, TermoAceite
from common.models import TextoTermo

import datetime

@shared_task
def gerar_e_salvar_termos_pdf_task(dependente_id):
    """
    Tarefa Celery para gerar todos os PDFs para um novo dependente.
    """
    try:
        dependente = Dependente.objects.get(id=dependente_id)
        responsavel = dependente.responsavel
        termos_texto = TextoTermo.objects.filter(ativo=True)

        for termo_texto in termos_texto:
            # 1. Preparar o contexto para personalizar o termo
            endereco_completo = f"{responsavel.logradouro}, {responsavel.numero} - {responsavel.bairro}, {responsavel.cidade}/{responsavel.estado}"
            
            context = {
                'nome_responsavel': responsavel.nome_completo,
                'cpf_responsavel': responsavel.cpf,
                'rg_responsavel': responsavel.rg,
                'endereco_completo_responsavel': endereco_completo,
                'nome_dependente': dependente.nome_completo,
                'data_nascimento_dependente': dependente.data_nascimento.strftime('%d/%m/%Y'),
                'cpf_dependente': dependente.cpf or "Não informado",
                'parentesco_contato_emergencia': dependente.parentesco or "Não informado",
                'nome_contato_emergencia': dependente.contato_emergencia_nome,
                'telefone_emergencia': dependente.contato_emergencia_telefone,
                'descrever_condicoes_medicas': dependente.condicoes_medicas or "Nenhuma condição médica informada.",
                'localidade': responsavel.cidade,
                'data_atual': datetime.date.today().strftime('%d de %B de %Y'),
                'titulo_termo': termo_texto.titulo,
                'conteudo_termo': termo_texto.conteudo,
            }

            # 2. Renderizar o template HTML com o contexto
            html_string = render_to_string('inscription/termo_pdf.html', context)
            html = HTML(string=html_string)
            
            # 3. Gerar o PDF em memória
            pdf_file = html.write_pdf()

            # 4. Criar e salvar o objeto TermoAceite
            nome_arquivo = f"termo_{termo_texto.identificador}_{dependente.id}.pdf"
            
            TermoAceite.objects.create(
                dependente=dependente,
                nome_termo=termo_texto.titulo,
                pdf_gerado=ContentFile(pdf_file, name=nome_arquivo),
                # Aqui poderíamos adicionar o IP e outras evidências
                # que viriam do payload do frontend.
                ip_assinatura="127.0.0.1" # Placeholder
            )
        
        # Após gerar todos os PDFs, delega a tarefa de envio de e-mail
        enviar_email_confirmacao_task.delay(responsavel.id)

    except Dependente.DoesNotExist:
        # Lidar com o caso de o dependente não ser encontrado
        print(f"Dependente com id {dependente_id} não encontrado.")
    except Exception as e:
        # É uma boa prática logar qualquer outro erro que possa ocorrer
        print(f"Ocorreu um erro ao gerar PDFs para o dependente {dependente_id}: {e}")


@shared_task
def enviar_email_confirmacao_task(responsavel_id):
    """
    Tarefa Celery para enviar o e-mail de confirmação com os PDFs em anexo.
    """
    try:
        responsavel = Responsavel.objects.get(id=responsavel_id)
        
        # Encontra todos os termos aceitos para todos os dependentes deste responsável
        termos_aceitos = TermoAceite.objects.filter(dependente__responsavel=responsavel)

        if not termos_aceitos.exists():
            print(f"Nenhum termo encontrado para o responsável {responsavel_id}. O e-mail não será enviado.")
            return

        assunto = "Confirmação de Inscrição - Dojô Eumura"
        mensagem = f"Olá {responsavel.nome_completo},\n\nSua inscrição no Dojô Eumura foi recebida com sucesso!\n\nEm anexo, você encontra os termos de responsabilidade assinados eletronicamente.\n\nAtenciosamente,\nEquipe Dojô Eumura."
        
        email = EmailMessage(
            assunto,
            mensagem,
            'nao-responda@dojoeumura.com', # Remetente
            [responsavel.email], # Destinatário
        )

        for termo in termos_aceitos:
            termo.pdf_gerado.open(mode='rb')
            email.attach(
                termo.pdf_gerado.name,
                termo.pdf_gerado.read(),
                'application/pdf'
            )
            termo.pdf_gerado.close()

        email.send()

    except Responsavel.DoesNotExist:
        print(f"Responsável com id {responsavel_id} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail para o responsável {responsavel_id}: {e}")
