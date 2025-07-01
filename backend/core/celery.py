# backend/core/celery.py

import os
from celery import Celery

# Define o módulo de configurações do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria a instância da aplicação Celery
app = Celery('core')

# Carrega as configurações do Celery a partir do settings.py do Django
# O namespace='CELERY' significa que todas as configurações do Celery
# no settings.py devem começar com CELERY_ (ex: CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre e carrega automaticamente as tarefas de todas as apps registadas
# O Celery irá procurar por um ficheiro chamado 'tasks.py' em cada app.
app.autodiscover_tasks()