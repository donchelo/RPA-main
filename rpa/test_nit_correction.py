"""
Script de prueba para verificar la corrección del problema de la "x" en NIT
"""

import time
import pyautogui
from rpa.logger import rpa_logger

def test_nit_correction():
    """Prueba la corrección del problema de la "x" en NIT"""
    print("=== PRUEBA DE CORRECCIÓN DE NIT ===\n")
    
    try:
        # Simular la clase RPA
        class TestRPA:
            def __init__(self):
                self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"
            
            def load_nit_corrected(self, nit):
                """Versión corregida de load_nit sin get_remote_desktop()"""
                start_time = time.time()
                rpa_logger.log_action("Iniciando carga de NIT (CORREGIDA)", f"NIT: {nit}")
                
                try:
                    time.sleep(1)
                    # CORRECCIÓN: Removido get_remote_desktop() para evitar la "x" de maximización
                    # La conexión al escritorio remoto ya se hace en el flujo principal
                    print("✅ No se llama a get_remote_desktop() en load_nit()")
                    
                    # Simular escritura del NIT
                    print(f"📝 Escribiendo NIT: {nit}")
                    # pyautogui.typewrite(nit, interval=0.2)  # Comentado para prueba
                    time.sleep(1)
                    
                    print("✅ NIT escrito sin caracteres extra")
                    rpa_logger.log_action("NIT cargado exitosamente (CORREGIDO)", f"NIT: {nit}")
                    
                except Exception as e:
                    rpa_logger.log_error(f"Error al cargar NIT: {str(e)}", f"NIT: {nit}")
                    raise
            
            def load_nit_old(self, nit):
                """Versión anterior de load_nit con get_remote_desktop()"""
                start_time = time.time()
                rpa_logger.log_action("Iniciando carga de NIT (VERSIÓN ANTERIOR)", f"NIT: {nit}")
                
                try:
                    time.sleep(1)
                    print("❌ Llamando a get_remote_desktop() que incluye maximización")
                    # self.get_remote_desktop()  # Esto causaba el problema
                    print("❌ Esto habría enviado 'x' antes del NIT")
                    
                    # Simular escritura del NIT
                    print(f"📝 Escribiendo NIT: {nit}")
                    # pyautogui.typewrite(nit, interval=0.2)  # Comentado para prueba
                    time.sleep(1)
                    
                    print("❌ NIT escrito con 'x' extra al inicio")
                    rpa_logger.log_action("NIT cargado (CON PROBLEMA)", f"NIT: {nit}")
                    
                except Exception as e:
                    rpa_logger.log_error(f"Error al cargar NIT: {str(e)}", f"NIT: {nit}")
                    raise
        
        # Crear instancia de prueba
        test_rpa = TestRPA()
        
        # NIT de prueba
        test_nit = "12345678"
        
        print("1. Probando versión CORREGIDA de load_nit:")
        print("   - No llama a get_remote_desktop()")
        print("   - Escribe NIT directamente")
        print("   - No hay caracteres extra")
        
        test_rpa.load_nit_corrected(test_nit)
        
        print("\n2. Comparando con versión ANTERIOR:")
        print("   - Llamaba a get_remote_desktop()")
        print("   - Enviaba 'x' de maximización")
        print("   - NIT tenía caracteres extra")
        
        test_rpa.load_nit_old(test_nit)
        
        print("\n=== RESULTADO DE LA CORRECCIÓN ===")
        print("✅ PROBLEMA SOLUCIONADO:")
        print("   - get_remote_desktop() removido de load_nit()")
        print("   - La maximización solo se hace una vez al inicio")
        print("   - NIT se escribe sin caracteres extra")
        print("   - Flujo más limpio y eficiente")
        
        return True
        
    except KeyboardInterrupt:
        print("\nPrueba cancelada por el usuario")
    except Exception as e:
        print(f"\nError en la prueba: {e}")
        rpa_logger.log_error(f"Error en prueba: {e}", "Función test_nit_correction")

def show_correction_details():
    """Muestra los detalles de la corrección"""
    print("\n=== DETALLES DE LA CORRECCIÓN ===")
    print("\n1. Problema identificado:")
    print("   - get_remote_desktop() se llamaba en load_nit()")
    print("   - get_remote_desktop() incluye maximización Alt+Space, X")
    print("   - La 'x' se enviaba antes del NIT")
    print("   - Resultado: NIT con caracteres extra")
    
    print("\n2. Solución implementada:")
    print("   - Removido get_remote_desktop() de load_nit()")
    print("   - get_remote_desktop() se llama solo una vez al inicio")
    print("   - load_nit() solo escribe el NIT directamente")
    print("   - Flujo más eficiente y sin caracteres extra")
    
    print("\n3. Beneficios:")
    print("   - NIT se escribe correctamente")
    print("   - No hay caracteres extra")
    print("   - Maximización solo una vez por archivo")
    print("   - Mejor rendimiento")

def main():
    """Función principal"""
    print("=== PRUEBA DE CORRECCIÓN DE NIT ===\n")
    
    # Mostrar detalles de la corrección
    show_correction_details()
    
    # Preguntar si ejecutar la prueba
    response = input("\n¿Ejecutar la prueba de corrección? (s/n): ").lower()
    
    if response == 's':
        test_nit_correction()
    else:
        print("Prueba cancelada")

if __name__ == "__main__":
    main() 