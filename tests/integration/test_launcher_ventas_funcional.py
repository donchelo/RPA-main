#!/usr/bin/env python3
"""
Script de prueba para verificar el launcher funcional de ventas
"""

import os
import sys
import json
import glob
from datetime import datetime

def test_launcher_setup():
    """Prueba la configuración del launcher funcional"""
    print("🧪 PRUEBA: Configuración del Launcher Funcional de Ventas")
    print("=" * 60)
    
    # 1. Verificar que existe el launcher funcional
    print("\n1️⃣ Verificando archivos del launcher...")
    if os.path.exists("launcher_funcional.py"):
        print("   ✅ launcher_funcional.py encontrado")
    else:
        print("   ❌ launcher_funcional.py NO encontrado")
        return False
    
    if os.path.exists("launcher_ventas_funcional.bat"):
        print("   ✅ launcher_ventas_funcional.bat encontrado")
    else:
        print("   ❌ launcher_ventas_funcional.bat NO encontrado")
        return False
    
    # 2. Verificar directorios del RPA
    print("\n2️⃣ Verificando componentes del RPA...")
    rpa_components = [
        "rpa/simple_logger.py",
        "rpa/config_manager.py", 
        "rpa/vision/main.py",
        "rpa/modules/sales_order/sales_order_handler.py"
    ]
    
    for component in rpa_components:
        if os.path.exists(component):
            print(f"   ✅ {component} encontrado")
        else:
            print(f"   ❌ {component} NO encontrado")
            return False
    
    # 3. Verificar directorios de datos
    print("\n3️⃣ Verificando directorios de datos...")
    data_dirs = [
        "data/outputs_json/sales_order/01_Pendiente",
        "data/outputs_json/sales_order/02_Procesando", 
        "data/outputs_json/sales_order/03_Completado",
        "data/outputs_json/sales_order/04_Error"
    ]
    
    for data_dir in data_dirs:
        if os.path.exists(data_dir):
            print(f"   ✅ {data_dir} encontrado")
        else:
            print(f"   ❌ {data_dir} NO encontrado")
            os.makedirs(data_dir, exist_ok=True)
            print(f"   🔧 {data_dir} creado")
    
    # 4. Verificar archivos pendientes
    print("\n4️⃣ Verificando archivos pendientes...")
    pending_dir = "data/outputs_json/sales_order/01_Pendiente"
    pending_files = glob.glob(os.path.join(pending_dir, "*.json"))
    
    if pending_files:
        print(f"   ✅ {len(pending_files)} archivos pendientes encontrados:")
        for file in pending_files[:3]:  # Mostrar solo los primeros 3
            filename = os.path.basename(file)
            print(f"      📄 {filename}")
        if len(pending_files) > 3:
            print(f"      ... y {len(pending_files) - 3} más")
    else:
        print("   ⚠️ No hay archivos pendientes")
    
    # 5. Verificar estructura de un archivo JSON
    print("\n5️⃣ Verificando estructura de archivo JSON...")
    if pending_files:
        try:
            with open(pending_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required_fields = ['orden_compra', 'comprador', 'items', 'fecha_entrega']
            missing_fields = []
            
            for field in required_fields:
                if field in data:
                    print(f"   ✅ Campo '{field}' presente")
                else:
                    print(f"   ❌ Campo '{field}' faltante")
                    missing_fields.append(field)
            
            if not missing_fields:
                print("   ✅ Estructura JSON válida")
            else:
                print(f"   ❌ Campos faltantes: {missing_fields}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error leyendo JSON: {str(e)}")
            return False
    
    # 6. Verificar configuración
    print("\n6️⃣ Verificando configuración...")
    if os.path.exists("config.yaml"):
        print("   ✅ config.yaml encontrado")
    else:
        print("   ⚠️ config.yaml no encontrado (se usará configuración por defecto)")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA: Launcher funcional está configurado correctamente")
    print("\n🚀 Para ejecutar el launcher funcional:")
    print("   Opción 1: Hacer doble clic en 'launcher_ventas_funcional.bat'")
    print("   Opción 2: Ejecutar 'python launcher_funcional.py'")
    print("\n⚠️ IMPORTANTE:")
    print("   - Asegúrate de que SAP esté abierto")
    print("   - Verifica la conexión al escritorio remoto")
    print("   - El launcher seleccionará automáticamente el módulo de ventas")
    
    return True

def test_imports():
    """Prueba las importaciones del launcher funcional"""
    print("\n🧪 PRUEBA: Importaciones del Launcher Funcional")
    print("=" * 60)
    
    try:
        # Agregar el directorio raíz al path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Intentar importar componentes
        print("📦 Importando componentes del RPA...")
        
        from rpa.simple_logger import rpa_logger
        print("   ✅ rpa_logger importado")
        
        from rpa.config_manager import ConfigManager
        print("   ✅ ConfigManager importado")
        
        from rpa.vision.main import Vision
        print("   ✅ Vision importado")
        
        from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
        print("   ✅ SalesOrderHandler importado")
        
        print("\n✅ Todas las importaciones exitosas")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en importaciones: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DEL LAUNCHER FUNCIONAL DE VENTAS")
    print("=" * 60)
    
    # Ejecutar pruebas
    setup_ok = test_launcher_setup()
    imports_ok = test_imports()
    
    print("\n" + "=" * 60)
    if setup_ok and imports_ok:
        print("🎉 TODAS LAS PRUEBAS EXITOSAS")
        print("El launcher funcional está listo para usar")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("Revisa los errores anteriores")
    
    print("\nPresiona Enter para salir...")
    input()
