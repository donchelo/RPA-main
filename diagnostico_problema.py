#!/usr/bin/env python3
"""
Diagnostico Especifico del Problema
Identifica exactamente que causa que el launcher se cierre
"""

import sys
import os
import traceback

def test_basic_imports():
    """Prueba importaciones basicas"""
    print("=== PRUEBA 1: IMPORTACIONES BASICAS ===")
    
    try:
        import tkinter as tk
        print("✅ tkinter importado")
        
        from tkinter import ttk, messagebox
        print("✅ ttk y messagebox importados")
        
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_simple_window():
    """Prueba crear una ventana simple"""
    print("\n=== PRUEBA 2: VENTANA SIMPLE ===")
    
    try:
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        print("✅ Ventana creada")
        
        root.destroy()
        print("✅ Ventana destruida")
        
        return True
    except Exception as e:
        print(f"❌ Error creando ventana: {e}")
        return False

def test_complex_window():
    """Prueba crear una ventana compleja"""
    print("\n=== PRUEBA 3: VENTANA COMPLEJA ===")
    
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        root = tk.Tk()
        root.title("Test")
        root.geometry("300x200")
        
        # Agregar widgets
        label = ttk.Label(root, text="Test")
        label.pack()
        
        button = ttk.Button(root, text="Test")
        button.pack()
        
        print("✅ Ventana compleja creada")
        
        root.destroy()
        print("✅ Ventana compleja destruida")
        
        return True
    except Exception as e:
        print(f"❌ Error en ventana compleja: {e}")
        return False

def test_threading():
    """Prueba threading"""
    print("\n=== PRUEBA 4: THREADING ===")
    
    try:
        import threading
        import queue
        import time
        
        print("✅ threading importado")
        print("✅ queue importado")
        
        # Probar queue
        q = queue.Queue()
        q.put("test")
        item = q.get()
        print(f"✅ Queue funciona: {item}")
        
        return True
    except Exception as e:
        print(f"❌ Error en threading: {e}")
        return False

def test_file_operations():
    """Prueba operaciones de archivo"""
    print("\n=== PRUEBA 5: OPERACIONES DE ARCHIVO ===")
    
    try:
        import glob
        import json
        from datetime import datetime
        
        # Probar glob
        files = glob.glob("*.py")
        print(f"✅ glob funciona: {len(files)} archivos .py encontrados")
        
        # Probar datetime
        now = datetime.now()
        print(f"✅ datetime funciona: {now}")
        
        return True
    except Exception as e:
        print(f"❌ Error en operaciones de archivo: {e}")
        return False

def test_encoding():
    """Prueba problemas de codificacion"""
    print("\n=== PRUEBA 6: CODIFICACION ===")
    
    try:
        import locale
        
        # Verificar codificacion del sistema
        encoding = locale.getpreferredencoding()
        print(f"Codificacion del sistema: {encoding}")
        
        # Probar escribir archivo con caracteres especiales
        test_text = "áéíóú ñ ç"
        with open("test_encoding.txt", "w", encoding="utf-8") as f:
            f.write(test_text)
        
        with open("test_encoding.txt", "r", encoding="utf-8") as f:
            read_text = f.read()
        
        if test_text == read_text:
            print("✅ Codificacion UTF-8 funciona")
        else:
            print("❌ Problema con codificacion UTF-8")
        
        # Limpiar archivo de prueba
        os.remove("test_encoding.txt")
        
        return True
    except Exception as e:
        print(f"❌ Error en codificacion: {e}")
        return False

def test_launcher_components():
    """Prueba componentes del launcher"""
    print("\n=== PRUEBA 7: COMPONENTES DEL LAUNCHER ===")
    
    try:
        # Probar crear una ventana con componentes similares al launcher
        import tkinter as tk
        from tkinter import ttk, scrolledtext
        
        root = tk.Tk()
        root.title("Test Launcher")
        root.geometry("600x400")
        
        # Frame principal
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label
        label = ttk.Label(main_frame, text="Test Label")
        label.pack()
        
        # Button
        button = ttk.Button(main_frame, text="Test Button")
        button.pack()
        
        # ScrolledText
        text = scrolledtext.ScrolledText(main_frame, height=10)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, "Test text")
        
        print("✅ Todos los componentes del launcher funcionan")
        
        root.destroy()
        
        return True
    except Exception as e:
        print(f"❌ Error en componentes del launcher: {e}")
        return False

def main():
    """Funcion principal de diagnostico"""
    print("🔍 DIAGNOSTICO ESPECIFICO DEL PROBLEMA")
    print("=" * 50)
    
    tests = [
        ("Importaciones Basicas", test_basic_imports),
        ("Ventana Simple", test_simple_window),
        ("Ventana Compleja", test_complex_window),
        ("Threading", test_threading),
        ("Operaciones de Archivo", test_file_operations),
        ("Codificacion", test_encoding),
        ("Componentes del Launcher", test_launcher_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASO" if result else "❌ FALLO"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("El problema puede estar en la logica del launcher")
    else:
        print(f"\n⚠️ {len(results) - passed} PRUEBAS FALLARON")
        print("Se identificaron problemas especificos")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        success = main()
        print("\n" + "=" * 50)
        if success:
            print("✅ DIAGNOSTICO COMPLETADO - SIN PROBLEMAS")
        else:
            print("❌ DIAGNOSTICO COMPLETADO - PROBLEMAS IDENTIFICADOS")
        
        input("\nPresiona Enter para salir...")
        
    except Exception as e:
        print(f"\n❌ Error critico en diagnostico: {e}")
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
