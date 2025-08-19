#!/usr/bin/env python
"""
Script para verificar dependentes/atletas no sistema
"""
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from usuarios.models import Usuario, Dependente

def verificar_dependentes():
    """Verifica se existem dependentes no sistema"""
    print("\n" + "="*60)
    print("VERIFICAÇÃO DE DEPENDENTES/ATLETAS NO SISTEMA")
    print("="*60)
    
    usuarios = Usuario.objects.all()
    print(f"Total de usuários: {usuarios.count()}")
    
    for usuario in usuarios:
        print(f"\n- Usuário: {usuario.first_name} {usuario.last_name}")
        print(f"  Email: {usuario.email}")
        print(f"  Verificado: {usuario.email_verificado}")
        print(f"  Ativo: {usuario.is_active}")
        
        dependentes = Dependente.objects.filter(usuario=usuario)
        print(f"  Total de atletas: {dependentes.count()}")
        
        if dependentes.exists():
            for dependente in dependentes:
                print(f"    - Atleta: {dependente.nome}")
                print(f"      CPF: {dependente.cpf}")
                print(f"      Parentesco: {dependente.get_parentesco_display()}")
                print(f"      Data Nascimento: {dependente.data_nascimento}")
                print(f"      Escola: {dependente.escola}")
                print(f"      Escolaridade: {dependente.get_escolaridade_display()}")
                print(f"      Turno: {dependente.get_turno_display()}")
                print(f"      Termos aceitos: Responsabilidade={dependente.termo_responsabilidade}, Imagem={dependente.termo_uso_imagem}")
        else:
            print("    - Nenhum atleta cadastrado")

def main():
    """Função principal"""
    print("INICIANDO VERIFICAÇÃO DE DEPENDENTES")
    print("="*60)
    
    try:
        verificar_dependentes()
        
        print("\n" + "="*60)
        print("VERIFICAÇÃO CONCLUÍDA!")
        print("="*60)
        
    except Exception as e:
        print(f"\nERRO durante a verificação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
