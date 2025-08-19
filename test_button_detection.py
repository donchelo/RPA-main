#!/usr/bin/env python3
"""
Script de prueba para verificar la detección del botón de orden de ventas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.simple_logger import rpa_logger
import time
import pyautogui

def test_button_detection():
    """Prueba la detección del botón de orden de ventas"""
    print("=== PRUEBA DE DETECCIÓN DE BOTÓN DE ORDEN DE VENTAS ===")
    print("Este script verificará si el botón de orden de ventas es detectable")
    print("Asegúrate de estar en SAP con el menú de ventas abierto")
    print()
    
    # Retraso para permitir cambio manual de pantalla
    print("Iniciando retraso de 5 segundos para cambio manual de pantalla...")
    print("Por favor, navega a SAP → Módulos → Ventas y abre el menú de ventas")
    time.sleep(5)
    print("Retraso completado, procediendo con detección...")
    print()
    
    try:
        # Inicializar visión
        vision = Vision()
        
        # Probar detección del botón
        print("🔍 Buscando botón de Orden de Ventas...")
        coordinates = vision.get_ventas_order_button_coordinates()
        
        if coordinates:
            print(f"✅ Botón encontrado en coordenadas: {coordinates}")
            print("🎯 El RPA debería poder hacer clic en esta ubicación")
            
            # Opcional: mostrar las coordenadas para verificación manual
            print(f"📍 Coordenadas para verificación: X={coordinates[0]}, Y={coordinates[1]}")
            
            return True
        else:
            print("❌ Botón no encontrado")
            print("💡 Posibles causas:")
            print("   - El menú de ventas no está abierto")
            print("   - La imagen de referencia no coincide con la pantalla actual")
            print("   - El botón está en una ubicación diferente")
            print("   - La resolución o tema de SAP es diferente")
            
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        rpa_logger.log_error(f"Error en prueba de detección de botón: {str(e)}", "Test fallido")
        return False

def test_screenshot_analysis():
    """Analiza la captura de pantalla actual para debugging"""
    print("\n=== ANÁLISIS DE CAPTURA DE PANTALLA ===")
    
    try:
        # Tomar captura de pantalla
        print("📸 Tomando captura de pantalla...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        print(f"✅ Captura tomada: {screenshot.size[0]}x{screenshot.size[1]} píxeles")
        
        # Guardar captura para análisis
        import cv2
        cv2.imwrite("debug_screenshot.png", screenshot_cv)
        print("💾 Captura guardada como 'debug_screenshot.png' para análisis")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en análisis de captura: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 SISTEMA DE PRUEBA DE DETECCIÓN DE BOTÓN")
    print("Versión: Verificación específica de botón de orden de ventas")
    print()
    
    # Probar detección del botón
    button_success = test_button_detection()
    
    if button_success:
        print("\n🎉 ¡BOTÓN DETECTADO EXITOSAMENTE!")
        print("✅ El RPA debería poder navegar correctamente")
    else:
        print("\n❌ BOTÓN NO DETECTADO")
        print("⚠️ Revisar la configuración de SAP y las imágenes de referencia")
        
        # Opcional: analizar captura de pantalla
        print("\n🔍 ¿Deseas analizar la captura de pantalla actual? (s/n): ", end="")
        try:
            response = input().lower()
            if response == 's':
                test_screenshot_analysis()
        except:
            pass
    
    print("\n👋 ¡Hasta luego!")
