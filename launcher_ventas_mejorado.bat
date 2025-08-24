@echo off
echo ========================================
echo RPA TAMAPRINT v3.0 - Launcher Ventas
echo ========================================
echo.
echo Iniciando launcher mejorado para ordenes de venta...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.7 o superior
    pause
    exit /b 1
)

REM Ejecutar el launcher
python launcher_ventas_mejorado.py

REM Si hay un error, pausar para ver el mensaje
if errorlevel 1 (
    echo.
    echo ERROR: El launcher se cerró con errores
    pause
)

echo.
echo Launcher cerrado.
pause
