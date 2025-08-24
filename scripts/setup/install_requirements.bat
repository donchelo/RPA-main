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
echo Opciones de instalacion disponibles:
echo.
echo 1. Instalacion COMPLETA (recomendada)
echo    - Todas las dependencias principales
echo    - Funcionalidades avanzadas (EasyOCR, procesamiento de imagenes)
echo    - Dependencias adicionales para mejor rendimiento
echo.
echo 2. Instalacion MINIMA
echo    - Solo dependencias esenciales
echo    - Funcionalidad basica
echo    - Menor espacio en disco
echo.
echo 3. Instalacion de DESARROLLO
echo    - Todas las dependencias principales
echo    - Herramientas de testing y desarrollo
echo    - Solo para desarrolladores
echo.

set /p choice="Seleccione el tipo de instalacion (1/2/3): "

if "%choice%"=="1" (
    set requirements_file=requirements.txt
    echo.
    echo Instalacion COMPLETA seleccionada
) else if "%choice%"=="2" (
    set requirements_file=requirements-minimal.txt
    echo.
    echo Instalacion MINIMA seleccionada
) else if "%choice%"=="3" (
    set requirements_file=requirements.txt
    set dev_requirements=requirements-dev.txt
    echo.
    echo Instalacion de DESARROLLO seleccionada
) else (
    echo Opcion invalida. Instalacion cancelada.
    pause
    exit /b 0
)

echo Dependencias que se instalaran:
if "%choice%"=="1" (
    echo - PyAutoGUI (automatizacion de GUI)
    echo - OpenCV (procesamiento de imagenes)
    echo - Tesseract/EasyOCR (reconocimiento de texto)
    echo - Schedule (programacion de tareas)
    echo - Dependencias adicionales para funcionalidad completa
) else if "%choice%"=="2" (
    echo - PyAutoGUI (automatizacion de GUI)
    echo - OpenCV (procesamiento de imagenes)
    echo - Tesseract (reconocimiento de texto basico)
    echo - Schedule (programacion de tareas)
    echo - Dependencias esenciales unicamente
) else if "%choice%"=="3" (
    echo - Todas las dependencias principales
    echo - Herramientas de testing (pytest, coverage)
    echo - Herramientas de formateo (black, flake8)
    echo - Herramientas de documentacion (sphinx)
    echo - Herramientas de profiling y debugging
)
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

:: Instalar dependencias principales
echo Instalando dependencias desde %requirements_file%...
python -m pip install -r %requirements_file%

:: Instalar dependencias de desarrollo si se selecciono
if defined dev_requirements (
    echo.
    echo Instalando dependencias de desarrollo desde %dev_requirements%...
    python -m pip install -r %dev_requirements%
)

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
    if "%choice%"=="2" (
        echo NOTA: Instalacion MINIMA completada.
        echo Algunas funcionalidades avanzadas no estaran disponibles.
        echo Para funcionalidad completa, ejecute este script nuevamente y seleccione opcion 1.
        echo.
    ) else if "%choice%"=="3" (
        echo NOTA: Instalacion de DESARROLLO completada.
        echo Todas las herramientas de desarrollo estan disponibles.
        echo.
    )
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