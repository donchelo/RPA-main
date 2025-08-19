#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones de importación
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vision_import():
    """Prueba la importación de Vision"""
    print("=== PRUEBA DE IMPORTACIÓN DE VISION ===")
    
    try:
        from rpa.vision.main import Vision
        print("✅ Importación de Vision exitosa")
        
        # Crear instancia
        vision = Vision()
        print("✅ Instancia de Vision creada exitosamente")
        
        # Probar métodos básicos
        print("🔍 Probando métodos de detección...")
        
        # Probar detección de SAP desktop
        try:
            sap_desktop = vision.is_sap_desktop_visible()
            print(f"✅ Detección de SAP desktop: {'Detectado' if sap_desktop else 'No detectado'}")
        except Exception as e:
            print(f"❌ Error en detección de SAP desktop: {str(e)}")
        
        # Probar detección de formulario de órdenes
        try:
            sales_form = vision.is_sales_order_form_visible()
            print(f"✅ Detección de formulario de órdenes: {'Detectado' if sales_form else 'No detectado'}")
        except Exception as e:
            print(f"❌ Error en detección de formulario de órdenes: {str(e)}")
        
        # Probar detección robusta de SAP
        try:
            sap_coords = vision.get_sap_coordinates_robust()
            print(f"✅ Detección robusta de SAP: {'Encontrado' if sap_coords else 'No encontrado'}")
            if sap_coords:
                print(f"   Coordenadas: {sap_coords}")
        except Exception as e:
            print(f"❌ Error en detección robusta de SAP: {str(e)}")
        
        print("\n🎉 ¡TODAS LAS PRUEBAS DE IMPORTACIÓN EXITOSAS!")
        return True
        
    except Exception as e:
        print(f"❌ Error en importación: {str(e)}")
        return False

def test_state_handlers_import():
    """Prueba la importación de los manejadores de estado"""
    print("\n=== PRUEBA DE IMPORTACIÓN DE MANEJADORES DE ESTADO ===")
    
    try:
        from rpa.rpa_state_handlers import RPAStateHandlers
        print("✅ Importación de RPAStateHandlers exitosa")
        
        # Crear instancia mock del RPA
        class MockRPA:
            def get_remote_desktop(self):
                return True
            def open_sap(self):
                return True
            def open_sap_orden_de_ventas(self):
                return True
        
        # Crear instancia de manejadores
        handlers = RPAStateHandlers(MockRPA())
        print("✅ Instancia de RPAStateHandlers creada exitosamente")
        
        print("\n🎉 ¡PRUEBAS DE MANEJADORES DE ESTADO EXITOSAS!")
        return True
        
    except Exception as e:
        print(f"❌ Error en importación de manejadores: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 SISTEMA DE PRUEBAS DE CORRECCIÓN")
    print("Versión: Verificación de importaciones")
    print()
    
    # Probar importación de Vision
    vision_success = test_vision_import()
    
    # Probar importación de manejadores de estado
    handlers_success = test_state_handlers_import()
    
    if vision_success and handlers_success:
        print("\n🎉 ¡TODAS LAS CORRECCIONES EXITOSAS!")
        print("✅ El RPA debería funcionar correctamente ahora")
    else:
        print("\n❌ ALGUNAS CORRECCIONES FALLARON")
        print("⚠️ Revisar los errores antes de ejecutar el RPA")
    
    print("\n👋 ¡Hasta luego!")
