#!/usr/bin/env python3
"""
Script para capturar una nueva imagen de referencia del botón "Orden de Venta"
"""

import cv2
import numpy as np
import pyautogui
import time
import os
import sys

def capture_sales_order_button():
    """Captura una nueva imagen de referencia del botón 'Orden de Venta'"""
    
    print("=== CAPTURA DE IMAGEN DE REFERENCIA DEL BOTÓN 'ORDEN DE VENTA' ===")
    print("Este script te ayudará a capturar una nueva imagen del botón 'Orden de Venta'")
    print("para mejorar la detección automática.")
    print()
    
    # Verificar que el directorio existe
    reference_dir = "./rpa/vision/reference_images"
    if not os.path.exists(reference_dir):
        os.makedirs(reference_dir)
        print(f"📁 Directorio creado: {reference_dir}")
    
    # Dar instrucciones al usuario
    print("📋 INSTRUCCIONES:")
    print("1. Abre SAP y navega a la pantalla principal")
    print("2. Haz clic en 'Módulos'")
    print("3. Haz clic en 'Ventas'")
    print("4. Asegúrate de que el menú de ventas esté abierto y visible")
    print("5. El script capturará la pantalla y te permitirá seleccionar el botón")
    print()
    
    input("Presiona ENTER cuando estés listo para continuar...")
    
    print("⏳ Esperando 3 segundos...")
    time.sleep(3)
    
    try:
        # Capturar screenshot
        print("📸 Capturando screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Guardar screenshot temporal
        temp_path = os.path.join(reference_dir, "temp_screenshot.png")
        cv2.imwrite(temp_path, screenshot_cv)
        
        print(f"✅ Screenshot guardado en: {temp_path}")
        print(f"📏 Tamaño de la imagen: {screenshot_cv.shape[1]}x{screenshot_cv.shape[0]} píxeles")
        
        # Mostrar la imagen para selección
        print("\n🖱️  Selección del botón 'Orden de Venta':")
        print("1. Se abrirá la imagen en una ventana")
        print("2. Haz clic y arrastra para seleccionar el área del botón")
        print("3. Presiona 'Enter' para confirmar la selección")
        print("4. Presiona 'r' para reintentar")
        print("5. Presiona 'q' para salir")
        print()
        
        # Función para seleccionar región
        def select_region(event, x, y, flags, param):
            global roi_selected, roi_coords, drawing, start_point, end_point
            
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                start_point = (x, y)
                roi_coords = None
                
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    img_copy = screenshot_cv.copy()
                    cv2.rectangle(img_copy, start_point, (x, y), (0, 255, 0), 2)
                    cv2.imshow('Seleccionar Botón Orden de Venta', img_copy)
                    
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                end_point = (x, y)
                roi_coords = (min(start_point[0], end_point[0]), 
                            min(start_point[1], end_point[1]),
                            abs(end_point[0] - start_point[0]),
                            abs(end_point[1] - start_point[1]))
                
                # Dibujar rectángulo final
                img_copy = screenshot_cv.copy()
                cv2.rectangle(img_copy, start_point, end_point, (0, 255, 0), 2)
                cv2.imshow('Seleccionar Botón Orden de Venta', img_copy)
        
        # Variables globales para la selección
        global roi_selected, roi_coords, drawing, start_point, end_point
        roi_selected = False
        roi_coords = None
        drawing = False
        start_point = None
        end_point = None
        
        # Crear ventana y configurar callback
        cv2.namedWindow('Seleccionar Botón Orden de Venta')
        cv2.setMouseCallback('Seleccionar Botón Orden de Venta', select_region)
        
        # Mostrar imagen
        cv2.imshow('Seleccionar Botón Orden de Venta', screenshot_cv)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("❌ Captura cancelada por el usuario")
                cv2.destroyAllWindows()
                return False
                
            elif key == ord('r'):
                # Reintentar
                roi_coords = None
                cv2.imshow('Seleccionar Botón Orden de Venta', screenshot_cv)
                print("🔄 Reintentando selección...")
                
            elif key == 13:  # Enter
                if roi_coords is not None:
                    # Extraer la región seleccionada
                    x, y, w, h = roi_coords
                    roi = screenshot_cv[y:y+h, x:x+w]
                    
                    # Guardar la imagen del botón
                    output_path = os.path.join(reference_dir, "sap_ventas_order_button.png")
                    cv2.imwrite(output_path, roi)
                    
                    print(f"✅ Imagen del botón guardada en: {output_path}")
                    print(f"📏 Tamaño del botón: {w}x{h} píxeles")
                    
                    # Mostrar información adicional
                    print("\n📊 INFORMACIÓN DE LA CAPTURA:")
                    print(f"   - Formato: PNG")
                    print(f"   - Canales de color: {roi.shape[2] if len(roi.shape) > 2 else 1}")
                    print(f"   - Tamaño del archivo: {os.path.getsize(output_path) / 1024:.1f} KB")
                    print(f"   - Coordenadas: x={x}, y={y}, w={w}, h={h}")
                    
                    # Guardar backup de la imagen anterior
                    old_path = os.path.join(reference_dir, "sap_ventas_order_button_old.png")
                    if os.path.exists(output_path):
                        import shutil
                        shutil.copy2(output_path, old_path)
                        print(f"   - Backup de imagen anterior guardado en: {old_path}")
                    
                    cv2.destroyAllWindows()
                    return True
                else:
                    print("❌ No se ha seleccionado ninguna región")
        
    except Exception as e:
        print(f"❌ Error durante la captura: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando captura de imagen del botón 'Orden de Venta'")
    print()
    
    success = capture_sales_order_button()
    
    print()
    if success:
        print("🎉 ¡Captura completada exitosamente!")
        print("   La nueva imagen de referencia está lista para usar")
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ejecuta el script de diagnóstico: python diagnose_sap_navigation.py")
        print("2. Prueba la navegación mejorada: python improved_sap_navigation.py")
        print("3. Verifica que la detección funcione correctamente")
    else:
        print("⚠️  La captura no fue exitosa")
        print("   Revisa los errores y vuelve a intentar")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
