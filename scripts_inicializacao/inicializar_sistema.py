#!/usr/bin/env python
"""
Script principal para inicialização completa do sistema Dojô Uemura
Executa todos os scripts de configuração na ordem correta
"""
import os
import sys
import subprocess
import time

def executar_script(script_path, descricao):
    """Executa um script Python e exibe o resultado"""
    print(f"\n{'='*60}")
    print(f"🚀 EXECUTANDO: {descricao}")
    print(f"📁 Script: {script_path}")
    print(f"{'='*60}")
    
    try:
        # Executar o script
        resultado = subprocess.run([sys.executable, script_path], 
                                 capture_output=True, text=True, cwd=os.getcwd())
        
        # Exibir saída
        if resultado.stdout:
            print("✅ SAÍDA:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️ AVISOS:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print(f"✅ {descricao} executado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao executar {descricao}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar {script_path}: {e}")
        return False

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente"""
    print("🔍 Verificando ambiente...")
    
    # Verificar se está no diretório correto
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script do diretório raiz do projeto!")
        print("   Diretório atual:", os.getcwd())
        print("   Procure por: manage.py")
        return False
    
    # Verificar se o ambiente virtual está ativo
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️ AVISO: Ambiente virtual não detectado!")
        print("   Recomendado: ativar com 'venv\\Scripts\\activate'")
        resposta = input("   Continuar mesmo assim? (s/N): ").lower()
        if resposta != 's':
            return False
    
    print("✅ Ambiente verificado!")
    return True

def main():
    """Função principal de inicialização"""
    print("🏋️ INICIALIZAÇÃO DO SISTEMA DOJÔ UEMURA")
    print("=" * 60)
    
    # Verificar ambiente
    if not verificar_ambiente():
        return
    
    # Lista de scripts para executar (em ordem)
    scripts = [
        ('setup_empresa.py', 'Configuração da Empresa'),
        ('setup_modalidades.py', 'Configuração das Modalidades'),
        ('setup_termos_condicoes.py', 'Configuração dos Termos e Condições'),
        ('testar_empresa.py', 'Teste da Configuração')
    ]
    
    print(f"\n📋 Executando {len(scripts)} scripts de inicialização...")
    
    # Executar cada script
    sucessos = 0
    for script, descricao in scripts:
        if executar_script(script, descricao):
            sucessos += 1
        else:
            print(f"❌ Falha em: {descricao}")
            resposta = input("   Continuar com os próximos scripts? (s/N): ").lower()
            if resposta != 's':
                break
        
        # Pausa entre scripts
        if script != scripts[-1][0]:  # Se não for o último
            print("\n⏳ Aguardando 2 segundos...")
            time.sleep(2)
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DA INICIALIZAÇÃO")
    print(f"{'='*60}")
    print(f"✅ Scripts executados com sucesso: {sucessos}/{len(scripts)}")
    
    if sucessos == len(scripts):
        print("🎉 SISTEMA INICIALIZADO COM SUCESSO!")
        print("\n📝 Próximos passos:")
        print("   1. Acesse /admin/ para configurar usuários")
        print("   2. Adicione imagens às modalidades")
        print("   3. Teste o sistema completo")
    else:
        print("⚠️ ALGUNS SCRIPTS FALHARAM!")
        print("   Verifique os erros acima e execute novamente")
    
    print(f"\n🏋️ Dojô Uemura - Sistema de Gestão")
    print("=" * 60)

if __name__ == '__main__':
    main()
