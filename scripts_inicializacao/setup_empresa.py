#!/usr/bin/env python
"""
Script para configurar dados de exemplo da empresa Dojô Uemura
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from empresa.models import Empresa

def setup_empresa():
    """Configura dados de exemplo da empresa"""
    
    # Verificar se já existe uma empresa
    if Empresa.objects.exists():
        print("✅ Empresa já configurada!")
        empresa = Empresa.objects.first()
        print(f"   Nome: {empresa.nome_fantasia}")
        print(f"   CNPJ: {empresa.cnpj}")
        print(f"   Ativa: {'Sim' if empresa.ativo else 'Não'}")
        return empresa
    
    print("🚀 Configurando empresa Dojô Uemura...")
    
    # Criar empresa de exemplo
    empresa = Empresa.objects.create(
        cnpj="12.345.678/0001-90",
        nome_empresarial="DOJO UEMURA LTDA",
        nome_fantasia="Dojô Uemura",
        logradouro="Rua das Artes Marciais",
        numero="123",
        complemento="Sala 1",
        cep="78195-000",
        bairro="Centro",
        municipio="Chapada dos Guimarães",
        uf="MT",
        email="contato@dojouemura.com",
        telefone1="(65) 99999-9999",
        telefone2="(65) 98888-8888",
        situacao_cadastral="ATIVA",
        
        # Horários de funcionamento
        segunda_feira="8h às 10h, 13h às 22h",
        terca_feira="8h às 10h, 13h às 22h",
        quarta_feira="8h às 10h, 13h às 22h",
        quinta_feira="8h às 10h, 13h às 22h",
        sexta_feira="8h às 10h, 13h às 22h",
        sabado="8h às 12h",
        domingo="Fechado",
        
        # Redes sociais
        instagram="https://www.instagram.com/dojouemura",
        facebook="https://www.facebook.com/dojouemura",
        youtube="https://www.youtube.com/@dojouemura",
        
        ativo=True
    )
    
    print("✅ Empresa configurada com sucesso!")
    print(f"   Nome: {empresa.nome_fantasia}")
    print(f"   CNPJ: {empresa.cnpj}")
    print(f"   Endereço: {empresa.get_endereco_completo()}")
    print(f"   Telefones: {', '.join(empresa.get_telefones())}")
    print(f"   Email: {empresa.email}")
    print(f"   Horários ativos: {len(empresa.get_horarios_ativos())} dias")
    
    return empresa

def main():
    """Função principal"""
    try:
        empresa = setup_empresa()
        
        print("\n🎯 Próximos passos:")
        print("1. Acesse http://localhost:8000/admin/")
        print("2. Faça login com admin/admin")
        print("3. Vá para Empresa > Empresas")
        print("4. Edite os dados conforme necessário")
        print("5. Acesse http://localhost:8000/contato/ para ver a página")
        
    except Exception as e:
        print(f"❌ Erro ao configurar empresa: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
