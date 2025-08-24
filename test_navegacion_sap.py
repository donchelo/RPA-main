#!/usr/bin/env python3
"""
Prueba de Navegación SAP
Verifica que la navegación funcione correctamente asumiendo que SAP ya está abierto
"""

import os
import sys
import time
from datetime import datetime

# Importar componentes del RPA
from rpa.simple_logger import rpa_logger
from rpa.config_manager import ConfigManager
from rpa.vision.main import Vision
from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler

def test_sap_navigation():
    """Prueba la navegación en SAP asumiendo que ya está abierto"""
    print("🧪 Probando navegación en SAP (asumiendo que ya está abierto)...")
    
    try:
        # Inicializar componentes
        print("📋 Inicializando componentes...")
        config_manager = ConfigManager()
        vision_system = Vision()
        sales_handler = SalesOrderHandler(vision_system, config_manager)
        
        print("✅ Componentes inicializados")
        
        # Probar navegación a ventas
        print("\n🔄 Probando navegación al módulo de ventas...")
        success = sales_handler.navigate_to_sales_order()
        
        if success:
            print("✅ Navegación a ventas exitosa")
            return True
        else:
            print("❌ Navegación a ventas falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de navegación: {e}")
        return False

def test_vision_system():
    """Prueba el sistema de visión"""
    print("\n👁️ Probando sistema de visión...")
    
    try:
        vision = Vision()
        
        # Probar detección de elementos
        print("🔍 Probando detección de elementos...")
        
        # Verificar que las imágenes de referencia existan
        reference_dir = "rpa/vision/reference_images"
        required_images = [
            "sap_ventas_order_button.png",
            "sap_modulos_menu.png",
            "sap_desktop.png"
        ]
        
        for image in required_images:
            image_path = os.path.join(reference_dir, image)
            if os.path.exists(image_path):
                print(f"✅ {image} - Existe")
            else:
                print(f"❌ {image} - NO EXISTE")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando sistema de visión: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA DE NAVEGACIÓN SAP")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("⚠️  IMPORTANTE: Asegúrate de que:")
    print("   1. SAP Business One esté abierto")
    print("   2. Estés en la pantalla del escritorio de SAP")
    print("   3. La ventana esté maximizada")
    print()
    
    input("Presiona Enter cuando SAP esté listo...")
    
    # Prueba 1: Sistema de visión
    if not test_vision_system():
        print("\n❌ PRUEBA FALLIDA: Sistema de visión")
        return False
    
    # Prueba 2: Navegación en SAP
    if not test_sap_navigation():
        print("\n❌ PRUEBA FALLIDA: Navegación en SAP")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 60)
    print("\n📋 La navegación en SAP funciona correctamente")
    print("🚀 El launcher funcional debería funcionar ahora")
    
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
