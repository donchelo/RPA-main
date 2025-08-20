#!/usr/bin/env python3
"""
Script de diagnóstico para el botón "Agregar y"
Ayuda a validar y mejorar la detección del botón en la esquina inferior izquierda
"""

import os
import sys
import cv2
import numpy as np
import pyautogui
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(__file__))

from rpa.simple_logger import rpa_logger
from rpa.vision.template_matcher import template_matcher
from rpa.config_manager import config

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    print(f"\n--- {title} ---")

def test_screen_resolution():
    """Prueba la resolución de pantalla"""
    print_section("RESOLUCIÓN DE PANTALLA")
    
    screen_width, screen_height = pyautogui.size()
    print(f"Resolución actual: {screen_width}x{screen_height}")
    
    # Calcular región de búsqueda
    width_ratio = config.get('template_matching.agregar_y_button.search_region_width_ratio', 0.33)
    height_ratio = config.get('template_matching.agregar_y_button.search_region_height_ratio', 0.25)
    
    search_width = int(screen_width * width_ratio)
    search_height = int(screen_height * height_ratio)
    search_x = 0
    search_y = screen_height - search_height
    
    print(f"Región de búsqueda: ({search_x}, {search_y}) - ({search_x + search_width}, {search_y + search_height})")
    print(f"Tamaño de región: {search_width}x{search_height}")
    
    return (search_x, search_y, search_width, search_height)

def test_template_loading():
    """Prueba la carga del template"""
    print_section("CARGA DE TEMPLATE")
    
    template_path = os.path.join("rpa", "vision", "reference_images", "agregar_y_button.png")
    
    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return None
    
    print(f"✅ Template encontrado: {template_path}")
    
    # Cargar imagen
    template_image = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template_image is None:
        print("❌ No se pudo cargar la imagen")
        return None
    
    height, width = template_image.shape[:2]
    print(f"✅ Template cargado: {width}x{height} píxeles")
    
    # Verificar tamaño mínimo
    if width < 20 or height < 10:
        print("⚠️  Template muy pequeño, puede causar problemas de detección")
    else:
        print("✅ Tamaño de template adecuado")
    
    return template_image

def test_template_matching(template_image, search_region):
    """Prueba el template matching en la región específica"""
    print_section("PRUEBA DE TEMPLATE MATCHING")
    
    if template_image is None:
        print("❌ No hay template para probar")
        return False
    
    # Obtener configuraciones
    primary_confidence = config.get('template_matching.agregar_y_button.primary_confidence', 0.85)
    fallback_confidence = config.get('template_matching.agregar_y_button.fallback_confidence', 0.75)
    
    print(f"Confianza primaria: {primary_confidence}")
    print(f"Confianza fallback: {fallback_confidence}")
    
    # Tomar screenshot de la región
    x, y, w, h = search_region
    print(f"Capturando región: ({x}, {y}) - {w}x{h}")
    
    try:
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Guardar screenshot para análisis
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"debug_screenshot_{timestamp}.png"
        cv2.imwrite(screenshot_path, screenshot_np)
        print(f"✅ Screenshot guardado: {screenshot_path}")
        
        # Probar template matching
        print("\nProbando template matching...")
        
        # Búsqueda en región específica
        coordinates = template_matcher.find_template(
            template_image,
            confidence=primary_confidence,
            search_region=(0, 0, w, h)  # Región relativa al screenshot
        )
        
        if coordinates:
            print(f"✅ Botón encontrado en región específica: {coordinates}")
            # Convertir coordenadas relativas a absolutas
            abs_x = x + coordinates[0]
            abs_y = y + coordinates[1]
            print(f"   Coordenadas absolutas: ({abs_x}, {abs_y})")
            return True
        else:
            print(f"❌ Botón no encontrado con confianza {primary_confidence}")
            
            # Probar con confianza más baja
            coordinates = template_matcher.find_template(
                template_image,
                confidence=fallback_confidence,
                search_region=(0, 0, w, h)
            )
            
            if coordinates:
                print(f"⚠️  Botón encontrado con confianza reducida: {coordinates}")
                abs_x = x + coordinates[0]
                abs_y = y + coordinates[1]
                print(f"   Coordenadas absolutas: ({abs_x}, {abs_y})")
                return True
            else:
                print(f"❌ Botón no encontrado con confianza {fallback_confidence}")
                return False
                
    except Exception as e:
        print(f"❌ Error en template matching: {str(e)}")
        return False

def capture_new_template():
    """Captura un nuevo template del botón"""
    print_section("CAPTURA DE NUEVO TEMPLATE")
    
    print("Para capturar un nuevo template:")
    print("1. Abra SAP y navegue hasta la pantalla con el botón 'Agregar y'")
    print("2. Posicione el mouse sobre el botón 'Agregar y'")
    print("3. Presione Enter cuando esté listo")
    
    try:
        input("Presione Enter cuando el mouse esté sobre el botón 'Agregar y'...")
        
        mouse_x, mouse_y = pyautogui.position()
        print(f"Posición del mouse: ({mouse_x}, {mouse_y})")
        
        # Capturar región
        region_size = 100
        region_x = max(0, mouse_x - region_size // 2)
        region_y = max(0, mouse_y - region_size // 2)
        
        screenshot = pyautogui.screenshot(region=(region_x, region_y, region_size, region_size))
        
        # Guardar template
        template_path = os.path.join("rpa", "vision", "reference_images", "agregar_y_button.png")
        screenshot.save(template_path)
        
        print(f"✅ Nuevo template guardado: {template_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error capturando template: {str(e)}")
        return False

def main():
    """Función principal del script de diagnóstico"""
    print_header("DIAGNÓSTICO DEL BOTÓN 'AGREGAR Y'")
    
    print("Este script ayuda a diagnosticar y mejorar la detección del botón 'Agregar y'")
    print("que se encuentra en la esquina inferior izquierda de la pantalla.")
    
    # 1. Probar resolución de pantalla
    search_region = test_screen_resolution()
    
    # 2. Probar carga de template
    template_image = test_template_loading()
    
    # 3. Probar template matching
    if template_image is not None:
        success = test_template_matching(template_image, search_region)
        
        if not success:
            print_section("RECOMENDACIONES")
            print("❌ El botón no se pudo detectar. Posibles soluciones:")
            print("1. Verificar que SAP esté abierto y visible")
            print("2. Verificar que el botón 'Agregar y' esté en la esquina inferior izquierda")
            print("3. Capturar un nuevo template del botón")
            print("4. Ajustar las configuraciones de confianza en config.yaml")
            
            response = input("\n¿Desea capturar un nuevo template? (s/n): ")
            if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                capture_new_template()
    
    print_section("FIN DEL DIAGNÓSTICO")
    print("Revise los archivos de log para más detalles.")

if __name__ == "__main__":
    main()
