"""
Test Runner Principal - FASE 1
Ejecuta todos los tests de la Fase 1 y genera reporte
"""

import unittest
import sys
import os
import time
from io import StringIO

# Agregar directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar test de config manager
from tests.test_config_manager import TestConfigManager, TestConfigManagerErrorHandling


def create_test_suite_fase1():
    """Crea suite de tests para Fase 1 - Solo ConfigManager por ahora"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tests de ConfigManager - lo más básico y crítico
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManagerErrorHandling))
    
    return suite


def run_tests_fase1():
    """Ejecuta tests Fase 1 y genera reporte detallado"""
    print("🧪 EJECUTANDO TESTS - FASE 1 (Testing Básico)")
    print("🎯 Enfoque: ConfigManager (Fácil + Alto impacto)")
    print("=" * 60)
    
    # Capturar output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        buffer=True
    )
    
    # Ejecutar tests
    start_time = time.time()
    suite = create_test_suite_fase1()
    result = runner.run(suite)
    end_time = time.time()
    
    # Mostrar resultados
    output = stream.getvalue()
    print(output)
    
    # Reporte de resumen
    print("\n" + "=" * 60)
    print("📊 REPORTE DE TESTING - FASE 1")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success = total_tests - failures - errors
    
    print(f"🧪 Tests ejecutados: {total_tests}")
    print(f"✅ Exitosos: {success}")
    print(f"❌ Fallos: {failures}")
    print(f"🔥 Errores: {errors}")
    print(f"⏱️  Tiempo total: {end_time - start_time:.2f}s")
    
    # Porcentaje de éxito
    if total_tests > 0:
        success_rate = (success / total_tests) * 100
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")
    
    # Mostrar fallos detallados
    if failures:
        print("\n❌ FALLOS DETALLADOS:")
        for test, traceback in result.failures:
            print(f"  - {test}")
            print(f"    Error: {traceback.split('AssertionError: ')[-1].split(chr(10))[0]}")
    
    # Mostrar errores detallados
    if errors:
        print("\n🔥 ERRORES DETALLADOS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
            error_lines = traceback.split('\n')
            for line in error_lines:
                if 'Error:' in line or 'Exception:' in line:
                    print(f"    {line.strip()}")
                    break
    
    # Estado final y siguiente paso
    print("\n" + "=" * 60)
    if failures == 0 and errors == 0:
        print("🎉 ¡TODOS LOS TESTS DE FASE 1 PASARON!")
        print("✅ ConfigManager validado y funcional") 
        print("🚀 LISTO PARA FASE 2: Testing de Componentes")
        print("\n📋 Próximos pasos:")
        print("   1. Tests de validación de datos JSON")
        print("   2. Tests de utilidades de archivos")
        print("   3. Tests de sistema de logging")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - REVISAR Y CORREGIR")
        print("🔧 Corregir errores antes de avanzar a Fase 2")
        print("💡 Sugerencias:")
        print("   - Verificar imports y paths")
        print("   - Revisar configuración de test environment")
        print("   - Validar mocks y fixtures")
    
    return result


if __name__ == '__main__':
    # Ejecutar tests de Fase 1
    result = run_tests_fase1()
    
    # Exit code para CI/CD
    if result.failures or result.errors:
        sys.exit(1)
    else:
        sys.exit(0)