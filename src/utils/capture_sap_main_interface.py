#!/usr/bin/env python3
"""
Script para capturar la imagen de referencia de la interfaz principal de SAP
"""

import cv2
import numpy as np
import pyautogui
import time
import os
import sys

def capture_sap_main_interface():
    """Captura la imagen de referencia de la interfaz principal de SAP"""
    
    print("=== CAPTURA DE IMAGEN DE REFERENCIA DE SAP ===")
    print("Este script capturará una imagen de la interfaz principal de SAP")
    print("para usarla como referencia en la detección automática.")
    print()
    
    # Verificar que el directorio existe
    reference_dir = "./rpa/vision/reference_images"
    if not os.path.exists(reference_dir):
        os.makedirs(reference_dir)
        print(f"📁 Directorio creado: {reference_dir}")
    
    # Dar instrucciones al usuario
    print("📋 INSTRUCCIONES:")
    print("1. Asegúrate de que SAP esté abierto")
    print("2. Navega a la pantalla principal de SAP (donde ves la barra de menú)")
    print("3. El script esperará 5 segundos y luego capturará la pantalla")
    print()
    
    input("Presiona ENTER cuando estés listo para continuar...")
    
    print("⏳ Esperando 5 segundos...")
    time.sleep(5)
    
    try:
        # Capturar screenshot
        print("📸 Capturando screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Guardar imagen
        output_path = os.path.join(reference_dir, "sap_main_interface.png")
        cv2.imwrite(output_path, screenshot_np)
        
        print(f"✅ Imagen guardada exitosamente en: {output_path}")
        print(f"📏 Tamaño de la imagen: {screenshot_np.shape[1]}x{screenshot_np.shape[0]} píxeles")
        
        # Mostrar información adicional
        print("\n📊 INFORMACIÓN DE LA CAPTURA:")
        print(f"   - Formato: PNG")
        print(f"   - Canales de color: {screenshot_np.shape[2] if len(screenshot_np.shape) > 2 else 1}")
        print(f"   - Tamaño del archivo: {os.path.getsize(output_path) / 1024:.1f} KB")
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ejecuta el script de prueba: python test_sap_main_interface_detection.py")
        print("2. Verifica que la detección funcione correctamente")
        print("3. Si es necesario, ajusta el umbral de confianza en el detector")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la captura: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando captura de imagen de referencia de SAP")
    print()
    
    success = capture_sap_main_interface()
    
    print()
    if success:
        print("🎉 ¡Captura completada exitosamente!")
        print("   La imagen de referencia está lista para usar")
    else:
        print("⚠️  La captura no fue exitosa")
        print("   Revisa los errores y vuelve a intentar")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
