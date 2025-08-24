#!/usr/bin/env python
"""
Script principal para ejecutar todos los tests del Sistema RPA
Incluye tests unitarios, de integración y verificaciones rápidas
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Imprime un header formateado"""
    print("\n" + "=" * 60)
    print(f"TEST: {title}")
    print("=" * 60)

def print_result(name, success, duration=None):
    """Imprime resultado de test"""
    status = "[PASS]" if success else "[FAIL]"
    duration_str = f" ({duration:.2f}s)" if duration else ""
    print(f"{status} - {name}{duration_str}")

def run_component_test(component_name, import_path):
    """Ejecuta test de importación de componente"""
    try:
        start_time = time.time()
        __import__(import_path)
        duration = time.time() - start_time
        print_result(f"Importación {component_name}", True, duration)
        return True
    except Exception as e:
        print_result(f"Importación {component_name}", False)
        print(f"  Error: {str(e)}")
        return False

def run_python_file(filename):
    """Ejecuta un archivo Python y retorna si fue exitoso"""
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=30
        )
        duration = time.time() - start_time
        
        success = result.returncode == 0
        print_result(f"Archivo {filename}", success, duration)
        
        if not success:
            print(f"  Error: {result.stderr}")
        
        return success
    except subprocess.TimeoutExpired:
        print_result(f"Archivo {filename}", False)
        print("  Error: Timeout (>30s)")
        return False
    except Exception as e:
        print_result(f"Archivo {filename}", False)
        print(f"  Error: {str(e)}")
        return False

def check_dependencies():
    """Verifica dependencias críticas"""
    print_header("VERIFICACIÓN DE DEPENDENCIAS")
    
    dependencies = [
        ("PyAutoGUI", "pyautogui"),
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("PIL", "PIL"),
        ("PyYAML", "yaml"),
        ("Schedule", "schedule")
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            print_result(f"Dependencia {name}", True)
        except ImportError:
            print_result(f"Dependencia {name}", False)
            all_ok = False
    
    return all_ok

def check_file_structure():
    """Verifica estructura de archivos"""
    print_header("VERIFICACIÓN DE ESTRUCTURA")
    
    required_files = [
        "config.yaml",
        "requirements.txt", 
        "rpa/main.py",
        "rpa/simple_logger.py",
        "rpa/config_manager.py",
        "rpa/smart_waits.py",
        "rpa/error_handler.py",
        "rpa/vision/main.py",
        "rpa/vision/template_matcher.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        print_result(f"Archivo {file_path}", exists)
        if not exists:
            all_ok = False
    
    return all_ok

def run_component_tests():
    """Ejecuta tests de importación de componentes"""
    print_header("TESTS DE COMPONENTES")
    
    components = [
        ("RPA Main", "rpa.main"),
        ("Config Manager", "rpa.config_manager"),
        ("Simple Logger", "rpa.simple_logger"),
        ("Smart Waits", "rpa.smart_waits"),
        ("Error Handler", "rpa.error_handler"),
        ("Template Matcher", "rpa.vision.template_matcher"),
        ("Vision Main", "rpa.vision.main")
    ]
    
    passed = 0
    for name, import_path in components:
        if run_component_test(name, import_path):
            passed += 1
    
    print(f"\nComponentes: {passed}/{len(components)} pasaron")
    return passed == len(components)

def run_unit_tests():
    """Ejecuta tests unitarios"""
    print_header("TESTS UNITARIOS")
    
    test_files = []
    
    # Buscar archivos de test
    if os.path.exists("test_framework.py"):
        test_files.append("test_framework.py")
    
    if os.path.exists("test_integration.py"):
        test_files.append("test_integration.py")
    
    if not test_files:
        print("⚠️  No se encontraron archivos de test")
        return True
    
    passed = 0
    for test_file in test_files:
        if run_python_file(test_file):
            passed += 1
    
    print(f"\nTests: {passed}/{len(test_files)} pasaron")
    return passed == len(test_files)

def run_configuration_test():
    """Verifica configuración del sistema"""
    print_header("TEST DE CONFIGURACIÓN")
    
    try:
        from rpa.config_manager import ConfigManager
        
        # Test configuración por defecto
        config = ConfigManager('nonexistent.yaml')
        
        # Verificar valores críticos
        checks = [
            ("delays.medium", lambda x: x > 0),
            ("template_matching.default_confidence", lambda x: 0 < x <= 1),
            ("retries.max_sap_open_attempts", lambda x: x > 0)
        ]
        
        all_passed = True
        for key, validator in checks:
            try:
                value = config.get(key)
                valid = validator(value)
                print_result(f"Config {key} = {value}", valid)
                if not valid:
                    all_passed = False
            except Exception as e:
                print_result(f"Config {key}", False)
                print(f"  Error: {str(e)}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_result("Configuración general", False)
        print(f"  Error: {str(e)}")
        return False

def generate_test_report():
    """Genera reporte de test"""
    print_header("REPORTE FINAL")
    
    total_checks = 5
    passed_checks = 0
    
    print("📋 Resumen de verificaciones:")
    
    # Ejecutar todas las verificaciones
    checks = [
        ("Dependencias", check_dependencies),
        ("Estructura de archivos", check_file_structure),
        ("Componentes", run_component_tests),
        ("Configuración", run_configuration_test),
        ("Tests unitarios", run_unit_tests)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
            if result:
                passed_checks += 1
        except Exception as e:
            results.append((name, False))
            print(f"Error en {name}: {e}")
    
    print("\n📊 RESULTADOS:")
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")
    
    success_rate = (passed_checks / total_checks) * 100
    print(f"\n🎯 Tasa de éxito: {success_rate:.1f}% ({passed_checks}/{total_checks})")
    
    if success_rate >= 80:
        print("🎉 Sistema RPA en buen estado para producción!")
    elif success_rate >= 60:
        print("⚠️  Sistema RPA funcional pero necesita atención")
    else:
        print("🚨 Sistema RPA requiere correcciones antes de usar")
    
    return success_rate >= 80

def main():
    """Función principal"""
    print("🤖 SISTEMA DE TESTING RPA TAMAPRINT")
    print("Verificando integridad y funcionalidad del sistema...")
    
    start_time = time.time()
    
    try:
        success = generate_test_report()
        
        total_time = time.time() - start_time
        print(f"\n⏱️  Tiempo total: {total_time:.2f} segundos")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos por usuario")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error crítico en testing: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)