# backend/core/__init__.py

# Isto garante que a app Celery é carregada quando o Django inicia
from .celery import app as celery_app

__all__ = ('celery_app',)