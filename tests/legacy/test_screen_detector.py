#!/usr/bin/env python3
"""
Script de prueba para el sistema de detección de pantalla
"""

import sys
import time
from rpa.screen_detector import screen_detector, ScreenState
from rpa.simple_logger import rpa_logger


def test_screen_detection():
    """Prueba el sistema de detección de pantalla"""
    
    print("=" * 60)
    print("🧪 PRUEBA DEL SISTEMA DE DETECCIÓN DE PANTALLA")
    print("=" * 60)
    print()
    
    print("📋 Instrucciones:")
    print("1. Asegúrate de tener una de estas pantallas abierta:")
    print("   - Remote Desktop")
    print("   - SAP Desktop")
    print("   - Formulario de Órdenes de Venta")
    print("2. El sistema detectará automáticamente en qué pantalla estás")
    print()
    
    input("Presiona Enter cuando estés listo para comenzar la detección...")
    
    print("\n🔍 Iniciando detección...")
    print("-" * 40)
    
    # Realizar detección
    try:
        result = screen_detector.detect_current_screen(save_screenshot=True)
        
        print(f"✅ Estado detectado: {result.state.value}")
        print(f"📊 Confianza: {result.confidence:.3f}")
        print(f"📁 Screenshot guardado: {result.screenshot_path}")
        
        # Mostrar detalles de confianza
        if "all_confidences" in result.details:
            print("\n📈 Confianzas por estado:")
            for state, conf in result.details["all_confidences"].items():
                print(f"   {state.value}: {conf:.3f}")
        
        # Interpretar resultado
        print(f"\n🎯 Interpretación:")
        if result.state == ScreenState.UNKNOWN:
            print("   ❌ No se pudo identificar la pantalla actual")
            print("   💡 Asegúrate de tener una de las pantallas esperadas abierta")
        elif result.state == ScreenState.ERROR:
            print("   ❌ Error en la detección")
            print(f"   🔍 Detalles: {result.details.get('error', 'Error desconocido')}")
        else:
            print(f"   ✅ Pantalla identificada correctamente: {result.state.value}")
            
            # Sugerir siguiente paso
            if result.state == ScreenState.REMOTE_DESKTOP:
                print("   📋 Próximo paso: Maximizar y conectar Remote Desktop")
            elif result.state == ScreenState.SAP_DESKTOP:
                print("   📋 Próximo paso: Navegar al formulario de órdenes")
            elif result.state == ScreenState.SALES_ORDER_FORM:
                print("   📋 Próximo paso: Comenzar a procesar datos")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante la detección: {e}")
        return None


def test_verification():
    """Prueba la verificación de estado"""
    
    print("\n" + "=" * 60)
    print("🔍 PRUEBA DE VERIFICACIÓN DE ESTADO")
    print("=" * 60)
    
    # Primero detectar estado actual
    result = screen_detector.detect_current_screen()
    
    if result.state == ScreenState.UNKNOWN or result.state == ScreenState.ERROR:
        print("❌ No se puede verificar un estado desconocido o con error")
        return
    
    print(f"📋 Verificando estado: {result.state.value}")
    print("⏳ Esperando 3 segundos antes de verificar...")
    time.sleep(3)
    
    # Verificar estado
    is_verified = screen_detector.verify_screen_state(result.state, max_attempts=2)
    
    if is_verified:
        print("✅ Estado verificado correctamente")
    else:
        print("❌ No se pudo verificar el estado")


def interactive_test():
    """Prueba interactiva del detector"""
    
    print("\n" + "=" * 60)
    print("🔄 PRUEBA INTERACTIVA")
    print("=" * 60)
    
    while True:
        print("\nOpciones:")
        print("1. Detectar pantalla actual")
        print("2. Verificar estado actual")
        print("3. Detección con screenshot")
        print("4. Salir")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == "1":
            result = screen_detector.detect_current_screen()
            print(f"Estado: {result.state.value}, Confianza: {result.confidence:.3f}")
            
        elif choice == "2":
            result = screen_detector.detect_current_screen()
            if result.state not in [ScreenState.UNKNOWN, ScreenState.ERROR]:
                is_verified = screen_detector.verify_screen_state(result.state)
                print(f"Verificación: {'✅' if is_verified else '❌'}")
            else:
                print("No se puede verificar un estado desconocido")
                
        elif choice == "3":
            result = screen_detector.detect_current_screen(save_screenshot=True)
            print(f"Estado: {result.state.value}, Screenshot: {result.screenshot_path}")
            
        elif choice == "4":
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción inválida")


def main():
    """Función principal"""
    
    print("🎯 SISTEMA DE DETECCIÓN DE PANTALLA - RPA TAMAPRINT")
    print("Versión: Fase 1 - Detección básica")
    print()
    
    try:
        # Prueba básica
        result = test_screen_detection()
        
        if result and result.state not in [ScreenState.UNKNOWN, ScreenState.ERROR]:
            # Prueba de verificación
            test_verification()
            
            # Prueba interactiva
            interactive_test()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
