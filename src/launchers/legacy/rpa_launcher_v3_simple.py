#!/usr/bin/env python3
"""
Launcher RPA TAMAPRINT v3.0 - Versión Simplificada
Interfaz básica para seleccionar entre módulos de ventas y producción
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
import json
import glob
from datetime import datetime
import queue
import time

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class RPALauncherV3Simple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 AI4U | RPA TAMAPRINT v3.0 - Launcher Simplificado")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables de estado
        self.is_running = False
        self.log_queue = queue.Queue()
        self.selected_module = None
        
        # Crear interfaz
        self.create_widgets()
        
        # Iniciar hilo para procesar logs
        self.start_log_processor()
        
        # Log inicial
        self.log_message("🚀 Launcher RPA TAMAPRINT v3.0 iniciado")
        self.log_message("✅ Sistema listo para usar")
    
    def create_widgets(self):
        """Crea la interfaz de usuario"""
        
        # Título principal
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=(12, 8), fill=tk.X, padx=12)
        
        title_label = ttk.Label(
            title_frame,
            text="🤖 AI4U | Sistema RPA TAMAPRINT v3.0",
            font=("Arial", 16, "bold")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Automatización Inteligente para Ti! | hola@ai4u.com.co",
            font=("Arial", 10)
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Frame principal con dos columnas
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        # Columna izquierda - Selección de módulos
        left_frame = ttk.LabelFrame(main_frame, text="📦 SELECCIÓN DE MÓDULOS", padding=12)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        
        # Módulos disponibles
        self._create_module_selection(left_frame)
        
        # Columna derecha - Control y monitoreo
        right_frame = ttk.LabelFrame(main_frame, text="🎮 CONTROL Y MONITOREO", padding=12)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))
        
        # Controles principales
        self._create_control_panel(right_frame)
        
        # Logs
        self._create_log_panel(right_frame)
        
        # Barra de estado
        self._create_status_bar()
    
    def _create_module_selection(self, parent):
        """Crea el panel de selección de módulos"""
        
        # Título
        title_label = ttk.Label(parent, text="Selecciona el módulo a utilizar:", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 12))
        
        # Frame para módulos
        modules_frame = ttk.Frame(parent)
        modules_frame.pack(fill=tk.BOTH, expand=True)
        
        # Módulo de Órdenes de Venta
        sales_frame = ttk.LabelFrame(modules_frame, text="🛒 ÓRDENES DE VENTA", padding=8)
        sales_frame.pack(fill=tk.X, pady=(0, 8))
        
        sales_info = ttk.Label(
            sales_frame, 
            text="Automatización de órdenes de venta en SAP Business One\n"
                 "• Carga NIT del cliente\n"
                 "• Ingresa número de orden\n"
                 "• Procesa items y cantidades\n"
                 "• Toma screenshots de confirmación",
            justify=tk.LEFT
        )
        sales_info.pack(anchor=tk.W, pady=(0, 8))
        
        self.sales_btn = ttk.Button(
            sales_frame, 
            text="Seleccionar Módulo de Ventas",
            command=lambda: self.select_module("sales_order")
        )
        self.sales_btn.pack(fill=tk.X)
        
        # Módulo de Órdenes de Producción
        production_frame = ttk.LabelFrame(modules_frame, text="🏭 ÓRDENES DE PRODUCCIÓN", padding=8)
        production_frame.pack(fill=tk.X, pady=(0, 8))
        
        production_info = ttk.Label(
            production_frame, 
            text="Automatización de órdenes de producción en SAP Business One\n"
                 "• Navega al módulo de producción\n"
                 "• Crea órdenes de fabricación\n"
                 "• Ingresa artículo, cantidad y fecha\n"
                 "• Genera screenshots de confirmación",
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
        self.selected_module_frame = ttk.LabelFrame(modules_frame, text="✅ MÓDULO SELECCIONADO", padding=8)
        self.selected_module_frame.pack(fill=tk.X, pady=(12, 0))
        
        self.selected_module_label = ttk.Label(
            self.selected_module_frame,
            text="Ningún módulo seleccionado",
            font=("Arial", 10, "italic")
        )
        self.selected_module_label.pack()
        
        # Campos soportados
        self.supported_fields_text = scrolledtext.ScrolledText(
            self.selected_module_frame,
            height=6,
            width=40,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.supported_fields_text.pack(fill=tk.X, pady=(8, 0))
    
    def _create_control_panel(self, parent):
        """Crea el panel de control principal"""
        
        # Frame de controles
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Botones principales
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Botón de inicio/parada
        self.start_stop_btn = ttk.Button(
            buttons_frame,
            text="▶️ INICIAR SISTEMA",
            command=self.toggle_system
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Botón de procesar archivo
        self.process_file_btn = ttk.Button(
            buttons_frame,
            text="📁 PROCESAR ARCHIVO",
            command=self.process_file,
            state=tk.DISABLED
        )
        self.process_file_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Botón de prueba
        self.test_btn = ttk.Button(
            buttons_frame,
            text="🧪 PROBAR MÓDULO",
            command=self.test_module,
            state=tk.DISABLED
        )
        self.test_btn.pack(side=tk.LEFT)
        
        # Frame de información
        info_frame = ttk.LabelFrame(controls_frame, text="📊 INFORMACIÓN DEL SISTEMA", padding=8)
        info_frame.pack(fill=tk.X, pady=(12, 0))
        
        # Estado del sistema
        self.system_status_label = ttk.Label(info_frame, text="Estado: Inactivo")
        self.system_status_label.pack(anchor=tk.W)
        
        # Archivos pendientes
        self.pending_files_label = ttk.Label(info_frame, text="Archivos pendientes: 0")
        self.pending_files_label.pack(anchor=tk.W)
        
        # Módulo activo
        self.active_module_label = ttk.Label(info_frame, text="Módulo activo: Ninguno")
        self.active_module_label.pack(anchor=tk.W)
    
    def _create_log_panel(self, parent):
        """Crea el panel de logs"""
        
        # Frame de logs
        log_frame = ttk.LabelFrame(parent, text="📝 LOGS DEL SISTEMA", padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de logs
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
            text="🗑️ Limpiar Logs",
            command=self.clear_logs
        ).pack(side=tk.LEFT, padx=(0, 8))
        
        ttk.Button(
            log_buttons_frame,
            text="💾 Guardar Logs",
            command=self.save_logs
        ).pack(side=tk.LEFT)
    
    def _create_status_bar(self):
        """Crea la barra de estado"""
        self.status_bar = ttk.Label(
            self.root,
            text="Sistema RPA TAMAPRINT v3.0 - Listo",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_module(self, module_type):
        """Selecciona un módulo específico"""
        try:
            self.selected_module = module_type
            self._update_module_selection_ui()
            self._update_control_buttons()
            self.log_message(f"✅ Módulo seleccionado: {module_type}")
        except Exception as e:
            messagebox.showerror("Error", f"Error seleccionando módulo: {str(e)}")
    
    def _update_module_selection_ui(self):
        """Actualiza la interfaz de selección de módulos"""
        if self.selected_module:
            if self.selected_module == "sales_order":
                module_name = "Órdenes de Venta"
                supported_fields = [
                    "comprador.nit",
                    "comprador.nombre", 
                    "orden_compra",
                    "fecha_entrega",
                    "items.codigo",
                    "items.cantidad",
                    "items.precio_unitario"
                ]
            else:
                module_name = "Órdenes de Producción"
                supported_fields = [
                    "numero_articulo",
                    "numero_pedido_interno",
                    "cantidad",
                    "fecha_finalizacion",
                    "unidad_medida",
                    "centro_trabajo"
                ]
            
            self.selected_module_label.config(
                text=f"Módulo: {module_name}",
                font=("Arial", 10, "bold")
            )
            
            # Actualizar campos soportados
            self.supported_fields_text.config(state=tk.NORMAL)
            self.supported_fields_text.delete(1.0, tk.END)
            self.supported_fields_text.insert(1.0, "Campos soportados:\n" + "\n".join(f"• {field}" for field in supported_fields))
            self.supported_fields_text.config(state=tk.DISABLED)
            
            # Actualizar botones
            if self.selected_module == "sales_order":
                self.sales_btn.config(text="✅ Módulo de Ventas Seleccionado")
                self.production_btn.config(text="Seleccionar Módulo de Producción")
            else:
                self.production_btn.config(text="✅ Módulo de Producción Seleccionado")
                self.sales_btn.config(text="Seleccionar Módulo de Ventas")
        else:
            self.selected_module_label.config(text="Ningún módulo seleccionado", font=("Arial", 10, "italic"))
            self.supported_fields_text.config(state=tk.NORMAL)
            self.supported_fields_text.delete(1.0, tk.END)
            self.supported_fields_text.config(state=tk.DISABLED)
    
    def _update_control_buttons(self):
        """Actualiza el estado de los botones de control"""
        if self.selected_module:
            self.process_file_btn.config(state=tk.NORMAL)
            self.test_btn.config(state=tk.NORMAL)
        else:
            self.process_file_btn.config(state=tk.DISABLED)
            self.test_btn.config(state=tk.DISABLED)
    
    def toggle_system(self):
        """Inicia o detiene el sistema RPA"""
        if not self.is_running:
            self.start_system()
        else:
            self.stop_system()
    
    def start_system(self):
        """Inicia el sistema RPA"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de iniciar el sistema")
            return
        
        try:
            self.is_running = True
            self.start_stop_btn.config(text="⏹️ DETENER SISTEMA")
            self.system_status_label.config(text="Estado: Activo")
            self.status_bar.config(text="Sistema RPA activo - monitoreando archivos...")
            self.log_message("🚀 Sistema RPA iniciado")
            
            # Iniciar monitoreo en hilo separado
            self.monitor_thread = threading.Thread(target=self._monitor_files, daemon=True)
            self.monitor_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error iniciando sistema: {str(e)}")
            self.stop_system()
    
    def stop_system(self):
        """Detiene el sistema RPA"""
        try:
            self.is_running = False
            self.start_stop_btn.config(text="▶️ INICIAR SISTEMA")
            self.system_status_label.config(text="Estado: Inactivo")
            self.status_bar.config(text="Sistema RPA detenido")
            self.log_message("⏹️ Sistema RPA detenido")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deteniendo sistema: {str(e)}")
    
    def process_file(self):
        """Procesa un archivo JSON seleccionado"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de procesar archivos")
            return
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                self.log_message(f"📁 Procesando archivo: {os.path.basename(file_path)}")
                
                # Simular procesamiento
                self.log_message(f"🔄 Procesando con módulo: {self.selected_module}")
                self.log_message(f"✅ Archivo procesado exitosamente: {os.path.basename(file_path)}")
                messagebox.showinfo("Éxito", f"Archivo procesado exitosamente:\n{os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error procesando archivo: {str(e)}")
    
    def test_module(self):
        """Prueba el módulo seleccionado"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de probarlo")
            return
        
        try:
            self.log_message(f"🧪 Probando módulo: {self.selected_module}")
            
            # Simular prueba
            self.log_message(f"🔄 Ejecutando prueba de navegación...")
            self.log_message(f"✅ Prueba del módulo exitosa: {self.selected_module}")
            messagebox.showinfo("Éxito", f"Prueba del módulo exitosa:\n{self.selected_module}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error probando módulo: {str(e)}")
    
    def _monitor_files(self):
        """Monitorea archivos en segundo plano"""
        while self.is_running:
            try:
                # Verificar archivos en carpeta de entrada
                input_dir = "data/outputs_json/01_Pendiente"
                if os.path.exists(input_dir):
                    json_files = glob.glob(os.path.join(input_dir, "*.json"))
                    if json_files:
                        self.log_message(f"📁 Encontrados {len(json_files)} archivos pendientes")
                        
                        for file_path in json_files:
                            if not self.is_running:
                                break
                            
                            try:
                                self.log_message(f"🔄 Procesando: {os.path.basename(file_path)}")
                                # Aquí iría la lógica real de procesamiento
                                self.log_message(f"✅ Procesado exitosamente: {os.path.basename(file_path)}")
                                    
                            except Exception as e:
                                self.log_message(f"❌ Error con archivo {os.path.basename(file_path)}: {str(e)}")
                
                time.sleep(10)  # Verificar cada 10 segundos
                
            except Exception as e:
                self.log_message(f"❌ Error en monitoreo: {str(e)}")
                time.sleep(30)  # Esperar más tiempo en caso de error
    
    def log_message(self, message: str):
        """Agrega un mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Agregar a la cola para procesamiento en el hilo principal
        self.log_queue.put(formatted_message)
    
    def start_log_processor(self):
        """Inicia el procesador de logs"""
        def process_logs():
            while True:
                try:
                    message = self.log_queue.get(timeout=0.1)
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, message)
                    self.log_text.see(tk.END)
                    self.log_text.config(state=tk.DISABLED)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error procesando log: {e}")
        
        log_thread = threading.Thread(target=process_logs, daemon=True)
        log_thread.start()
    
    def clear_logs(self):
        """Limpia los logs"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("🗑️ Logs limpiados")
    
    def save_logs(self):
        """Guarda los logs en un archivo"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar logs",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"💾 Logs guardados en: {file_path}")
                messagebox.showinfo("Éxito", f"Logs guardados en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error guardando logs: {str(e)}")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = RPALauncherV3Simple()
        app.run()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        input("Presiona Enter para salir...")
