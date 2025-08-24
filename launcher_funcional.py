#!/usr/bin/env python3
"""
Launcher Funcional RPA TAMAPRINT v3.0
Versión que realmente ejecuta el procesamiento de órdenes de venta
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

# Importar componentes del RPA
from rpa.simple_logger import rpa_logger
from rpa.config_manager import ConfigManager
from rpa.vision.main import Vision
from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
from rpa.modules.production_order.production_order_handler import ProductionOrderHandler

class RPALauncherFuncional:
    def __init__(self):
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("RPA TAMAPRINT v3.0 - Launcher Funcional")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables de estado
        self.selected_module = None
        self.is_running = False
        self.processing_thread = None
        self.stop_processing = False
        
        # Configurar directorios base
        self.base_dir = "data/outputs_json"
        
        # Directorios para módulo de ventas
        self.sales_base_dir = os.path.join(self.base_dir, "sales_order")
        self.sales_pending_dir = os.path.join(self.sales_base_dir, "01_Pendiente")
        self.sales_processing_dir = os.path.join(self.sales_base_dir, "02_Procesando")
        self.sales_completed_dir = os.path.join(self.sales_base_dir, "03_Completado")
        self.sales_error_dir = os.path.join(self.sales_base_dir, "04_Error")
        self.sales_archived_dir = os.path.join(self.sales_base_dir, "05_Archivado")
        
        # Directorios para módulo de producción
        self.production_base_dir = os.path.join(self.base_dir, "production_order")
        self.production_pending_dir = os.path.join(self.production_base_dir, "01_Pendiente")
        self.production_processing_dir = os.path.join(self.production_base_dir, "02_Procesando")
        self.production_completed_dir = os.path.join(self.production_base_dir, "03_Completado")
        self.production_error_dir = os.path.join(self.production_base_dir, "04_Error")
        self.production_archived_dir = os.path.join(self.production_base_dir, "05_Archivado")
        
        # Directorios actuales (se actualizan según el módulo seleccionado)
        self.pending_dir = self.sales_pending_dir
        self.processing_dir = self.sales_processing_dir
        self.completed_dir = self.sales_completed_dir
        self.error_dir = self.sales_error_dir
        self.archived_dir = self.sales_archived_dir
        
        # Crear interfaz PRIMERO
        self.create_interface()
        
        # Inicializar componentes del RPA DESPUÉS
        self.initialize_rpa_components()
        
        # Log inicial
        self.log_message("Launcher RPA TAMAPRINT v3.0 iniciado")
        self.log_message("Sistema listo para procesar órdenes de venta")
        self.update_queue_status()
    
    def initialize_rpa_components(self):
        """Inicializa los componentes del RPA"""
        try:
            self.log_message("Inicializando componentes del RPA...")
            
            # Inicializar configuración
            self.config_manager = ConfigManager()
            
            # Inicializar sistema de visión
            self.vision_system = Vision()
            
            # Inicializar handler de órdenes de venta
            self.sales_handler = SalesOrderHandler(self.vision_system, self.config_manager)
            
            # Inicializar handler de órdenes de producción
            self.production_handler = ProductionOrderHandler(self.vision_system, self.config_manager)
            
            self.log_message("✅ Componentes del RPA inicializados correctamente")
            
        except Exception as e:
            self.log_message(f"❌ Error inicializando RPA: {str(e)}")
            messagebox.showerror("Error", f"Error inicializando RPA:\n{str(e)}")
    
    def create_interface(self):
        """Crea la interfaz de usuario"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="RPA TAMAPRINT v3.0 - Procesamiento Real", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para dos columnas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Módulos y Control
        left_frame = ttk.LabelFrame(content_frame, text="Selección de Módulos y Control", padding="10")
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
        sales_frame = ttk.LabelFrame(parent, text="Órdenes de Venta", padding="8")
        sales_frame.pack(fill=tk.X, pady=(0, 10))
        
        sales_info = ttk.Label(
            sales_frame,
            text="Automatización de órdenes de venta en SAP Business One\n"
                 "• Carga NIT del cliente\n"
                 "• Ingresa número de orden\n"
                 "• Procesa items y cantidades\n"
                 "• Toma screenshot final",
            justify=tk.LEFT
        )
        sales_info.pack(anchor=tk.W, pady=(0, 8))
        
        self.sales_btn = ttk.Button(
            sales_frame,
            text="Seleccionar Módulo de Ventas",
            command=lambda: self.select_module("sales_order")
        )
        self.sales_btn.pack(fill=tk.X)
        
        # Módulo de Producción
        production_frame = ttk.LabelFrame(parent, text="Órdenes de Producción", padding="8")
        production_frame.pack(fill=tk.X, pady=(0, 10))
        
        production_info = ttk.Label(
            production_frame,
            text="Automatización de órdenes de producción en SAP Business One\n"
                 "• Navega al módulo de producción\n"
                 "• Crea órdenes de fabricación\n"
                 "• Ingresa artículo, cantidad y fecha\n"
                 "• Toma screenshot final",
            justify=tk.LEFT
        )
        production_info.pack(anchor=tk.W, pady=(0, 8))
        
        self.production_btn = ttk.Button(
            production_frame,
            text="Seleccionar Módulo de Producción",
            command=lambda: self.select_module("production_order")
        )
        self.production_btn.pack(fill=tk.X)
        
        # Información del módulo seleccionado
        self.selected_module_frame = ttk.LabelFrame(parent, text="Módulo Seleccionado", padding="8")
        self.selected_module_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.selected_module_label = ttk.Label(
            self.selected_module_frame,
            text="Ningún módulo seleccionado",
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
            text="Iniciar Procesamiento Automático",
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
            text="Probar Módulo",
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
        self.update_directories_for_module()
        self.log_message(f"Módulo seleccionado: {module_type}")
    
    def update_directories_for_module(self):
        """Actualiza los directorios según el módulo seleccionado"""
        if self.selected_module == "sales_order":
            self.pending_dir = self.sales_pending_dir
            self.processing_dir = self.sales_processing_dir
            self.completed_dir = self.sales_completed_dir
            self.error_dir = self.sales_error_dir
            self.archived_dir = self.sales_archived_dir
            self.log_message("📁 Directorios actualizados para módulo de ventas")
        elif self.selected_module == "production_order":
            self.pending_dir = self.production_pending_dir
            self.processing_dir = self.production_processing_dir
            self.completed_dir = self.production_completed_dir
            self.error_dir = self.production_error_dir
            self.archived_dir = self.production_archived_dir
            self.log_message("📁 Directorios actualizados para módulo de producción")
        
        # Actualizar estado de la cola
        self.update_queue_status()
    
    def update_module_selection_ui(self):
        """Actualiza la interfaz de selección de módulos"""
        if self.selected_module:
            if self.selected_module == "sales_order":
                module_name = "Órdenes de Venta"
                self.sales_btn.config(text="Módulo de Ventas Seleccionado")
                self.production_btn.config(text="Seleccionar Módulo de Producción")
            elif self.selected_module == "production_order":
                module_name = "Órdenes de Producción"
                self.production_btn.config(text="Módulo de Producción Seleccionado")
                self.sales_btn.config(text="Seleccionar Módulo de Ventas")
            
            self.selected_module_label.config(
                text=f"Módulo: {module_name}",
                font=("Arial", 10, "bold")
            )
        else:
            self.selected_module_label.config(
                text="Ningún módulo seleccionado",
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
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de iniciar el procesamiento")
            return
        
        self.is_running = True
        self.stop_processing = False
        self.start_stop_btn.config(text="Detener Procesamiento Automático")
        self.processing_status_label.config(text="Estado: Procesando automáticamente")
        self.log_message("🚀 Iniciando procesamiento automático de la cola")
        
        # Iniciar hilo de procesamiento
        self.processing_thread = threading.Thread(target=self.process_queue_automatically, daemon=True)
        self.processing_thread.start()
    
    def stop_automatic_processing(self):
        """Detiene el procesamiento automático"""
        self.is_running = False
        self.stop_processing = True
        self.start_stop_btn.config(text="Iniciar Procesamiento Automático")
        self.processing_status_label.config(text="Estado: Detenido")
        self.current_file_label.config(text="Archivo actual: Ninguno")
        self.log_message("⏹️ Procesamiento automático detenido")
    
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
                    
                    self.log_message(f"📄 Procesando archivo: {filename}")
                    self.current_file_label.config(text=f"Archivo actual: {filename}")
                    
                    # Mover a procesando
                    processing_path = os.path.join(self.processing_dir, filename)
                    shutil.move(file_path, processing_path)
                    
                    # Procesar el archivo con el RPA real
                    success = self.process_file_with_rpa(processing_path)
                    
                    if success:
                        # Mover a completado
                        completed_path = os.path.join(self.completed_dir, filename)
                        shutil.move(processing_path, completed_path)
                        self.log_message(f"✅ Archivo procesado exitosamente: {filename}")
                    else:
                        # Mover a error
                        error_path = os.path.join(self.error_dir, filename)
                        shutil.move(processing_path, error_path)
                        self.log_message(f"❌ Error procesando archivo: {filename}")
                    
                    self.current_file_label.config(text="Archivo actual: Ninguno")
                    self.update_queue_status()
                else:
                    # No hay archivos pendientes
                    time.sleep(5)  # Esperar 5 segundos antes de verificar nuevamente
                
            except Exception as e:
                self.log_message(f"❌ Error en procesamiento automático: {str(e)}")
                time.sleep(10)  # Esperar más tiempo en caso de error
    
    def process_file_with_rpa(self, file_path):
        """Procesa un archivo usando el RPA real"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.log_message(f"🔄 Iniciando procesamiento RPA para: {data.get('orden_compra', 'N/A')}")
            
            # Procesar con el handler correspondiente
            if self.selected_module == "sales_order":
                success = self.sales_handler.process_sales_order(data)
                if success:
                    self.log_message("✅ Procesamiento RPA de ventas completado exitosamente")
                else:
                    self.log_message("❌ Error en procesamiento RPA de ventas")
                return success
            elif self.selected_module == "production_order":
                success = self.production_handler.process_production_order(data)
                if success:
                    self.log_message("✅ Procesamiento RPA de producción completado exitosamente")
                else:
                    self.log_message("❌ Error en procesamiento RPA de producción")
                return success
            else:
                self.log_message("❌ Módulo no soportado")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Error leyendo archivo {os.path.basename(file_path)}: {str(e)}")
            return False
    
    def process_single_file(self):
        """Procesa un archivo individual seleccionado manualmente"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de procesar archivos")
            return
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.log_message(f"📄 Procesando archivo manual: {os.path.basename(file_path)}")
            success = self.process_file_with_rpa(file_path)
            
            if success:
                self.log_message(f"✅ Archivo procesado exitosamente: {os.path.basename(file_path)}")
                messagebox.showinfo("Éxito", f"Archivo procesado exitosamente:\n{os.path.basename(file_path)}")
            else:
                self.log_message(f"❌ Error procesando archivo: {os.path.basename(file_path)}")
                messagebox.showerror("Error", f"Error procesando archivo:\n{os.path.basename(file_path)}")
    
    def test_module(self):
        """Prueba el módulo seleccionado"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de probarlo")
            return
        
        self.log_message(f"🧪 Probando módulo: {self.selected_module}")
        
        try:
            if self.selected_module == "sales_order":
                success = self.sales_handler.test_module()
                if success:
                    self.log_message("✅ Prueba del módulo de ventas exitosa")
                    messagebox.showinfo("Éxito", "Prueba del módulo de ventas exitosa")
                else:
                    self.log_message("❌ Prueba del módulo de ventas falló")
                    messagebox.showerror("Error", "Prueba del módulo de ventas falló")
            elif self.selected_module == "production_order":
                success = self.production_handler.test_module()
                if success:
                    self.log_message("✅ Prueba del módulo de producción exitosa")
                    messagebox.showinfo("Éxito", "Prueba del módulo de producción exitosa")
                else:
                    self.log_message("❌ Prueba del módulo de producción falló")
                    messagebox.showerror("Error", "Prueba del módulo de producción falló")
        except Exception as e:
            self.log_message(f"❌ Error en prueba del módulo: {str(e)}")
            messagebox.showerror("Error", f"Error en prueba del módulo:\n{str(e)}")
    
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
            self.log_message(f"❌ Error actualizando estado de cola: {str(e)}")
    
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
        self.log_message("🧹 Logs limpiados")
    
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
            self.log_message(f"💾 Logs guardados en: {file_path}")
            messagebox.showinfo("Éxito", f"Logs guardados en:\n{file_path}")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        print("🚀 Iniciando Launcher Funcional...")
        app = RPALauncherFuncional()
        print("✅ Launcher creado exitosamente")
        app.run()
        print("👋 Launcher cerrado correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
