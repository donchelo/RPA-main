#!/usr/bin/env python3
"""
Script para verificar las dependencias instaladas del sistema RPA TAMAPRINT
"""

import sys
import importlib
import subprocess
from typing import Dict, List, Tuple

# Lista de dependencias principales
MAIN_DEPENDENCIES = {
    'pyautogui': 'PyAutoGUI',
    'cv2': 'OpenCV',
    'PIL': 'Pillow',
    'numpy': 'NumPy',
    'schedule': 'Schedule',
    'psutil': 'psutil',
    'colorama': 'Colorama',
    'requests': 'Requests',
    'yaml': 'PyYAML',
    'pytesseract': 'pytesseract',
    'easyocr': 'EasyOCR',
    'torch': 'PyTorch',
    'skimage': 'scikit-image',
    'matplotlib': 'Matplotlib',
    'loguru': 'Loguru',
    'jsonschema': 'jsonschema'
}

# Lista de dependencias de desarrollo
DEV_DEPENDENCIES = {
    'pytest': 'pytest',
    'pytest_cov': 'pytest-cov',
    'pytest_mock': 'pytest-mock',
    'black': 'black',
    'flake8': 'flake8',
    'mypy': 'mypy',
    'sphinx': 'sphinx',
    'memory_profiler': 'memory-profiler'
}

# Dependencias críticas que deben estar instaladas
CRITICAL_DEPENDENCIES = ['pyautogui', 'cv2', 'PIL', 'numpy', 'schedule', 'psutil']

def check_python_version() -> bool:
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def check_dependency(dep_name: str, display_name: str) -> Tuple[bool, str]:
    """Verifica si una dependencia está instalada"""
    try:
        importlib.import_module(dep_name)
        return True, f"✅ {display_name} - Instalado"
    except ImportError:
        return False, f"❌ {display_name} - No instalado"

def check_tesseract() -> Tuple[bool, str]:
    """Verifica si Tesseract OCR está instalado"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, f"✅ Tesseract OCR - {version_line}"
        else:
            return False, "❌ Tesseract OCR - No encontrado"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "❌ Tesseract OCR - No encontrado"

def check_pip_packages() -> Dict[str, str]:
    """Obtiene información de paquetes instalados via pip"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            packages = {}
            for line in result.stdout.split('\n')[2:]:  # Saltar header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        packages[parts[0].lower()] = parts[1]
            return packages
    except:
        pass
    return {}

def main():
    """Función principal"""
    print("=" * 60)
    print("🔍 VERIFICADOR DE DEPENDENCIAS - RPA TAMAPRINT")
    print("=" * 60)
    print()
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    print()
    print("📦 VERIFICANDO DEPENDENCIAS PRINCIPALES")
    print("-" * 40)
    
    # Verificar dependencias principales
    main_status = {}
    critical_errors = []
    
    for dep_name, display_name in MAIN_DEPENDENCIES.items():
        is_installed, message = check_dependency(dep_name, display_name)
        main_status[dep_name] = is_installed
        print(message)
        
        if not is_installed and dep_name in CRITICAL_DEPENDENCIES:
            critical_errors.append(display_name)
    
    print()
    print("🔧 VERIFICANDO DEPENDENCIAS DE DESARROLLO")
    print("-" * 40)
    
    # Verificar dependencias de desarrollo
    dev_status = {}
    for dep_name, display_name in DEV_DEPENDENCIES.items():
        is_installed, message = check_dependency(dep_name, display_name)
        dev_status[dep_name] = is_installed
        print(message)
    
    print()
    print("🔍 VERIFICANDO TESSERACT OCR")
    print("-" * 40)
    
    # Verificar Tesseract
    tesseract_ok, tesseract_message = check_tesseract()
    print(tesseract_message)
    
    print()
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("-" * 40)
    
    # Contar dependencias instaladas
    main_installed = sum(main_status.values())
    main_total = len(main_status)
    dev_installed = sum(dev_status.values())
    dev_total = len(dev_status)
    
    print(f"Dependencias principales: {main_installed}/{main_total} instaladas")
    print(f"Dependencias de desarrollo: {dev_installed}/{dev_total} instaladas")
    print(f"Tesseract OCR: {'✅ Instalado' if tesseract_ok else '❌ No instalado'}")
    
    # Verificar paquetes pip para versiones
    print()
    print("📋 VERSIONES DE PAQUETES PRINCIPALES")
    print("-" * 40)
    
    pip_packages = check_pip_packages()
    important_packages = ['pyautogui', 'opencv-python', 'pillow', 'numpy', 'schedule']
    
    for pkg in important_packages:
        version = pip_packages.get(pkg, 'No encontrado')
        print(f"{pkg}: {version}")
    
    print()
    print("=" * 60)
    
    # Resultado final
    if critical_errors:
        print("❌ VERIFICACIÓN FALLIDA")
        print(f"Faltan dependencias críticas: {', '.join(critical_errors)}")
        print()
        print("💡 SOLUCIÓN:")
        print("Ejecute: pip install -r requirements.txt")
        sys.exit(1)
    elif not tesseract_ok:
        print("⚠️  VERIFICACIÓN PARCIAL")
        print("Todas las dependencias Python están instaladas, pero falta Tesseract OCR")
        print()
        print("💡 SOLUCIÓN:")
        print("Descargue e instale Tesseract OCR desde:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
    else:
        print("✅ VERIFICACIÓN EXITOSA")
        print("Todas las dependencias están instaladas correctamente")
        print()
        print("🚀 El sistema RPA está listo para usar")
        print("Ejecute: python rpa_launcher.py")

if __name__ == "__main__":
    main()
