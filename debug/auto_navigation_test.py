#!/usr/bin/env python3
"""
Script de Prueba de Navegación Automática - RPA TAMAPRINT
Con delays automáticos para preparación de pantallas
"""

import time
import sys
from rpa.navigation_planner import navigation_planner
from rpa.screen_detector import ScreenState, screen_detector
from rpa.simple_logger import rpa_logger


def main():
    """Función principal con navegación automática"""
    
    print("🚀 SISTEMA DE NAVEGACIÓN AUTOMÁTICA - RPA TAMAPRINT")
    print("=" * 60)
    print()
    print("📋 Este script navegará automáticamente entre pantallas")
    print("⏰ Incluye delays automáticos para preparación")
    print()
    
    # Delay inicial para preparación
    print("⏳ Iniciando en 5 segundos...")
    print("💡 Prepárate para que el sistema detecte automáticamente tu pantalla")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔍 Iniciando detección automática...")
    
    try:
        # 1. Detectar estado actual
        print("\n1️⃣ DETECTANDO ESTADO ACTUAL")
        print("-" * 40)
        
        detection_result = screen_detector.detect_current_screen(save_screenshot=True)
        print(f"✅ Estado detectado: {detection_result.state.value}")
        print(f"📊 Confianza: {detection_result.confidence:.3f}")
        
        if detection_result.state == ScreenState.ERROR:
            print("❌ Error en detección, abortando...")
            return False
        
        # 2. Navegar a Remote Desktop si no estamos ahí
        if detection_result.state != ScreenState.REMOTE_DESKTOP:
            print(f"\n2️⃣ NAVEGANDO A REMOTE DESKTOP")
            print("-" * 40)
            print("⏳ Esperando 3 segundos antes de navegar...")
            time.sleep(3)
            
            if navigation_planner.navigate_to_target_state(ScreenState.REMOTE_DESKTOP):
                print("✅ Llegamos a Remote Desktop")
            else:
                print("❌ No se pudo llegar a Remote Desktop")
                return False
        else:
            print("✅ Ya estamos en Remote Desktop")
        
        # 3. Navegar a SAP Desktop
        print(f"\n3️⃣ NAVEGANDO A SAP DESKTOP")
        print("-" * 40)
        print("⏳ Esperando 3 segundos antes de navegar...")
        time.sleep(3)
        
        if navigation_planner.navigate_to_target_state(ScreenState.SAP_DESKTOP):
            print("✅ Llegamos a SAP Desktop")
        else:
            print("❌ No se pudo llegar a SAP Desktop")
            return False
        
        # 4. Navegar a Formulario de Órdenes
        print(f"\n4️⃣ NAVEGANDO A FORMULARIO DE ÓRDENES")
        print("-" * 40)
        print("⏳ Esperando 3 segundos antes de navegar...")
        time.sleep(3)
        
        if navigation_planner.navigate_to_target_state(ScreenState.SALES_ORDER_FORM):
            print("✅ Llegamos al Formulario de Órdenes")
        else:
            print("❌ No se pudo llegar al Formulario de Órdenes")
            return False
        
        # 5. Verificación final
        print(f"\n5️⃣ VERIFICACIÓN FINAL")
        print("-" * 40)
        
        final_detection = screen_detector.detect_current_screen(save_screenshot=True)
        print(f"Estado final: {final_detection.state.value}")
        print(f"Confianza final: {final_detection.confidence:.3f}")
        
        if final_detection.state == ScreenState.SALES_ORDER_FORM:
            print("🎉 ¡NAVEGACIÓN COMPLETADA EXITOSAMENTE!")
            print("✅ El sistema está listo para procesar órdenes")
            return True
        else:
            print("⚠️ Navegación completada pero estado final no confirmado")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Navegación interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error durante la navegación: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_specific_navigation():
    """Prueba navegación a un estado específico"""
    
    print("🎯 PRUEBA DE NAVEGACIÓN ESPECÍFICA")
    print("=" * 60)
    print()
    print("Opciones:")
    print("1. Remote Desktop")
    print("2. SAP Desktop") 
    print("3. Formulario de Órdenes")
    print()
    
    try:
        choice = input("Selecciona destino (1-3): ").strip()
        
        target_state = None
        if choice == "1":
            target_state = ScreenState.REMOTE_DESKTOP
        elif choice == "2":
            target_state = ScreenState.SAP_DESKTOP
        elif choice == "3":
            target_state = ScreenState.SALES_ORDER_FORM
        else:
            print("❌ Opción inválida")
            return False
        
        print(f"\n🎯 Navegando a: {target_state.value}")
        print("⏳ Esperando 5 segundos para preparación...")
        time.sleep(5)
        
        success = navigation_planner.navigate_to_target_state(target_state)
        
        if success:
            print(f"✅ Navegación exitosa a {target_state.value}")
        else:
            print(f"❌ Fallo en navegación a {target_state.value}")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️ Prueba interrumpida")
        return False


if __name__ == "__main__":
    print("🎯 SISTEMA DE NAVEGACIÓN AUTOMÁTICA")
    print("Versión: Fase 2 - Navegación inteligente")
    print()
    
    # Preguntar tipo de prueba
    print("Tipos de prueba:")
    print("1. Navegación completa (Remote Desktop → SAP → Órdenes)")
    print("2. Navegación específica")
    print()
    
    try:
        test_type = input("Selecciona tipo de prueba (1-2): ").strip()
        
        if test_type == "1":
            success = main()
        elif test_type == "2":
            success = test_specific_navigation()
        else:
            print("❌ Opción inválida")
            success = False
        
        if success:
            print("\n🎉 ¡PRUEBA EXITOSA!")
        else:
            print("\n❌ PRUEBA FALLIDA")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n👋 ¡Hasta luego!")
