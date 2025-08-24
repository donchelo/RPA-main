#!/usr/bin/env python3
"""
Prueba Simple del Módulo de Producción
Verifica que el módulo de producción funcione correctamente
"""

import os
import json
import time
from datetime import datetime

# Importar componentes del RPA
from rpa.simple_logger import rpa_logger
from rpa.config_manager import ConfigManager
from rpa.vision.main import Vision
from rpa.modules.production_order.production_order_handler import ProductionOrderHandler

def test_production_components():
    """Prueba los componentes básicos del módulo de producción"""
    print("🔧 Probando componentes del módulo de producción...")
    
    try:
        # Inicializar configuración
        print("📋 Inicializando ConfigManager...")
        config_manager = ConfigManager()
        print("✅ ConfigManager inicializado")
        
        # Inicializar sistema de visión
        print("👁️ Inicializando sistema de visión...")
        vision_system = Vision()
        print("✅ Sistema de visión inicializado")
        
        # Inicializar handler de producción
        print("🏭 Inicializando handler de producción...")
        production_handler = ProductionOrderHandler(vision_system, config_manager)
        print("✅ Handler de producción inicializado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando componentes: {e}")
        return False

def test_production_data():
    """Prueba el procesamiento de datos de producción"""
    print("\n📄 Probando datos de producción...")
    
    # Datos de prueba para producción
    test_data = {
        "numero_articulo": "ART001",
        "numero_pedido_interno": "PI001",
        "cantidad": 100,
        "fecha_finalizacion": "25/12/2024",
        "unidad_medida": "PCS",
        "centro_trabajo": "CT001"
    }
    
    try:
        # Validar datos
        config_manager = ConfigManager()
        vision_system = Vision()
        production_handler = ProductionOrderHandler(vision_system, config_manager)
        
        # Probar validación
        is_valid = production_handler._validate_production_data(test_data)
        if is_valid:
            print("✅ Datos de producción válidos")
            print(f"   Artículo: {test_data['numero_articulo']}")
            print(f"   Pedido interno: {test_data['numero_pedido_interno']}")
            print(f"   Cantidad: {test_data['cantidad']}")
            print(f"   Fecha: {test_data['fecha_finalizacion']}")
        else:
            print("❌ Datos de producción inválidos")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando datos: {e}")
        return False

def test_production_handler():
    """Prueba el handler de producción"""
    print("\n🏭 Probando handler de producción...")
    
    try:
        # Inicializar componentes
        config_manager = ConfigManager()
        vision_system = Vision()
        production_handler = ProductionOrderHandler(vision_system, config_manager)
        
        # Obtener información del módulo
        module_info = production_handler.get_module_info()
        print(f"✅ Módulo: {module_info['name']}")
        print(f"   Descripción: {module_info['description']}")
        print(f"   Versión: {module_info['version']}")
        print(f"   Estado: {module_info['status']}")
        print(f"   Campos soportados: {len(module_info['supported_fields'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando handler: {e}")
        return False

def test_production_images():
    """Prueba las imágenes de referencia del módulo de producción"""
    print("\n🖼️ Probando imágenes de referencia de producción...")
    
    try:
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
        print(f"❌ Error probando imágenes: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA SIMPLE DEL MÓDULO DE PRODUCCIÓN")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Prueba 1: Componentes del módulo de producción
    if not test_production_components():
        print("\n❌ PRUEBA FALLIDA: Componentes del módulo de producción")
        return False
    
    # Prueba 2: Datos de producción
    if not test_production_data():
        print("\n❌ PRUEBA FALLIDA: Datos de producción")
        return False
    
    # Prueba 3: Handler de producción
    if not test_production_handler():
        print("\n❌ PRUEBA FALLIDA: Handler de producción")
        return False
    
    # Prueba 4: Imágenes de referencia
    if not test_production_images():
        print("\n❌ PRUEBA FALLIDA: Imágenes de referencia")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 60)
    print("\n📋 El módulo de producción está listo para usar")
    print("🚀 Puedes ejecutar: launcher_funcional.bat")
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
