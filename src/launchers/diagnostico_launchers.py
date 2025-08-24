#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico de Launchers RPA
Script para identificar problemas con los launchers
"""

import os
import sys
import traceback
from datetime import datetime

def print_header(title):
    """Imprime un encabezado"""
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)

def check_python_version():
    """Verifica la versión de Python"""
    print_header("VERIFICACIÓN DE PYTHON")
    print(f"Versión de Python: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    print(f"Ejecutable: {sys.executable}")
    print()

def check_directories():
    """Verifica los directorios del proyecto"""
    print_header("VERIFICACIÓN DE DIRECTORIOS")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    print(f"Directorio actual: {current_dir}")
    print(f"Directorio del proyecto: {project_root}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    print()
    
    # Verificar directorios importantes
    dirs_to_check = [
        "rpa",
        "rpa/modules",
        "rpa/modules/sales_order",
        "rpa/modules/production_order",
        "data",
        "data/outputs_json",
        "data/outputs_json/sales_order",
        "data/outputs_json/production_order"
    ]
    
    print("Verificando directorios del proyecto:")
    for dir_path in dirs_to_check:
        full_path = os.path.join(project_root, dir_path)
        exists = os.path.exists(full_path)
        print(f"  {'✓' if exists else '✗'} {dir_path}: {full_path}")
    print()

def check_modules():
    """Verifica la disponibilidad de módulos"""
    print_header("VERIFICACIÓN DE MÓDULOS")
    
    modules_to_check = [
        "tkinter",
        "threading",
        "queue",
        "json",
        "glob",
        "datetime",
        "time",
        "traceback"
    ]
    
    print("Verificando módulos básicos:")
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module}: {e}")
    print()
    
    # Verificar módulos RPA específicos
    print("Verificando módulos RPA:")
    rpa_modules = [
        "rpa.modules.sales_order.sales_order_handler",
        "rpa.modules.production_order.production_order_handler"
    ]
    
    for module in rpa_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module}: {e}")
    print()

def check_files():
    """Verifica archivos importantes"""
    print_header("VERIFICACIÓN DE ARCHIVOS")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    files_to_check = [
        "src/launchers/launcher_ventas.py",
        "src/launchers/launcher_produccion.py",
        "src/launchers/launcher_ventas_simple.py",
        "src/launchers/launcher_produccion_simple.py",
        "src/launchers/test_launcher.py",
        "rpa/modules/sales_order/sales_order_config.yaml",
        "rpa/modules/production_order/production_order_config.yaml",
        "requirements.txt",
        "config.yaml"
    ]
    
    print("Verificando archivos importantes:")
    for file_path in files_to_check:
        full_path = os.path.join(project_root, file_path)
        exists = os.path.exists(full_path)
        size = os.path.getsize(full_path) if exists else 0
        print(f"  {'✓' if exists else '✗'} {file_path}: {size} bytes")
    print()

def test_tkinter():
    """Prueba la funcionalidad básica de tkinter"""
    print_header("PRUEBA DE TKINTER")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Crear ventana de prueba
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        # Crear un widget simple
        label = ttk.Label(root, text="Test")
        
        print("  ✓ Tkinter funciona correctamente")
        print("  ✓ Ttk funciona correctamente")
        
        # Cerrar ventana
        root.destroy()
        
    except Exception as e:
        print(f"  ✗ Error en Tkinter: {e}")
        print(f"  Detalles: {traceback.format_exc()}")
    
    print()

def test_launcher_simple():
    """Prueba el launcher de prueba"""
    print_header("PRUEBA DE LAUNCHER SIMPLE")
    
    try:
        # Importar y ejecutar el launcher de prueba
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        sys.path.append(project_root)
        
        # Simular ejecución del launcher de prueba
        print("  Probando importación del launcher de prueba...")
        
        # Aquí podrías importar y ejecutar el launcher de prueba
        # Por ahora solo verificamos que el archivo existe
        test_launcher_path = os.path.join(current_dir, "test_launcher.py")
        if os.path.exists(test_launcher_path):
            print("  ✓ Archivo test_launcher.py encontrado")
        else:
            print("  ✗ Archivo test_launcher.py no encontrado")
            
    except Exception as e:
        print(f"  ✗ Error en prueba de launcher: {e}")
        print(f"  Detalles: {traceback.format_exc()}")
    
    print()

def generate_report():
    """Genera un reporte de diagnóstico"""
    print_header("REPORTE DE DIAGNÓSTICO")
    
    report_file = f"diagnostico_launchers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("DIAGNÓSTICO DE LAUNCHERS RPA\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"Plataforma: {sys.platform}\n")
            f.write(f"Directorio: {os.getcwd()}\n\n")
            
            # Aquí podrías agregar más información al reporte
            
        print(f"  ✓ Reporte generado: {report_file}")
        
    except Exception as e:
        print(f"  ✗ Error generando reporte: {e}")
    
    print()

def main():
    """Función principal"""
    print_header("DIAGNÓSTICO DE LAUNCHERS RPA")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        check_python_version()
        check_directories()
        check_modules()
        check_files()
        test_tkinter()
        test_launcher_simple()
        generate_report()
        
        print_header("DIAGNÓSTICO COMPLETADO")
        print("Revisa los resultados anteriores para identificar problemas.")
        print("Si hay errores, verifica:")
        print("  1. Instalación de Python")
        print("  2. Dependencias (tkinter, etc.)")
        print("  3. Estructura de directorios")
        print("  4. Archivos de configuración")
        print()
        
    except Exception as e:
        print(f"Error en diagnóstico: {e}")
        print(traceback.format_exc())
    
    input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
