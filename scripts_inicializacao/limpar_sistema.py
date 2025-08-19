#!/usr/bin/env python
"""
Script para limpeza e reset do sistema Dojô Uemura
Remove dados de teste e prepara para nova inicialização
"""
import os
import sys
import django
from pathlib import Path

def configurar_django():
    """Configura o ambiente Django"""
    try:
        # Adicionar o diretório raiz ao path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadastro_pessoas.settings')
        django.setup()
        
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        return False

def limpar_modalidades():
    """Remove todas as modalidades (exceto as básicas)"""
    try:
        from usuarios.models import Modalidade
        
        print("🗑️ Limpando modalidades...")
        
        # Contar modalidades existentes
        total = Modalidade.objects.count()
        print(f"   Modalidades encontradas: {total}")
        
        if total > 0:
            # Manter apenas as modalidades padrão
            modalidades_padrao = ['Jiu-Jitsu', 'Judô', 'Muay Thai', 'Boxe', 'Capoeira']
            
            for modalidade in Modalidade.objects.all():
                if modalidade.nome in modalidades_padrao:
                    print(f"   ✅ Mantendo: {modalidade.nome}")
                else:
                    print(f"   🗑️ Removendo: {modalidade.nome}")
                    modalidade.delete()
        
        print("✅ Modalidades limpas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar modalidades: {e}")
        return False

def limpar_termos_condicoes():
    """Remove todos os termos e condições"""
    try:
        from empresa.models import TermosCondicoes
        
        print("🗑️ Limpando termos e condições...")
        
        # Contar termos existentes
        total = TermosCondicoes.objects.count()
        print(f"   Termos encontrados: {total}")
        
        if total > 0:
            TermosCondicoes.objects.all().delete()
            print(f"   🗑️ {total} termos removidos")
        
        print("✅ Termos e condições limpos!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar termos: {e}")
        return False

def limpar_usuarios():
    """Remove usuários de teste"""
    try:
        from usuarios.models import Usuario
        
        print("🗑️ Limpando usuários de teste...")
        
        # Contar usuários existentes
        total = Usuario.objects.count()
        print(f"   Usuários encontrados: {total}")
        
        if total > 0:
            # Remover usuários não verificados (possíveis testes)
            usuarios_removidos = Usuario.objects.filter(email_verificado=False).count()
            Usuario.objects.filter(email_verificado=False).delete()
            print(f"   🗑️ Usuários não verificados removidos: {usuarios_removidos}")
        
        print("✅ Usuários limpos!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar usuários: {e}")
        return False

def limpar_mensagens_contato():
    """Remove mensagens de contato antigas"""
    try:
        from empresa.models import MensagemContato
        
        print("🗑️ Limpando mensagens de contato...")
        
        # Contar mensagens existentes
        total = MensagemContato.objects.count()
        print(f"   Mensagens encontradas: {total}")
        
        if total > 0:
            # Manter apenas as últimas 10 mensagens
            if total > 10:
                mensagens_para_remover = total - 10
                MensagemContato.objects.order_by('data_envio')[:mensagens_para_remover].delete()
                print(f"   🗑️ Mensagens antigas removidas: {mensagens_para_remover}")
            else:
                print("   ✅ Poucas mensagens, mantendo todas")
        
        print("✅ Mensagens de contato limpas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar mensagens: {e}")
        return False

def resetar_empresa():
    """Reseta dados da empresa para valores padrão"""
    try:
        from empresa.models import Empresa
        
        print("🔄 Resetando dados da empresa...")
        
        # Verificar se existe empresa
        if Empresa.objects.exists():
            empresa = Empresa.objects.first()
            print(f"   Empresa encontrada: {empresa.nome}")
            
            # Resetar para valores padrão
            empresa.nome = "Dojô Uemura"
            empresa.endereco = "Chapada dos Guimarães, MT"
            empresa.telefone = "(65) 99999-9999"
            empresa.email = "contato@dojouemura.com"
            empresa.horario_funcionamento = "Segunda a Sexta, das 8h às 20h"
            empresa.save()
            
            print("   ✅ Dados da empresa resetados!")
        else:
            print("   ℹ️ Nenhuma empresa encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao resetar empresa: {e}")
        return False

def main():
    """Função principal de limpeza"""
    print("🧹 LIMPEZA DO SISTEMA DOJÔ UEMURA")
    print("=" * 50)
    
    # Configurar Django
    if not configurar_django():
        print("❌ Falha na configuração do Django")
        return
    
    print("⚠️ ATENÇÃO: Esta operação irá limpar dados do sistema!")
    print("   - Usuários não verificados serão removidos")
    print("   - Termos e condições serão removidos")
    print("   - Mensagens antigas serão removidas")
    print("   - Dados da empresa serão resetados")
    
    resposta = input("\n🤔 Continuar com a limpeza? (s/N): ").lower()
    if resposta != 's':
        print("❌ Operação cancelada!")
        return
    
    print("\n🚀 Iniciando limpeza...")
    
    # Executar limpezas
    operacoes = [
        (limpar_modalidades, "Modalidades"),
        (limpar_termos_condicoes, "Termos e Condições"),
        (limpar_usuarios, "Usuários"),
        (limpar_mensagens_contato, "Mensagens de Contato"),
        (resetar_empresa, "Empresa")
    ]
    
    sucessos = 0
    for funcao, nome in operacoes:
        if funcao():
            sucessos += 1
        else:
            print(f"❌ Falha ao limpar: {nome}")
    
    # Resumo final
    print(f"\n{'='*50}")
    print("📊 RESUMO DA LIMPEZA")
    print(f"{'='*50}")
    print(f"✅ Operações realizadas com sucesso: {sucessos}/{len(operacoes)}")
    
    if sucessos == len(operacoes):
        print("🎉 SISTEMA LIMPO COM SUCESSO!")
        print("\n📝 Próximos passos:")
        print("   1. Execute 'inicializar_sistema.py' para reconfigurar")
        print("   2. Ou execute scripts individuais conforme necessário")
    else:
        print("⚠️ ALGUMAS OPERAÇÕES FALHARAM!")
        print("   Verifique os erros acima")
    
    print(f"\n🏋️ Dojô Uemura - Sistema de Gestão")
    print("=" * 50)

if __name__ == '__main__':
    main()
