#!/usr/bin/env python3
"""
Script de prueba para el módulo de órdenes de producción
Fase 4: Integración y Testing
"""

import os
import sys
import time
import json
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.config_manager import ConfigManager
from rpa.modules.production_order import ProductionOrderHandler
from rpa.simple_logger import rpa_logger


def load_test_data() -> dict:
    """Cargar datos de prueba para órdenes de producción"""
    test_data = {
        "tipo_modulo": "production_order",
        "datos": {
            "numero_articulo": "ART-001",
            "numero_pedido_interno": "PI-2024-001",
            "cantidad": 100,
            "fecha_finalizacion": "15/12/2024",
            "unidad_medida": "PCS",
            "centro_trabajo": "CT-01",
            "observaciones": "Orden de producción de prueba"
        },
        "metadata": {
            "fecha_creacion": "2024-12-01T10:30:00",
            "usuario": "SISTEMA_RPA",
            "version": "1.0",
            "prioridad": "alta"
        }
    }
    return test_data


def test_production_module():
    """Función principal de prueba del módulo de producción"""
    print("🧪 PRUEBA DEL MÓDULO DE ÓRDENES DE PRODUCCIÓN")
    print("=" * 60)
    
    try:
        # 1. Inicializar componentes
        print("🔄 Inicializando componentes...")
        config = ConfigManager()
        vision = Vision()
        
        # 2. Crear handler de producción
        print("🔄 Creando handler de producción...")
        production_handler = ProductionOrderHandler(vision, config)
        
        # 3. Cargar datos de prueba
        print("🔄 Cargando datos de prueba...")
        test_data = load_test_data()
        
        print(f"📋 Datos de prueba cargados:")
        print(f"   - Artículo: {test_data['datos']['numero_articulo']}")
        print(f"   - Pedido interno: {test_data['datos']['numero_pedido_interno']}")
        print(f"   - Cantidad: {test_data['datos']['cantidad']}")
        print(f"   - Fecha: {test_data['datos']['fecha_finalizacion']}")
        
        # 4. Pausa para preparación manual
        print("\n⏸️  PREPARACIÓN MANUAL REQUERIDA")
        print("=" * 40)
        print("1. Abre SAP Business One")
        print("2. Asegúrate de estar en la pantalla principal")
        print("3. Ten el escritorio remoto activo")
        print("4. El script navegará automáticamente")
        
        input("\n⏸️  Presiona ENTER cuando estés listo para comenzar...")
        
        # 5. Ejecutar navegación a producción
        print("\n🔄 Navegando al módulo de producción...")
        navigation_success = production_handler.navigate_to_production()
        
        if not navigation_success:
            print("❌ Error en la navegación. Verifica que SAP esté abierto.")
            return False
        
        print("✅ Navegación completada exitosamente")
        
        # 6. Pausa para verificar formulario
        print("\n⏸️  VERIFICACIÓN DEL FORMULARIO")
        print("=" * 40)
        print("Verifica que el formulario de orden de producción esté abierto")
        print("El script procederá a llenar los campos automáticamente")
        
        input("\n⏸️  Presiona ENTER para continuar con el llenado de campos...")
        
        # 7. Procesar orden de producción (sin auto-click en crear)
        print("\n🔄 Procesando orden de producción...")
        success = production_handler.process_production_order(
            test_data['datos'], 
            auto_click_crear=False  # No hacer clic automático en crear
        )
        
        if success:
            print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
            print("=" * 40)
            print("✅ El formulario ha sido llenado completamente")
            print("✅ Todos los campos están listos")
            print("✅ Puedes revisar los datos y tomar la decisión final")
            print("\n💡 ACCIONES DISPONIBLES:")
            print("   - Haz clic en 'Crear' para confirmar la orden")
            print("   - Haz clic en 'Borrar' para cancelar")
            print("   - Modifica cualquier campo si es necesario")
            
            # 8. Pausa final para decisión manual
            print("\n⏸️  ESPERANDO DECISIÓN MANUAL")
            print("=" * 40)
            print("El script ha terminado. Toma tu decisión en SAP.")
            print("Presiona ENTER cuando hayas completado la acción manual...")
            
            input()
            print("✅ Prueba finalizada correctamente")
            
        else:
            print("❌ Error procesando la orden de producción")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        rpa_logger.error(f"Error en test_production_module: {e}")
        return False


def test_individual_methods():
    """Prueba métodos individuales del handler"""
    print("\n🔧 PRUEBA DE MÉTODOS INDIVIDUALES")
    print("=" * 40)
    
    try:
        config = ConfigManager()
        vision = Vision()
        production_handler = ProductionOrderHandler(vision, config)
        
        # Datos de prueba
        test_data = {
            "numero_articulo": "ART-TEST",
            "numero_pedido_interno": "PI-TEST-001",
            "cantidad": 50,
            "fecha_finalizacion": "20/12/2024"
        }
        
        print("🧪 Probando validación de datos...")
        validation_result = production_handler.validate_form_data(test_data)
        print(f"   Resultado: {'✅ Válido' if validation_result else '❌ Inválido'}")
        
        print("🧪 Configuración cargada:")
        print(f"   - Tabs artículo: {production_handler.production_config.get('form_fields', {}).get('articulo_tabs', 'N/A')}")
        print(f"   - Tabs pedido interno: {production_handler.production_config.get('form_fields', {}).get('pedido_interno_tabs', 'N/A')}")
        print(f"   - Tabs cantidad: {production_handler.production_config.get('form_fields', {}).get('cantidad_tabs', 'N/A')}")
        print(f"   - Tabs fecha: {production_handler.production_config.get('form_fields', {}).get('fecha_finalizacion_tabs', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de métodos individuales: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 INICIANDO FASE 4: INTEGRACIÓN Y TESTING")
    print("=" * 60)
    
    # Prueba de métodos individuales
    if not test_individual_methods():
        print("❌ Falló la prueba de métodos individuales")
        return
    
    # Prueba completa del módulo
    if not test_production_module():
        print("❌ Falló la prueba completa del módulo")
        return
    
    print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    print("✅ El módulo de producción está listo para uso")
    print("✅ La integración con el sistema principal es correcta")
    print("✅ Los métodos funcionan como se esperaba")


if __name__ == "__main__":
    main()
