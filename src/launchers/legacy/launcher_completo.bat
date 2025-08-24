@echo off
echo ========================================
echo    RPA TAMAPRINT v3.0
echo    Launcher Completo - Procesamiento Automatico
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo Error: Python no encontrado
    pause
    exit /b 1
)

echo.
echo Iniciando launcher completo...
python launcher_completo.py

echo.
echo Launcher cerrado
pause
