from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import socket
import logging

# Configurar logger específico para tarefas de email
logger = logging.getLogger('usuarios.tasks')

@shared_task(bind=True, queue='emails')
def enviar_email_verificacao_task(self, usuario_id, senha_temp):
    """
    Tarefa Celery para enviar email de verificação em background
    """
    logger.info(f"Iniciando tarefa de envio de email de verificação para usuário {usuario_id}")
    
    try:
        from .models import Usuario
        
        # Buscar o usuário
        usuario = Usuario.objects.get(id=usuario_id)
        logger.info(f"Usuário encontrado: {usuario.email} (ID: {usuario_id})")
        
        # Configurar timeout manualmente
        socket.setdefaulttimeout(30)  # Timeout de 30 segundos para tarefas
        logger.debug(f"Timeout SMTP configurado: 30 segundos")
        
        # Preparar o email
        subject = 'Ativação de Conta - Dojô Uemura'
        
        # Template simples para o email
        message = f"""
        Olá {usuario.first_name}!
        
        Sua conta foi criada com sucesso no Dojô Uemura.
        
        Sua senha temporária é: {senha_temp}
        
        Por favor, faça login e altere sua senha.
        
        Atenciosamente,
        Equipe Dojô Uemura
        """
        
        logger.debug(f"Email preparado - Assunto: {subject}, Destinatário: {usuario.email}")
        
        # Enviar o email
        resultado = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [usuario.email],
            fail_silently=False,
        )
        
        if resultado:
            logger.info(f"✅ Email de verificação enviado com sucesso para {usuario.email}")
            return {
                'status': 'success',
                'message': f'Email enviado para {usuario.email}',
                'usuario_id': usuario_id
            }
        else:
            logger.error(f"❌ Falha ao enviar email de verificação para {usuario.email}")
            return {
                'status': 'error',
                'message': 'Falha ao enviar email',
                'usuario_id': usuario_id
            }
            
    except Usuario.DoesNotExist:
        logger.error(f"❌ Usuário com ID {usuario_id} não encontrado")
        return {
            'status': 'error',
            'message': 'Usuário não encontrado',
            'usuario_id': usuario_id
        }
    except socket.timeout:
        logger.error(f"❌ Timeout na conexão SMTP ao enviar email para usuário {usuario_id}")
        return {
            'status': 'error',
            'message': 'Timeout na conexão SMTP',
            'usuario_id': usuario_id
        }
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao enviar email para usuário {usuario_id}: {e}", exc_info=True)
        return {
            'status': 'error',
            'message': f'Erro: {str(e)}',
            'usuario_id': usuario_id
        }

@shared_task(bind=True, queue='emails')
def enviar_email_recuperacao_senha_task(self, usuario_id, reset_url):
    """
    Tarefa Celery para enviar email de recuperação de senha
    """
    logger.info(f"Iniciando tarefa de envio de email de recuperação para usuário {usuario_id}")
    
    try:
        from .models import Usuario
        
        usuario = Usuario.objects.get(id=usuario_id)
        logger.info(f"Usuário encontrado: {usuario.email} (ID: {usuario_id})")
        
        subject = 'Recuperação de Senha - Dojô Uemura'
        message = f"""
        Olá {usuario.first_name}!
        
        Você solicitou a recuperação de senha para sua conta no Dojô Uemura.
        
        Para redefinir sua senha, clique no link abaixo:
        {reset_url}
        
        Se você não solicitou esta recuperação, ignore este email.
        
        Atenciosamente,
        Equipe Dojô Uemura
        """
        
        logger.debug(f"Email de recuperação preparado - Assunto: {subject}, Destinatário: {usuario.email}")
        
        resultado = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [usuario.email],
            fail_silently=False,
        )
        
        if resultado:
            logger.info(f"✅ Email de recuperação enviado com sucesso para {usuario.email}")
            return {
                'status': 'success',
                'message': f'Email de recuperação enviado para {usuario.email}',
                'usuario_id': usuario_id
            }
        else:
            logger.error(f"❌ Falha ao enviar email de recuperação para {usuario.email}")
            return {
                'status': 'error',
                'message': 'Falha ao enviar email de recuperação',
                'usuario_id': usuario_id
            }
            
    except Usuario.DoesNotExist:
        logger.error(f"❌ Usuário com ID {usuario_id} não encontrado")
        return {
            'status': 'error',
            'message': 'Usuário não encontrado',
            'usuario_id': usuario_id
        }
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao enviar email de recuperação para usuário {usuario_id}: {e}", exc_info=True)
        return {
            'status': 'error',
            'message': f'Erro: {str(e)}',
            'usuario_id': usuario_id
        }
