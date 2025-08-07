#!/usr/bin/env python3
"""
Script simple para probar los arreglos realizados en el RPA
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_logger_fixes():
    """Prueba los arreglos del logger"""
    print("TESTING LOGGER FIXES")
    print("=" * 40)
    
    try:
        from rpa.simple_logger import rpa_logger
        
        # Test 1: Context como string
        print("Test 1: Context como string")
        rpa_logger.log_error("Test error with string context", "archivo_test.json")
        print("PASSED: Context string")
        
        # Test 2: Context como dict
        print("Test 2: Context como dict")
        rpa_logger.log_error("Test error with dict context", {"archivo": "test.json", "linea": 123})
        print("PASSED: Context dict")
        
        # Test 3: Context como None
        print("Test 3: Context como None")
        rpa_logger.log_error("Test error with no context")
        print("PASSED: Context None")
        
        print("TODOS LOS TESTS DEL LOGGER PASARON")
        return True
        
    except Exception as e:
        print(f"ERROR EN TEST DEL LOGGER: {e}")
        return False

def test_vision_import():
    """Prueba que los imports de vision funcionen"""
    print("\nTESTING VISION IMPORTS")
    print("=" * 40)
    
    try:
        # Test 1: Import de Vision class
        print("Test 1: Import de Vision class")
        from rpa.vision.main import Vision
        vision = Vision()
        print("PASSED: Vision class imported")
        
        # Test 2: Función get_scrollbar_coordinates existe
        print("Test 2: get_scrollbar_coordinates existe")
        if hasattr(vision, 'get_scrollbar_coordinates'):
            print("PASSED: get_scrollbar_coordinates existe")
        else:
            print("FAILED: get_scrollbar_coordinates no existe")
            return False
        
        print("TODOS LOS TESTS DE VISION PASARON")
        return True
        
    except Exception as e:
        print(f"ERROR EN TEST DE VISION: {e}")
        return False

def main():
    """Función principal para ejecutar todos los tests"""
    print("EJECUTANDO TESTS DE ARREGLOS RPA")
    print("=" * 50)
    
    results = []
    
    # Ejecutar tests
    results.append(("Logger Fixes", test_logger_fixes()))
    results.append(("Vision Imports", test_vision_import()))
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("RESUMEN DE RESULTADOS")
    print("=" * 50)
    
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
        print("\nTODOS LOS ARREGLOS FUNCIONAN CORRECTAMENTE!")
        return True
    else:
        print(f"\n{failed} test(s) fallaron. Revisar errores arriba.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)