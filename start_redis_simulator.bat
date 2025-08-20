@echo off
echo ========================================
echo    INICIANDO SIMULADOR REDIS
echo ========================================
echo.
echo NOTA: Este é um simulador para desenvolvimento
echo Para produção, instale o Redis real
echo.

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Iniciar simulador Redis (usando Celery com broker em memória)
echo Iniciando simulador Redis...
celery -A cadastro_pessoas worker --loglevel=info --pool=solo --broker=memory://

pause
