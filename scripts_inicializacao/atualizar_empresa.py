#!/usr/bin/env python
"""
Script para atualizar dados da empresa existente para Dojô Uemura
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
django.setup()

from empresa.models import Empresa

def atualizar_empresa():
    """Atualiza dados da empresa para Dojô Uemura"""
    
    # Buscar empresa existente
    empresa = Empresa.objects.first()
    if not empresa:
        print("❌ Nenhuma empresa encontrada!")
        return None
    
    print(f"🔄 Atualizando empresa: {empresa.nome_fantasia}")
    
    # Atualizar dados
    empresa.cnpj = "12.345.678/0001-90"
    empresa.nome_empresarial = "DOJO UEMURA LTDA"
    empresa.nome_fantasia = "Dojô Uemura"
    empresa.logradouro = "Rua das Artes Marciais"
    empresa.numero = "123"
    empresa.complemento = "Sala 1"
    empresa.cep = "78195-000"
    empresa.bairro = "Centro"
    empresa.municipio = "Chapada dos Guimarães"
    empresa.uf = "MT"
    empresa.email = "contato@dojouemura.com"
    empresa.telefone1 = "(65) 99999-9999"
    empresa.telefone2 = "(65) 98888-8888"
    empresa.situacao_cadastral = "ATIVA"
    
    # Horários de funcionamento
    empresa.segunda_feira = "8h às 10h, 13h às 22h"
    empresa.terca_feira = "8h às 10h, 13h às 22h"
    empresa.quarta_feira = "8h às 10h, 13h às 22h"
    empresa.quinta_feira = "8h às 10h, 13h às 22h"
    empresa.sexta_feira = "8h às 10h, 13h às 22h"
    empresa.sabado = "8h às 12h"
    empresa.domingo = "Fechado"
    
    # Redes sociais
    empresa.instagram = "https://www.instagram.com/dojouemura"
    empresa.facebook = "https://www.facebook.com/dojouemura"
    empresa.youtube = "https://www.youtube.com/@dojouemura"
    
    empresa.ativo = True
    
    # Salvar alterações
    empresa.save()
    
    print("✅ Empresa atualizada com sucesso!")
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
        empresa = atualizar_empresa()
        
        if empresa:
            print("\n🎯 Próximos passos:")
            print("1. Acesse http://localhost:8000/admin/")
            print("2. Faça login com admin/admin")
            print("3. Vá para Empresa > Empresas")
            print("4. Verifique se os dados estão corretos")
            print("5. Acesse http://localhost:8000/contato/ para ver a página")
            print("6. Verifique se o footer está atualizado")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar empresa: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
