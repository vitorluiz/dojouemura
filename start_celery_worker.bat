@echo off
echo ========================================
echo    INICIANDO WORKER DO CELERY
echo ========================================
echo.

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Iniciar worker do Celery
echo Iniciando worker do Celery...
celery -A cadastro_pessoas worker --loglevel=info --pool=solo

pause
