#!/usr/bin/env python
"""
Script para configurar modalidades do Dojô Uemura
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from usuarios.models import Modalidade

def setup_modalidades():
    """Configura as modalidades padrão do Dojô Uemura"""
    
    modalidades_data = [
        {
            'nome': 'Jiu-Jitsu',
            'descricao': 'Arte marcial brasileira focada em técnicas de luta no chão e finalizações. Desenvolve técnica, estratégia e disciplina.',
            'ordem': 1,
            'ativa': True
        },
        {
            'nome': 'Judô',
            'descricao': 'Arte marcial japonesa que significa "caminho suave". Foca em projeções e técnicas de chão.',
            'ordem': 2,
            'ativa': True
        },
        {
            'nome': 'Muay Thai',
            'descricao': 'Arte marcial tailandesa conhecida como "arte dos oito membros". Desenvolve condicionamento físico e autodefesa.',
            'ordem': 3,
            'ativa': True
        },
        {
            'nome': 'Boxe',
            'descricao': 'Esporte de combate que desenvolve coordenação motora, condicionamento cardiovascular e autodefesa.',
            'ordem': 4,
            'ativa': True
        },
        {
            'nome': 'Capoeira',
            'descricao': 'Arte marcial brasileira que combina luta, dança e música. Desenvolve flexibilidade e ritmo.',
            'ordem': 5,
            'ativa': True
        }
    ]
    
    print("🏋️ Configurando modalidades do Dojô Uemura...")
    
    for data in modalidades_data:
        modalidade, created = Modalidade.objects.get_or_create(
            nome=data['nome'],
            defaults=data
        )
        
        if created:
            print(f"✅ Modalidade '{data['nome']}' criada com sucesso!")
        else:
            print(f"ℹ️ Modalidade '{data['nome']}' já existe.")
    
    print(f"\n🎯 Total de modalidades configuradas: {Modalidade.objects.count()}")
    print("📝 Para adicionar imagens, acesse o admin Django e edite cada modalidade.")

if __name__ == '__main__':
    setup_modalidades()
