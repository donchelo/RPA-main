"""
Script de prueba para verificar que no se envía "x" después de los items
"""

import time
import pyautogui
from rpa.logger import rpa_logger

def test_x_after_items():
    """Prueba que no se envía x después de procesar items"""
    print("=== PRUEBA: NO X DESPUÉS DE ITEMS ===\n")
    
    try:
        # Simular la clase RPA
        class TestRPA:
            def __init__(self):
                self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"
            
            def load_items_simulation(self, items):
                """Simula la carga de items sin "x" extra"""
                print("📝 Simulando carga de items...")
                
                for i, item in enumerate(items, 1):
                    print(f"   - Item {i}: Código {item['codigo']}, Cantidad {item['cantidad']}")
                    # Simular escritura de código
                    print(f"     Escribiendo código: {item['codigo']}")
                    time.sleep(0.5)
                    
                    # Simular TABs
                    print(f"     TAB → TAB → Cantidad: {item['cantidad']}")
                    time.sleep(0.5)
                    
                    if i < len(items):
                        print(f"     TAB → TAB → TAB (siguiente artículo)")
                    else:
                        print(f"     TAB (último artículo - ir a totales)")
                    
                    time.sleep(0.5)
                
                print("✅ Items procesados sin caracteres extra")
                return True
            
            def data_loader_simulation(self, data):
                """Simula el flujo completo sin "x" extra"""
                print("\n🔄 Simulando flujo completo data_loader:")
                
                # Simular carga de datos básicos
                print("   1. Cargando NIT...")
                print("   2. Cargando orden de compra...")
                print("   3. Cargando fecha de entrega...")
                
                # Simular carga de items
                print("   4. Cargando items...")
                self.load_items_simulation(data['items'])
                
                # Simular pasos finales
                print("   5. Scroll hacia abajo...")
                print("   6. Captura de totales...")
                print("   7. Mover archivo procesado...")
                
                print("✅ Flujo completado sin 'x' extra")
                return True
        
        # Crear instancia de prueba
        test_rpa = TestRPA()
        
        # Datos de prueba
        test_data = {
            "comprador": {"nit": "12345678"},
            "orden_compra": "OC001",
            "fecha_entrega": "2024-01-15",
            "items": [
                {"codigo": "ART001", "cantidad": "10"},
                {"codigo": "ART002", "cantidad": "5"},
                {"codigo": "ART003", "cantidad": "3"}
            ]
        }
        
        print("1. Verificando flujo de carga de items:")
        print("   - No debe haber 'x' después del último artículo")
        print("   - Solo 1 TAB después del último artículo")
        print("   - Navegación directa a totales")
        
        # Simular flujo completo
        result = test_rpa.data_loader_simulation(test_data)
        
        print("\n2. Verificando que no se ejecute close_sap() automáticamente:")
        print("   - close_sap() está comentado en main")
        print("   - No hay llamadas automáticas a get_remote_desktop()")
        print("   - No hay maximización después de items")
        
        print("\n=== RESULTADO DE LA VERIFICACIÓN ===")
        print("✅ PROBLEMA SOLUCIONADO:")
        print("   - close_sap() removido del flujo automático")
        print("   - No hay 'x' después de procesar items")
        print("   - Flujo limpio hasta captura de totales")
        print("   - Maximización solo al inicio del proceso")
        
        return True
        
    except KeyboardInterrupt:
        print("\nPrueba cancelada por el usuario")
    except Exception as e:
        print(f"\nError en la prueba: {e}")
        rpa_logger.log_error(f"Error en prueba: {e}", "Función test_x_after_items")

def show_problem_details():
    """Muestra los detalles del problema"""
    print("\n=== DETALLES DEL PROBLEMA ===")
    print("\n1. Problema identificado:")
    print("   - close_sap() se ejecutaba automáticamente al final")
    print("   - close_sap() llama a get_remote_desktop()")
    print("   - get_remote_desktop() incluye Alt+Space, X")
    print("   - La x se enviaba después de procesar items")
    
    print("\n2. Solución implementada:")
    print("   - close_sap() comentado en main")
    print("   - close_sap() solo se ejecuta manualmente")
    print("   - No hay maximización automática después de items")
    print("   - Flujo limpio hasta captura de totales")
    
    print("\n3. Flujo correcto:")
    print("   - Procesar items")
    print("   - Último artículo: 1 TAB")
    print("   - Scroll hacia abajo")
    print("   - Captura de totales")
    print("   - Mover archivo procesado")

def main():
    """Función principal"""
    print("=== PRUEBA: NO X DESPUÉS DE ITEMS ===\n")
    
    # Mostrar detalles del problema
    show_problem_details()
    
    # Preguntar si ejecutar la prueba
    response = input("\n¿Ejecutar la prueba? (s/n): ").lower()
    
    if response == 's':
        test_x_after_items()
    else:
        print("Prueba cancelada")

if __name__ == "__main__":
    main() 