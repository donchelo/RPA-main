#!/usr/bin/env python3
"""
Prueba Simple del Launcher RPA
Verifica que el sistema funcione correctamente
"""

import os
import json
import time
from datetime import datetime

# Importar componentes del RPA
from rpa.simple_logger import rpa_logger
from rpa.config_manager import ConfigManager
from rpa.vision.main import Vision
from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler

def test_rpa_components():
    """Prueba los componentes básicos del RPA"""
    print("🔧 Probando componentes del RPA...")
    
    try:
        # Inicializar configuración
        print("📋 Inicializando ConfigManager...")
        config_manager = ConfigManager()
        print("✅ ConfigManager inicializado")
        
        # Inicializar sistema de visión
        print("👁️ Inicializando sistema de visión...")
        vision_system = Vision()
        print("✅ Sistema de visión inicializado")
        
        # Inicializar handler de ventas
        print("🛒 Inicializando handler de ventas...")
        sales_handler = SalesOrderHandler(vision_system, config_manager)
        print("✅ Handler de ventas inicializado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando componentes: {e}")
        return False

def test_file_processing():
    """Prueba el procesamiento de un archivo"""
    print("\n📄 Probando procesamiento de archivo...")
    
    # Buscar archivos pendientes
    pending_dir = "data/outputs_json/01_Pendiente"
    if not os.path.exists(pending_dir):
        print(f"❌ Directorio no existe: {pending_dir}")
        return False
    
    json_files = [f for f in os.listdir(pending_dir) if f.endswith('.json')]
    if not json_files:
        print("❌ No hay archivos JSON pendientes")
        return False
    
    # Tomar el primer archivo
    test_file = json_files[0]
    file_path = os.path.join(pending_dir, test_file)
    
    print(f"📋 Archivo de prueba: {test_file}")
    
    try:
        # Leer el archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Archivo leído correctamente")
        print(f"   Orden de compra: {data.get('orden_compra', 'N/A')}")
        print(f"   Cliente: {data.get('comprador', {}).get('nombre', 'N/A')}")
        print(f"   Items: {len(data.get('items', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return False

def test_sales_handler():
    """Prueba el handler de ventas"""
    print("\n🛒 Probando handler de ventas...")
    
    try:
        # Inicializar componentes
        config_manager = ConfigManager()
        vision_system = Vision()
        sales_handler = SalesOrderHandler(vision_system, config_manager)
        
        # Obtener información del módulo
        module_info = sales_handler.get_module_info()
        print(f"✅ Módulo: {module_info['name']}")
        print(f"   Descripción: {module_info['description']}")
        print(f"   Versión: {module_info['version']}")
        print(f"   Estado: {module_info['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando handler: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA SIMPLE DEL LAUNCHER RPA TAMAPRINT")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Prueba 1: Componentes del RPA
    if not test_rpa_components():
        print("\n❌ PRUEBA FALLIDA: Componentes del RPA")
        return False
    
    # Prueba 2: Procesamiento de archivos
    if not test_file_processing():
        print("\n❌ PRUEBA FALLIDA: Procesamiento de archivos")
        return False
    
    # Prueba 3: Handler de ventas
    if not test_sales_handler():
        print("\n❌ PRUEBA FALLIDA: Handler de ventas")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 60)
    print("\n📋 El sistema está listo para usar el launcher funcional")
    print("🚀 Puedes ejecutar: launcher_funcional.bat")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Prueba completada exitosamente")
        else:
            print("\n❌ Prueba falló")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    input("\nPresiona Enter para continuar...")
