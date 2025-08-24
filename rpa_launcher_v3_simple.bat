@echo off
echo ========================================
echo    AI4U | RPA TAMAPRINT v3.0
echo    Launcher Simplificado
echo ========================================
echo.

cd /d "%~dp0"

echo Iniciando launcher RPA...
python rpa_launcher_v3_simple.py

if %errorlevel% neq 0 (
    echo.
    echo Error al ejecutar el launcher
    echo Verifica que Python esté instalado y en el PATH
    pause
)

echo.
echo Launcher cerrado
pause
