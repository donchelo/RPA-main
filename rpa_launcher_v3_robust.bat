@echo off
chcp 65001 >nul
echo ========================================
echo    AI4U | RPA TAMAPRINT v3.0
echo    Launcher Robusto para Windows
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo Verificando archivos necesarios...
if not exist "rpa_launcher_v3_robust.py" (
    echo ❌ Error: No se encontró rpa_launcher_v3_robust.py
    pause
    exit /b 1
)

echo ✅ Archivos encontrados
echo.

echo Iniciando launcher RPA...
echo Presiona Ctrl+C para cerrar la aplicación
echo.

python rpa_launcher_v3_robust.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error al ejecutar el launcher
    echo Código de error: %errorlevel%
    echo.
    echo Posibles soluciones:
    echo 1. Verifica que Python esté instalado correctamente
    echo 2. Verifica que tkinter esté disponible
    echo 3. Ejecuta como administrador si es necesario
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Launcher cerrado correctamente
pause
