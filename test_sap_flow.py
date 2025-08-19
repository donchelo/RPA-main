#!/usr/bin/env python3
"""
Script de prueba para verificar el flujo completo de SAP
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.rpa_with_state_machine import RPAWithStateMachine
from rpa.simple_logger import rpa_logger
import time
import json

def test_sap_flow():
    """Prueba el flujo completo de detección y navegación de SAP"""
    print("=== PRUEBA DE FLUJO COMPLETO DE SAP ===")
    print("Este script probará la detección de SAP y navegación a órdenes de ventas")
    print("Asegúrate de tener SAP abierto y visible antes de continuar")
    print()
    
    # Retraso inicial para permitir cambio manual de pantalla
    print("Iniciando retraso de 5 segundos para cambio manual de pantalla...")
    print("Por favor, cambia a la pantalla de SAP Business One ahora")
    time.sleep(5)
    print("Retraso completado, procediendo con prueba...")
    print()
    
    try:
        # Crear datos de prueba
        test_data = {
            "comprador": {
                "nit": "123456789",
                "nombre": "Cliente de Prueba"
            },
            "orden": {
                "numero": "OC-001",
                "fecha_entrega": "2024-12-31"
            },
            "items": [
                {
                    "codigo": "ART001",
                    "descripcion": "Artículo de prueba",
                    "cantidad": 1,
                    "precio": 100.00
                }
            ]
        }
        
        # Inicializar RPA
        rpa = RPAWithStateMachine()
        
        # Probar detección de SAP
        print("1. Verificando detección de SAP...")
        from rpa.vision.main import vision
        is_visible = vision.is_sap_desktop_visible()
        
        if is_visible:
            print("✅ SAP detectado - procediendo directamente a órdenes de ventas")
            
            # Probar navegación a órdenes de ventas
            print("2. Navegando a órdenes de ventas...")
            success = rpa.open_sap_orden_de_ventas()
            
            if success:
                print("✅ Navegación a órdenes de ventas exitosa")
                
                # Probar carga de datos
                print("3. Probando carga de datos...")
                rpa.load_nit(test_data["comprador"]["nit"])
                print("✅ NIT cargado exitosamente")
                
                rpa.load_order(test_data["orden"]["numero"])
                print("✅ Número de orden cargado exitosamente")
                
                rpa.load_date(test_data["orden"]["fecha_entrega"])
                print("✅ Fecha de entrega cargada exitosamente")
                
                print("✅ FLUJO COMPLETO EXITOSO")
                return True
            else:
                print("❌ Falló la navegación a órdenes de ventas")
                return False
        else:
            print("❌ SAP no detectado - necesitaría abrir SAP primero")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        rpa_logger.log_error(f"Error en prueba de flujo: {str(e)}", "Test fallido")
        return False

if __name__ == "__main__":
    success = test_sap_flow()
    
    if success:
        print("\n🎉 ¡PRUEBA EXITOSA!")
    else:
        print("\n❌ PRUEBA FALLIDA")
    
    print("\n👋 ¡Hasta luego!")
