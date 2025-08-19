@echo off
chcp 65001 >nul
echo.
echo 🏋️ INICIALIZAÇÃO AUTOMÁTICA - DOJÔ UEMURA
echo ================================================
echo.
echo Este script irá executar todos os scripts de inicialização
echo na ordem correta para configurar o sistema completo.
echo.
echo ⚠️  ATENÇÃO: Certifique-se de que:
echo    - O ambiente virtual está ativado
echo    - O Django está configurado
echo    - O banco de dados está criado
echo.
pause

echo.
echo 🚀 Iniciando configuração automática...
echo.

REM Ativar ambiente virtual (se existir)
if exist "..\venv\Scripts\activate.bat" (
    echo 🔧 Ativando ambiente virtual...
    call "..\venv\Scripts\activate.bat"
    echo ✅ Ambiente virtual ativado!
) else (
    echo ⚠️  Ambiente virtual não encontrado!
    echo    Certifique-se de que está na pasta correta
    pause
    exit /b 1
)

echo.
echo 📋 Executando scripts de inicialização...
echo.

REM Executar script principal
python inicializar_sistema.py

echo.
echo 🎯 Inicialização concluída!
echo.
echo 📝 Próximos passos:
echo    1. Acesse o admin Django: http://localhost:8000/admin/
echo    2. Configure usuários e permissões
echo    3. Adicione imagens às modalidades
echo    4. Teste o sistema completo
echo.
echo 🏋️ Dojô Uemura - Sistema de Gestão
echo ================================================
pause
