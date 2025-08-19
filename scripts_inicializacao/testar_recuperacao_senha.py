#!/usr/bin/env python
"""
Script para testar as funcionalidades de recuperação de senha
"""
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from usuarios.models import Usuario
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def testar_usuarios():
    """Testa se existem usuários no sistema"""
    print("\n" + "="*60)
    print("TESTE DE USUÁRIOS NO SISTEMA")
    print("="*60)
    
    usuarios = Usuario.objects.all()
    print(f"Total de usuários: {usuarios.count()}")
    
    for usuario in usuarios:
        print(f"\n- ID: {usuario.id}")
        print(f"  Nome: {usuario.first_name} {usuario.last_name}")
        print(f"  Email: {usuario.email}")
        print(f"  Verificado: {usuario.email_verificado}")
        print(f"  Ativo: {usuario.is_active}")
        print(f"  Username: {usuario.username}")

def testar_tokens():
    """Testa a geração de tokens para recuperação de senha"""
    print("\n" + "="*60)
    print("TESTE DE GERAÇÃO DE TOKENS")
    print("="*60)
    
    usuarios = Usuario.objects.all()[:3]  # Testar com até 3 usuários
    
    for usuario in usuarios:
        try:
            # Gerar token para reset de senha
            token = default_token_generator.make_token(usuario)
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            
            print(f"\n- Usuário: {usuario.email}")
            print(f"  Token: {token}")
            print(f"  UID: {uid}")
            print(f"  Token válido: {default_token_generator.check_token(usuario, token)}")
            
        except Exception as e:
            print(f"\n- Erro ao gerar token para {usuario.email}: {e}")

def testar_verificacao_email():
    """Testa a verificação de email"""
    print("\n" + "="*60)
    print("TESTE DE VERIFICAÇÃO DE EMAIL")
    print("="*60)
    
    usuarios_nao_verificados = Usuario.objects.filter(email_verificado=False)
    usuarios_verificados = Usuario.objects.filter(email_verificado=True)
    
    print(f"Usuários não verificados: {usuarios_nao_verificados.count()}")
    print(f"Usuários verificados: {usuarios_verificados.count()}")
    
    if usuarios_nao_verificados.exists():
        print("\nUsuários que precisam de verificação:")
        for usuario in usuarios_nao_verificados:
            print(f"  - {usuario.email}")

def main():
    """Função principal"""
    print("INICIANDO TESTES DE RECUPERAÇÃO DE SENHA")
    print("="*60)
    
    try:
        testar_usuarios()
        testar_tokens()
        testar_verificacao_email()
        
        print("\n" + "="*60)
        print("TESTES CONCLUÍDOS COM SUCESSO!")
        print("="*60)
        
    except Exception as e:
        print(f"\nERRO durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
