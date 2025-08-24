#!/usr/bin/env python3
"""
Script de prueba rápida para el módulo de producción (sin SAP)
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.modules.production_order import ProductionOrderHandler
from rpa.simple_logger import rpa_logger


def test_rapido_produccion():
    """Prueba rápida del módulo de producción sin SAP"""
    print("⚡ PRUEBA RÁPIDA DEL MÓDULO DE PRODUCCIÓN")
    print("=" * 50)
    
    try:
        # 1. Verificar que el módulo se puede importar
        print("🔄 Verificando importación del módulo...")
        from rpa.modules.production_order import ProductionOrderHandler
        print("✅ Módulo importado correctamente")
        
        # 2. Crear datos ficticios
        print("🔄 Creando datos de prueba...")
        datos_ficticios = {
            "numero_articulo": "ART-TEST-001",
            "numero_pedido_interno": "PI-TEST-2024-001",
            "cantidad": 200,
            "fecha_finalizacion": "25/12/2024"
        }
        
        print("📋 Datos de prueba:")
        for key, value in datos_ficticios.items():
            print(f"   - {key}: {value}")
        
        # 3. Verificar configuración
        print("\n🔄 Verificando configuración...")
        config_path = "rpa/modules/production_order/production_order_config.yaml"
        if os.path.exists(config_path):
            print(f"✅ Archivo de configuración encontrado: {config_path}")
        else:
            print(f"❌ Archivo de configuración no encontrado: {config_path}")
            return False
        
        # 4. Verificar imágenes de referencia
        print("\n🔄 Verificando imágenes de referencia...")
        images_dir = "rpa/vision/reference_images/production"
        if os.path.exists(images_dir):
            images = os.listdir(images_dir)
            print(f"✅ Directorio de imágenes encontrado: {images_dir}")
            print(f"📸 Imágenes disponibles: {len(images)}")
            for img in images:
                print(f"   - {img}")
        else:
            print(f"❌ Directorio de imágenes no encontrado: {images_dir}")
            return False
        
        # 5. Verificar estructura del handler
        print("\n🔄 Verificando estructura del handler...")
        handler_methods = [
            'navigate_to_production',
            'load_articulo',
            'load_pedido_interno', 
            'load_cantidad',
            'load_fecha_finalizacion',
            'click_crear_button',
            'validate_form_data',
            'process_production_order'
        ]
        
        for method in handler_methods:
            if hasattr(ProductionOrderHandler, method):
                print(f"✅ Método {method}: Disponible")
            else:
                print(f"❌ Método {method}: No encontrado")
                return False
        
        # 6. Simular validación de datos
        print("\n🔄 Simulando validación de datos...")
        # Crear un mock del handler para validación
        class MockVision:
            def find_and_click(self, *args, **kwargs):
                return True
        
        class MockConfig:
            def get(self, *args, **kwargs):
                return 1.0
        
        mock_vision = MockVision()
        mock_config = MockConfig()
        
        # Crear handler con configuración mock
        import yaml
        mock_production_config = {
            'navigation': {'alt_m_delay': 0.5, 'p_key_delay': 1.0},
            'form_fields': {'articulo_tabs': 2, 'pedido_interno_tabs': 3, 'cantidad_tabs': 2, 'fecha_finalizacion_tabs': 3},
            'validation': {'max_cantidad': 999999, 'formato_fecha': 'DD/MM/YYYY'},
            'template_matching': {'orden_fabricacion_button_confidence': 0.8, 'field_confidence': 0.85},
            'timeouts': {'navigation_timeout': 10.0, 'field_input_timeout': 5.0}
        }
        
        import unittest.mock
        with unittest.mock.patch.object(ProductionOrderHandler, '_load_production_config', return_value=mock_production_config):
            handler = ProductionOrderHandler(mock_vision, mock_config)
            
            # Probar validación
            validation_result = handler.validate_form_data(datos_ficticios)
            if validation_result:
                print("✅ Validación de datos: Exitosa")
            else:
                print("❌ Validación de datos: Falló")
                return False
        
        # 7. Resumen final
        print("\n📊 RESUMEN DE LA PRUEBA RÁPIDA")
        print("=" * 40)
        print("✅ Importación del módulo: OK")
        print("✅ Archivo de configuración: OK")
        print("✅ Imágenes de referencia: OK")
        print("✅ Estructura del handler: OK")
        print("✅ Validación de datos: OK")
        print("✅ Módulo listo para uso: OK")
        
        print("\n🎯 EL MÓDULO ESTÁ LISTO PARA PRUEBAS CON SAP")
        print("💡 Ejecuta 'python test_produccion_ficticia.py' para probar con SAP")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba rápida: {e}")
        rpa_logger.error(f"Error en test_rapido_produccion: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA RÁPIDA")
    print("=" * 50)
    print("🎯 Objetivo: Verificar que el módulo está listo")
    print("🎯 Modo: Sin SAP (solo verificación de componentes)")
    
    if test_rapido_produccion():
        print("\n🎉 PRUEBA RÁPIDA EXITOSA")
        print("=" * 50)
        print("✅ Todos los componentes están en orden")
        print("✅ El módulo está listo para pruebas con SAP")
        print("✅ Puedes proceder con la prueba completa")
    else:
        print("\n❌ PRUEBA RÁPIDA FALLÓ")
        print("=" * 50)
        print("💡 Revisa los errores antes de continuar")


if __name__ == "__main__":
    main()
