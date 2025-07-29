#!/usr/bin/env python3
"""
Script para capturar imágenes de referencia de SAP Business One
"""

import pyautogui
import time
import os
from rpa.logger import rpa_logger

def capture_sap_references():
    """Captura imágenes de referencia de SAP Business One"""
    print("📸 Iniciando captura de imágenes de referencia de SAP")
    print("=" * 60)
    
    # Crear directorio si no existe
    reference_dir = "./rpa/vision/reference_images"
    if not os.path.exists(reference_dir):
        os.makedirs(reference_dir)
        print(f"✅ Directorio creado: {reference_dir}")
    
    try:
        # 1. Capturar escritorio remoto
        print("1️⃣ Capturando escritorio remoto...")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{reference_dir}/remote_desktop.png")
        print("✅ Escritorio remoto capturado")
        
        # 2. Buscar SAP Business One
        print("2️⃣ Buscando SAP Business One...")
        print("💡 Asegúrate de que SAP Business One esté visible en la pantalla")
        
        # Tomar captura de pantalla completa
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{reference_dir}/sap_desktop.png")
        print("✅ Pantalla completa capturada")
        
        # 3. Instrucciones para el usuario
        print("\n📋 INSTRUCCIONES:")
        print("1. Abre SAP Business One en el escritorio remoto")
        print("2. Asegúrate de que el ícono de SAP sea visible")
        print("3. Ejecuta este script nuevamente")
        print("4. El sistema detectará automáticamente SAP Business One")
        
        # 4. Probar detección de texto
        print("\n🔍 Probando detección de texto...")
        from rpa.vision.main import Vision
        vision = Vision()
        
        coordinates = vision.get_sap_text_coordinates()
        if coordinates:
            print(f"✅ SAP Business One encontrado en: {coordinates}")
            print("🎉 El sistema está listo para usar!")
        else:
            print("❌ SAP Business One no encontrado")
            print("💡 Asegúrate de que SAP esté abierto y visible")
        
    except Exception as e:
        print(f"❌ Error durante la captura: {str(e)}")
        rpa_logger.log_error(f"Error en captura de referencias: {str(e)}", "Función capture_sap_references")

def main():
    """Función principal"""
    print("🚀 Script de captura de imágenes de referencia")
    print("=" * 60)
    
    capture_sap_references()

if __name__ == "__main__":
    main() 