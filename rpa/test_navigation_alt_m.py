"""
Script de prueba para la navegación Alt+M, V en SAP
"""

import time
import pyautogui
from rpa.logger import rpa_logger

def test_alt_m_navigation():
    """Prueba la navegación Alt+M, V"""
    print("=== PRUEBA DE NAVEGACIÓN ALT+M, V ===\n")
    
    try:
        # Simular la clase RPA
        class TestRPA:
            def __init__(self):
                self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"
            
            def test_navigation_methods(self):
                """Prueba diferentes métodos de navegación"""
                
                print("1. Verificando ventana del escritorio remoto...")
                windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
                if not windows:
                    print("❌ No se encontró la ventana del escritorio remoto")
                    return False
                
                window = windows[0]
                print(f"✅ Ventana encontrada: {window.title}")
                
                # Activar ventana si no está activa
                if not window.isActive:
                    print("🔄 Activando ventana...")
                    window.activate()
                    time.sleep(2)
                    print("✅ Ventana activada")
                else:
                    print("✅ Ventana ya está activa")
                
                print("\n2. Probando método 1: pyautogui.hotkey('alt', 'm')")
                try:
                    pyautogui.hotkey('alt', 'm')
                    time.sleep(2)
                    print("✅ Método 1 ejecutado")
                except Exception as e:
                    print(f"❌ Error en método 1: {e}")
                
                print("\n3. Probando método 2: keyDown/keyUp")
                try:
                    pyautogui.keyDown('alt')
                    time.sleep(0.1)
                    pyautogui.press('m')
                    time.sleep(0.1)
                    pyautogui.keyUp('alt')
                    time.sleep(2)
                    print("✅ Método 2 ejecutado")
                except Exception as e:
                    print(f"❌ Error en método 2: {e}")
                
                print("\n4. Probando método 3: typewrite")
                try:
                    pyautogui.typewrite(['alt', 'm'])
                    time.sleep(2)
                    print("✅ Método 3 ejecutado")
                except Exception as e:
                    print(f"❌ Error en método 3: {e}")
                
                print("\n5. Probando tecla 'V'")
                try:
                    pyautogui.press('v')
                    time.sleep(2)
                    print("✅ Tecla 'V' ejecutada")
                except Exception as e:
                    print(f"❌ Error con tecla 'V': {e}")
                
                return True
        
        # Crear instancia de prueba
        test_rpa = TestRPA()
        
        print("Preparándose para la prueba...")
        print("Asegúrate de que:")
        print("- La ventana del escritorio remoto esté abierta")
        print("- SAP Business One esté visible")
        print("- No haya otras ventanas interfiriendo")
        
        # Dar tiempo para prepararse
        print("\nPreparándose para la prueba...")
        for i in range(5, 0, -1):
            print(f"Ejecutando en {i} segundos...")
            time.sleep(1)
        
        # Ejecutar pruebas
        result = test_rpa.test_navigation_methods()
        
        if result:
            print("\n=== PRUEBA COMPLETADA ===")
            print("Revisa los logs para ver qué método funcionó mejor")
        else:
            print("\n=== PRUEBA FALLIDA ===")
            
    except KeyboardInterrupt:
        print("\nPrueba cancelada por el usuario")
    except Exception as e:
        print(f"\nError en la prueba: {e}")
        rpa_logger.log_error(f"Error en prueba: {e}", "Función test_alt_m_navigation")

def show_navigation_details():
    """Muestra los detalles de navegación"""
    print("\n=== DETALLES DE NAVEGACIÓN ALT+M, V ===")
    print("\n1. Problema identificado:")
    print("   - Los atajos de teclado pueden no funcionar después de maximización")
    print("   - La ventana puede perder el foco")
    print("   - Los comandos pueden ser interceptados por el sistema")
    
    print("\n2. Métodos de solución:")
    print("   - Verificar que la ventana esté activa antes de enviar comandos")
    print("   - Usar keyDown/keyUp en lugar de hotkey")
    print("   - Agregar delays entre comandos")
    print("   - Usar typewrite como alternativa")
    
    print("\n3. Logging mejorado:")
    print("   - Log de activación de ventana")
    print("   - Log de cada método de navegación")
    print("   - Log de errores específicos")
    print("   - Log de confirmación de navegación")

def main():
    """Función principal"""
    print("=== PRUEBA DE NAVEGACIÓN ALT+M, V ===\n")
    
    # Mostrar detalles de navegación
    show_navigation_details()
    
    # Preguntar si ejecutar la prueba
    response = input("\n¿Ejecutar la prueba de navegación? (s/n): ").lower()
    
    if response == 's':
        test_alt_m_navigation()
    else:
        print("Prueba cancelada")

if __name__ == "__main__":
    main() 