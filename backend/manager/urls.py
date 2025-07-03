from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('info/', views.informacao_empresa_view, name='informacao_empresa'),
    path('info/update/', views.atualizar_informacao_empresa_view, name='atualizar_informacao_empresa'),
]

