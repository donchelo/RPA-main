#!/usr/bin/env python3
"""
Script de prueba para verificar la detección de la interfaz principal de SAP
"""

import time
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.screen_detector import ScreenDetector
from rpa.simple_logger import rpa_logger

def test_sap_main_interface_detection():
    """Prueba la detección de la interfaz principal de SAP"""
    
    print("=== PRUEBA DE DETECCIÓN DE INTERFAZ PRINCIPAL DE SAP ===")
    print("Este script verificará si el sistema puede detectar la interfaz principal de SAP")
    print()
    
    # Crear detector
    detector = ScreenDetector()
    
    # Dar tiempo para cambiar a la pantalla de SAP
    print("⏳ Esperando 5 segundos para que cambies a la pantalla de SAP...")
    print("   Por favor, asegúrate de que SAP esté abierto y visible")
    time.sleep(5)
    
    print("🔍 Iniciando detección...")
    
    try:
        # Realizar detección
        result = detector.detect_current_screen(save_screenshot=True)
        
        print(f"\n📊 RESULTADOS DE LA DETECCIÓN:")
        print(f"   Estado detectado: {result.state.value}")
        print(f"   Confianza: {result.confidence:.3f}")
        print(f"   Umbral requerido: {detector.confidence_thresholds.get(result.state, 0.8):.3f}")
        
        if result.state.value == "sap_desktop":
            print("✅ ¡ÉXITO! El sistema detectó correctamente la interfaz de SAP")
        else:
            print("❌ El sistema no detectó la interfaz de SAP")
            print(f"   Estado actual: {result.state.value}")
            
            # Mostrar todas las confianzas
            if "all_confidences" in result.details:
                print("\n📈 Confianzas de todos los estados:")
                for state, conf in result.details["all_confidences"].items():
                    print(f"   - {state.value}: {conf:.3f}")
        
        # Guardar screenshot de debug
        if result.screenshot_path:
            print(f"\n📸 Screenshot guardado en: {result.screenshot_path}")
        
        return result.state.value == "sap_desktop"
        
    except Exception as e:
        print(f"❌ Error durante la detección: {e}")
        rpa_logger.log_error("PRUEBA SAP", f"Error en detección: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando prueba de detección de interfaz principal de SAP")
    print()
    
    success = test_sap_main_interface_detection()
    
    print()
    if success:
        print("🎉 ¡Prueba completada exitosamente!")
        print("   El sistema puede detectar correctamente la interfaz principal de SAP")
    else:
        print("⚠️  La prueba no fue exitosa")
        print("   Revisa que:")
        print("   1. SAP esté abierto y visible")
        print("   2. La imagen de referencia esté correctamente guardada")
        print("   3. La pantalla esté en la interfaz principal de SAP")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
