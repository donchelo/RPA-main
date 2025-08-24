@echo off
title Launcher RPA TAMAPRINT
color 0A
echo.
echo ================================
echo   LAUNCHER RPA TAMAPRINT
echo ================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encontro main.py en este directorio
    echo Asegurese de ejecutar este script desde la carpeta RPA-main
    echo.
    pause
    exit /b 1
)

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instale Python desde https://python.org
    echo.
    pause
    exit /b 1
)

echo Iniciando Launcher RPA...
echo.

:: Ejecutar el launcher
python rpa_launcher.py

:: Si hay error, mostrar mensaje
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar el launcher
    echo Verifique que todas las dependencias esten instaladas
    echo.
)

pause