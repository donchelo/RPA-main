@echo off
title Instalar Dependencias RPA TAMAPRINT
color 0B
echo.
echo ==========================================
echo   INSTALADOR DE DEPENDENCIAS RPA
echo ==========================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "requirements.txt" (
    echo ERROR: No se encontro requirements.txt en este directorio
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
    echo Asegurese de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

:: Mostrar información
echo Este script instalara todas las dependencias necesarias para el sistema RPA
echo.
echo Dependencias que se instalaran:
echo - PyAutoGUI (automatizacion de GUI)
echo - OpenCV (procesamiento de imagenes)
echo - Tesseract/EasyOCR (reconocimiento de texto)
echo - Schedule (programacion de tareas)
echo - Y otras dependencias de soporte
echo.

set /p confirm="Desea continuar? (s/n): "
if /i "%confirm%" neq "s" (
    echo Instalacion cancelada
    pause
    exit /b 0
)

echo.
echo ==========================================
echo   INSTALANDO DEPENDENCIAS...
echo ==========================================
echo.

:: Actualizar pip primero
echo Actualizando pip...
python -m pip install --upgrade pip
echo.

:: Instalar dependencias
echo Instalando dependencias desde requirements.txt...
python -m pip install -r requirements.txt

:: Verificar instalacion
if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo   INSTALACION COMPLETADA EXITOSAMENTE
    echo ==========================================
    echo.
    echo Todas las dependencias han sido instaladas correctamente.
    echo.
    echo IMPORTANTE: Asegurese tambien de tener Tesseract OCR instalado:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo Ya puede ejecutar el sistema RPA con:
    echo - Doble clic en rpa_launcher.bat
    echo - O ejecutar: python rpa_launcher.py
    echo.
) else (
    echo.
    echo ==========================================
    echo   ERROR EN LA INSTALACION
    echo ==========================================
    echo.
    echo Hubo un error instalando las dependencias.
    echo Por favor:
    echo 1. Verifique su conexion a internet
    echo 2. Ejecute este script como administrador
    echo 3. Contacte soporte tecnico si el problema persiste
    echo.
)

pause