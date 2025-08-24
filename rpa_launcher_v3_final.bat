@echo off
chcp 65001 >nul
echo ========================================
echo    AI4U | RPA TAMAPRINT v3.0
echo    Launcher Final para Windows
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no esta instalado o no esta en el PATH
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado
echo.

echo Verificando archivos necesarios...
if not exist "rpa_launcher_v3_final.py" (
    echo Error: No se encontro rpa_launcher_v3_final.py
    pause
    exit /b 1
)

echo Archivos encontrados
echo.

echo Iniciando launcher RPA...
echo Presiona Ctrl+C para cerrar la aplicacion
echo.

python rpa_launcher_v3_final.py

if %errorlevel% neq 0 (
    echo.
    echo Error al ejecutar el launcher
    echo Codigo de error: %errorlevel%
    echo.
    echo Posibles soluciones:
    echo 1. Verifica que Python este instalado correctamente
    echo 2. Verifica que tkinter este disponible
    echo 3. Ejecuta como administrador si es necesario
    echo.
    pause
    exit /b 1
)

echo.
echo Launcher cerrado correctamente
pause
