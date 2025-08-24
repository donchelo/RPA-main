#!/usr/bin/env python3
"""
Script para capturar imágenes de referencia del módulo de órdenes de producción
"""

import os
import time
import pyautogui
from datetime import datetime

# Configuración
IMAGES_DIR = "rpa/vision/reference_images/production"
DELAY_BETWEEN_CAPTURES = 3  # segundos

def create_directory():
    """Crear directorio si no existe"""
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"✅ Directorio creado: {IMAGES_DIR}")

def capture_screenshot(filename, description):
    """Capturar screenshot con descripción"""
    print(f"\n📸 {description}")
    print(f"   Preparándose para capturar: {filename}")
    print(f"   Tienes {DELAY_BETWEEN_CAPTURES} segundos para posicionar la pantalla...")
    
    for i in range(DELAY_BETWEEN_CAPTURES, 0, -1):
        print(f"   Capturando en {i}...")
        time.sleep(1)
    
    filepath = os.path.join(IMAGES_DIR, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"   ✅ Imagen guardada: {filepath}")
    return filepath

def main():
    """Función principal"""
    print("🎯 CAPTURA DE IMÁGENES DE REFERENCIA - MÓDULO DE PRODUCCIÓN")
    print("=" * 60)
    
    # Crear directorio
    create_directory()
    
    print("\n📋 INSTRUCCIONES:")
    print("1. Abre SAP Business One")
    print("2. Sigue las instrucciones para cada captura")
    print("3. Posiciona la pantalla según se indique")
    print("4. El script capturará automáticamente")
    
    input("\n⏸️  Presiona ENTER cuando estés listo para comenzar...")
    
    # Lista de imágenes a capturar
    images_to_capture = [
        {
            "filename": "sap_produccion_menu.png",
            "description": "Menú de módulos después de presionar Alt+M (debe mostrar 'Producción' visible)"
        },
        {
            "filename": "sap_orden_fabricacion_button.png",
            "description": "Botón específico de 'Orden de Fabricación' en el menú de producción"
        },
        {
            "filename": "sap_produccion_form.png",
            "description": "Formulario completo de orden de producción (pantalla completa)"
        },
        {
            "filename": "sap_articulo_field.png",
            "description": "Campo específico donde se ingresa el número de artículo (zoom en el campo)"
        },
        {
            "filename": "sap_pedido_interno_field.png",
            "description": "Campo donde se ingresa el número de pedido interno (zoom en el campo)"
        },
        {
            "filename": "sap_cantidad_field.png",
            "description": "Campo de cantidad (zoom en el campo)"
        },
        {
            "filename": "sap_fecha_finalizacion_field.png",
            "description": "Campo de fecha de finalización (zoom en el campo)"
        },
        {
            "filename": "sap_produccion_crear_button.png",
            "description": "Botón 'Crear' para finalizar la orden de producción"
        }
    ]
    
    captured_images = []
    
    for i, image_info in enumerate(images_to_capture, 1):
        print(f"\n🔄 Progreso: {i}/{len(images_to_capture)}")
        
        # Instrucciones específicas
        if image_info["filename"] == "sap_produccion_menu.png":
            print("\n📝 INSTRUCCIONES ESPECÍFICAS:")
            print("1. En SAP, presiona Alt+M")
            print("2. Asegúrate de que el menú de módulos esté visible")
            print("3. La palabra 'Producción' debe estar visible en la pantalla")
            
        elif image_info["filename"] == "sap_orden_fabricacion_button.png":
            print("\n📝 INSTRUCCIONES ESPECÍFICAS:")
            print("1. En el menú de módulos, busca 'Producción'")
            print("2. Haz clic en 'Producción' para abrir el submenú")
            print("3. Busca el botón 'Orden de Fabricación'")
            print("4. Posiciona la pantalla para que el botón sea claramente visible")
            
        elif image_info["filename"] == "sap_produccion_form.png":
            print("\n📝 INSTRUCCIONES ESPECÍFICAS:")
            print("1. Haz clic en 'Orden de Fabricación'")
            print("2. Espera a que se abra el formulario")
            print("3. Captura toda la pantalla del formulario")
            
        elif "field" in image_info["filename"]:
            print("\n📝 INSTRUCCIONES ESPECÍFICAS:")
            print("1. En el formulario de orden de producción")
            print("2. Navega al campo correspondiente")
            print("3. Haz zoom en el campo específico")
            print("4. Asegúrate de que el campo esté claramente visible")
            
        elif "button" in image_info["filename"]:
            print("\n📝 INSTRUCCIONES ESPECÍFICAS:")
            print("1. En el formulario de orden de producción")
            print("2. Busca el botón correspondiente")
            print("3. Posiciona la pantalla para que el botón sea claramente visible")
        
        # Capturar imagen
        filepath = capture_screenshot(image_info["filename"], image_info["description"])
        captured_images.append(filepath)
        
        if i < len(images_to_capture):
            print(f"\n⏸️  Pausa de 2 segundos antes de la siguiente captura...")
            time.sleep(2)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 CAPTURA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"📁 Directorio: {IMAGES_DIR}")
    print(f"📸 Imágenes capturadas: {len(captured_images)}")
    
    print("\n📋 IMÁGENES CAPTURADAS:")
    for i, filepath in enumerate(captured_images, 1):
        filename = os.path.basename(filepath)
        print(f"   {i}. {filename}")
    
    print("\n✅ El módulo de producción está listo para usar estas imágenes de referencia!")
    print("💡 Recuerda: Estas imágenes son críticas para el funcionamiento del RPA.")

if __name__ == "__main__":
    main()
