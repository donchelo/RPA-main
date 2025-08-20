#!/usr/bin/env python3
"""
Script de prueba para verificar la navegación completa a órdenes de ventas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.rpa_with_state_machine import RPAWithStateMachine
from rpa.simple_logger import rpa_logger
import time

def test_complete_navigation():
    """Prueba la navegación completa a órdenes de ventas"""
    print("=== PRUEBA DE NAVEGACIÓN COMPLETA A ÓRDENES DE VENTAS ===")
    print("Este script probará la navegación completa desde SAP hasta el formulario")
    print("Asegúrate de estar en SAP Business One antes de continuar")
    print()
    
    # Retraso para permitir cambio manual de pantalla
    print("Iniciando retraso de 5 segundos para cambio manual de pantalla...")
    print("Por favor, asegúrate de estar en SAP Business One")
    time.sleep(5)
    print("Retraso completado, procediendo con navegación...")
    print()
    
    try:
        # Inicializar RPA
        rpa = RPAWithStateMachine()
        
        print("🚀 PASO 1: Verificando conexión al escritorio remoto...")
        
        # Verificar conexión al escritorio remoto
        success = rpa.get_remote_desktop()
        if success:
            print("✅ Conexión al escritorio remoto exitosa")
        else:
            print("❌ Falló la conexión al escritorio remoto")
            return False
        
        print("\n🚀 PASO 2: Navegando a órdenes de ventas...")
        
        # Navegar a órdenes de ventas
        success = rpa.open_sap_orden_de_ventas()
        if success:
            print("✅ Navegación a órdenes de ventas exitosa")
            print("🎉 ¡El RPA debería poder procesar archivos correctamente!")
            return True
        else:
            print("❌ Falló la navegación a órdenes de ventas")
            print("💡 Posibles problemas:")
            print("   - El menú de módulos no se abrió correctamente")
            print("   - El módulo de ventas no se seleccionó")
            print("   - El botón de orden de ventas no se encontró")
            print("   - La imagen de referencia no coincide")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        rpa_logger.log_error(f"Error en prueba de navegación completa: {str(e)}", "Test fallido")
        return False

def test_step_by_step():
    """Prueba paso a paso la navegación"""
    print("\n=== PRUEBA PASO A PASO ===")
    
    try:
        from rpa.vision.main import Vision
        vision = Vision()
        
        print("🔍 PASO 1: Verificando detección de SAP...")
        sap_desktop = vision.is_sap_desktop_visible()
        print(f"   SAP Desktop: {'✅ Detectado' if sap_desktop else '❌ No detectado'}")
        
        print("🔍 PASO 2: Verificando detección de formulario...")
        sales_form = vision.is_sales_order_form_visible()
        print(f"   Formulario de órdenes: {'✅ Detectado' if sales_form else '❌ No detectado'}")
        
        print("🔍 PASO 3: Verificando detección de botón...")
        button_coords = vision.get_ventas_order_button_coordinates()
        print(f"   Botón de orden de ventas: {'✅ Encontrado' if button_coords else '❌ No encontrado'}")
        if button_coords:
            print(f"   Coordenadas: {button_coords}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba paso a paso: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧭 SISTEMA DE PRUEBA DE NAVEGACIÓN COMPLETA")
    print("Versión: Verificación de navegación a órdenes de ventas")
    print()
    
    # Probar paso a paso
    step_success = test_step_by_step()
    
    if step_success:
        print("\n" + "="*50)
        # Probar navegación completa
        nav_success = test_complete_navigation()
        
        if nav_success:
            print("\n🎉 ¡NAVEGACIÓN COMPLETA EXITOSA!")
            print("✅ El RPA está listo para procesar archivos")
        else:
            print("\n❌ NAVEGACIÓN COMPLETA FALLIDA")
            print("⚠️ Revisar la configuración de SAP y las imágenes")
    else:
        print("\n❌ PRUEBA PASO A PASO FALLIDA")
        print("⚠️ Revisar la detección de elementos")
    
    print("\n👋 ¡Hasta luego!")
