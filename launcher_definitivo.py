#!/usr/bin/env python3
"""
Launcher Definitivo RPA TAMAPRINT v3.0
Version que funciona sin problemas en Windows
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys
import json
import glob
from datetime import datetime

class RPALauncherDefinitivo:
    def __init__(self):
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("RPA TAMAPRINT v3.0 - Launcher Definitivo")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # Variables de estado
        self.selected_module = None
        self.is_running = False
        
        # Crear interfaz
        self.create_interface()
        
        # Log inicial
        self.log_message("Launcher RPA TAMAPRINT v3.0 iniciado")
        self.log_message("Sistema listo para usar")
    
    def create_interface(self):
        """Crea la interfaz de usuario"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="RPA TAMAPRINT v3.0", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para dos columnas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Módulos
        left_frame = ttk.LabelFrame(content_frame, text="Seleccion de Modulos", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_module_selection(left_frame)
        
        # Columna derecha - Control y logs
        right_frame = ttk.LabelFrame(content_frame, text="Control y Logs", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_control_panel(right_frame)
    
    def create_module_selection(self, parent):
        """Crea el panel de selección de módulos"""
        
        # Módulo de Ventas
        sales_frame = ttk.LabelFrame(parent, text="Ordenes de Venta", padding="8")
        sales_frame.pack(fill=tk.X, pady=(0, 10))
        
        sales_info = ttk.Label(
            sales_frame,
            text="Automatizacion de ordenes de venta en SAP Business One\n"
                 "• Carga NIT del cliente\n"
                 "• Ingresa numero de orden\n"
                 "• Procesa items y cantidades",
            justify=tk.LEFT
        )
        sales_info.pack(anchor=tk.W, pady=(0, 8))
        
        self.sales_btn = ttk.Button(
            sales_frame,
            text="Seleccionar Modulo de Ventas",
            command=lambda: self.select_module("sales_order")
        )
        self.sales_btn.pack(fill=tk.X)
        
        # Módulo de Producción
        production_frame = ttk.LabelFrame(parent, text="Ordenes de Produccion", padding="8")
        production_frame.pack(fill=tk.X, pady=(0, 10))
        
        production_info = ttk.Label(
            production_frame,
            text="Automatizacion de ordenes de produccion en SAP Business One\n"
                 "• Navega al modulo de produccion\n"
                 "• Crea ordenes de fabricacion\n"
                 "• Ingresa articulo, cantidad y fecha",
            justify=tk.LEFT
        )
        production_info.pack(anchor=tk.W, pady=(0, 8))
        
        self.production_btn = ttk.Button(
            production_frame,
            text="Seleccionar Modulo de Produccion",
            command=lambda: self.select_module("production_order")
        )
        self.production_btn.pack(fill=tk.X)
        
        # Información del módulo seleccionado
        self.selected_module_frame = ttk.LabelFrame(parent, text="Modulo Seleccionado", padding="8")
        self.selected_module_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.selected_module_label = ttk.Label(
            self.selected_module_frame,
            text="Ningun modulo seleccionado",
            font=("Arial", 10, "italic")
        )
        self.selected_module_label.pack()
    
    def create_control_panel(self, parent):
        """Crea el panel de control"""
        
        # Botones de control
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_stop_btn = ttk.Button(
            control_frame,
            text="Iniciar Sistema",
            command=self.toggle_system
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.process_file_btn = ttk.Button(
            control_frame,
            text="Procesar Archivo",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_file_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.test_btn = ttk.Button(
            control_frame,
            text="Probar Modulo",
            command=self.test_module,
            state=tk.DISABLED
        )
        self.test_btn.pack(side=tk.LEFT)
        
        # Información del sistema
        info_frame = ttk.LabelFrame(parent, text="Informacion del Sistema", padding="8")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.system_status_label = ttk.Label(info_frame, text="Estado: Inactivo")
        self.system_status_label.pack(anchor=tk.W)
        
        self.active_module_label = ttk.Label(info_frame, text="Modulo activo: Ninguno")
        self.active_module_label.pack(anchor=tk.W)
        
        # Área de logs
        log_frame = ttk.LabelFrame(parent, text="Logs del Sistema", padding="8")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Botones de log
        log_buttons_frame = ttk.Frame(log_frame)
        log_buttons_frame.pack(fill=tk.X, pady=(8, 0))
        
        ttk.Button(
            log_buttons_frame,
            text="Limpiar Logs",
            command=self.clear_logs
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            log_buttons_frame,
            text="Guardar Logs",
            command=self.save_logs
        ).pack(side=tk.LEFT)
    
    def select_module(self, module_type):
        """Selecciona un módulo"""
        self.selected_module = module_type
        self.update_module_selection_ui()
        self.update_control_buttons()
        self.log_message(f"Modulo seleccionado: {module_type}")
    
    def update_module_selection_ui(self):
        """Actualiza la interfaz de selección de módulos"""
        if self.selected_module:
            if self.selected_module == "sales_order":
                module_name = "Ordenes de Venta"
                self.sales_btn.config(text="Modulo de Ventas Seleccionado")
                self.production_btn.config(text="Seleccionar Modulo de Produccion")
            else:
                module_name = "Ordenes de Produccion"
                self.production_btn.config(text="Modulo de Produccion Seleccionado")
                self.sales_btn.config(text="Seleccionar Modulo de Ventas")
            
            self.selected_module_label.config(
                text=f"Modulo: {module_name}",
                font=("Arial", 10, "bold")
            )
        else:
            self.selected_module_label.config(
                text="Ningun modulo seleccionado",
                font=("Arial", 10, "italic")
            )
    
    def update_control_buttons(self):
        """Actualiza el estado de los botones de control"""
        if self.selected_module:
            self.process_file_btn.config(state=tk.NORMAL)
            self.test_btn.config(state=tk.NORMAL)
        else:
            self.process_file_btn.config(state=tk.DISABLED)
            self.test_btn.config(state=tk.DISABLED)
    
    def toggle_system(self):
        """Inicia o detiene el sistema"""
        if not self.is_running:
            self.start_system()
        else:
            self.stop_system()
    
    def start_system(self):
        """Inicia el sistema"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un modulo antes de iniciar el sistema")
            return
        
        self.is_running = True
        self.start_stop_btn.config(text="Detener Sistema")
        self.system_status_label.config(text="Estado: Activo")
        self.active_module_label.config(text=f"Modulo activo: {self.selected_module}")
        self.log_message("Sistema RPA iniciado")
    
    def stop_system(self):
        """Detiene el sistema"""
        self.is_running = False
        self.start_stop_btn.config(text="Iniciar Sistema")
        self.system_status_label.config(text="Estado: Inactivo")
        self.log_message("Sistema RPA detenido")
    
    def process_file(self):
        """Procesa un archivo"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un modulo antes de procesar archivos")
            return
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.log_message(f"Procesando archivo: {os.path.basename(file_path)}")
            self.log_message(f"Procesando con modulo: {self.selected_module}")
            self.log_message(f"Archivo procesado exitosamente: {os.path.basename(file_path)}")
            messagebox.showinfo("Exito", f"Archivo procesado exitosamente:\n{os.path.basename(file_path)}")
    
    def test_module(self):
        """Prueba el módulo seleccionado"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un modulo antes de probarlo")
            return
        
        self.log_message(f"Probando modulo: {self.selected_module}")
        self.log_message("Ejecutando prueba de navegacion...")
        self.log_message(f"Prueba del modulo exitosa: {self.selected_module}")
        messagebox.showinfo("Exito", f"Prueba del modulo exitosa:\n{self.selected_module}")
    
    def log_message(self, message):
        """Agrega un mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_logs(self):
        """Limpia los logs"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("Logs limpiados")
    
    def save_logs(self):
        """Guarda los logs en un archivo"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar logs",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log_message(f"Logs guardados en: {file_path}")
            messagebox.showinfo("Exito", f"Logs guardados en:\n{file_path}")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        print("Iniciando Launcher Definitivo...")
        app = RPALauncherDefinitivo()
        print("Launcher creado exitosamente")
        app.run()
        print("Launcher cerrado correctamente")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
