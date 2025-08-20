#!/usr/bin/env python3
"""
Script para probar el flujo simplificado sin scrolling
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_state_machine_flow():
    """Prueba el flujo de la máquina de estados simplificado"""
    print("TESTING SIMPLIFIED STATE MACHINE FLOW")
    print("=" * 50)
    
    try:
        from rpa.state_machine import StateMachine, RPAState, RPAEvent
        
        # Test 1: Crear máquina de estados
        print("Test 1: Crear máquina de estados")
        sm = StateMachine()
        print("PASSED: State machine created")
        
        # Test 2: Verificar estado inicial
        print("Test 2: Estado inicial")
        initial_state = sm.get_current_state()
        assert initial_state == RPAState.IDLE, f"Estado inicial incorrecto: {initial_state}"
        print("PASSED: Estado inicial es IDLE")
        
        # Test 3: Verificar flujo simplificado - LOADING_ITEMS -> TAKING_SCREENSHOT
        print("Test 3: Flujo simplificado ITEMS -> SCREENSHOT")
        
        # Simular flujo hasta LOADING_ITEMS
        sm.trigger_event(RPAEvent.START_PROCESSING)
        sm.trigger_event(RPAEvent.REMOTE_DESKTOP_CONNECTED)
        sm.trigger_event(RPAEvent.SAP_OPENED)
        sm.trigger_event(RPAEvent.SALES_ORDER_OPENED)
        sm.trigger_event(RPAEvent.NIT_LOADED)
        sm.trigger_event(RPAEvent.ORDER_LOADED)
        sm.trigger_event(RPAEvent.DATE_LOADED)
        sm.trigger_event(RPAEvent.ITEMS_LOADED)
        
        # Verificar que después de ITEMS_LOADED vamos directo a TAKING_SCREENSHOT
        current_state = sm.get_current_state()
        assert current_state == RPAState.TAKING_SCREENSHOT, f"Estado después de ITEMS_LOADED: {current_state}"
        print("PASSED: LOADING_ITEMS va directo a TAKING_SCREENSHOT")
        
        # Test 4: Verificar que SCROLLING_TO_TOTALS ya no existe
        print("Test 4: SCROLLING_TO_TOTALS eliminado")
        
        # Verificar que el estado SCROLLING_TO_TOTALS ya no existe
        all_states = [state.value for state in RPAState]
        assert "scrolling_to_totals" not in all_states, "SCROLLING_TO_TOTALS aún existe"
        print("PASSED: SCROLLING_TO_TOTALS eliminado correctamente")
        
        # Test 5: Verificar eventos de scroll eliminados
        print("Test 5: Eventos de scroll eliminados")
        all_events = [event.value for event in RPAEvent]
        assert "scrolled_to_totals" not in all_events, "SCROLLED_TO_TOTALS aún existe"
        assert "scroll_failed" not in all_events, "SCROLL_FAILED aún existe"
        print("PASSED: Eventos de scroll eliminados")
        
        print("TODOS LOS TESTS DEL FLUJO PASARON")
        return True
        
    except Exception as e:
        print(f"ERROR EN TEST DE FLUJO: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_handlers():
    """Prueba que los handlers funcionen correctamente"""
    print("\nTESTING STATE HANDLERS")
    print("=" * 40)
    
    try:
        from rpa.rpa_state_handlers import RPAStateHandlers
        from unittest.mock import Mock
        
        # Test 1: Crear handlers con mock RPA
        print("Test 1: Crear handlers")
        mock_rpa = Mock()
        handlers = RPAStateHandlers(mock_rpa)
        print("PASSED: Handlers created")
        
        # Test 2: Verificar que handle_scrolling_to_totals no existe
        print("Test 2: handle_scrolling_to_totals eliminado")
        assert not hasattr(handlers, 'handle_scrolling_to_totals'), "handle_scrolling_to_totals aún existe"
        print("PASSED: handle_scrolling_to_totals eliminado")
        
        # Test 3: Verificar que otros handlers existen
        print("Test 3: Handlers necesarios existen")
        required_handlers = [
            'handle_loading_items',
            'handle_taking_screenshot',
            'handle_moving_json'
        ]
        
        for handler_name in required_handlers:
            assert hasattr(handlers, handler_name), f"{handler_name} no existe"
        
        print("PASSED: Handlers necesarios existen")
        
        print("TODOS LOS TESTS DE HANDLERS PASARON")
        return True
        
    except Exception as e:
        print(f"ERROR EN TEST DE HANDLERS: {e}")
        return False

def main():
    """Función principal"""
    print("PROBANDO FLUJO SIMPLIFICADO SIN SCROLLING")
    print("=" * 60)
    
    results = []
    results.append(("State Machine Flow", test_state_machine_flow()))
    results.append(("State Handlers", test_handlers()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed + failed} tests")
    print(f"Pasaron: {passed}")
    print(f"Fallaron: {failed}")
    
    if failed == 0:
        print("\nFLUJO SIMPLIFICADO FUNCIONA CORRECTAMENTE!")
        print("AHORA: Items -> Espera 2s -> Screenshot -> Guardar -> Completado")
        return True
    else:
        print(f"\n{failed} test(s) fallaron.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)