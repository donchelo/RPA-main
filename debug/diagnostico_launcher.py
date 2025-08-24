#!/usr/bin/env python3
"""
Diagnóstico del Launcher RPA
Identifica problemas en el sistema de launcher
"""

import os
import sys
import json
import glob
import time
from datetime import datetime

def check_directories():
    """Verifica que existan los directorios necesarios"""
    print("🔍 Verificando directorios...")
    
    base_dir = "data/outputs_json"
    directories = [
        os.path.join(base_dir, "01_Pendiente"),
        os.path.join(base_dir, "02_Procesando"),
        os.path.join(base_dir, "03_Completado"),
        os.path.join(base_dir, "04_Error"),
        os.path.join(base_dir, "05_Archivado")
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - NO EXISTE")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"   📁 Directorio creado")
            except Exception as e:
                print(f"   ❌ Error creando directorio: {e}")

def check_files():
    """Verifica archivos importantes"""
    print("\n🔍 Verificando archivos importantes...")
    
    files_to_check = [
        "rpa/modules/sales_order/sales_order_handler.py",
        "rpa/modules/sales_order/sales_order_config.yaml",
        "rpa/rpa_with_state_machine.py",
        "rpa/vision/main.py",
        "requirements.txt"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NO EXISTE")

def check_pending_files():
    """Verifica archivos pendientes"""
    print("\n🔍 Verificando archivos pendientes...")
    
    pending_dir = "data/outputs_json/01_Pendiente"
    if os.path.exists(pending_dir):
        json_files = glob.glob(os.path.join(pending_dir, "*.json"))
        print(f"📁 Archivos pendientes encontrados: {len(json_files)}")
        
        for file_path in json_files[:5]:  # Mostrar solo los primeros 5
            filename = os.path.basename(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    orden_compra = data.get('orden_compra', 'N/A')
                    cliente = data.get('comprador', {}).get('nombre', 'N/A')
                    items = len(data.get('items', []))
                    print(f"   📄 {filename} - Orden: {orden_compra}, Cliente: {cliente}, Items: {items}")
            except Exception as e:
                print(f"   ❌ Error leyendo {filename}: {e}")
    else:
        print("❌ Directorio de pendientes no existe")

def check_dependencies():
    """Verifica dependencias de Python"""
    print("\n🔍 Verificando dependencias...")
    
    required_modules = [
        'pyautogui',
        'opencv-python',
        'pillow',
        'numpy',
        'yaml',
        'tkinter'
    ]
    
    for module in required_modules:
        try:
            if module == 'opencv-python':
                import cv2
                print(f"✅ opencv-python (cv2)")
            elif module == 'pillow':
                from PIL import Image
                print(f"✅ pillow (PIL)")
            elif module == 'yaml':
                import yaml
                print(f"✅ PyYAML")
            elif module == 'tkinter':
                import tkinter
                print(f"✅ tkinter")
            else:
                __import__(module)
                print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module} - NO INSTALADO: {e}")

def test_simple_import():
    """Prueba importación simple del RPA"""
    print("\n🔍 Probando importación del RPA...")
    
    try:
        # Intentar importar componentes básicos
        from rpa.simple_logger import rpa_logger
        print("✅ rpa_logger importado correctamente")
        
        from rpa.config_manager import ConfigManager
        print("✅ ConfigManager importado correctamente")
        
        from rpa.vision.main import Vision
        print("✅ Vision importado correctamente")
        
        from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
        print("✅ SalesOrderHandler importado correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error importando RPA: {e}")
        return False

def test_launcher_creation():
    """Prueba la creación del launcher"""
    print("\n🔍 Probando creación del launcher...")
    
    try:
        from launcher_completo import RPALauncherCompleto
        print("✅ Clase RPALauncherCompleto importada correctamente")
        
        # Intentar crear una instancia (sin mostrar la ventana)
        launcher = RPALauncherCompleto()
        print("✅ Instancia del launcher creada correctamente")
        
        # Verificar que los directorios se configuraron
        if hasattr(launcher, 'pending_dir') and os.path.exists(launcher.pending_dir):
            print("✅ Directorios del launcher configurados correctamente")
        else:
            print("❌ Directorios del launcher no configurados")
        
        return True
    except Exception as e:
        print(f"❌ Error creando launcher: {e}")
        return False

def check_system_info():
    """Muestra información del sistema"""
    print("\n🔍 Información del sistema...")
    
    print(f"📋 Python version: {sys.version}")
    print(f"📋 Sistema operativo: {os.name}")
    print(f"📋 Directorio actual: {os.getcwd()}")
    print(f"📋 Hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Función principal de diagnóstico"""
    print("=" * 60)
    print("🔧 DIAGNÓSTICO DEL LAUNCHER RPA TAMAPRINT")
    print("=" * 60)
    
    check_system_info()
    check_directories()
    check_files()
    check_pending_files()
    check_dependencies()
    
    if test_simple_import():
        test_launcher_creation()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 60)
    
    print("\n📋 RECOMENDACIONES:")
    print("1. Si hay directorios faltantes, se crearon automáticamente")
    print("2. Si hay dependencias faltantes, ejecuta: pip install -r requirements.txt")
    print("3. Si hay errores de importación, verifica la estructura de archivos")
    print("4. Asegúrate de tener archivos JSON en data/outputs_json/01_Pendiente/")
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
