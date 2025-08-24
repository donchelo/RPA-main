@echo off
chcp 65001 >nul
title "AI4U RPA - Ordenes de Produccion"

echo.
echo ========================================
echo  AI4U RPA - Ordenes de Produccion
echo ========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor, instale Python 3.8+ y vuelva a intentar
    pause
    exit /b 1
)

:: Cambiar al directorio del proyecto
cd /d "%~dp0..\.."

:: Verificar que existe el launcher
if not exist "src\launchers\launcher_produccion_simple.py" (
    echo ERROR: No se encontro el launcher de produccion
    echo Verificar que el archivo launcher_produccion_simple.py existe
    pause
    exit /b 1
)

:: Verificar dependencias
echo Verificando dependencias...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Tkinter no esta disponible
    echo Instalando dependencias...
    pip install -r requirements.txt
)

:: Ejecutar el launcher
echo.
echo Iniciando Launcher de Ordenes de Produccion...
echo.
python "src\launchers\launcher_produccion_simple.py"

:: Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: El launcher se cerro con errores
    echo Verificar los logs para mas detalles
    pause
)

echo.
echo Launcher cerrado.
pause
