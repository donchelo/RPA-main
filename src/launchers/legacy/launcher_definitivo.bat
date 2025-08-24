@echo off
echo ========================================
echo    RPA TAMAPRINT v3.0
echo    Launcher Definitivo
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
echo Iniciando launcher definitivo...
python launcher_definitivo.py

echo.
echo Launcher cerrado
pause
