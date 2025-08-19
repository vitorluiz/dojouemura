#!/usr/bin/env python
"""
Script para testar se os dados da empresa estão sendo carregados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from empresa.models import Empresa

def testar_empresa():
    """Testa se os dados da empresa estão sendo carregados"""
    
    print("🔍 Testando dados da empresa...")
    
    # Verificar se existe empresa
    empresas = Empresa.objects.all()
    print(f"Total de empresas no banco: {empresas.count()}")
    
    if empresas.exists():
        empresa = empresas.first()
        print(f"\n✅ Empresa encontrada:")
        print(f"   Nome: {empresa.nome_fantasia}")
        print(f"   CNPJ: {empresa.cnpj}")
        print(f"   Ativa: {'Sim' if empresa.ativo else 'Não'}")
        print(f"   Email: {empresa.email}")
        print(f"   Telefone 1: {empresa.telefone1}")
        print(f"   Telefone 2: {empresa.telefone2}")
        print(f"   Endereço: {empresa.get_endereco_completo()}")
        print(f"   Horários: {len(empresa.get_horarios_ativos())} dias")
        
        # Testar context processor
        from empresa.context_processors import empresa_info
        from django.test import RequestFactory
        
        # Criar request fake
        factory = RequestFactory()
        request = factory.get('/')
        
        # Executar context processor
        context = empresa_info(request)
        print(f"\n🔧 Context processor retornou:")
        print(f"   empresa_info: {context.get('empresa_info')}")
        
        if context.get('empresa_info'):
            print(f"   ✅ Context processor funcionando!")
        else:
            print(f"   ❌ Context processor não retornou dados!")
            
    else:
        print("❌ Nenhuma empresa encontrada no banco!")
    
    return empresas.exists()

def main():
    """Função principal"""
    try:
        sucesso = testar_empresa()
        
        if sucesso:
            print("\n🎯 Próximos passos:")
            print("1. Verifique se o servidor foi reiniciado após adicionar o context processor")
            print("2. Acesse http://localhost:8000/contato/")
            print("3. Verifique o console do navegador para erros")
            print("4. Verifique se o template está usando 'empresa_info' corretamente")
        
    except Exception as e:
        print(f"❌ Erro ao testar empresa: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
