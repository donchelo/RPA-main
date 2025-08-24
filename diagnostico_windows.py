#!/usr/bin/env python3
"""
Script de diagnóstico para Windows
Identifica problemas específicos que pueden causar que el launcher se cierre
"""

import sys
import os
import platform
import traceback

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 VERIFICANDO VERSIÓN DE PYTHON")
    print("=" * 40)
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Versión de Python muy antigua. Se recomienda Python 3.7+")
        return False
    else:
        print("✅ Versión de Python compatible")
        return True

def check_tkinter():
    """Verifica que tkinter esté disponible"""
    print("\n🎨 VERIFICANDO TKINTER")
    print("=" * 40)
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        print("✅ tkinter importado correctamente")
        
        # Probar crear una ventana simple
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        print("✅ Ventana tkinter creada correctamente")
        
        # Probar messagebox
        print("✅ messagebox disponible")
        
        root.destroy()
        return True
        
    except ImportError as e:
        print(f"❌ Error importando tkinter: {e}")
        return False
    except Exception as e:
        print(f"❌ Error con tkinter: {e}")
        return False

def check_system_info():
    """Verifica información del sistema"""
    print("\n💻 INFORMACIÓN DEL SISTEMA")
    print("=" * 40)
    
    print(f"Sistema operativo: {platform.system()}")
    print(f"Versión: {platform.version()}")
    print(f"Arquitectura: {platform.machine()}")
    print(f"Procesador: {platform.processor()}")
    
    # Verificar si es Windows
    if platform.system() == "Windows":
        print("✅ Sistema Windows detectado")
        return True
    else:
        print("⚠️ Sistema no Windows detectado")
        return False

def check_dependencies():
    """Verifica dependencias básicas"""
    print("\n📦 VERIFICANDO DEPENDENCIAS")
    print("=" * 40)
    
    dependencies = [
        ("threading", "threading"),
        ("queue", "queue"),
        ("datetime", "datetime"),
        ("json", "json"),
        ("glob", "glob"),
        ("os", "os"),
        ("sys", "sys"),
        ("time", "time"),
        ("traceback", "traceback")
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            all_ok = False
    
    return all_ok

def check_directory():
    """Verifica el directorio actual y archivos"""
    print("\n📁 VERIFICANDO DIRECTORIO")
    print("=" * 40)
    
    current_dir = os.getcwd()
    print(f"Directorio actual: {current_dir}")
    
    # Verificar archivos importantes
    important_files = [
        "rpa_launcher_v3_robust.py",
        "rpa_unified_interface.py",
        "rpa_orchestrator.py"
    ]
    
    all_files_exist = True
    for file in important_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (no encontrado)")
            all_files_exist = False
    
    return all_files_exist

def test_launcher_creation():
    """Prueba la creación del launcher"""
    print("\n🚀 PROBANDO CREACIÓN DEL LAUNCHER")
    print("=" * 40)
    
    try:
        # Importar el launcher
        from rpa_launcher_v3_robust import RPALauncherV3Robust
        print("✅ Importación exitosa")
        
        # Crear instancia
        launcher = RPALauncherV3Robust()
        print("✅ Instancia creada correctamente")
        
        # Verificar que la ventana se creó
        if hasattr(launcher, 'root') and launcher.root:
            print("✅ Ventana principal creada")
        else:
            print("❌ Error: Ventana principal no creada")
            return False
        
        # Cerrar la ventana
        launcher.root.destroy()
        print("✅ Ventana cerrada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando launcher: {e}")
        print("Detalles del error:")
        traceback.print_exc()
        return False

def check_windows_specific():
    """Verifica problemas específicos de Windows"""
    print("\n🪟 VERIFICANDO PROBLEMAS ESPECÍFICOS DE WINDOWS")
    print("=" * 40)
    
    issues = []
    
    # Verificar codificación
    try:
        import locale
        encoding = locale.getpreferredencoding()
        print(f"Codificación del sistema: {encoding}")
        if encoding.lower() != 'utf-8':
            issues.append(f"Codificación no UTF-8: {encoding}")
        else:
            print("✅ Codificación UTF-8")
    except Exception as e:
        issues.append(f"Error verificando codificación: {e}")
    
    # Verificar permisos
    try:
        test_file = "test_permissions.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Permisos de escritura OK")
    except Exception as e:
        issues.append(f"Error de permisos: {e}")
    
    # Verificar variables de entorno
    try:
        path = os.environ.get('PATH', '')
        if 'python' in path.lower():
            print("✅ Python en PATH")
        else:
            issues.append("Python no encontrado en PATH")
    except Exception as e:
        issues.append(f"Error verificando PATH: {e}")
    
    if issues:
        print("⚠️ Problemas detectados:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ No se detectaron problemas específicos de Windows")
        return True

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("=" * 60)
    print(f"Fecha y hora: {os.popen('date /t & time /t').read().strip()}")
    print()
    
    results = []
    
    # Ejecutar todas las verificaciones
    results.append(("Python Version", check_python_version()))
    results.append(("Tkinter", check_tkinter()))
    results.append(("System Info", check_system_info()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Directory", check_directory()))
    results.append(("Windows Specific", check_windows_specific()))
    results.append(("Launcher Creation", test_launcher_creation()))
    
    # Resumen
    print("\n📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("El sistema está listo para ejecutar el launcher")
        return True
    else:
        print(f"\n⚠️ {total - passed} PRUEBAS FALLARON")
        print("Revisa los errores arriba para solucionar los problemas")
        return False

if __name__ == "__main__":
    try:
        success = main()
        print("\n" + "=" * 60)
        if success:
            print("✅ DIAGNÓSTICO EXITOSO")
        else:
            print("❌ DIAGNÓSTICO FALLÓ")
        
        input("\nPresiona Enter para salir...")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Diagnóstico interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico en diagnóstico: {e}")
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
