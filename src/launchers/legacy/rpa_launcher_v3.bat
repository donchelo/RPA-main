@echo off
echo ========================================
echo    AI4U | RPA TAMAPRINT v3.0
echo    Launcher con Modulos Unificados
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

REM Verificar si el archivo principal existe
if not exist "rpa_launcher_v3.py" (
    echo ERROR: No se encontró el archivo rpa_launcher_v3.py
    echo Asegúrate de estar en el directorio correcto del proyecto
    pause
    exit /b 1
)

echo Iniciando Sistema RPA TAMAPRINT v3.0...
echo.
echo Características:
echo - Módulo de Órdenes de Venta
echo - Módulo de Órdenes de Producción
echo - Interfaz gráfica unificada
echo - Selección de módulos
echo - Monitoreo automático
echo.

REM Ejecutar el launcher
python rpa_launcher_v3.py

REM Si hay un error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: El sistema se cerró inesperadamente
    echo Revisa los logs para más detalles
    pause
)

echo.
echo Sistema RPA TAMAPRINT v3.0 cerrado
pause
