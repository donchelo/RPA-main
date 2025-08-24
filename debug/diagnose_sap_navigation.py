#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas en la navegación a "Orden de Venta" en SAP
"""

import time
import sys
import os
import cv2
import numpy as np
import pyautogui

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.screen_detector import ScreenDetector
from rpa.simple_logger import rpa_logger

def diagnose_sap_navigation():
    """Diagnostica la navegación a Orden de Venta en SAP"""
    
    print("=== DIAGNÓSTICO DE NAVEGACIÓN A ORDEN DE VENTA EN SAP ===")
    print("Este script identificará exactamente dónde falla la navegación")
    print()
    
    # Crear instancias
    vision = Vision()
    detector = ScreenDetector()
    
    # Paso 1: Verificar estado actual
    print("🔍 PASO 1: Verificando estado actual de la pantalla...")
    result = detector.detect_current_screen(save_screenshot=True)
    print(f"   Estado detectado: {result.state.value}")
    print(f"   Confianza: {result.confidence:.3f}")
    
    if result.state.value != "sap_desktop":
        print("❌ No estamos en SAP Desktop. Por favor, navega a SAP primero.")
        return False
    
    print("✅ Estamos en SAP Desktop")
    print()
    
    # Paso 2: Buscar botón de módulos
    print("🔍 PASO 2: Buscando botón de módulos...")
    modulos_coords = vision.get_modulos_menu_coordinates()
    
    if modulos_coords:
        print(f"✅ Botón de módulos encontrado en: {modulos_coords}")
        
        # Tomar screenshot para verificar
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Guardar screenshot con marca en el botón
        marked_screenshot = screenshot_cv.copy()
        cv2.circle(marked_screenshot, modulos_coords, 10, (0, 255, 0), 2)
        cv2.imwrite("./debug_screenshots/modulos_button_found.png", marked_screenshot)
        print("   📸 Screenshot guardado: debug_screenshots/modulos_button_found.png")
        
    else:
        print("❌ Botón de módulos NO encontrado")
        print("   Posibles causas:")
        print("   - La imagen de referencia no coincide con la pantalla actual")
        print("   - El botón está en una posición diferente")
        print("   - La resolución de pantalla es diferente")
        return False
    
    print()
    
    # Paso 3: Simular clic en módulos
    print("🔍 PASO 3: Simulando clic en módulos...")
    print("   ⚠️  NO se hará clic real, solo se mostrará dónde se haría")
    print(f"   Coordenadas donde se haría clic: {modulos_coords}")
    
    # Esperar confirmación del usuario
    input("   Presiona ENTER para continuar con el siguiente paso...")
    print()
    
    # Paso 4: Buscar menú de ventas
    print("🔍 PASO 4: Buscando menú de ventas...")
    ventas_coords = vision.get_ventas_menu_coordinates()
    
    if ventas_coords:
        print(f"✅ Menú de ventas encontrado en: {ventas_coords}")
        
        # Tomar screenshot para verificar
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Guardar screenshot con marca en el menú
        marked_screenshot = screenshot_cv.copy()
        cv2.circle(marked_screenshot, ventas_coords, 10, (0, 255, 0), 2)
        cv2.imwrite("./debug_screenshots/ventas_menu_found.png", marked_screenshot)
        print("   📸 Screenshot guardado: debug_screenshots/ventas_menu_found.png")
        
    else:
        print("❌ Menú de ventas NO encontrado")
        print("   Posibles causas:")
        print("   - El menú de módulos no se abrió correctamente")
        print("   - La imagen de referencia no coincide")
        print("   - El menú está en una posición diferente")
        return False
    
    print()
    
    # Paso 5: Buscar botón de orden de venta
    print("🔍 PASO 5: Buscando botón de orden de venta...")
    orden_coords = vision.get_ventas_order_coordinates()
    
    if orden_coords:
        print(f"✅ Botón de orden de venta encontrado en: {orden_coords}")
        
        # Tomar screenshot para verificar
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Guardar screenshot con marca en el botón
        marked_screenshot = screenshot_cv.copy()
        cv2.circle(marked_screenshot, orden_coords, 10, (0, 255, 0), 2)
        cv2.imwrite("./debug_screenshots/orden_venta_found.png", marked_screenshot)
        print("   📸 Screenshot guardado: debug_screenshots/orden_venta_found.png")
        
    else:
        print("❌ Botón de orden de venta NO encontrado")
        print("   Posibles causas:")
        print("   - El menú de ventas no se abrió correctamente")
        print("   - La imagen de referencia no coincide")
        print("   - El botón tiene un nombre diferente")
        print("   - El botón está en una posición diferente")
        
        # Mostrar información de debug
        print("\n🔧 INFORMACIÓN DE DEBUG:")
        print("   - Imagen de referencia: sap_ventas_order_button.png")
        print("   - Tamaño de imagen: ", vision.sap_ventas_order_button_image.shape if vision.sap_ventas_order_button_image is not None else "No cargada")
        
        # Intentar búsqueda con umbral más bajo
        print("\n🔍 Intentando búsqueda con umbral más bajo...")
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            result = cv2.matchTemplate(screenshot_cv, vision.sap_ventas_order_button_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            print(f"   - Confianza máxima encontrada: {max_val:.3f}")
            print(f"   - Posición del mejor match: {max_loc}")
            
            if max_val > 0.3:  # Umbral muy bajo para debug
                w = vision.sap_ventas_order_button_image.shape[1]
                h = vision.sap_ventas_order_button_image.shape[0]
                center = (max_loc[0] + w//2, max_loc[1] + h//2)
                print(f"   - Centro del mejor match: {center}")
                
                # Guardar screenshot con el mejor match
                marked_screenshot = screenshot_cv.copy()
                cv2.rectangle(marked_screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 2)
                cv2.circle(marked_screenshot, center, 5, (0, 0, 255), -1)
                cv2.imwrite("./debug_screenshots/best_match_orden_venta.png", marked_screenshot)
                print("   📸 Screenshot del mejor match guardado: debug_screenshots/best_match_orden_venta.png")
        
        except Exception as e:
            print(f"   ❌ Error en búsqueda de debug: {e}")
        
        return False
    
    print()
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("   Todos los elementos de navegación fueron encontrados correctamente")
    print("   El problema podría estar en:")
    print("   - Los tiempos de espera entre clics")
    print("   - La secuencia de navegación")
    print("   - La detección de estado después de cada clic")
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando diagnóstico de navegación SAP")
    print()
    
    # Crear directorio de debug si no existe
    os.makedirs("./debug_screenshots", exist_ok=True)
    
    success = diagnose_sap_navigation()
    
    print()
    if success:
        print("🎉 ¡Diagnóstico completado exitosamente!")
        print("   Todos los elementos de navegación están funcionando")
    else:
        print("⚠️  Se encontraron problemas en la navegación")
        print("   Revisa los screenshots en debug_screenshots/ para más detalles")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
