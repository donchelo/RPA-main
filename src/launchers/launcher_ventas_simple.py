#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher Simple para Órdenes de Venta RPA TAMAPRINT v3.0
Versión sin emojis para evitar problemas de codificación en Windows
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import sys
import json
import glob
import shutil
from datetime import datetime
import threading
import time

# Agregar el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Suprimir warnings de OpenCV
os.environ['OPENCV_LOG_LEVEL'] = 'SILENT'

class LauncherVentasSimple:
    def __init__(self):
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("RPA TAMAPRINT v3.0 - Launcher Ventas")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables de estado
        self.is_running = False
        self.processing_thread = None
        self.stop_processing = False
        self.current_file = None
        self.rpa_handler = None
        
        # Configurar directorios por defecto
        self.base_dir = os.path.join(project_root, "data", "outputs_json", "sales_order")
        self.pending_dir = os.path.join(self.base_dir, "01_Pendiente")
        self.processing_dir = os.path.join(self.base_dir, "02_Procesando")
        self.completed_dir = os.path.join(self.base_dir, "03_Completado")
        self.error_dir = os.path.join(self.base_dir, "04_Error")
        
        # Estadísticas
        self.stats = {
            'processed': 0,
            'errors': 0,
            'start_time': None
        }
        
        # Crear interfaz PRIMERO
        self.create_interface()
        
        # DESPUÉS inicializar el handler RPA
        self._initialize_rpa_handler()
        
        # Log inicial
        self.log_message("Launcher de Ventas iniciado correctamente")
        self.log_message(f"Directorio de pendientes: {self.pending_dir}")
        self.update_status()
    
    def create_interface(self):
        """Crea la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="RPA TAMAPRINT v3.0 - Procesamiento de Ordenes de Venta",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de control
        control_frame = ttk.LabelFrame(main_frame, text="Control de Procesamiento", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X)
        
        self.start_stop_btn = ttk.Button(
            buttons_frame,
            text="INICIAR Procesamiento Automatico",
            command=self.toggle_processing
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.refresh_btn = ttk.Button(
            buttons_frame,
            text="Actualizar Estado",
            command=self.update_status
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_logs_btn = ttk.Button(
            buttons_frame,
            text="Limpiar Logs",
            command=self.clear_logs
        )
        self.clear_logs_btn.pack(side=tk.LEFT)
        
        # Estado del procesamiento
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Estado: Inactivo", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.LEFT)
        
        self.current_file_label = ttk.Label(status_frame, text="Archivo actual: Ninguno")
        self.current_file_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Frame de estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadisticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Contadores
        counters_frame = ttk.Frame(stats_frame)
        counters_frame.pack(fill=tk.X)
        
        self.pending_count_label = ttk.Label(counters_frame, text="Pendientes: 0")
        self.pending_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.processing_count_label = ttk.Label(counters_frame, text="Procesando: 0")
        self.processing_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.completed_count_label = ttk.Label(counters_frame, text="Completados: 0")
        self.completed_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.error_count_label = ttk.Label(counters_frame, text="Errores: 0")
        self.error_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.processed_count_label = ttk.Label(counters_frame, text="Procesados en sesion: 0")
        self.processed_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Frame de logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs del Sistema", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def _initialize_rpa_handler(self):
        """Inicializa el handler RPA completo"""
        try:
            from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
            self.rpa_handler = SalesOrderHandler()
            
            # Actualizar directorios con los del handler
            self.base_dir = self.rpa_handler.base_dir
            self.pending_dir = self.rpa_handler.pending_dir
            self.processing_dir = self.rpa_handler.processing_dir
            self.completed_dir = self.rpa_handler.completed_dir
            self.error_dir = self.rpa_handler.error_dir
            
            self.log_message("OK - Handler RPA de ventas inicializado correctamente")
            self.log_message("AVISO - Sistema completo con navegacion SAP disponible")
        except Exception as e:
            self.rpa_handler = None
            self.log_message(f"ERROR - Error inicializando handler RPA: {str(e)}")
            self.log_message("AVISO - Se continuara con funcionalidad limitada")
    
    def toggle_processing(self):
        """Inicia o detiene el procesamiento automático"""
        if not self.is_running:
            self.start_processing()
        else:
            self.stop_processing_manual()
    
    def start_processing(self):
        """Inicia el procesamiento automático"""
        self.is_running = True
        self.stop_processing = False
        self.stats['start_time'] = datetime.now()
        self.stats['processed'] = 0
        self.stats['errors'] = 0
        
        self.start_stop_btn.config(text="DETENER Procesamiento")
        self.status_label.config(text="Estado: Procesando automaticamente")
        
        self.log_message("Iniciando procesamiento automatico de ordenes de venta")
        self.log_message(f"Monitoreando directorio: {self.pending_dir}")
        
        # Iniciar hilo de procesamiento
        self.processing_thread = threading.Thread(target=self.process_queue_automatically, daemon=True)
        self.processing_thread.start()
    
    def stop_processing_manual(self):
        """Detiene el procesamiento automático"""
        self.is_running = False
        self.stop_processing = True
        
        self.start_stop_btn.config(text="INICIAR Procesamiento Automatico")
        self.status_label.config(text="Estado: Detenido")
        self.current_file_label.config(text="Archivo actual: Ninguno")
        
        if self.stats['start_time']:
            duration = datetime.now() - self.stats['start_time']
            self.log_message(f"Procesamiento detenido manualmente")
            self.log_message(f"Sesion completada: {self.stats['processed']} procesados, {self.stats['errors']} errores")
            self.log_message(f"Duracion: {duration}")
    
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
                    self.current_file = filename
                    self.current_file_label.config(text=f"Archivo actual: {filename}")
                    
                    # Mover a procesando
                    processing_path = os.path.join(self.processing_dir, filename)
                    shutil.move(file_path, processing_path)
                    self.log_message(f"   Movido a procesando: {filename}")
                    
                    # Procesar el archivo
                    success = self.process_file_with_rpa(processing_path)
                    
                    if success:
                        # Mover a completado
                        completed_path = os.path.join(self.completed_dir, filename)
                        shutil.move(processing_path, completed_path)
                        self.log_message(f"   Procesado exitosamente: {filename}")
                        self.stats['processed'] += 1
                    else:
                        # Mover a error
                        error_path = os.path.join(self.error_dir, filename)
                        shutil.move(processing_path, error_path)
                        self.log_message(f"   Error procesando: {filename}")
                        self.stats['errors'] += 1
                    
                    self.current_file = None
                    self.current_file_label.config(text="Archivo actual: Ninguno")
                    self.update_status()
                    
                    # Pausa entre archivos
                    time.sleep(2)
                else:
                    # No hay archivos pendientes
                    if self.is_running:
                        self.log_message("No hay archivos pendientes, esperando...")
                    time.sleep(10)  # Esperar 10 segundos antes de verificar nuevamente
                
            except Exception as e:
                self.log_message(f"Error en procesamiento automatico: {str(e)}")
                time.sleep(15)  # Esperar más tiempo en caso de error
    
    def process_file_with_rpa(self, file_path):
        """Procesa un archivo usando el RPA completo con navegación SAP"""
        try:
            # Verificar que el handler RPA esté disponible
            if not self.rpa_handler:
                self.log_message(f"   Handler RPA no disponible")
                return False
            
            # Leer el archivo JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.log_message(f"   Datos cargados:")
            self.log_message(f"      - Orden: {data.get('orden_compra', 'N/A')}")
            self.log_message(f"      - Comprador: {data.get('comprador', {}).get('nombre', 'N/A')}")
            self.log_message(f"      - NIT: {data.get('comprador', {}).get('nit', 'N/A')}")
            self.log_message(f"      - Items: {len(data.get('items', []))}")
            
            # Procesar usando el RPA handler completo
            self.log_message(f"   Iniciando procesamiento RPA completo...")
            self.log_message(f"   Conectando al escritorio remoto...")
            self.log_message(f"   Detectando escritorio SAP...")
            self.log_message(f"   Navegando al modulo de ordenes de venta...")
            self.log_message(f"   Procesando datos en SAP...")
            
            # Usar el handler real para procesar el archivo
            success = self.rpa_handler.process_single_file(file_path)
            
            if success:
                self.log_message(f"   Procesamiento RPA completado exitosamente")
                self.log_message(f"   Screenshot capturado")
                self.log_message(f"   Archivo subido a Google Drive")
            else:
                self.log_message(f"   Error en procesamiento RPA")
            
            return success
            
        except json.JSONDecodeError as e:
            self.log_message(f"   Error JSON en archivo: {str(e)}")
            return False
        except Exception as e:
            self.log_message(f"   Error procesando archivo: {str(e)}")
            return False
    
    def update_status(self):
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
            self.processed_count_label.config(text=f"Procesados en sesion: {self.stats['processed']}")
            
        except Exception as e:
            self.log_message(f"Error actualizando estado: {str(e)}")
    
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
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        print("Iniciando Launcher de Ventas...")
        app = LauncherVentasSimple()
        print("Launcher creado exitosamente")
        app.run()
        print("Launcher cerrado correctamente")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()