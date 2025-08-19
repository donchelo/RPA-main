#!/usr/bin/env python3
"""
Script de diagnóstico detallado para la navegación a órdenes de ventas
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

def debug_navigation_step_by_step():
    """Diagnóstico paso a paso de la navegación"""
    print("=== DIAGNÓSTICO DETALLADO DE NAVEGACIÓN ===")
    print("Este script diagnosticará exactamente dónde falla la navegación")
    print()
    
    # Retraso para cambio manual de pantalla
    print("⏳ Esperando 5 segundos para cambio manual de pantalla...")
    print("Por favor, navega a SAP → Módulos → Ventas y abre el menú de ventas")
    time.sleep(5)
    print("✅ Retraso completado")
    print()
    
    try:
        vision = Vision()
        
        # PASO 1: Verificar que estamos en SAP
        print("🔍 PASO 1: Verificando que estamos en SAP...")
        sap_desktop = vision.is_sap_desktop_visible()
        print(f"   Resultado: {'✅ En SAP' if sap_desktop else '❌ No en SAP'}")
        
        # PASO 2: Tomar captura de pantalla actual
        print("\n📸 PASO 2: Tomando captura de pantalla actual...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        print(f"   ✅ Captura tomada: {screenshot.size[0]}x{screenshot.size[1]} píxeles")
        
        # Guardar captura para análisis
        cv2.imwrite("debug_current_screen.png", screenshot_cv)
        print("   💾 Captura guardada como 'debug_current_screen.png'")
        
        # PASO 3: Verificar que la imagen de referencia existe
        print("\n🖼️ PASO 3: Verificando imagen de referencia...")
        reference_path = "./rpa/vision/reference_images/sap_ventas_order_button.png"
        if os.path.exists(reference_path):
            print(f"   ✅ Imagen de referencia encontrada: {reference_path}")
            reference_img = cv2.imread(reference_path, cv2.IMREAD_COLOR)
            if reference_img is not None:
                print(f"   ✅ Imagen cargada: {reference_img.shape[1]}x{reference_img.shape[0]} píxeles")
            else:
                print("   ❌ Error al cargar la imagen de referencia")
                return False
        else:
            print(f"   ❌ Imagen de referencia no encontrada: {reference_path}")
            return False
        
        # PASO 4: Realizar template matching manual
        print("\n🔍 PASO 4: Realizando template matching manual...")
        result = cv2.matchTemplate(screenshot_cv, reference_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        print(f"   📊 Confianza máxima: {max_val:.4f}")
        print(f"   📍 Ubicación máxima: {max_loc}")
        
        # PASO 5: Verificar umbral de confianza
        print("\n🎯 PASO 5: Verificando umbral de confianza...")
        confidence_threshold = 0.7
        print(f"   Umbral configurado: {confidence_threshold}")
        print(f"   Confianza obtenida: {max_val:.4f}")
        
        if max_val > confidence_threshold:
            print("   ✅ Confianza suficiente - botón detectado")
            
            # Calcular coordenadas del centro
            w_button = reference_img.shape[1]
            h_button = reference_img.shape[0]
            center_x = max_loc[0] + w_button // 2
            center_y = max_loc[1] + h_button // 2
            
            print(f"   📍 Coordenadas del centro: ({center_x}, {center_y})")
            print(f"   📏 Dimensiones del botón: {w_button}x{h_button}")
            
            # PASO 6: Simular movimiento del mouse
            print("\n🖱️ PASO 6: Simulando movimiento del mouse...")
            print(f"   Moviendo mouse a: ({center_x}, {center_y})")
            
            # Obtener posición actual del mouse
            current_pos = pyautogui.position()
            print(f"   Posición actual del mouse: {current_pos}")
            
            # Mover mouse (sin hacer clic por seguridad)
            pyautogui.moveTo(center_x, center_y, duration=1)
            time.sleep(0.5)
            
            # Verificar nueva posición
            new_pos = pyautogui.position()
            print(f"   Nueva posición del mouse: {new_pos}")
            
            if abs(new_pos[0] - center_x) < 5 and abs(new_pos[1] - center_y) < 5:
                print("   ✅ Mouse movido correctamente")
                
                # Preguntar si hacer clic
                print("\n❓ ¿Deseas que haga clic en el botón? (s/n): ", end="")
                try:
                    response = input().lower()
                    if response == 's':
                        print("   🖱️ Haciendo clic...")
                        pyautogui.click()
                        print("   ✅ Clic ejecutado")
                        time.sleep(2)
                        print("   ⏳ Esperando 2 segundos para ver resultado...")
                    else:
                        print("   ⏭️ Clic omitido por seguridad")
                except:
                    print("   ⏭️ Clic omitido por seguridad")
            else:
                print("   ❌ Error al mover el mouse")
                return False
            
        else:
            print("   ❌ Confianza insuficiente - botón no detectado")
            print("   💡 Posibles causas:")
            print("      - El menú de ventas no está abierto")
            print("      - La imagen de referencia no coincide")
            print("      - La resolución o tema de SAP es diferente")
            print("      - El botón está en una ubicación diferente")
            
            # Mostrar las mejores coincidencias
            print("\n🔍 Buscando las mejores coincidencias...")
            threshold = 0.3  # Umbral más bajo para debugging
            locations = np.where(result >= threshold)
            if len(locations[0]) > 0:
                print(f"   Encontradas {len(locations[0])} coincidencias con confianza >= {threshold}")
                for i in range(min(5, len(locations[0]))):  # Mostrar máximo 5
                    y, x = locations[0][i], locations[1][i]
                    conf = result[y, x]
                    print(f"      Coincidencia {i+1}: ({x}, {y}) - Confianza: {conf:.4f}")
            else:
                print("   No se encontraron coincidencias significativas")
            
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_navigation():
    """Prueba la navegación manual paso a paso"""
    print("\n=== PRUEBA DE NAVEGACIÓN MANUAL ===")
    print("Este script simulará la navegación manual paso a paso")
    print()
    
    try:
        print("🖥️ PASO 1: Activando ventana del escritorio remoto...")
        windows = pyautogui.getWindowsWithTitle("20.96.6.64 - Conexión a Escritorio remoto")
        if windows:
            window = windows[0]
            if not window.isActive:
                window.activate()
                time.sleep(2)
                print("   ✅ Ventana activada")
            else:
                print("   ✅ Ventana ya estaba activa")
        else:
            print("   ❌ Ventana del escritorio remoto no encontrada")
            return False
        
        print("\n⌨️ PASO 2: Abriendo menú módulos (Alt + M)...")
        pyautogui.keyDown('alt')
        time.sleep(0.1)
        pyautogui.press('m')
        time.sleep(0.1)
        pyautogui.keyUp('alt')
        time.sleep(2)
        print("   ✅ Menú módulos abierto")
        
        print("\n⌨️ PASO 3: Seleccionando módulo Ventas (V)...")
        pyautogui.press('v')
        time.sleep(2)
        print("   ✅ Módulo Ventas seleccionado")
        
        print("\n🔍 PASO 4: Buscando botón de Orden de Ventas...")
        vision = Vision()
        coordinates = vision.get_ventas_order_button_coordinates()
        
        if coordinates:
            print(f"   ✅ Botón encontrado en: {coordinates}")
            
            print("\n🖱️ PASO 5: Moviendo mouse al botón...")
            pyautogui.moveTo(coordinates, duration=1)
            time.sleep(1)
            print("   ✅ Mouse movido")
            
            print("\n🖱️ PASO 6: Haciendo clic...")
            pyautogui.click()
            time.sleep(3)
            print("   ✅ Clic ejecutado")
            
            print("\n🎉 ¡NAVEGACIÓN MANUAL COMPLETADA!")
            return True
        else:
            print("   ❌ Botón no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error en navegación manual: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 SISTEMA DE DIAGNÓSTICO DE NAVEGACIÓN")
    print("Versión: Análisis detallado de problemas de navegación")
    print()
    
    # Diagnóstico paso a paso
    debug_success = debug_navigation_step_by_step()
    
    if debug_success:
        print("\n" + "="*50)
        # Prueba de navegación manual
        nav_success = test_manual_navigation()
        
        if nav_success:
            print("\n🎉 ¡DIAGNÓSTICO COMPLETADO EXITOSAMENTE!")
            print("✅ La navegación debería funcionar correctamente")
        else:
            print("\n❌ NAVEGACIÓN MANUAL FALLIDA")
            print("⚠️ Revisar la configuración de SAP")
    else:
        print("\n❌ DIAGNÓSTICO FALLIDO")
        print("⚠️ Revisar las imágenes de referencia y la configuración")
    
    print("\n👋 ¡Hasta luego!")
