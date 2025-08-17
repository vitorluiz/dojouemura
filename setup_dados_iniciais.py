#!/usr/bin/env python
"""
Script para criar dados iniciais no sistema Dojô Uemura
Execute: python setup_dados_iniciais.py
"""

import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from usuarios.models import Modalidade, TipoMatricula, StatusMatricula

def criar_modalidades():
    """Cria as modalidades esportivas disponíveis"""
    modalidades = [
        {'nome': 'Jiu-Jitsu', 'descricao': 'Arte marcial brasileira focada em técnicas de luta no chão', 'ordem': 1},
        {'nome': 'Judô', 'descricao': 'Arte marcial japonesa que utiliza técnicas de projeção e imobilização', 'ordem': 2},
        {'nome': 'Muay Thai', 'descricao': 'Arte marcial tailandesa conhecida como "boxe tailandês"', 'ordem': 3},
        {'nome': 'Boxe', 'descricao': 'Esporte de combate que utiliza apenas os punhos', 'ordem': 4},
        {'nome': 'Capoeira', 'descricao': 'Arte marcial afro-brasileira que combina luta, dança e música', 'ordem': 5},
    ]
    
    for modalidade_data in modalidades:
        modalidade, created = Modalidade.objects.get_or_create(
            nome=modalidade_data['nome'],
            defaults=modalidade_data
        )
        if created:
            print(f"✅ Modalidade criada: {modalidade.nome}")
        else:
            print(f"ℹ️  Modalidade já existe: {modalidade.nome}")

def criar_tipos_matricula():
    """Cria os tipos de matrícula disponíveis"""
    tipos = [
        {
            'nome': 'Projeto Social',
            'descricao': 'Matrícula gratuita para crianças e adolescentes de 6 a 18 anos, estudantes de escola regular',
            'gratuito': True,
            'taxa_inscricao': 50.00,
            'ordem': 1
        },
        {
            'nome': 'Modalidade Paga',
            'descricao': 'Matrícula paga para todas as modalidades disponíveis, com mensalidade',
            'gratuito': False,
            'taxa_inscricao': 0.00,
            'ordem': 2
        },
    ]
    
    for tipo_data in tipos:
        tipo, created = TipoMatricula.objects.get_or_create(
            nome=tipo_data['nome'],
            defaults=tipo_data
        )
        if created:
            print(f"✅ Tipo de matrícula criado: {tipo.nome}")
        else:
            print(f"ℹ️  Tipo de matrícula já existe: {tipo.nome}")

def criar_status_matricula():
    """Cria os status de matrícula disponíveis"""
    status = [
        {
            'nome': 'Pendente',
            'descricao': 'Matrícula em processo de análise e aprovação',
            'cor': '#ffc107',
            'ordem': 1
        },
        {
            'nome': 'Ativa',
            'descricao': 'Matrícula aprovada e ativa para participação nas aulas',
            'cor': '#28a745',
            'ordem': 2
        },
        {
            'nome': 'Suspensa',
            'descricao': 'Matrícula temporariamente suspensa por pendências',
            'cor': '#fd7e14',
            'ordem': 3
        },
        {
            'nome': 'Cancelada',
            'descricao': 'Matrícula cancelada definitivamente',
            'cor': '#dc3545',
            'ordem': 4
        },
    ]
    
    for status_data in status:
        status_obj, created = StatusMatricula.objects.get_or_create(
            nome=status_data['nome'],
            defaults=status_data
        )
        if created:
            print(f"✅ Status de matrícula criado: {status_obj.nome}")
        else:
            print(f"ℹ️  Status de matrícula já existe: {status_obj.nome}")

def main():
    """Função principal para executar a criação dos dados iniciais"""
    print("🚀 Iniciando criação de dados iniciais para o Dojô Uemura...")
    print("=" * 60)
    
    try:
        criar_modalidades()
        print("-" * 40)
        
        criar_tipos_matricula()
        print("-" * 40)
        
        criar_status_matricula()
        print("-" * 40)
        
        print("✅ Todos os dados iniciais foram criados com sucesso!")
        print("\n📊 Resumo dos dados criados:")
        print(f"   • Modalidades: {Modalidade.objects.count()}")
        print(f"   • Tipos de Matrícula: {TipoMatricula.objects.count()}")
        print(f"   • Status de Matrícula: {StatusMatricula.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
