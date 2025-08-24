#!/usr/bin/env python3
"""
Prueba de Navegación del Módulo de Producción
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
from rpa.modules.production_order.production_order_handler import ProductionOrderHandler

def test_production_navigation():
    """Prueba la navegación en el módulo de producción"""
    print("🧪 Probando navegación al módulo de producción...")
    
    try:
        # Inicializar componentes
        print("📋 Inicializando componentes...")
        config_manager = ConfigManager()
        vision_system = Vision()
        production_handler = ProductionOrderHandler(vision_system, config_manager)
        
        print("✅ Componentes inicializados")
        
        # Probar navegación a producción
        print("\n🔄 Probando navegación al módulo de producción...")
        success = production_handler.navigate_to_production()
        
        if success:
            print("✅ Navegación a producción exitosa")
            return True
        else:
            print("❌ Navegación a producción falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de navegación: {e}")
        return False

def test_production_vision():
    """Prueba el sistema de visión para producción"""
    print("\n👁️ Probando sistema de visión para producción...")
    
    try:
        vision = Vision()
        
        # Probar detección de elementos
        print("🔍 Probando detección de elementos de producción...")
        
        # Verificar que las imágenes de referencia existan
        reference_dir = "rpa/vision/reference_images/production"
        required_images = [
            "sap_orden_fabricacion_button.png",
            "sap_produccion_crear_button.png",
            "sap_articulo_field.png",
            "sap_cantidad_field.png",
            "sap_fecha_finalizacion_field.png"
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
    print("🧪 PRUEBA DE NAVEGACIÓN DEL MÓDULO DE PRODUCCIÓN")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("⚠️  IMPORTANTE: Asegúrate de que:")
    print("   1. SAP Business One esté abierto")
    print("   2. Estés en la pantalla del escritorio de SAP")
    print("   3. La ventana esté maximizada")
    print()
    
    input("Presiona Enter cuando SAP esté listo...")
    
    # Prueba 1: Sistema de visión para producción
    if not test_production_vision():
        print("\n❌ PRUEBA FALLIDA: Sistema de visión para producción")
        return False
    
    # Prueba 2: Navegación en producción
    if not test_production_navigation():
        print("\n❌ PRUEBA FALLIDA: Navegación en producción")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 60)
    print("\n📋 La navegación del módulo de producción funciona correctamente")
    print("🚀 El launcher funcional debería funcionar ahora")
    print("🏭 Selecciona 'Módulo de Producción' en el launcher")
    
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
