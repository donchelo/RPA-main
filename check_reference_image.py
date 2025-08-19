#!/usr/bin/env python3
"""
Script para verificar y actualizar la imagen de referencia del botón de orden de ventas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pyautogui
import cv2
import numpy as np
import time

def check_current_reference_image():
    """Verifica la imagen de referencia actual"""
    print("=== VERIFICACIÓN DE IMAGEN DE REFERENCIA ===")
    
    reference_path = "./rpa/vision/reference_images/sap_ventas_order_button.png"
    
    if os.path.exists(reference_path):
        print(f"✅ Imagen de referencia encontrada: {reference_path}")
        
        # Cargar imagen de referencia
        reference_img = cv2.imread(reference_path, cv2.IMREAD_COLOR)
        if reference_img is not None:
            print(f"✅ Imagen cargada correctamente")
            print(f"   Dimensiones: {reference_img.shape[1]}x{reference_img.shape[0]} píxeles")
            print(f"   Tipo: {reference_img.dtype}")
            
            # Guardar una copia para visualización
            cv2.imwrite("current_reference.png", reference_img)
            print("   💾 Copia guardada como 'current_reference.png'")
            
            return True
        else:
            print("❌ Error al cargar la imagen de referencia")
            return False
    else:
        print(f"❌ Imagen de referencia no encontrada: {reference_path}")
        return False

def capture_new_reference_image():
    """Captura una nueva imagen de referencia del botón"""
    print("\n=== CAPTURA DE NUEVA IMAGEN DE REFERENCIA ===")
    print("Este proceso capturará una nueva imagen del botón de orden de ventas")
    print()
    
    print("📋 INSTRUCCIONES:")
    print("1. Navega a SAP Business One")
    print("2. Abre el menú Módulos (Alt + M)")
    print("3. Selecciona Ventas (V)")
    print("4. Cuando aparezca el menú de ventas con el botón 'Orden de Ventas'")
    print("5. El script tomará una captura de la pantalla")
    print()
    
    # Retraso para preparación
    print("⏳ Esperando 10 segundos para que prepares la pantalla...")
    for i in range(10, 0, -1):
        print(f"   {i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n✅ Tiempo completado")
    
    try:
        # Tomar captura de pantalla
        print("\n📸 Tomando captura de pantalla...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        print(f"✅ Captura tomada: {screenshot.size[0]}x{screenshot.size[1]} píxeles")
        
        # Guardar captura completa
        cv2.imwrite("full_screenshot.png", screenshot_cv)
        print("💾 Captura completa guardada como 'full_screenshot.png'")
        
        # Solicitar coordenadas del botón
        print("\n🎯 SELECCIÓN DEL BOTÓN:")
        print("Ahora necesito que me indiques las coordenadas del botón 'Orden de Ventas'")
        print("Puedes usar el mouse para ver las coordenadas en la esquina inferior derecha de la pantalla")
        print()
        
        print("❓ ¿Deseas seleccionar el área del botón manualmente? (s/n): ", end="")
        try:
            response = input().lower()
            if response == 's':
                return select_button_area_manually(screenshot_cv)
            else:
                return capture_button_by_coordinates(screenshot_cv)
        except:
            return capture_button_by_coordinates(screenshot_cv)
            
    except Exception as e:
        print(f"❌ Error al tomar captura: {str(e)}")
        return False

def select_button_area_manually(screenshot_cv):
    """Permite seleccionar manualmente el área del botón"""
    print("\n🖱️ SELECCIÓN MANUAL DEL BOTÓN:")
    print("1. Haz clic y arrastra para seleccionar el área del botón 'Orden de Ventas'")
    print("2. Presiona Enter cuando hayas terminado")
    print()
    
    # Crear ventana para selección
    window_name = "Selecciona el botón de Orden de Ventas"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, screenshot_cv)
    
    # Variables para selección
    drawing = False
    start_point = None
    end_point = None
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, start_point, end_point
        
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_copy = screenshot_cv.copy()
                cv2.rectangle(img_copy, start_point, (x, y), (0, 255, 0), 2)
                cv2.imshow(window_name, img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x, y)
            img_copy = screenshot_cv.copy()
            cv2.rectangle(img_copy, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow(window_name, img_copy)
    
    cv2.setMouseCallback(window_name, mouse_callback)
    
    print("⏳ Esperando selección... (presiona Enter cuando termines)")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    if start_point and end_point:
        # Extraer el área seleccionada
        x1, y1 = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])
        x2, y2 = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])
        
        button_img = screenshot_cv[y1:y2, x1:x2]
        
        # Guardar nueva imagen de referencia
        reference_path = "./rpa/vision/reference_images/sap_ventas_order_button.png"
        cv2.imwrite(reference_path, button_img)
        
        print(f"✅ Nueva imagen de referencia guardada: {reference_path}")
        print(f"   Dimensiones: {button_img.shape[1]}x{button_img.shape[0]} píxeles")
        print(f"   Área seleccionada: ({x1}, {y1}) a ({x2}, {y2})")
        
        return True
    else:
        print("❌ No se seleccionó un área válida")
        return False

def capture_button_by_coordinates(screenshot_cv):
    """Captura el botón usando coordenadas específicas"""
    print("\n📍 CAPTURA POR COORDENADAS:")
    print("Por favor, proporciona las coordenadas del botón 'Orden de Ventas'")
    print("Formato: x1,y1,x2,y2 (ejemplo: 100,200,300,250)")
    print()
    
    try:
        coords_input = input("Coordenadas (x1,y1,x2,y2): ").strip()
        coords = [int(x.strip()) for x in coords_input.split(',')]
        
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            
            # Extraer el área del botón
            button_img = screenshot_cv[y1:y2, x1:x2]
            
            # Guardar nueva imagen de referencia
            reference_path = "./rpa/vision/reference_images/sap_ventas_order_button.png"
            cv2.imwrite(reference_path, button_img)
            
            print(f"✅ Nueva imagen de referencia guardada: {reference_path}")
            print(f"   Dimensiones: {button_img.shape[1]}x{button_img.shape[0]} píxeles")
            print(f"   Área capturada: ({x1}, {y1}) a ({x2}, {y2})")
            
            return True
        else:
            print("❌ Formato de coordenadas inválido")
            return False
            
    except Exception as e:
        print(f"❌ Error al procesar coordenadas: {str(e)}")
        return False

def test_new_reference_image():
    """Prueba la nueva imagen de referencia"""
    print("\n=== PRUEBA DE NUEVA IMAGEN DE REFERENCIA ===")
    
    try:
        from rpa.vision.main import Vision
        vision = Vision()
        
        print("🔍 Probando detección con nueva imagen...")
        coordinates = vision.get_ventas_order_button_coordinates()
        
        if coordinates:
            print(f"✅ Botón detectado en: {coordinates}")
            print("🎉 ¡La nueva imagen de referencia funciona correctamente!")
            return True
        else:
            print("❌ Botón no detectado con nueva imagen")
            print("💡 Posiblemente necesites ajustar el umbral de confianza")
            return False
            
    except Exception as e:
        print(f"❌ Error al probar nueva imagen: {str(e)}")
        return False

if __name__ == "__main__":
    print("🖼️ SISTEMA DE VERIFICACIÓN DE IMAGEN DE REFERENCIA")
    print("Versión: Verificación y actualización de imágenes de referencia")
    print()
    
    # Verificar imagen actual
    current_exists = check_current_reference_image()
    
    if current_exists:
        print("\n❓ ¿Deseas capturar una nueva imagen de referencia? (s/n): ", end="")
        try:
            response = input().lower()
            if response == 's':
                # Capturar nueva imagen
                capture_success = capture_new_reference_image()
                
                if capture_success:
                    print("\n" + "="*50)
                    # Probar nueva imagen
                    test_success = test_new_reference_image()
                    
                    if test_success:
                        print("\n🎉 ¡IMAGEN DE REFERENCIA ACTUALIZADA EXITOSAMENTE!")
                        print("✅ El RPA debería funcionar correctamente ahora")
                    else:
                        print("\n⚠️ Nueva imagen capturada pero no detectada")
                        print("💡 Revisar la calidad de la captura")
                else:
                    print("\n❌ Error al capturar nueva imagen")
            else:
                print("\n⏭️ Manteniendo imagen de referencia actual")
        except:
            print("\n⏭️ Manteniendo imagen de referencia actual")
    else:
        print("\n⚠️ No se encontró imagen de referencia")
        print("💡 Se recomienda capturar una nueva imagen")
        
        # Capturar nueva imagen automáticamente
        capture_success = capture_new_reference_image()
        if capture_success:
            test_success = test_new_reference_image()
            if test_success:
                print("\n🎉 ¡IMAGEN DE REFERENCIA CREADA EXITOSAMENTE!")
    
    print("\n👋 ¡Hasta luego!")
