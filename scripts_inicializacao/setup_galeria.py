#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar a galeria do Dojô Uemura
Copiar e organizar imagens do diretório de fotos para o projeto
"""

import os
import shutil
import glob
from pathlib import Path
import argparse

def setup_galeria():
    """Configura a galeria com as imagens do diretório de fotos"""
    
    print("🥋 Dojô Uemura - Configuração da Galeria")
    print("=" * 50)
    
    # Diretório de origem (suas fotos)
    fotos_origem = r"D:\FotosDojoUemura\Jiu-jitsu 24062025 Graduação"
    
    # Diretório de destino no projeto
    destino_projeto = "static/assets/img/galeria"
    
    # Verificar se o diretório de origem existe
    if not os.path.exists(fotos_origem):
        print(f"❌ Diretório de origem não encontrado: {fotos_origem}")
        print("Por favor, verifique o caminho e execute novamente.")
        return False
    
    # Criar diretório de destino se não existir
    os.makedirs(destino_projeto, exist_ok=True)
    
    print(f"📁 Diretório de origem: {fotos_origem}")
    print(f"📁 Diretório de destino: {destino_projeto}")
    print()
    
    # Encontrar todas as imagens no diretório de origem
    extensoes = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    imagens_encontradas = []
    
    for extensao in extensoes:
        imagens_encontradas.extend(glob.glob(os.path.join(fotos_origem, extensao)))
        imagens_encontradas.extend(glob.glob(os.path.join(fotos_origem, "**", extensao), recursive=True))
    
    if not imagens_encontradas:
        print("❌ Nenhuma imagem encontrada no diretório de origem")
        return False
    
    print(f"📸 Encontradas {len(imagens_encontradas)} imagens")
    print()
    
    # Copiar imagens com nomes organizados
    imagens_copiadas = []
    contador = 1
    
    for imagem_origem in imagens_encontradas[:12]:  # Limitar a 12 imagens para a galeria
        # Obter extensão do arquivo
        _, extensao = os.path.splitext(imagem_origem)
        
        # Criar nome organizado baseado no tipo de imagem
        nome_arquivo = f"dojo_imagem_{contador:02d}{extensao.lower()}"
        
        # Caminho de destino
        destino_arquivo = os.path.join(destino_projeto, nome_arquivo)
        
        try:
            # Copiar arquivo
            shutil.copy2(imagem_origem, destino_arquivo)
            imagens_copiadas.append(nome_arquivo)
            print(f"✅ Copiado: {os.path.basename(imagem_origem)} → {nome_arquivo}")
            contador += 1
        except Exception as e:
            print(f"❌ Erro ao copiar {os.path.basename(imagem_origem)}: {e}")
    
    print()
    print(f"🎉 Configuração concluída! {len(imagens_copiadas)} imagens copiadas")
    
    # Criar arquivo de configuração da galeria
    criar_config_galeria(imagens_copiadas, destino_projeto)
    
    return True

def criar_config_galeria(imagens, diretorio):
    """Cria arquivo de configuração para a galeria"""
    
    config_file = os.path.join(diretorio, "config_galeria.txt")
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("🥋 Dojô Uemura - Configuração da Galeria\n")
        f.write("=" * 50 + "\n\n")
        f.write("Imagens disponíveis para uso na galeria:\n\n")
        
        for i, imagem in enumerate(imagens, 1):
            f.write(f"{i:2d}. {imagem}\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("Para usar estas imagens na galeria:\n\n")
        f.write("1. Atualize o template home.html\n")
        f.write("2. Substitua os caminhos das imagens\n")
        f.write("3. Use o formato: {% static 'assets/img/galeria/nome_arquivo' %}\n\n")
        f.write("Exemplo:\n")
        f.write('<img src="{% static \'assets/img/galeria/dojo_imagem_01.jpg\' %}" ')
        f.write('alt="Dojô Uemura" class="img-fluid rounded shadow-sm">\n')
    
    print(f"📝 Arquivo de configuração criado: {config_file}")

def atualizar_template_galeria():
    """Atualiza o template com as imagens copiadas"""
    
    template_file = "usuarios/templates/usuarios/home.html"
    
    if not os.path.exists(template_file):
        print(f"❌ Template não encontrado: {template_file}")
        return False
    
    # Verificar se existem imagens na galeria
    galeria_dir = "static/assets/img/galeria"
    if not os.path.exists(galeria_dir):
        print(f"❌ Diretório da galeria não encontrado: {galeria_dir}")
        return False
    
    # Encontrar imagens na galeria
    extensoes = ['*.jpg', '*.jpeg', '*.png']
    imagens_galeria = []
    
    for extensao in extensoes:
        imagens_galeria.extend(glob.glob(os.path.join(galeria_dir, extensao)))
    
    if not imagens_galeria:
        print("❌ Nenhuma imagem encontrada na galeria")
        return False
    
    print(f"📸 Encontradas {len(imagens_galeria)} imagens na galeria")
    print("🔄 Atualizando template...")
    
    # Ler o template
    with open(template_file, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Substituir imagens da galeria
    imagens_galeria = sorted(imagens_galeria)[:6]  # Limitar a 6 imagens
    
    # Padrões para substituição
    padroes_antigos = [
        "{% static 'assets/img/jiujitsu1.jpg' %}",
        "{% static 'assets/img/jiujitsu2.jpg' %}",
        "{% static 'assets/img/graduacao1.jpg' %}",
        "{% static 'assets/img/treino1.jpg' %}",
        "{% static 'assets/img/meditacao1.jpg' %}",
        "{% static 'assets/img/familia1.jpg' %}"
    ]
    
    # Novos caminhos
    novos_caminhos = []
    for i, imagem in enumerate(imagens_galeria):
        nome_arquivo = os.path.basename(imagem)
        novo_caminho = f"{{% static 'assets/img/galeria/{nome_arquivo}' %}}"
        novos_caminhos.append(novo_caminho)
    
    # Fazer as substituições
    for i, padrao_antigo in enumerate(padroes_antigos):
        if i < len(novos_caminhos):
            conteudo = conteudo.replace(padrao_antigo, novos_caminhos[i])
    
    # Salvar o template atualizado
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print("✅ Template atualizado com sucesso!")
    return True

def main():
    """Função principal"""
    
    parser = argparse.ArgumentParser(description='Configurar galeria do Dojô Uemura')
    parser.add_argument('--setup', action='store_true', help='Configurar galeria com imagens')
    parser.add_argument('--update-template', action='store_true', help='Atualizar template com imagens da galeria')
    parser.add_argument('--all', action='store_true', help='Executar todas as operações')
    
    args = parser.parse_args()
    
    if args.all or args.setup:
        if setup_galeria():
            print("\n🎯 Próximo passo: Atualizar o template")
        else:
            print("\n❌ Falha na configuração da galeria")
            return
    
    if args.all or args.update_template:
        if atualizar_template_galeria():
            print("\n🎉 Galeria configurada com sucesso!")
        else:
            print("\n❌ Falha na atualização do template")
            return
    
    if not any([args.setup, args.update_template, args.all]):
        print("🥋 Dojô Uemura - Configuração da Galeria")
        print("=" * 50)
        print("Uso:")
        print("  python setup_galeria.py --setup          # Configurar galeria")
        print("  python setup_galeria.py --update-template # Atualizar template")
        print("  python setup_galeria.py --all            # Executar tudo")
        print()
        print("Para mais informações, consulte o README_GALERIA.md")

if __name__ == "__main__":
    main()
