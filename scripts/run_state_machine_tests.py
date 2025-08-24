#!/usr/bin/env python3
"""
Script para ejecutar los tests de la máquina de estados del RPA.
"""

import sys
import os
import unittest
from unittest.mock import patch

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Patch para evitar problemas con los imports de RPA específicos durante testing
def mock_imports():
    """Mock de imports que podrían causar problemas durante testing"""
    mocks = [
        'pyautogui',
        'rpa.vision.main',
        'rpa.smart_waits',
        'rpa.config_manager',
        'rpa.error_handler',
    ]
    
    for module in mocks:
        if module not in sys.modules:
            sys.modules[module] = unittest.mock.MagicMock()

def run_tests():
    """Ejecuta todos los tests de la máquina de estados"""
    print("=" * 60)
    print("EJECUTANDO TESTS DE LA MÁQUINA DE ESTADOS RPA")
    print("=" * 60)
    
    # Mock imports problemáticos
    mock_imports()
    
    # Cargar tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    try:
        # Agregar tests de máquina de estados
        from tests.test_state_machine import (
            TestStateMachine, 
            TestRPAStateHandlers, 
            TestStateIntegration
        )
        
        suite.addTests(loader.loadTestsFromTestCase(TestStateMachine))
        suite.addTests(loader.loadTestsFromTestCase(TestRPAStateHandlers))
        suite.addTests(loader.loadTestsFromTestCase(TestStateIntegration))
        
        print(f"Tests cargados: {suite.countTestCases()}")
        
    except ImportError as e:
        print(f"Error importando tests: {e}")
        return False
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    print("\nIniciando ejecución de tests...\n")
    result = runner.run(suite)
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("RESUMEN DE EJECUCIÓN")
    print("=" * 60)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Omitidos: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.errors:
        print(f"\nERRORES ({len(result.errors)}):")
        for test, error in result.errors:
            print(f"- {test}: {error.split('\\n')[0]}")
    
    if result.failures:
        print(f"\nFALLOS ({len(result.failures)}):")
        for test, failure in result.failures:
            print(f"- {test}: {failure.split('\\n')[0]}")
    
    success = len(result.errors) == 0 and len(result.failures) == 0
    
    if success:
        print("\n✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
    
    print("=" * 60)
    
    return success

def run_specific_test(test_class_name=None, test_method_name=None):
    """Ejecuta un test específico"""
    mock_imports()
    
    if test_class_name:
        if test_method_name:
            # Ejecutar método específico
            suite = unittest.TestLoader().loadTestsFromName(
                f'tests.test_state_machine.{test_class_name}.{test_method_name}'
            )
        else:
            # Ejecutar clase específica
            from tests import test_state_machine
            test_class = getattr(test_state_machine, test_class_name)
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return len(result.errors) == 0 and len(result.failures) == 0
    else:
        print("Uso: run_specific_test('TestStateMachine', 'test_initial_state')")
        return False

def validate_state_machine():
    """Validaciones básicas de la estructura de la máquina de estados"""
    print("=" * 60)
    print("VALIDACIÓN DE ESTRUCTURA DE MÁQUINA DE ESTADOS")
    print("=" * 60)
    
    try:
        from rpa.state_machine import StateMachine, RPAState, RPAEvent
        
        # Crear instancia
        sm = StateMachine()
        
        print("✅ Máquina de estados creada exitosamente")
        
        # Verificar estados
        states_count = len(RPAState)
        events_count = len(RPAEvent)
        transitions_count = len(sm.transitions)
        
        print(f"✅ Estados definidos: {states_count}")
        print(f"✅ Eventos definidos: {events_count}")
        print(f"✅ Transiciones definidas: {transitions_count}")
        
        # Verificar que todos los estados tengan transiciones definidas
        missing_transitions = []
        for state in RPAState:
            if state not in sm.transitions:
                missing_transitions.append(state)
        
        if missing_transitions:
            print(f"⚠️  Estados sin transiciones: {missing_transitions}")
        else:
            print("✅ Todos los estados tienen transiciones definidas")
        
        # Verificar estado inicial
        initial_state = sm.get_current_state()
        print(f"✅ Estado inicial: {initial_state.value}")
        
        # Verificar contexto inicial
        context = sm.get_context()
        print(f"✅ Contexto inicializado: {context is not None}")
        
        print("=" * 60)
        print("✅ VALIDACIÓN COMPLETADA EXITOSAMENTE")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Ejecutar tests de la máquina de estados RPA'
    )
    parser.add_argument(
        '--validate', 
        action='store_true',
        help='Solo ejecutar validaciones de estructura'
    )
    parser.add_argument(
        '--test-class',
        help='Ejecutar solo una clase de test específica'
    )
    parser.add_argument(
        '--test-method',
        help='Ejecutar solo un método de test específico (requiere --test-class)'
    )
    
    args = parser.parse_args()
    
    if args.validate:
        success = validate_state_machine()
    elif args.test_class:
        success = run_specific_test(args.test_class, args.test_method)
    else:
        # Ejecutar validación primero
        print("Ejecutando validación de estructura...\n")
        validation_success = validate_state_machine()
        
        if not validation_success:
            print("❌ Validación falló, no se ejecutarán los tests")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("VALIDACIÓN EXITOSA - PROCEDIENDO CON TESTS")
        print("=" * 60 + "\n")
        
        # Ejecutar tests
        success = run_tests()
    
    sys.exit(0 if success else 1)