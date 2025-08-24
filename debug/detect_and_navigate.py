#!/usr/bin/env python3
"""
Script Simple de Detección y Navegación - RPA TAMAPRINT
Detecta automáticamente el estado y navega al objetivo
"""

import time
from rpa.navigation_planner import navigation_planner
from rpa.screen_detector import ScreenState, screen_detector
from rpa.simple_logger import rpa_logger


def main():
    """Script principal con delays automáticos"""
    
    print("🎯 DETECCIÓN Y NAVEGACIÓN AUTOMÁTICA")
    print("=" * 50)
    print()
    
    # Delay inicial de 5 segundos
    print("⏳ Iniciando en 5 segundos...")
    print("💡 Prepárate para la detección automática")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔍 Detectando estado actual...")
    
    try:
        # Detectar estado actual
        result = screen_detector.detect_current_screen(save_screenshot=True)
        
        print(f"✅ Estado detectado: {result.state.value}")
        print(f"📊 Confianza: {result.confidence:.3f}")
        
        # Determinar objetivo
        if result.state == ScreenState.SALES_ORDER_FORM:
            print("🎉 ¡Ya estamos en el formulario de órdenes!")
            print("✅ Listo para procesar datos")
            return True
        elif result.state == ScreenState.SAP_DESKTOP:
            print("📋 Navegando al formulario de órdenes...")
            target = ScreenState.SALES_ORDER_FORM
        elif result.state == ScreenState.REMOTE_DESKTOP:
            print("📋 Navegando a SAP...")
            target = ScreenState.SAP_DESKTOP
        else:
            print("📋 Navegando a Remote Desktop...")
            target = ScreenState.REMOTE_DESKTOP
        
        # Delay antes de navegar
        print("⏳ Esperando 3 segundos antes de navegar...")
        time.sleep(3)
        
        # Navegar al objetivo
        success = navigation_planner.navigate_to_target_state(target)
        
        if success:
            print(f"✅ Navegación exitosa a {target.value}")
            
            # Si llegamos a SAP, continuar a órdenes
            if target == ScreenState.SAP_DESKTOP:
                print("📋 Continuando al formulario de órdenes...")
                time.sleep(3)
                
                success = navigation_planner.navigate_to_target_state(ScreenState.SALES_ORDER_FORM)
                if success:
                    print("🎉 ¡Llegamos al formulario de órdenes!")
                    print("✅ Listo para procesar datos")
                    return True
                else:
                    print("❌ No se pudo llegar al formulario de órdenes")
                    return False
            else:
                return True
        else:
            print(f"❌ No se pudo navegar a {target.value}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 SISTEMA DE DETECCIÓN Y NAVEGACIÓN")
    print("Versión: Automática con delays")
    print()
    
    success = main()
    
    if success:
        print("\n🎉 ¡OPERACIÓN EXITOSA!")
    else:
        print("\n❌ OPERACIÓN FALLIDA")
    
    print("\n👋 ¡Hasta luego!")
