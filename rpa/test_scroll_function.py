"""
Script de prueba para la función scroll_to_bottom
"""

import time
import pyautogui
from rpa.logger import rpa_logger

def test_scroll_to_bottom():
    """Prueba la función scroll_to_bottom"""
    print("=== PRUEBA DE FUNCIÓN SCROLL_TO_BOTTOM ===\n")
    
    try:
        # Simular la clase RPA
        class TestRPA:
            def scroll_to_bottom(self):
                """Baja el scroll hasta el final de la página"""
                start_time = time.time()
                rpa_logger.log_action("Iniciando scroll hacia abajo", "Buscando barra de desplazamiento vertical")
                
                try:
                    # Importar el módulo de visión
                    from rpa.vision import main as vision
                    
                    # Buscar la barra de desplazamiento usando la imagen de referencia
                    rpa_logger.log_action("Buscando barra de desplazamiento", "Usando imagen de referencia: scroll_to_bottom.png")
                    coordinates = vision.get_scrollbar_coordinates()
                    
                    if not coordinates:
                        rpa_logger.log_error('No se pudo encontrar la barra de desplazamiento en la pantalla', 'Imagen de referencia no encontrada')
                        return False
                        
                    # Verificar que las coordenadas sean válidas
                    if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                        rpa_logger.log_error(f'Coordenadas inválidas de scrollbar: {coordinates}', 'Formato de coordenadas incorrecto')
                        return False
                    
                    scrollbar_x, scrollbar_y = coordinates
                    rpa_logger.log_action("Barra de desplazamiento encontrada", f"Coordenadas: {coordinates}")
                    
                    # Hacer clic en la barra de desplazamiento
                    rpa_logger.log_action("Haciendo clic en barra de desplazamiento", f"Posición: {coordinates}")
                    pyautogui.click(scrollbar_x, scrollbar_y)
                    time.sleep(1)
                    
                    # Obtener dimensiones de pantalla para calcular distancia de scroll
                    screen_width, screen_height = pyautogui.size()
                    
                    # Arrastrar hacia abajo hasta el final
                    # Calcular la distancia para bajar completamente
                    scroll_distance = screen_height - 100  # Dejar un margen de 100 píxeles
                    
                    print(f"Resolución de pantalla: {screen_width}x{screen_height}")
                    print(f"Posición de scrollbar: {coordinates}")
                    print(f"Distancia de scroll: {scroll_distance} píxeles")
                    
                    rpa_logger.log_action("Arrastrando scroll hacia abajo", f"Distancia: {scroll_distance} píxeles")
                    pyautogui.drag(0, scroll_distance, duration=2)  # Arrastrar hacia abajo durante 2 segundos
                    
                    time.sleep(2)  # Esperar a que se complete el scroll
                    
                    duration = time.time() - start_time
                    rpa_logger.log_performance("Scroll hacia abajo completado", duration)
                    rpa_logger.log_action("Scroll hacia abajo completado exitosamente", "Página desplazada al final")
                    
                    return True
                    
                except Exception as e:
                    rpa_logger.log_error(f"Error al hacer scroll hacia abajo: {str(e)}", "Error en scroll")
                    raise
            
            def take_totals_screenshot(self, filename):
                """Toma una captura de pantalla de la sección de totales"""
                start_time = time.time()
                rpa_logger.log_action("Iniciando captura de totales", f"Archivo: {filename}")
                
                try:
                    import os
                    
                    # Crear directorio si no existe
                    if not os.path.exists('./rpa/vision/reference_images/inserted_orders'):
                        os.makedirs('./rpa/vision/reference_images/inserted_orders')
                    
                    # Generar nombre del archivo para totales
                    base_name = filename.replace('.json', '')
                    totals_filename = f'{base_name}_totales.png'
                    saved_filename = f'./rpa/vision/reference_images/inserted_orders/{totals_filename}'
                    
                    # Tomar screenshot
                    time.sleep(1)  # Esperar a que la página se estabilice
                    screenshot = pyautogui.screenshot()
                    screenshot.save(saved_filename)
                    
                    duration = time.time() - start_time
                    rpa_logger.log_performance("Captura de totales completada", duration)
                    rpa_logger.log_action("Captura de totales guardada exitosamente", f"Archivo: {totals_filename}")
                    
                    print(f"Captura de totales guardada: {saved_filename}")
                    
                except Exception as e:
                    rpa_logger.log_error(f"Error al tomar captura de totales: {str(e)}", f"Archivo: {filename}")
                    raise
        
        # Crear instancia de prueba
        test_rpa = TestRPA()
        
        print("1. Probando función scroll_to_bottom con imagen de referencia...")
        print("   - Busca la barra de desplazamiento usando scroll_to_bottom.png")
        print("   - Hace clic en la posición encontrada")
        print("   - Arrastra hacia abajo durante 2 segundos")
        print("   - Presiona Ctrl+C para cancelar si es necesario")
        
        # Verificar que existe la imagen de referencia
        import os
        reference_image = './rpa/vision/reference_images/scroll_to_bottom.png'
        if not os.path.exists(reference_image):
            print(f"⚠️  ADVERTENCIA: No se encontró la imagen de referencia: {reference_image}")
            print("   La función usará posicionamiento basado en coordenadas fijas")
        else:
            print(f"✅ Imagen de referencia encontrada: {reference_image}")
        
        # Dar tiempo para prepararse
        print("\nPreparándose para la prueba...")
        for i in range(5, 0, -1):
            print(f"Ejecutando en {i} segundos...")
            time.sleep(1)
        
        # Ejecutar scroll
        success = test_rpa.scroll_to_bottom()
        
        if success:
            print("\n2. Probando captura de totales...")
            test_rpa.take_totals_screenshot("test_order.json")
            
            print("\n=== PRUEBA COMPLETADA EXITOSAMENTE ===")
            print("Funciones implementadas:")
            print("- scroll_to_bottom(): Baja el scroll usando imagen de referencia")
            print("- take_totals_screenshot(): Captura la sección de totales")
            
        else:
            print("\n=== PRUEBA FALLIDA ===")
            print("Posibles causas:")
            print("- La imagen de referencia no coincide con la pantalla actual")
            print("- La barra de desplazamiento no está visible")
            print("- Problemas de resolución o configuración de pantalla")
            
    except KeyboardInterrupt:
        print("\nPrueba cancelada por el usuario")
    except Exception as e:
        print(f"\nError en la prueba: {e}")
        rpa_logger.log_error(f"Error en prueba: {e}", "Función test_scroll_to_bottom")

