@echo off
echo ========================================
echo RPA TAMAPRINT v3.0 - Launcher Ventas FUNCIONAL
echo ========================================
echo.
echo Iniciando launcher FUNCIONAL para ordenes de venta...
echo Este launcher ejecuta el RPA real para procesar pedidos en SAP
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

REM Verificar que existan las dependencias del RPA
if not exist "rpa" (
    echo ERROR: No se encontró el directorio 'rpa'
    echo Asegúrate de estar en el directorio correcto del proyecto
    pause
    exit /b 1
)

REM Ejecutar el launcher FUNCIONAL
python launcher_funcional.py

REM Si hay un error, pausar para ver el mensaje
if errorlevel 1 (
    echo.
    echo ERROR: El launcher se cerró con errores
    pause
)

echo.
echo Launcher cerrado.
pause
