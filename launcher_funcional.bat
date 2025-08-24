@echo off
echo ========================================
echo   RPA TAMAPRINT v3.0 - Launcher Funcional
echo ========================================
echo.
echo Iniciando sistema...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior
    pause
    exit /b 1
)

REM Verificar si estamos en el directorio correcto
if not exist "launcher_funcional.py" (
    echo ERROR: No se encontró launcher_funcional.py
    echo Asegúrate de ejecutar este archivo desde el directorio del proyecto
    pause
    exit /b 1
)

REM Ejecutar el launcher
echo Ejecutando Launcher Funcional...
python launcher_funcional.py

REM Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo ERROR: El launcher se cerró con errores
    echo Revisa los logs para más detalles
    pause
)

echo.
echo Launcher cerrado.
pause
