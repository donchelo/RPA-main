#!/usr/bin/env python3
"""
Script específico para probar el movimiento del mouse al botón de orden de ventas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.simple_logger import rpa_logger
import time
import pyautogui
import cv2
import numpy as np

def test_button_detection_and_mouse_movement():
    """Prueba específica de detección del botón y movimiento del mouse"""
    print("=== PRUEBA ESPECÍFICA DE DETECCIÓN Y MOVIMIENTO ===")
    print("Este script probará exactamente el mismo código que usa el RPA")
    print()
    
    # Retraso para cambio manual de pantalla
    print("⏳ Esperando 5 segundos para cambio manual de pantalla...")
    print("Por favor, navega a SAP → Módulos → Ventas y abre el menú de ventas")
    time.sleep(5)
    print("✅ Retraso completado")
    print()
    
    try:
        vision = Vision()
        
        # PASO 1: Buscar el botón usando el mismo método del RPA
        print("🔍 PASO 1: Buscando botón de Orden de Ventas...")
        print("   Usando: vision.get_ventas_order_button_coordinates()")
        
        orden_ventas_coordinates = vision.get_ventas_order_button_coordinates()
        
        print(f"   Resultado: {orden_ventas_coordinates}")
        
        if orden_ventas_coordinates is None:
            print("   ❌ Botón no encontrado - el RPA se detendría aquí")
            print("   💡 El problema está en la detección del botón, no en el movimiento del mouse")
            return False
        
        print("   ✅ Botón encontrado - continuando con movimiento del mouse")
        
        # PASO 2: Mover el mouse usando el mismo código del RPA
        print(f"\n🖱️ PASO 2: Moviendo cursor al botón...")
        print(f"   Usando: pyautogui.moveTo({orden_ventas_coordinates}, duration=0.5)")
        
        # Obtener posición actual del mouse
        current_pos = pyautogui.position()
        print(f"   Posición actual del mouse: {current_pos}")
        
        # Mover mouse usando el mismo código del RPA
        pyautogui.moveTo(orden_ventas_coordinates, duration=0.5)
        time.sleep(1)
        
        # Verificar nueva posición
        new_pos = pyautogui.position()
        print(f"   Nueva posición del mouse: {new_pos}")
        
        # Verificar si el mouse se movió correctamente
        if abs(new_pos[0] - orden_ventas_coordinates[0]) < 5 and abs(new_pos[1] - orden_ventas_coordinates[1]) < 5:
            print("   ✅ Mouse movido correctamente")
            
            # PASO 3: Hacer clic usando el mismo código del RPA
            print(f"\n🖱️ PASO 3: Haciendo clic...")
            print(f"   Usando: pyautogui.click()")
            
            pyautogui.click()
            time.sleep(3)
            print("   ✅ Clic ejecutado")
            
            print("\n🎉 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
            print("✅ El código del RPA debería funcionar correctamente")
            return True
        else:
            print("   ❌ Error al mover el mouse")
            print("   💡 El problema está en el movimiento del mouse")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_coordinates():
    """Prueba con coordenadas manuales para verificar si el problema es la detección"""
    print("\n=== PRUEBA CON COORDENADAS MANUALES ===")
    print("Esta prueba te permitirá probar el movimiento del mouse con coordenadas que tú proporciones")
    print()
    
    try:
        print("📍 Por favor, proporciona las coordenadas del botón 'Orden de Ventas'")
        print("   Puedes usar el mouse para ver las coordenadas en la esquina inferior derecha")
        print("   Formato: x,y (ejemplo: 500,300)")
        print()
        
        coords_input = input("Coordenadas (x,y): ").strip()
        coords = [int(x.strip()) for x in coords_input.split(',')]
        
        if len(coords) == 2:
            x, y = coords
            print(f"\n🖱️ Probando movimiento a coordenadas: ({x}, {y})")
            
            # Obtener posición actual
            current_pos = pyautogui.position()
            print(f"   Posición actual: {current_pos}")
            
            # Mover mouse
            pyautogui.moveTo(x, y, duration=1)
            time.sleep(1)
            
            # Verificar nueva posición
            new_pos = pyautogui.position()
            print(f"   Nueva posición: {new_pos}")
            
            if abs(new_pos[0] - x) < 5 and abs(new_pos[1] - y) < 5:
                print("   ✅ Mouse movido correctamente")
                
                # Preguntar si hacer clic
                print("\n❓ ¿Deseas que haga clic en estas coordenadas? (s/n): ", end="")
                try:
                    response = input().lower()
                    if response == 's':
                        print("   🖱️ Haciendo clic...")
                        pyautogui.click()
                        time.sleep(2)
                        print("   ✅ Clic ejecutado")
                    else:
                        print("   ⏭️ Clic omitido")
                except:
                    print("   ⏭️ Clic omitido")
                
                return True
            else:
                print("   ❌ Error al mover el mouse")
                return False
        else:
            print("❌ Formato de coordenadas inválido")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba manual: {str(e)}")
        return False

def test_vision_method_directly():
    """Prueba el método de visión directamente para debugging"""
    print("\n=== PRUEBA DIRECTA DEL MÉTODO DE VISIÓN ===")
    
    try:
        vision = Vision()
        
        print("🔍 Probando get_ventas_order_button_coordinates() directamente...")
        
        # Tomar captura de pantalla manualmente
        print("📸 Tomando captura de pantalla...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        print(f"✅ Captura tomada: {screenshot.size[0]}x{screenshot.size[1]} píxeles")
        
        # Guardar captura para análisis
        cv2.imwrite("test_screenshot.png", screenshot_cv)
        print("💾 Captura guardada como 'test_screenshot.png'")
        
        # Verificar imagen de referencia
        reference_path = "./rpa/vision/reference_images/sap_ventas_order_button.png"
        if os.path.exists(reference_path):
            reference_img = cv2.imread(reference_path, cv2.IMREAD_COLOR)
            if reference_img is not None:
                print(f"✅ Imagen de referencia cargada: {reference_img.shape[1]}x{reference_img.shape[0]} píxeles")
                
                # Realizar template matching manualmente
                print("🔍 Realizando template matching...")
                result = cv2.matchTemplate(screenshot_cv, reference_img, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                print(f"📊 Confianza máxima: {max_val:.4f}")
                print(f"📍 Ubicación máxima: {max_loc}")
                
                if max_val > 0.7:
                    w_button = reference_img.shape[1]
                    h_button = reference_img.shape[0]
                    center_x = max_loc[0] + w_button // 2
                    center_y = max_loc[1] + h_button // 2
                    
                    print(f"✅ Botón detectado en: ({center_x}, {center_y})")
                    print(f"📏 Dimensiones del botón: {w_button}x{h_button}")
                    
                    return (center_x, center_y)
                else:
                    print("❌ Confianza insuficiente")
                    return None
            else:
                print("❌ Error al cargar imagen de referencia")
                return None
        else:
            print(f"❌ Imagen de referencia no encontrada: {reference_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error en prueba directa: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🖱️ SISTEMA DE PRUEBA DE MOVIMIENTO DE MOUSE")
    print("Versión: Verificación específica de detección y movimiento")
    print()
    
    # Prueba 1: Método completo del RPA
    print("="*60)
    test1_success = test_button_detection_and_mouse_movement()
    
    if not test1_success:
        print("\n" + "="*60)
        # Prueba 2: Método de visión directamente
        print("🔍 El método del RPA falló, probando método de visión directamente...")
        coords = test_vision_method_directly()
        
        if coords:
            print(f"\n✅ Método de visión funciona, coordenadas: {coords}")
            print("💡 El problema puede estar en la integración")
        else:
            print("\n❌ Método de visión también falla")
            print("💡 El problema está en la detección del botón")
    
    print("\n" + "="*60)
    # Prueba 3: Coordenadas manuales
    print("🖱️ Prueba con coordenadas manuales...")
    test3_success = test_manual_coordinates()
    
    if test3_success:
        print("\n✅ Movimiento del mouse funciona con coordenadas manuales")
        print("💡 El problema está en la detección automática del botón")
    else:
        print("\n❌ Movimiento del mouse falla incluso con coordenadas manuales")
        print("💡 El problema está en el control del mouse")
    
    print("\n👋 ¡Hasta luego!")