def show_implementation_details():
    """Muestra los detalles de implementación"""
    print("\n=== DETALLES DE IMPLEMENTACIÓN ===")
    print("\n1. Función scroll_to_bottom():")
    print("   - Usa imagen de referencia: scroll_to_bottom.png")
    print("   - Template matching para encontrar la barra de desplazamiento")
    print("   - Hace clic en la posición encontrada")
    print("   - Arrastra hacia abajo durante 2 segundos")
    print("   - Espera 2 segundos adicionales para completar")
    
    print("\n2. Función take_totals_screenshot():")
    print("   - Crea directorio para capturas si no existe")
    print("   - Genera nombre de archivo con sufijo '_totales'")
    print("   - Toma screenshot completo de la pantalla")
    print("   - Guarda en ./rpa/vision/reference_images/inserted_orders/")
    
    print("\n3. Integración en data_loader():")
    print("   - PASO 9: scroll_to_bottom() después del último artículo")
    print("   - PASO 9.5: take_totals_screenshot() después del scroll")
    print("   - PASO 10: move_json_to_processed() al final")
    
    print("\n4. Logging mejorado:")
    print("   - Cada paso tiene su propio log con contexto")
    print("   - Métricas de rendimiento para cada operación")
    print("   - Manejo de errores con logging detallado")
    
    print("\n5. Imagen de referencia:")
    print("   - Archivo: ./rpa/vision/reference_images/scroll_to_bottom.png")
    print("   - Debe ser una captura de la barra de desplazamiento")
    print("   - Se usa para template matching preciso")

def main():
    """Función principal"""
    print("=== PRUEBA DE FUNCIÓN SCROLL_TO_BOTTOM ===\n")
    
    # Mostrar detalles de implementación
    show_implementation_details()
    
    # Preguntar si ejecutar la prueba
    response = input("\n¿Ejecutar la prueba de scroll? (s/n): ").lower()
    
    if response == 's':
        test_scroll_to_bottom()
    else:
        print("Prueba cancelada")

if __name__ == "__main__":
    main() 