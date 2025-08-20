#!/usr/bin/env python
"""
Script para testar o Celery
"""
import os
import django
import logging
from celery import current_app

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

def testar_celery():
    """Testa se o Celery está funcionando"""
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("="*60)
    logger.info("TESTE DO CELERY")
    logger.info("="*60)
    
    try:
        # Verificar se o Celery está configurado
        logger.info("1. Verificando configuração do Celery...")
        app = current_app
        logger.info(f"   [OK] App Celery: {app}")
        logger.info(f"   [OK] Broker: {app.conf.broker_url}")
        logger.info(f"   [OK] Result Backend: {app.conf.result_backend}")
        
        # Verificar se as tarefas estão registradas
        logger.info("\n2. Verificando tarefas registradas...")
        tarefas_registradas = app.tasks.keys()
        tarefas_emails = [t for t in tarefas_registradas if 'email' in t.lower()]
        
        logger.info(f"   [OK] Total de tarefas: {len(tarefas_registradas)}")
        logger.info(f"   [OK] Tarefas de email: {len(tarefas_emails)}")
        
        for tarefa in tarefas_emails:
            logger.info(f"      - {tarefa}")
        
        # Testar execução de tarefa simples
        logger.info("\n3. Testando execução de tarefa...")
        from cadastro_pessoas.celery import debug_task
        
        # Executar tarefa de teste
        resultado = debug_task.delay()
        logger.info(f"   [OK] Tarefa de teste criada: {resultado.id}")
        
        # Aguardar resultado
        logger.info("   [WAIT] Aguardando resultado...")
        resultado_final = resultado.get(timeout=10)
        logger.info(f"   [OK] Resultado recebido: {resultado_final}")
        
        logger.info("\n" + "="*60)
        logger.info("[OK] CELERY FUNCIONANDO PERFEITAMENTE!")
        logger.info("="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"\n[ERRO] ERRO no teste do Celery: {e}")
        logger.error(f"   Tipo de erro: {type(e).__name__}")
        return False

if __name__ == '__main__':
    testar_celery()
