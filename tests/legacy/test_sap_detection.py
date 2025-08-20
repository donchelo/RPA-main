#!/usr/bin/env python3
"""
Script de prueba para verificar la detección de SAP Business One
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.simple_logger import rpa_logger
import time

def test_sap_detection():
    """Prueba la detección de SAP Business One"""
    print("=== PRUEBA DE DETECCIÓN DE SAP BUSINESS ONE ===")
    print("Este script verificará si SAP Business One está visible en la pantalla")
    print("Asegúrate de tener SAP abierto y visible antes de continuar")
    print()
    
    # Retraso inicial para permitir cambio manual de pantalla
    print("Iniciando retraso de 5 segundos para cambio manual de pantalla...")
    print("Por favor, cambia a la pantalla de SAP Business One ahora")
    time.sleep(5)
    print("Retraso completado, procediendo con detección...")
    print()
    
    try:
        # Inicializar visión
        vision = Vision()
        
        # Probar detección de SAP desktop
        print("Verificando si SAP Business One está visible...")
        is_visible = vision.is_sap_desktop_visible()
        
        if is_visible:
            print("✅ SAP Business One detectado correctamente")
            print("El RPA puede proceder directamente a órdenes de ventas")
        else:
            print("❌ SAP Business One no detectado")
            print("El RPA necesitará abrir SAP primero")
            
        print()
        
        # Probar detección robusta de SAP
        print("Verificando detección robusta de SAP...")
        coordinates = vision.get_sap_coordinates_robust()
        
        if coordinates:
            print(f"✅ SAP encontrado en coordenadas: {coordinates}")
        else:
            print("❌ SAP no encontrado con ningún método")
            
        print()
        print("=== PRUEBA COMPLETADA ===")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        rpa_logger.log_error(f"Error en prueba de detección: {str(e)}", "Test fallido")

if __name__ == "__main__":
    test_sap_detection()
