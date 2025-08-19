#!/usr/bin/env python3
"""
Script de Debug para Detección - RPA TAMAPRINT
Para ver exactamente qué está detectando el sistema
"""

import time
import cv2
import numpy as np
from rpa.screen_detector import screen_detector, ScreenState
from rpa.simple_logger import rpa_logger


def debug_detection():
    """Debug detallado de la detección"""
    
    print("🔍 DEBUG DE DETECCIÓN")
    print("=" * 50)
    print()
    
    # Delay inicial
    print("⏳ Iniciando en 5 segundos...")
    print("💡 Asegúrate de tener Remote Desktop abierto y visible")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔍 Detectando con debug...")
    
    try:
        # Detectar con screenshot guardado
        result = screen_detector.detect_current_screen(save_screenshot=True)
        
        print(f"✅ Estado detectado: {result.state.value}")
        print(f"📊 Confianza: {result.confidence:.3f}")
        print(f"📁 Screenshot guardado: {result.screenshot_path}")
        
        # Mostrar detalles de confianza
        if "all_confidences" in result.details:
            print("\n📈 Confianzas por estado:")
            for state, conf in result.details["all_confidences"].items():
                print(f"   {state.value}: {conf:.3f}")
        
        # Análisis detallado
        print(f"\n🔍 Análisis detallado:")
        print(f"   - Umbral Remote Desktop: 0.85")
        print(f"   - Umbral SAP Desktop: 0.80")
        print(f"   - Umbral Sales Order Form: 0.85")
        print(f"   - Confianza más alta: {max(result.details['all_confidences'].values()):.3f}")
        
        # Recomendaciones
        print(f"\n💡 Recomendaciones:")
        if result.state == ScreenState.UNKNOWN:
            print("   - La pantalla actual no coincide con ninguna referencia")
            print("   - Verifica que Remote Desktop esté abierto y visible")
            print("   - Asegúrate de que la ventana esté maximizada")
            print("   - Revisa el screenshot guardado para ver qué capturó")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_remote_desktop_specific():
    """Test específico para Remote Desktop"""
    
    print("\n🎯 TEST ESPECÍFICO REMOTE DESKTOP")
    print("=" * 50)
    
    try:
        # Cargar imagen de referencia
        reference_image = cv2.imread('./rpa/vision/reference_images/remote_desktop.png', cv2.IMREAD_UNCHANGED)
        if reference_image is None:
            print("❌ No se pudo cargar la imagen de referencia")
            return
        
        print(f"✅ Imagen de referencia cargada: {reference_image.shape}")
        
        # Tomar screenshot actual
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        print(f"✅ Screenshot actual tomado: {screenshot_np.shape}")
        
        # Hacer template matching
        result = cv2.matchTemplate(screenshot_np, reference_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        print(f"📊 Resultado template matching:")
        print(f"   - Confianza máxima: {max_val:.3f}")
        print(f"   - Ubicación: {max_loc}")
        print(f"   - Umbral requerido: 0.85")
        print(f"   - ¿Cumple umbral?: {'✅' if max_val >= 0.85 else '❌'}")
        
        # Guardar imagen para análisis
        cv2.imwrite("./debug_screenshots/current_screen_debug.png", screenshot_np)
        print(f"📁 Screenshot guardado en: ./debug_screenshots/current_screen_debug.png")
        
    except Exception as e:
        print(f"❌ Error en test específico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🔍 SISTEMA DE DEBUG DE DETECCIÓN")
    print("Versión: Debug detallado")
    print()
    
    # Debug general
    result = debug_detection()
    
    # Test específico
    test_remote_desktop_specific()
    
    print("\n👋 Debug completado!")
    print("💡 Revisa los screenshots guardados para análisis")
