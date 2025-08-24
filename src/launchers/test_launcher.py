#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher de Prueba - Diagnóstico
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Configurar codificación para Windows
if sys.platform.startswith('win'):
    try:
        if hasattr(sys, 'setdefaultencoding'):
            sys.setdefaultencoding('utf-8')
    except:
        pass

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

print(f"Directorio actual: {current_dir}")
print(f"Directorio del proyecto: {project_root}")
print(f"Python path: {sys.path}")

class TestLauncher:
    def __init__(self):
        try:
            print("Iniciando TestLauncher...")
            
            # Configurar la ventana principal
            self.root = tk.Tk()
            self.root.title("Test Launcher")
            self.root.geometry("400x300")
            
            # Crear interfaz simple
            title_label = ttk.Label(
                self.root,
                text="Test Launcher - Funcionando",
                font=("Arial", 16, "bold")
            )
            title_label.pack(pady=20)
            
            info_label = ttk.Label(
                self.root,
                text="Si ves esta ventana, el launcher funciona correctamente",
                font=("Arial", 10)
            )
            info_label.pack(pady=10)
            
            # Botón de prueba
            test_btn = ttk.Button(
                self.root,
                text="Probar Módulos",
                command=self.test_modules
            )
            test_btn.pack(pady=10)
            
            # Botón de cerrar
            close_btn = ttk.Button(
                self.root,
                text="Cerrar",
                command=self.root.destroy
            )
            close_btn.pack(pady=10)
            
            print("TestLauncher iniciado correctamente")
            
        except Exception as e:
            print(f"Error en TestLauncher: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def test_modules(self):
        """Prueba la importación de módulos"""
        try:
            print("Probando importación de módulos...")
            
            # Probar importación de tkinter
            print("✓ Tkinter importado correctamente")
            
            # Probar importación de módulos RPA
            try:
                from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
                print("✓ Módulo sales_order importado correctamente")
            except ImportError as e:
                print(f"✗ Error importando sales_order: {e}")
            
            try:
                from rpa.modules.production_order.production_order_handler import ProductionOrderHandler
                print("✓ Módulo production_order importado correctamente")
            except ImportError as e:
                print(f"✗ Error importando production_order: {e}")
            
            # Mostrar información del sistema
            info = f"""
Información del Sistema:
- Python: {sys.version}
- Plataforma: {sys.platform}
- Directorio actual: {os.getcwd()}
- Directorio del proyecto: {project_root}
- Módulos en path: {len(sys.path)}
            """
            
            messagebox.showinfo("Test de Módulos", info)
            
        except Exception as e:
            print(f"Error en test_modules: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error en test: {e}")
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            print("Iniciando mainloop...")
            self.root.mainloop()
            print("Mainloop terminado")
        except Exception as e:
            print(f"Error en mainloop: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        print("Iniciando aplicación de prueba...")
        app = TestLauncher()
        app.run()
    except Exception as e:
        print(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para continuar...")
