import os
import logging
from celery import Celery
from celery.signals import setup_logging

# Configurar o módulo de configurações padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')

# Criar a instância do Celery
app = Celery('cadastro_pessoas')

# Usar configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descobrir tarefas em todos os apps Django
app.autodiscover_tasks()

# Configurar logging do Celery
@setup_logging.connect
def config_loggers(sender=None, **kwargs):
    from django.conf import settings
    if hasattr(settings, 'LOGGING'):
        import logging.config
        logging.config.dictConfig(settings.LOGGING)

@app.task(bind=True)
def debug_task(self):
    logger = logging.getLogger('celery')
    logger.info(f'Request: {self.request!r}')
    return f'Request: {self.request!r}'
