#!/usr/bin/env python3
"""
Launcher Ultra Simple para Windows
Version minimalista que funciona sin problemas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

def main():
    """Funcion principal ultra simple"""
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("RPA TAMAPRINT - Launcher")
    root.geometry("800x600")
    
    # Frame principal
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Titulo
    title_label = ttk.Label(main_frame, text="RPA TAMAPRINT v3.0", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Informacion
    info_label = ttk.Label(main_frame, text="Launcher funcionando correctamente!", font=("Arial", 12))
    info_label.pack(pady=(0, 20))
    
    # Botones
    def test_sales():
        messagebox.showinfo("Test", "Modulo de Ventas seleccionado")
    
    def test_production():
        messagebox.showinfo("Test", "Modulo de Produccion seleccionado")
    
    def test_exit():
        if messagebox.askyesno("Salir", "Deseas cerrar la aplicacion?"):
            root.destroy()
    
    # Frame para botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)
    
    # Botones de modulos
    sales_btn = ttk.Button(button_frame, text="Modulo de Ventas", command=test_sales, width=20)
    sales_btn.pack(pady=5)
    
    production_btn = ttk.Button(button_frame, text="Modulo de Produccion", command=test_production, width=20)
    production_btn.pack(pady=5)
    
    # Boton de salir
    exit_btn = ttk.Button(button_frame, text="Salir", command=test_exit, width=20)
    exit_btn.pack(pady=20)
    
    # Informacion del sistema
    system_info = f"""
    Sistema: {os.name}
    Python: {sys.version.split()[0]}
    Directorio: {os.getcwd()}
    """
    
    info_text = tk.Text(main_frame, height=8, width=60)
    info_text.pack(pady=20)
    info_text.insert(tk.END, system_info)
    info_text.config(state=tk.DISABLED)
    
    # Ejecutar la aplicacion
    root.mainloop()

if __name__ == "__main__":
    try:
        print("Iniciando launcher ultra simple...")
        main()
        print("Launcher cerrado correctamente")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")
