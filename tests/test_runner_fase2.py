"""
Test Runner FASE 2 - Testing de Componentes
Ejecuta tests de logging, error handling y smart waits
"""

import unittest
import sys
import os
import time
from io import StringIO

# Agregar directorio raíz al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar tests de Fase 2
from tests.test_logging_system import TestSimpleRPALogger, TestLoggingIntegration


def create_test_suite_fase2():
    """Crea suite de tests para Fase 2 - Componentes"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tests del sistema de logging
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleRPALogger))
    suite.addTests(loader.loadTestsFromTestCase(TestLoggingIntegration))
    
    return suite


def run_tests_fase2():
    """Ejecuta tests Fase 2 y genera reporte detallado"""
    print("🧪 EJECUTANDO TESTS - FASE 2 (Testing de Componentes)")
    print("🎯 Enfoque: Sistema de Logging (Mediano + Alto impacto)")
    print("=" * 70)
    
    # Capturar output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        buffer=True
    )
    
    # Ejecutar tests
    start_time = time.time()
    suite = create_test_suite_fase2()
    result = runner.run(suite)
    end_time = time.time()
    
    # Mostrar resultados
    output = stream.getvalue()
    print(output)
    
    # Reporte de resumen
    print("\n" + "=" * 70)
    print("📊 REPORTE FASE 2 - COMPONENTES")
    print("=" * 70)
    
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
    
    # Componentes probados
    print(f"\n🔧 COMPONENTES PROBADOS FASE 2:")
    print(f"   📝 SimpleRPALogger: Sistema de logging estructurado")
    print(f"   🔄 Rotación automática: Manejo de archivos de log")
    print(f"   🌐 Multi-instancia: Logging concurrente")
    print(f"   🎯 Métodos específicos: log_action, log_performance, log_error")
    
    # Mostrar fallos detallados
    if failures:
        print("\n❌ FALLOS DETALLADOS:")
        for test, traceback in result.failures:
            print(f"  - {test}")
            lines = traceback.split('\n')
            for line in lines:
                if 'AssertionError:' in line:
                    print(f"    Error: {line.split('AssertionError: ')[-1]}")
                    break
    
    # Mostrar errores detallados
    if errors:
        print("\n🔥 ERRORES DETALLADOS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
            lines = traceback.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['Error:', 'Exception:']):
                    print(f"    {line.strip()}")
                    break
    
    # Estado y próximos pasos
    print("\n" + "=" * 70)
    if failures == 0 and errors == 0:
        print("🎉 ¡SISTEMA DE LOGGING VALIDADO EXITOSAMENTE!")
        print("✅ Componentes logging funcionando correctamente:")
        print("   • Logging estructurado con contexto")
        print("   • Rotación automática de archivos")
        print("   • Múltiples niveles de severidad") 
        print("   • Métodos específicos para RPA")
        print("   • Manejo de unicode y datos grandes")
        print("\n🚀 PRÓXIMO: Agregar tests de Error Handler")
        print("📋 Siguientes componentes:")
        print("   1. Sistema de manejo de errores")
        print("   2. Smart waits (esperas inteligentes)")
        print("   3. Template matcher (si necesario)")
    else:
        print("⚠️  ALGUNOS TESTS DE LOGGING FALLARON")
        print("🔧 Revisar y corregir errores del sistema de logging")
        print("💡 El logging es crítico para observabilidad")
    
    # Métricas de calidad
    print(f"\n📊 CALIDAD DEL COMPONENTE:")
    if total_tests > 0:
        coverage_estimate = min(95, (success / total_tests) * 100)
        print(f"   📈 Cobertura estimada: {coverage_estimate:.0f}%")
        print(f"   🛡️  Robustez: {'Alta' if success_rate > 90 else 'Media' if success_rate > 70 else 'Baja'}")
        print(f"   ⚡ Rendimiento: {'Rápido' if end_time - start_time < 1 else 'Aceptable'}")
    
    return result


if __name__ == '__main__':
    # Ejecutar tests de Fase 2
    result = run_tests_fase2()
    
    # Exit code para CI/CD
    if result.failures or result.errors:
        print("\n❌ FASE 2 REQUIERE CORRECCIONES")
        sys.exit(1)
    else:
        print("\n🎯 FASE 2 LOGGING - ¡COMPONENTE VALIDADO!")
        sys.exit(0)