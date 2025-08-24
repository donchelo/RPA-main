#!/usr/bin/env python3
"""
Launcher RPA TAMAPRINT v3.0 - Interfaz Unificada con Selección de Módulos
Permite seleccionar entre módulo de órdenes de venta y módulo de órdenes de producción
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import os
import sys
import json
import glob
from datetime import datetime
import queue
import time
from PIL import Image, ImageTk
import webbrowser

# Importar la nueva arquitectura
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rpa_unified_interface import RPAUnifiedInterface, ModuleType

class RPALauncherV3:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("🤖 AI4U | Launcher RPA TAMAPRINT v3.0 - Módulos Unificados")
            self.root.geometry("1200x800")
            self.root.resizable(True, True)
            
            # Branding AI4U
            self.brand_name = "AI4U"
            self.brand_tagline = "Automatización Inteligente para Ti!"
            self.brand_email = "hola@ai4u.com.co"
            self.brand_logo_path = os.path.join("assets", "ai4u_logo.png")
            self.brand_banner_path = os.path.join("assets", "ai4u_banner.png")
            self.brand_icon_path = os.path.join("assets", "ai4u.ico")
            self._image_refs = {}
            
            # Icono de la ventana
            self._set_window_icon()
            
            # Variables de estado
            self.rpa_process = None
            self.is_running = False
            self.log_queue = queue.Queue()
            self.selected_module = None
            
            # Nueva arquitectura
            try:
                self.interface = RPAUnifiedInterface()
                print("✅ Interfaz unificada inicializada correctamente")
            except Exception as e:
                print(f"❌ Error inicializando interfaz: {e}")
                messagebox.showerror("Error", f"Error inicializando interfaz: {e}")
                raise
            
            # Crear interfaz
            self.create_widgets()
            
            # Verificar requisitos al inicio
            self.check_requirements()
            
            # Iniciar hilo para procesar logs
            self.start_log_processor()
            
            # Actualizar estado de módulos
            self.update_modules_status()
            
        except Exception as e:
            print(f"❌ Error crítico en inicialización: {e}")
            if hasattr(self, 'root'):
                messagebox.showerror("Error Crítico", f"Error inicializando launcher: {e}")
            raise
    
    def create_widgets(self):
        try:
            # Título principal
            title_frame = ttk.Frame(self.root)
            title_frame.pack(pady=(12, 8), fill=tk.X)
            
            # Menú superior
            self._create_menubar()
            
            # Banner/Logo
            banner_photo = None
            if os.path.exists(self.brand_banner_path):
                banner_photo = self._load_image(self.brand_banner_path, max_size=(400, 80))
            logo_photo = None
            if banner_photo is None and os.path.exists(self.brand_logo_path):
                logo_photo = self._load_image(self.brand_logo_path, max_size=(80, 80))
            
            if banner_photo is not None:
                self._image_refs['banner_photo'] = banner_photo
                banner_label = ttk.Label(title_frame, image=banner_photo)
                banner_label.pack(side=tk.LEFT, padx=(0, 12))
            elif logo_photo is not None:
                self._image_refs['logo_photo'] = logo_photo
                logo_label = ttk.Label(title_frame, image=logo_photo)
                logo_label.pack(side=tk.LEFT, padx=(0, 12))
            
            # Textos de marca
            title_text_frame = ttk.Frame(title_frame)
            title_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            title_label = ttk.Label(
                title_text_frame,
                text=f"{self.brand_name} · Sistema RPA TAMAPRINT v3.0",
                font=("Arial", 16, "bold")
            )
            title_label.pack(anchor=tk.W)
            
            subtitle_label = ttk.Label(
                title_text_frame,
                text=f"{self.brand_tagline} | {self.brand_email}",
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
            
        except Exception as e:
            print(f"❌ Error creando widgets: {e}")
            messagebox.showerror("Error", f"Error creando interfaz: {e}")
            raise
    
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
            command=lambda: self.select_module(ModuleType.SALES_ORDER),
            style="Module.TButton"
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
            command=lambda: self.select_module(ModuleType.PRODUCTION_ORDER),
            style="Module.TButton"
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
            command=self.toggle_system,
            style="Action.TButton"
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
    
    def _create_menubar(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Procesar archivo...", command=self.process_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Módulos
        modules_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Módulos", menu=modules_menu)
        modules_menu.add_command(label="Órdenes de Venta", command=lambda: self.select_module(ModuleType.SALES_ORDER))
        modules_menu.add_command(label="Órdenes de Producción", command=lambda: self.select_module(ModuleType.PRODUCTION_ORDER))
        modules_menu.add_separator()
        modules_menu.add_command(label="Probar módulo actual", command=self.test_module)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Verificar requisitos", command=self.check_requirements)
        tools_menu.add_command(label="Abrir carpeta de logs", command=self.open_logs_folder)
        tools_menu.add_command(label="Abrir carpeta de screenshots", command=self.open_screenshots_folder)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self.show_about)
        help_menu.add_command(label="Documentación", command=self.open_documentation)
    
    def select_module(self, module_type: ModuleType):
        """Selecciona un módulo específico"""
        try:
            if self.interface.select_module(module_type):
                self.selected_module = module_type
                self._update_module_selection_ui()
                self._update_control_buttons()
                self.log_message(f"✅ Módulo seleccionado: {module_type.value}")
            else:
                messagebox.showerror("Error", f"No se pudo seleccionar el módulo {module_type.value}")
        except Exception as e:
            messagebox.showerror("Error", f"Error seleccionando módulo: {str(e)}")
    
    def _update_module_selection_ui(self):
        """Actualiza la interfaz de selección de módulos"""
        if self.selected_module:
            module_info = self.interface.get_module_info(self.selected_module)
            self.selected_module_label.config(
                text=f"Módulo: {module_info.name}",
                font=("Arial", 10, "bold")
            )
            
            # Actualizar campos soportados
            supported_fields = self.interface.get_supported_fields(self.selected_module)
            self.supported_fields_text.config(state=tk.NORMAL)
            self.supported_fields_text.delete(1.0, tk.END)
            self.supported_fields_text.insert(1.0, "Campos soportados:\n" + "\n".join(f"• {field}" for field in supported_fields))
            self.supported_fields_text.config(state=tk.DISABLED)
            
            # Actualizar botones
            if self.selected_module == ModuleType.SALES_ORDER:
                self.sales_btn.config(text="✅ Módulo de Ventas Seleccionado", style="Selected.TButton")
                self.production_btn.config(text="Seleccionar Módulo de Producción", style="Module.TButton")
            else:
                self.production_btn.config(text="✅ Módulo de Producción Seleccionado", style="Selected.TButton")
                self.sales_btn.config(text="Seleccionar Módulo de Ventas", style="Module.TButton")
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
                
                # Procesar en hilo separado
                process_thread = threading.Thread(
                    target=self._process_file_thread,
                    args=(file_path,),
                    daemon=True
                )
                process_thread.start()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error procesando archivo: {str(e)}")
    
    def _process_file_thread(self, file_path: str):
        """Procesa un archivo en un hilo separado"""
        try:
            success = self.interface.process_file(file_path, self.selected_module)
            
            if success:
                self.log_message(f"✅ Archivo procesado exitosamente: {os.path.basename(file_path)}")
                messagebox.showinfo("Éxito", f"Archivo procesado exitosamente:\n{os.path.basename(file_path)}")
            else:
                self.log_message(f"❌ Error procesando archivo: {os.path.basename(file_path)}")
                messagebox.showerror("Error", f"Error procesando archivo:\n{os.path.basename(file_path)}")
                
        except Exception as e:
            self.log_message(f"❌ Error en procesamiento: {str(e)}")
            messagebox.showerror("Error", f"Error en procesamiento: {str(e)}")
    
    def test_module(self):
        """Prueba el módulo seleccionado"""
        if not self.selected_module:
            messagebox.showwarning("Advertencia", "Debes seleccionar un módulo antes de probarlo")
            return
        
        try:
            self.log_message(f"🧪 Probando módulo: {self.selected_module.value}")
            
            # Ejecutar prueba en hilo separado
            test_thread = threading.Thread(
                target=self._test_module_thread,
                daemon=True
            )
            test_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error probando módulo: {str(e)}")
    
    def _test_module_thread(self):
        """Prueba el módulo en un hilo separado"""
        try:
            success = self.interface.test_module(self.selected_module)
            
            if success:
                self.log_message(f"✅ Prueba del módulo exitosa: {self.selected_module.value}")
                messagebox.showinfo("Éxito", f"Prueba del módulo exitosa:\n{self.selected_module.value}")
            else:
                self.log_message(f"❌ Error en prueba del módulo: {self.selected_module.value}")
                messagebox.showerror("Error", f"Error en prueba del módulo:\n{self.selected_module.value}")
                
        except Exception as e:
            self.log_message(f"❌ Error en prueba: {str(e)}")
            messagebox.showerror("Error", f"Error en prueba: {str(e)}")
    
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
                                success = self.interface.process_file(file_path, self.selected_module)
                                
                                if success:
                                    self.log_message(f"✅ Procesado exitosamente: {os.path.basename(file_path)}")
                                else:
                                    self.log_message(f"❌ Error procesando: {os.path.basename(file_path)}")
                                    
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
    
    def update_modules_status(self):
        """Actualiza el estado de los módulos"""
        try:
            # Actualizar información de archivos pendientes
            input_dir = "data/outputs_json/01_Pendiente"
            if os.path.exists(input_dir):
                json_files = glob.glob(os.path.join(input_dir, "*.json"))
                self.pending_files_label.config(text=f"Archivos pendientes: {len(json_files)}")
            else:
                self.pending_files_label.config(text="Archivos pendientes: 0")
            
            # Actualizar módulo activo
            if self.selected_module:
                module_info = self.interface.get_module_info(self.selected_module)
                self.active_module_label.config(text=f"Módulo activo: {module_info.name}")
            else:
                self.active_module_label.config(text="Módulo activo: Ninguno")
                
        except Exception as e:
            self.log_message(f"Error actualizando estado: {str(e)}")
    
    def check_requirements(self):
        """Verifica los requisitos del sistema"""
        try:
            # Verificar dependencias básicas
            import pyautogui
            import cv2
            import yaml
            
            self.log_message("✅ Dependencias básicas verificadas")
            
            # Verificar archivos de configuración
            config_files = [
                "config.yaml",
                "rpa/modules/sales_order/sales_order_config.yaml",
                "rpa/modules/production_order/production_order_config.yaml"
            ]
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    self.log_message(f"✅ Configuración encontrada: {config_file}")
                else:
                    self.log_message(f"⚠️ Configuración faltante: {config_file}")
            
            # Verificar carpetas necesarias
            folders = ["data/outputs_json", "screenshots", "logs"]
            for folder in folders:
                if os.path.exists(folder):
                    self.log_message(f"✅ Carpeta encontrada: {folder}")
                else:
                    os.makedirs(folder, exist_ok=True)
                    self.log_message(f"📁 Carpeta creada: {folder}")
            
            messagebox.showinfo("Verificación", "Verificación de requisitos completada")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error verificando requisitos: {str(e)}")
    
    def open_logs_folder(self):
        """Abre la carpeta de logs"""
        logs_dir = "logs"
        if os.path.exists(logs_dir):
            os.startfile(logs_dir)
        else:
            messagebox.showwarning("Advertencia", "La carpeta de logs no existe")
    
    def open_screenshots_folder(self):
        """Abre la carpeta de screenshots"""
        screenshots_dir = "screenshots"
        if os.path.exists(screenshots_dir):
            os.startfile(screenshots_dir)
        else:
            messagebox.showwarning("Advertencia", "La carpeta de screenshots no existe")
    
    def show_about(self):
        """Muestra información sobre el sistema"""
        about_text = f"""
🤖 AI4U | Sistema RPA TAMAPRINT v3.0

{self.brand_tagline}

Características:
• Módulo de Órdenes de Venta
• Módulo de Órdenes de Producción
• Interfaz unificada
• Monitoreo automático
• Logs detallados
• Integración con Google Drive

Contacto: {self.brand_email}
        """
        messagebox.showinfo("Acerca de", about_text)
    
    def open_documentation(self):
        """Abre la documentación"""
        try:
            webbrowser.open("https://github.com/ai4u/rpa-tamaprint")
        except:
            messagebox.showinfo("Documentación", "Documentación disponible en:\nhttps://github.com/ai4u/rpa-tamaprint")
    
    def _set_window_icon(self):
        """Establece el icono de la ventana"""
        try:
            if os.path.exists(self.brand_icon_path):
                self.root.iconbitmap(self.brand_icon_path)
        except:
            pass
    
    def _load_image(self, path: str, max_size: tuple = None) -> ImageTk.PhotoImage:
        """Carga una imagen con redimensionamiento opcional"""
        try:
            if os.path.exists(path):
                image = Image.open(path)
                if max_size:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error cargando imagen {path}: {e}")
        return None
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = RPALauncherV3()
    app.run()
