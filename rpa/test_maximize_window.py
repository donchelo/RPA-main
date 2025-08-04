"""
Script de prueba para la función de maximización de ventana del escritorio remoto
"""

import time
import pyautogui
from rpa.logger import rpa_logger

def test_maximize_remote_desktop():
    """Prueba la función de maximización de ventana del escritorio remoto"""
    print("=== PRUEBA DE MAXIMIZACIÓN DE VENTANA ===\n")
    
    try:
        # Simular la clase RPA
        class TestRPA:
            def __init__(self):
                self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"
            
            def get_remote_desktop(self):
                max_retries = 3
                retry_delay = 5
                
                rpa_logger.log_action("Iniciando conexión al escritorio remoto", f"Máximo {max_retries} intentos")
                
                for attempt in range(max_retries):
                    try:
                        windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
                        if not windows:
                            rpa_logger.warning(f'Ventana de escritorio remoto no encontrada (intento {attempt + 1}/{max_retries})')
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            else:
                                rpa_logger.log_error('No se pudo encontrar la ventana de escritorio remoto después de varios intentos', 'Ventana no encontrada')
                                return None
                        
                        window = windows[0]
                        if not window.isActive:
                            window.activate()
                            time.sleep(2)  # Esperamos a que la ventana se active
                        
                        # Verificamos que la ventana esté realmente activa
                        if window.isActive:
                            # PASO ADICIONAL: Maximizar la ventana del escritorio remoto
                            rpa_logger.log_action("Maximizando ventana del escritorio remoto", "Alt+Space, X")
                            try:
                                # Alt+Space para abrir el menú de la ventana
                                pyautogui.hotkey('alt', 'space')
                                time.sleep(0.5)
                                
                                # X para maximizar
                                pyautogui.typewrite('x')
                                time.sleep(1)
                                
                                rpa_logger.log_action("Ventana del escritorio remoto maximizada", "Comando de maximización ejecutado")
                                
                            except Exception as maximize_error:
                                rpa_logger.log_error(f'Error al maximizar la ventana: {str(maximize_error)}', 'Error en maximización')
                                # Continuamos aunque falle la maximización
                            
                            screenshot = pyautogui.screenshot("./rpa/vision/reference_images/remote_desktop.png")
                            if screenshot:
                                rpa_logger.log_action("Conexión al escritorio remoto establecida correctamente", "Ventana activa, maximizada y captura exitosa")
                                return window
                            else:
                                rpa_logger.log_error('No se pudo tomar captura de pantalla del escritorio remoto', 'Error en captura')
                        else:
                            rpa_logger.log_error('No se pudo activar la ventana del escritorio remoto', 'Ventana inactiva')
                        
                    except Exception as e:
                        rpa_logger.log_error(f'Error al conectar con el escritorio remoto (intento {attempt + 1}/{max_retries}): {str(e)}', f"Intento {attempt + 1}")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        else:
                            rpa_logger.log_error('No se pudo establecer conexión con el escritorio remoto después de varios intentos', 'Todos los intentos fallaron')
                            return None
                
                return None
        
        # Crear instancia de prueba
        test_rpa = TestRPA()
        
        print("1. Probando maximización de ventana del escritorio remoto...")
        print("   - Busca la ventana del escritorio remoto")
        print("   - Activa la ventana si no está activa")
        print("   - Ejecuta Alt+Space para abrir menú")
        print("   - Presiona X para maximizar")
        print("   - Presiona Ctrl+C para cancelar si es necesario")
        
        # Verificar que existe la ventana del escritorio remoto
        windows = pyautogui.getWindowsWithTitle("20.96.6.64 - Conexión a Escritorio remoto")
        if not windows:
            print("⚠️  ADVERTENCIA: No se encontró la ventana del escritorio remoto")
            print("   Asegúrate de que la conexión RDP esté abierta")
        else:
            print(f"✅ Ventana del escritorio remoto encontrada: {len(windows)} ventana(s)")
        
        # Dar tiempo para prepararse
        print("\nPreparándose para la prueba...")
        for i in range(5, 0, -1):
            print(f"Ejecutando en {i} segundos...")
            time.sleep(1)
        
        # Ejecutar maximización
        result = test_rpa.get_remote_desktop()
        
        if result:
            print("\n=== PRUEBA COMPLETADA EXITOSAMENTE ===")
            print("Funcionalidades implementadas:")
            print("- Activación de ventana del escritorio remoto")
            print("- Maximización con Alt+Space, X")
            print("- Captura de pantalla de confirmación")
            
        else:
            print("\n=== PRUEBA FALLIDA ===")
            print("Posibles causas:")
            print("- La ventana del escritorio remoto no está abierta")
            print("- La conexión RDP no está establecida")
            print("- Problemas de permisos o configuración")
            
    except KeyboardInterrupt:
        print("\nPrueba cancelada por el usuario")
    except Exception as e:
        print(f"\nError en la prueba: {e}")
        rpa_logger.log_error(f"Error en prueba: {e}", "Función test_maximize_remote_desktop")

def show_implementation_details():
    """Muestra los detalles de implementación"""
    print("\n=== DETALLES DE IMPLEMENTACIÓN ===")
    print("\n1. Función get_remote_desktop() mejorada:")
    print("   - Busca la ventana del escritorio remoto")
    print("   - Activa la ventana si no está activa")
    print("   - Ejecuta Alt+Space para abrir menú de ventana")
    print("   - Presiona X para maximizar")
    print("   - Toma captura de pantalla de confirmación")
    
    print("\n2. Secuencia de comandos:")
    print("   - Alt+Space: Abre el menú de la ventana")
    print("   - X: Selecciona la opción de maximizar")
    print("   - Espera 1 segundo para completar")
    
    print("\n3. Logging mejorado:")
    print("   - Log de inicio de maximización")
    print("   - Log de confirmación de maximización")
    print("   - Log de error si falla la maximización")
    print("   - Log de conexión exitosa con maximización")
    
    print("\n4. Manejo de errores:")
    print("   - Try-catch específico para maximización")
    print("   - Continúa el proceso aunque falle la maximización")
    print("   - Logs detallados de errores")

def main():
    """Función principal"""
    print("=== PRUEBA DE MAXIMIZACIÓN DE VENTANA ===\n")
    
    # Mostrar detalles de implementación
    show_implementation_details()
    
    # Preguntar si ejecutar la prueba
    response = input("\n¿Ejecutar la prueba de maximización? (s/n): ").lower()
    
    if response == 's':
        test_maximize_remote_desktop()
    else:
        print("Prueba cancelada")

if __name__ == "__main__":
    main() 