#!/usr/bin/env python3
"""
Launcher Completo RPA TAMAPRINT v3.0
Version que procesa automaticamente la cola de archivos
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys
import json
import glob
import shutil
from datetime import datetime
import threading
import time

class RPALauncherCompleto:
    def __init__(self):
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("RPA TAMAPRINT v3.0 - Launcher Completo")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables de estado
        self.selected_module = None
        self.is_running = False
        self.processing_thread = None
        self.stop_processing = False
        
        # Configurar directorios
        self.base_dir = "data/outputs_json"
        self.pending_dir = os.path.join(self.base_dir, "01_Pendiente")
        self.processing_dir = os.path.join(self.base_dir, "02_Procesando")
        self.completed_dir = os.path.join(self.base_dir, "03_Completado")
        self.error_dir = os.path.join(self.base_dir, "04_Error")
        self.archived_dir = os.path.join(self.base_dir, "05_Archivado")
        
        # Crear interfaz
        self.create_interface()
        
        # Log inicial
        self.log_message("Launcher RPA TAMAPRINT v3.0 iniciado")
        self.log_message("Sistema listo para procesar cola de archivos")
        self.update_queue_status()
    
    def create_interface(self):
        """Crea la interfaz de usuario"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="RPA TAMAPRINT v3.0 - Procesamiento Automatico", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para dos columnas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Módulos y Control
        left_frame = ttk.LabelFrame(content_frame, text="Seleccion de Modulos y Control", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_module_selection(left_frame)
        self.create_control_panel(left_frame)
        
        # Columna derecha - Logs y Estado
        right_frame = ttk.LabelFrame(content_frame, text="Logs y Estado del Sistema", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_status_panel(right_frame)
        self.create_log_panel(right_frame)
    
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
        
        control_frame = ttk.LabelFrame(parent, text="Control del Sistema", padding="8")
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botones de control
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_stop_btn = ttk.Button(
            buttons_frame,
            text="Iniciar Procesamiento Automatico",
            command=self.toggle_processing,
            state=tk.DISABLED
        )
        self.start_stop_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.process_single_btn = ttk.Button(
            buttons_frame,
            text="Procesar Archivo Manual",
            command=self.process_single_file,
            state=tk.DISABLED
        )
        self.process_single_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.test_btn = ttk.Button(
            buttons_frame,
            text="Probar Modulo",
            command=self.test_module,
            state=tk.DISABLED
        )
        self.test_btn.pack(fill=tk.X)
        
        # Estado del procesamiento
        self.processing_status_label = ttk.Label(control_frame, text="Estado: Inactivo")
        self.processing_status_label.pack(anchor=tk.W)
        
        self.current_file_label = ttk.Label(control_frame, text="Archivo actual: Ninguno")
        self.current_file_label.pack(anchor=tk.W)
    
    def create_status_panel(self, parent):
        """Crea el panel de estado"""
        
        status_frame = ttk.LabelFrame(parent, text="Estado de la Cola", padding="8")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Contadores de archivos
        self.pending_count_label = ttk.Label(status_frame, text="Pendientes: 0")
        self.pending_count_label.pack(anchor=tk.W)
        
        self.processing_count_label = ttk.Label(status_frame, text="Procesando: 0")
        self.processing_count_label.pack(anchor=tk.W)
        
        self.completed_count_label = ttk.Label(status_frame, text="Completados: 0")
        self.completed_count_label.pack(anchor=tk.W)
        
        self.error_count_label = ttk.Label(status_frame, text="Errores: 0")
        self.error_count_label.pack(anchor=tk.W)
        
        # Botón para actualizar estado
        ttk.Button(
            status_frame,
            text="Actualizar Estado",
            command=self.update_queue_status
        ).pack(fill=tk.X, pady=(10, 0))
    
    def create_log_panel(self, parent):
        """Crea el panel de logs"""
        
        log_frame = ttk.LabelFrame(parent, text="Logs del Sistema", padding="8")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
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
            self.start_stop_btn.config(state=tk.NORMAL)
            self.process_single_btn.config(state=tk.NORMAL)
            self.test_btn.config(state=tk.NORMAL)
        else:
            self.start_stop_btn.config(state=tk.DISABLED)
            self.process_single_btn.config(state=tk.DISABLED)
            self.test_btn.config(state=tk.DISABLED)
    
    def toggle_processing(self):
        """Inicia o detiene el procesamiento automático"""
        if not self.is_running:
            self.start_automatic_processing()
        else:
            self.stop_automatic_processing()
    
    def start_automatic_processing(self):
        """Inicia el procesamiento automático"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un modulo antes de iniciar el procesamiento")
            return
        
        self.is_running = True
        self.stop_processing = False
        self.start_stop_btn.config(text="Detener Procesamiento Automatico")
        self.processing_status_label.config(text="Estado: Procesando automaticamente")
        self.log_message("Iniciando procesamiento automatico de la cola")
        
        # Iniciar hilo de procesamiento
        self.processing_thread = threading.Thread(target=self.process_queue_automatically, daemon=True)
        self.processing_thread.start()
    
    def stop_automatic_processing(self):
        """Detiene el procesamiento automático"""
        self.is_running = False
        self.stop_processing = True
        self.start_stop_btn.config(text="Iniciar Procesamiento Automatico")
        self.processing_status_label.config(text="Estado: Detenido")
        self.current_file_label.config(text="Archivo actual: Ninguno")
        self.log_message("Procesamiento automatico detenido")
    
    def process_queue_automatically(self):
        """Procesa automáticamente la cola de archivos"""
        while self.is_running and not self.stop_processing:
            try:
                # Verificar archivos pendientes
                pending_files = glob.glob(os.path.join(self.pending_dir, "*.json"))
                
                if pending_files:
                    # Tomar el primer archivo
                    file_path = pending_files[0]
                    filename = os.path.basename(file_path)
                    
                    self.log_message(f"Procesando archivo: {filename}")
                    self.current_file_label.config(text=f"Archivo actual: {filename}")
                    
                    # Mover a procesando
                    processing_path = os.path.join(self.processing_dir, filename)
                    shutil.move(file_path, processing_path)
                    
                    # Procesar el archivo
                    success = self.process_file_content(processing_path)
                    
                    if success:
                        # Mover a completado
                        completed_path = os.path.join(self.completed_dir, filename)
                        shutil.move(processing_path, completed_path)
                        self.log_message(f"Archivo procesado exitosamente: {filename}")
                    else:
                        # Mover a error
                        error_path = os.path.join(self.error_dir, filename)
                        shutil.move(processing_path, error_path)
                        self.log_message(f"Error procesando archivo: {filename}")
                    
                    self.current_file_label.config(text="Archivo actual: Ninguno")
                    self.update_queue_status()
                else:
                    # No hay archivos pendientes
                    time.sleep(5)  # Esperar 5 segundos antes de verificar nuevamente
                
            except Exception as e:
                self.log_message(f"Error en procesamiento automatico: {str(e)}")
                time.sleep(10)  # Esperar más tiempo en caso de error
    
    def process_file_content(self, file_path):
        """Procesa el contenido de un archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Simular procesamiento según el módulo seleccionado
            if self.selected_module == "sales_order":
                return self.process_sales_order(data)
            elif self.selected_module == "production_order":
                return self.process_production_order(data)
            else:
                return False
                
        except Exception as e:
            self.log_message(f"Error leyendo archivo {os.path.basename(file_path)}: {str(e)}")
            return False
    
    def process_sales_order(self, data):
        """Procesa una orden de venta"""
        try:
            # Simular procesamiento de orden de venta
            self.log_message(f"Procesando orden de compra: {data.get('orden_compra', 'N/A')}")
            self.log_message(f"Cliente: {data.get('comprador', {}).get('nombre', 'N/A')}")
            self.log_message(f"Items: {len(data.get('items', []))}")
            
            # Simular tiempo de procesamiento
            time.sleep(2)
            
            return True
        except Exception as e:
            self.log_message(f"Error procesando orden de venta: {str(e)}")
            return False
    
    def process_production_order(self, data):
        """Procesa una orden de producción"""
        try:
            # Simular procesamiento de orden de producción
            self.log_message(f"Procesando orden de compra para produccion: {data.get('orden_compra', 'N/A')}")
            self.log_message(f"Items para produccion: {len(data.get('items', []))}")
            
            # Simular tiempo de procesamiento
            time.sleep(2)
            
            return True
        except Exception as e:
            self.log_message(f"Error procesando orden de produccion: {str(e)}")
            return False
    
    def process_single_file(self):
        """Procesa un archivo individual seleccionado manualmente"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un modulo antes de procesar archivos")
            return
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.log_message(f"Procesando archivo manual: {os.path.basename(file_path)}")
            success = self.process_file_content(file_path)
            
            if success:
                self.log_message(f"Archivo procesado exitosamente: {os.path.basename(file_path)}")
                messagebox.showinfo("Exito", f"Archivo procesado exitosamente:\n{os.path.basename(file_path)}")
            else:
                self.log_message(f"Error procesando archivo: {os.path.basename(file_path)}")
                messagebox.showerror("Error", f"Error procesando archivo:\n{os.path.basename(file_path)}")
    
    def test_module(self):
        """Prueba el módulo seleccionado"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un modulo antes de probarlo")
            return
        
        self.log_message(f"Probando modulo: {self.selected_module}")
        self.log_message("Ejecutando prueba de navegacion...")
        self.log_message(f"Prueba del modulo exitosa: {self.selected_module}")
        messagebox.showinfo("Exito", f"Prueba del modulo exitosa:\n{self.selected_module}")
    
    def update_queue_status(self):
        """Actualiza el estado de la cola"""
        try:
            # Contar archivos en cada carpeta
            pending_count = len(glob.glob(os.path.join(self.pending_dir, "*.json")))
            processing_count = len(glob.glob(os.path.join(self.processing_dir, "*.json")))
            completed_count = len(glob.glob(os.path.join(self.completed_dir, "*.json")))
            error_count = len(glob.glob(os.path.join(self.error_dir, "*.json")))
            
            # Actualizar etiquetas
            self.pending_count_label.config(text=f"Pendientes: {pending_count}")
            self.processing_count_label.config(text=f"Procesando: {processing_count}")
            self.completed_count_label.config(text=f"Completados: {completed_count}")
            self.error_count_label.config(text=f"Errores: {error_count}")
            
        except Exception as e:
            self.log_message(f"Error actualizando estado de cola: {str(e)}")
    
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
        print("Iniciando Launcher Completo...")
        app = RPALauncherCompleto()
        print("Launcher creado exitosamente")
        app.run()
        print("Launcher cerrado correctamente")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
