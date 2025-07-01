# backend/inscription/urls.py
from django.urls import path
from .views import InscricaoAPIView

urlpatterns = [
    path('inscricoes/', InscricaoAPIView.as_view(), name='api-inscricao'),
]