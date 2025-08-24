#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher RPA - Órdenes de Producción (Versión Simplificada)
Sistema automatizado para procesamiento de órdenes de producción en SAP Business One
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import sys
import json
import glob
from datetime import datetime
import queue
import time
import traceback

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

class LauncherProduccionSimple:
    def __init__(self):
        try:
            # Configurar la ventana principal
            self.root = tk.Tk()
            self.root.title("AI4U | RPA - Órdenes de Producción")
            self.root.geometry("900x600")
            self.root.resizable(True, True)
            
            # Configurar para que no se cierre al hacer clic en X
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Variables de estado
            self.is_running = False
            self.log_queue = queue.Queue()
            self.is_closing = False
            
            # Crear interfaz
            self.create_widgets()
            
            # Iniciar hilo para procesar logs
            self.start_log_processor()
            
            # Log inicial
            self.log_message("🏭 Launcher de Órdenes de Producción iniciado")
            self.log_message("⚙️ Sistema listo para procesar órdenes de producción")
            
        except Exception as e:
            self.show_error_dialog("Error de inicialización", str(e))
            raise
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        try:
            if self.is_running:
                result = messagebox.askyesno(
                    "Confirmar cierre", 
                    "El sistema RPA está ejecutándose. ¿Deseas detenerlo y cerrar la aplicación?"
                )
                if result:
                    self.stop_system()
                    self.is_closing = True
                    self.root.after(1000, self.root.destroy)
                else:
                    return
            else:
                self.is_closing = True
                self.root.destroy()
        except Exception as e:
            print(f"Error en cierre: {e}")
            self.root.destroy()
    
    def show_error_dialog(self, title, message):
        """Muestra un diálogo de error"""
        try:
            messagebox.showerror(title, f"{message}\n\nDetalles técnicos:\n{traceback.format_exc()}")
        except:
            print(f"ERROR - {title}: {message}")
            print(traceback.format_exc())
    
    def create_widgets(self):
        """Crea la interfaz de usuario"""
        try:
            # Título principal
            title_frame = ttk.Frame(self.root)
            title_frame.pack(pady=(12, 8), fill=tk.X, padx=12)
            
            title_label = ttk.Label(
                title_frame,
                text="AI4U | Sistema RPA - Órdenes de Producción",
                font=("Arial", 16, "bold")
            )
            title_label.pack(anchor=tk.W)
            
            subtitle_label = ttk.Label(
                title_frame,
                text="Automatización de órdenes de producción en SAP Business One | hola@ai4u.com.co",
                font=("Arial", 10)
            )
            subtitle_label.pack(anchor=tk.W)
            
            # Frame principal con dos columnas
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
            
            # Columna izquierda - Información y configuración
            left_frame = ttk.LabelFrame(main_frame, text="CONFIGURACIÓN DE PRODUCCIÓN", padding=12)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
            
            self._create_production_info(left_frame)
            
            # Columna derecha - Control y monitoreo
            right_frame = ttk.LabelFrame(main_frame, text="CONTROL Y MONITOREO", padding=12)
            right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))
            
            # Controles principales
            self._create_control_panel(right_frame)
            
            # Logs
            self._create_log_panel(right_frame)
            
            # Barra de estado
            self._create_status_bar()
            
        except Exception as e:
            self.show_error_dialog("Error creando interfaz", str(e))
            raise
    
    def _create_production_info(self, parent):
        """Crea el panel de información de producción"""
        try:
            # Título
            title_label = ttk.Label(parent, text="🏭 Módulo de Órdenes de Producción", font=("Arial", 12, "bold"))
            title_label.pack(pady=(0, 12))
            
            # Información del módulo
            info_text = """
🎯 FUNCIONALIDADES:
• Navegación al módulo de producción en SAP
• Creación automática de órdenes de fabricación
• Ingreso de artículo, cantidad y fecha de finalización
• Procesamiento de pedidos internos
• Captura de screenshots de confirmación
• Integración con Google Drive

📁 ARCHIVOS PROCESADOS:
• Formato JSON con datos de órdenes de producción
• Ubicación: data/outputs_json/production_order/
• Estados: Pendiente, Procesando, Completado, Error

⚙️ CONFIGURACIÓN:
• SAP Business One debe estar abierto
• Escritorio remoto conectado
• Módulo de producción habilitado
• Archivos JSON en formato correcto
            """
            
            info_label = ttk.Label(parent, text=info_text, justify=tk.LEFT, font=("Arial", 9))
            info_label.pack(anchor=tk.W, pady=(0, 12))
            
            # Botón de configuración
            config_btn = ttk.Button(
                parent,
                text="⚙️ Ver Configuración",
                command=self.show_configuration
            )
            config_btn.pack(fill=tk.X, pady=(0, 8))
            
            # Botón de ver archivos
            files_btn = ttk.Button(
                parent,
                text="📁 Ver Archivos Pendientes",
                command=self.show_pending_files
            )
            files_btn.pack(fill=tk.X)
            
        except Exception as e:
            self.show_error_dialog("Error creando panel de producción", str(e))
    
    def _create_control_panel(self, parent):
        """Crea el panel de control"""
        try:
            # Botón principal de inicio
            self.start_btn = ttk.Button(
                parent,
                text="🏭 INICIAR PROCESAMIENTO DE PRODUCCIÓN",
                command=self.start_production_processing
            )
            self.start_btn.pack(fill=tk.X, pady=(0, 8))
            
            # Botón de parada
            self.stop_btn = ttk.Button(
                parent,
                text="⏹️ DETENER SISTEMA",
                command=self.stop_system,
                state=tk.DISABLED
            )
            self.stop_btn.pack(fill=tk.X, pady=(0, 8))
            
            # Botón de limpieza
            clean_btn = ttk.Button(
                parent,
                text="🧹 Limpiar Logs",
                command=self.clear_logs
            )
            clean_btn.pack(fill=tk.X, pady=(0, 8))
            
            # Información de estado
            self.status_label = ttk.Label(
                parent,
                text="Estado: Listo para procesar",
                font=("Arial", 10, "bold")
            )
            self.status_label.pack(pady=(8, 0))
            
        except Exception as e:
            self.show_error_dialog("Error creando panel de control", str(e))
    
    def _create_log_panel(self, parent):
        """Crea el panel de logs"""
        try:
            # Título del log
            log_title = ttk.Label(parent, text="📊 Logs del Sistema", font=("Arial", 10, "bold"))
            log_title.pack(anchor=tk.W, pady=(12, 4))
            
            # Área de logs
            self.log_text = scrolledtext.ScrolledText(
                parent,
                height=15,
                width=50,
                font=("Consolas", 9),
                bg="black",
                fg="white"
            )
            self.log_text.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            self.show_error_dialog("Error creando panel de logs", str(e))
    
    def _create_status_bar(self):
        """Crea la barra de estado"""
        try:
            self.status_bar = ttk.Label(
                self.root,
                text="Sistema de Órdenes de Producción - Listo",
                relief=tk.SUNKEN,
                anchor=tk.W
            )
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            
        except Exception as e:
            self.show_error_dialog("Error creando barra de estado", str(e))
    
    def start_log_processor(self):
        """Inicia el procesador de logs"""
        def process_logs():
            while not self.is_closing:
                try:
                    message = self.log_queue.get(timeout=0.1)
                    if message:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        log_entry = f"[{timestamp}] {message}\n"
                        
                        self.log_text.insert(tk.END, log_entry)
                        self.log_text.see(tk.END)
                        
                        # Limitar el tamaño del log
                        if self.log_text.index(tk.END).split('.')[0] > '1000':
                            self.log_text.delete('1.0', '100.0')
                            
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error procesando logs: {e}")
        
        log_thread = threading.Thread(target=process_logs, daemon=True)
        log_thread.start()
    
    def log_message(self, message):
        """Agrega un mensaje al log"""
        try:
            self.log_queue.put(message)
        except Exception as e:
            print(f"Error agregando mensaje al log: {e}")
    
    def start_production_processing(self):
        """Inicia el procesamiento de órdenes de producción"""
        try:
            if self.is_running:
                messagebox.showwarning("Sistema en ejecución", "El sistema ya está procesando órdenes de producción.")
                return
            
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Estado: Procesando órdenes de producción...")
            self.status_bar.config(text="Procesando órdenes de producción...")
            
            self.log_message("🏭 Iniciando procesamiento de órdenes de producción...")
            
            # Iniciar procesamiento en hilo separado
            processing_thread = threading.Thread(target=self._run_production_processing, daemon=True)
            processing_thread.start()
            
        except Exception as e:
            self.show_error_dialog("Error iniciando procesamiento", str(e))
            self.stop_system()
    
    def _run_production_processing(self):
        """Ejecuta el procesamiento de órdenes de producción"""
        try:
            self.log_message("🏭 Iniciando simulación de procesamiento...")
            
            # Simular procesamiento
            for i in range(5):
                self.log_message(f"🏭 Procesando archivo {i+1}/5...")
                time.sleep(1)
            
            self.log_message("✅ Procesamiento simulado completado")
            
        except Exception as e:
            self.log_message(f"❌ Error en procesamiento: {e}")
            self.log_message(f"Detalles: {traceback.format_exc()}")
        finally:
            # Restaurar estado
            self.root.after(0, self.stop_system)
    
    def stop_system(self):
        """Detiene el sistema"""
        try:
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Estado: Sistema detenido")
            self.status_bar.config(text="Sistema detenido")
            
            self.log_message("⏹️ Sistema detenido")
            
        except Exception as e:
            self.show_error_dialog("Error deteniendo sistema", str(e))
    
    def clear_logs(self):
        """Limpia los logs"""
        try:
            self.log_text.delete('1.0', tk.END)
            self.log_message("🧹 Logs limpiados")
        except Exception as e:
            self.show_error_dialog("Error limpiando logs", str(e))
    
    def show_configuration(self):
        """Muestra la configuración actual"""
        try:
            config_path = os.path.join(project_root, "rpa", "modules", "production_order", "production_order_config.yaml")
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()
                
                # Crear ventana de configuración
                config_window = tk.Toplevel(self.root)
                config_window.title("Configuración de Órdenes de Producción")
                config_window.geometry("600x400")
                
                text_widget = scrolledtext.ScrolledText(config_window, font=("Consolas", 10))
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                text_widget.insert('1.0', config_content)
                text_widget.config(state=tk.DISABLED)
                
            else:
                messagebox.showwarning("Configuración no encontrada", f"No se encontró el archivo de configuración:\n{config_path}")
                
        except Exception as e:
            self.show_error_dialog("Error mostrando configuración", str(e))
    
    def show_pending_files(self):
        """Muestra los archivos pendientes"""
        try:
            pending_dir = os.path.join(project_root, "data", "outputs_json", "production_order", "01_Pendiente")
            
            if os.path.exists(pending_dir):
                files = glob.glob(os.path.join(pending_dir, "*.json"))
                
                if files:
                    file_list = "\n".join([os.path.basename(f) for f in files])
                    messagebox.showinfo("Archivos Pendientes", f"Archivos pendientes de procesar:\n\n{file_list}")
                else:
                    messagebox.showinfo("Archivos Pendientes", "No hay archivos pendientes de procesar.")
            else:
                messagebox.showwarning("Directorio no encontrado", f"No se encontró el directorio:\n{pending_dir}")
                
        except Exception as e:
            self.show_error_dialog("Error mostrando archivos pendientes", str(e))
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.show_error_dialog("Error ejecutando aplicación", str(e))

if __name__ == "__main__":
    try:
        app = LauncherProduccionSimple()
        app.run()
    except Exception as e:
        print(f"Error fatal: {e}")
        print(traceback.format_exc())
        input("Presiona Enter para continuar...")
