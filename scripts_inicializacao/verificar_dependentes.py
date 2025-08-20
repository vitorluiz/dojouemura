#!/usr/bin/env python
"""
Script para verificar atletas/atletas no sistema
"""
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from usuarios.models import Usuario, Atleta

def verificar_atletas():
    """Verifica se existem atletas no sistema"""
    print("\n" + "="*60)
    print("VERIFICAÇÃO DE ATLETAS NO SISTEMA")
    print("="*60)
    
    usuarios = Usuario.objects.all()
    print(f"Total de usuários: {usuarios.count()}")
    
    for usuario in usuarios:
        print(f"\n- Usuário: {usuario.first_name} {usuario.last_name}")
        print(f"  Email: {usuario.email}")
        print(f"  Verificado: {usuario.email_verificado}")
        print(f"  Ativo: {usuario.is_active}")
        
        atletas = Atleta.objects.filter(usuario=usuario)
        print(f"  Total de atletas: {atletas.count()}")
        
        if atletas.exists():
            for atleta in atletas:
                print(f"    - Atleta: {atleta.nome}")
                print(f"      CPF: {atleta.cpf}")
                print(f"      Parentesco: {atleta.get_parentesco_display()}")
                print(f"      Data Nascimento: {atleta.data_nascimento}")
                print(f"      Escola: {atleta.escola}")
                print(f"      Escolaridade: {atleta.get_escolaridade_display()}")
                print(f"      Turno: {atleta.get_turno_display()}")
                print(f"      Termos aceitos: Responsabilidade={atleta.termo_responsabilidade}, Imagem={atleta.termo_uso_imagem}")
        else:
            print("    - Nenhum atleta cadastrado")

def main():
    """Função principal"""
    print("INICIANDO VERIFICAÇÃO DE ATLETAS")
    print("="*60)
    
    try:
        verificar_atletas()
        
        print("\n" + "="*60)
        print("VERIFICAÇÃO CONCLUÍDA!")
        print("="*60)
        
    except Exception as e:
        print(f"\nERRO durante a verificação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
