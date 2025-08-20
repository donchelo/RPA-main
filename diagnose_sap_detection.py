#!/usr/bin/env python3
"""
Script de diagnóstico para detectar problemas en la detección de SAP
"""

import cv2
import numpy as np
import pyautogui
import time
from datetime import datetime

def diagnose_sap_detection():
    """Diagnostica problemas de detección de SAP"""
    
    print("=== DIAGNÓSTICO DE DETECCIÓN SAP ===")
    print("Este script ayudará a identificar por qué no se detecta SAP")
    print()
    
    # 1. Capturar screenshot actual
    print("1. Capturando screenshot actual...")
    screenshot = pyautogui.screenshot()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"debug_current_screen_{timestamp}.png"
    screenshot.save(screenshot_path)
    print(f"   Screenshot guardado: {screenshot_path}")
    
    # Convertir para OpenCV
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    
    # 2. Cargar template de SAP
    print("2. Cargando template de SAP...")
    try:
        sap_icon = cv2.imread('./rpa/vision/reference_images/sap_icon.png', cv2.IMREAD_COLOR)
        if sap_icon is None:
            print("   ❌ ERROR: No se pudo cargar sap_icon.png")
            return
        print(f"   ✅ Template cargado: {sap_icon.shape}")
    except Exception as e:
        print(f"   ❌ ERROR cargando template: {e}")
        return
    
    # 3. Realizar template matching con diferentes umbrales
    print("3. Probando detección con diferentes umbrales...")
    result = cv2.matchTemplate(screenshot_cv, sap_icon, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"   Confianza máxima encontrada: {max_val:.4f}")
    print(f"   Ubicación: {max_loc}")
    
    # Probar diferentes umbrales
    umbrales = [0.3, 0.5, 0.7, 0.8, 0.9]
    for umbral in umbrales:
        if max_val >= umbral:
            print(f"   ✅ Pasaría con umbral {umbral}")
        else:
            print(f"   ❌ Fallaría con umbral {umbral}")
    
    # 4. Crear imagen de resultado visual
    print("4. Creando imagen de diagnóstico...")
    result_img = screenshot_cv.copy()
    
    # Dibujar rectángulo en la mejor coincidencia
    if max_val > 0.3:  # Umbral mínimo para visualización
        w, h = sap_icon.shape[1], sap_icon.shape[0]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(result_img, f"Conf: {max_val:.3f}", 
                   (top_left[0], top_left[1] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    result_path = f"debug_sap_detection_{timestamp}.png"
    cv2.imwrite(result_path, result_img)
    print(f"   Imagen de diagnóstico guardada: {result_path}")
    
    # 5. Buscar texto SAP usando OCR
    print("5. Buscando texto 'SAP' usando OCR...")
    try:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        ocr_text = pytesseract.image_to_string(screenshot, lang='eng')
        if 'SAP' in ocr_text.upper():
            print("   ✅ Texto 'SAP' encontrado via OCR")
            # Mostrar líneas que contienen SAP
            for i, line in enumerate(ocr_text.split('\n')):
                if 'SAP' in line.upper():
                    print(f"      Línea {i}: {line.strip()}")
        else:
            print("   ❌ Texto 'SAP' NO encontrado via OCR")
    except Exception as e:
        print(f"   ❌ Error en OCR: {e}")
    
    # 6. Recomendaciones
    print()
    print("=== RECOMENDACIONES ===")
    
    if max_val < 0.3:
        print("❌ CRÍTICO: Confianza muy baja (<0.3)")
        print("   - El template sap_icon.png no coincide con la pantalla actual")
        print("   - Necesitas capturar un nuevo template del ícono SAP actual")
    elif max_val < 0.7:
        print("⚠️  ADVERTENCIA: Confianza baja (<0.7)")
        print("   - Podrías reducir temporalmente el umbral a 0.5")
        print("   - O actualizar el template para mayor precisión")
    else:
        print("✅ Template matching OK - El problema podría estar en otro lugar")
    
    print()
    print("Para solucionar:")
    print("1. Abre SAP manualmente en el escritorio remoto")
    print("2. Toma un screenshot del ícono SAP actual")
    print("3. Reemplaza rpa/vision/reference_images/sap_icon.png")
    print("4. Ejecuta este diagnóstico nuevamente")

if __name__ == "__main__":
    diagnose_sap_detection()