@echo off
chcp 65001 >nul
title AI4U | RPA - Órdenes de Venta

echo.
echo ========================================
echo    AI4U | RPA - Órdenes de Venta
echo ========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instale Python 3.8+ y vuelva a intentar
    pause
    exit /b 1
)

:: Cambiar al directorio del proyecto
cd /d "%~dp0..\.."

:: Verificar que existe el launcher
if not exist "src\launchers\launcher_ventas.py" (
    echo ERROR: No se encontró el launcher de ventas
    echo Verificar que el archivo launcher_ventas.py existe
    pause
    exit /b 1
)

:: Verificar dependencias
echo Verificando dependencias...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Tkinter no está disponible
    echo Instalando dependencias...
    pip install -r requirements.txt
)

:: Ejecutar el launcher
echo.
echo Iniciando Launcher de Órdenes de Venta...
echo.
python "src\launchers\launcher_ventas.py"

:: Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: El launcher se cerró con errores
    echo Verificar los logs para más detalles
    pause
)

echo.
echo Launcher cerrado.
pause
