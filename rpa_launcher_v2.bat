@echo off
title Launcher RPA TAMAPRINT v2.0 - Arquitectura Unificada
color 0A
echo.
echo ========================================
echo   LAUNCHER RPA TAMAPRINT v2.0
echo   Arquitectura Unificada
echo ========================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "rpa_launcher_v2.py" (
    echo ERROR: No se encontro rpa_launcher_v2.py en este directorio
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

echo Iniciando Launcher RPA v2.0...
echo Sistema unificado con arquitectura modular
echo.

:: Ejecutar el launcher v2
python rpa_launcher_v2.py

:: Si hay error, mostrar mensaje
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar el launcher v2.0
    echo Verifique que todas las dependencias esten instaladas
    echo.
)

pause
