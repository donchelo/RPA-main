#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base RPA Handler
Clase base para todos los handlers RPA con funcionalidades comunes
"""

import os
import json
import glob
import shutil
import time
from datetime import datetime
from typing import Optional, Dict, Any
import logging
from abc import ABC, abstractmethod

# Importar componentes del sistema RPA
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rpa.state_machine import StateMachine, RPAState, RPAEvent
from rpa.rpa_state_handlers import RPAStateHandlers
from rpa.simple_logger import rpa_logger
from rpa.vision.main import Vision
from rpa.vision.template_matcher import TemplateMatcher
from rpa.config_manager import get_confidence, get_delay
from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader


class BaseRPAHandler(ABC):
    """Clase base para handlers RPA con funcionalidades comunes"""
    
    def __init__(self, module_name: str):
        """
        Inicializa el handler base
        
        Args:
            module_name: Nombre del módulo (sales_order, production_order)
        """
        self.module_name = module_name
        # Calcular project_root correctamente
        # Archivo actual: .../RPA-main/rpa/modules/base_rpa_handler.py
        # Project root: .../RPA-main/
        current_file = os.path.abspath(__file__)
        modules_dir = os.path.dirname(current_file)  # .../rpa/modules/
        rpa_dir = os.path.dirname(modules_dir)       # .../rpa/
        self.project_root = os.path.dirname(rpa_dir) # .../RPA-main/
        
        # Configurar directorios
        self.base_dir = os.path.join(self.project_root, "data", "outputs_json", module_name)
        self.pending_dir = os.path.join(self.base_dir, "01_Pendiente")
        self.processing_dir = os.path.join(self.base_dir, "02_Procesando")
        self.completed_dir = os.path.join(self.base_dir, "03_Completado")
        self.error_dir = os.path.join(self.base_dir, "04_Error")
        
        # Crear directorios si no existen
        for directory in [self.pending_dir, self.processing_dir, self.completed_dir, self.error_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Inicializar componentes del sistema RPA
        self.vision = Vision()
        self.template_matcher = TemplateMatcher()
        self.state_machine = StateMachine()
        
        # Configurar manejadores de estado
        self._setup_state_handlers()
        
        # Inicializar Google Drive uploader
        try:
            self.google_drive = GoogleDriveOAuthUploader()
        except Exception as e:
            rpa_logger.log_error(f"Error inicializando Google Drive uploader: {str(e)}")
            self.google_drive = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"{__name__}.{module_name}")
        
        rpa_logger.log_action(f"Handler {module_name} inicializado", "Sistema base configurado")
    
    def _setup_state_handlers(self):
        """Configura los manejadores de estado de la máquina"""
        # Crear instancia de RPA simulada para los handlers
        from rpa.rpa_with_state_machine import RPAWithStateMachine
        rpa_instance = RPAWithStateMachine()
        
        handlers = RPAStateHandlers(rpa_instance)
        
        # Registrar handlers para estados básicos
        self.state_machine.register_state_handler(RPAState.CONNECTING_REMOTE_DESKTOP, handlers.handle_connecting_remote_desktop)
        self.state_machine.register_state_handler(RPAState.OPENING_SAP, handlers.handle_opening_sap)
        
        # Los handlers específicos se registrarán en las clases derivadas
    
    def process_pending_orders(self):
        """Procesa las órdenes pendientes del módulo"""
        try:
            rpa_logger.log_action(f"Iniciando procesamiento de {self.module_name}...", "Verificando archivos pendientes")
            
            # Verificar directorio de pendientes
            if not os.path.exists(self.pending_dir):
                rpa_logger.log_warning(f"Directorio de pendientes no encontrado: {self.pending_dir}")
                return "No hay archivos pendientes para procesar"
            
            # Obtener archivos pendientes
            pending_files = glob.glob(os.path.join(self.pending_dir, "*.json"))
            
            if not pending_files:
                rpa_logger.log_action("No hay archivos pendientes para procesar", "Cola vacía")
                return "No hay archivos pendientes"
            
            rpa_logger.log_action(f"Encontrados {len(pending_files)} archivos pendientes", "Iniciando procesamiento")
            
            processed_count = 0
            error_count = 0
            
            for file_path in pending_files:
                try:
                    # Procesar cada archivo individualmente
                    success = self.process_single_file(file_path)
                    
                    if success:
                        processed_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    rpa_logger.log_error(f"Error procesando archivo {os.path.basename(file_path)}: {str(e)}")
                    error_count += 1
            
            result = f"Procesamiento completado: {processed_count} exitosos, {error_count} errores"
            rpa_logger.log_action(result, f"Módulo: {self.module_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error en procesamiento de {self.module_name}: {str(e)}"
            rpa_logger.log_error(error_msg)
            return error_msg
    
    def process_single_file(self, file_path: str) -> bool:
        """
        Procesa un archivo individual usando la máquina de estados
        
        Args:
            file_path: Ruta completa al archivo JSON
            
        Returns:
            True si el procesamiento fue exitoso, False en caso contrario
        """
        filename = os.path.basename(file_path)
        
        try:
            # Leer datos del archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                order_data = json.load(f)
            
            rpa_logger.log_action(f"Procesando archivo: {filename}", f"Módulo: {self.module_name}")
            
            # Mover a directorio de procesando
            processing_path = os.path.join(self.processing_dir, filename)
            shutil.move(file_path, processing_path)
            
            # Resetear máquina de estados
            self.state_machine.reset()
            
            # Iniciar procesamiento con la máquina de estados
            self.state_machine.start_processing(filename, order_data)
            
            # Ejecutar el flujo de procesamiento
            success = self._execute_rpa_workflow(processing_path, order_data)
            
            if success:
                # Mover a completado
                completed_path = os.path.join(self.completed_dir, filename)
                shutil.move(processing_path, completed_path)
                rpa_logger.log_action(f"Archivo procesado exitosamente: {filename}")
                
                # Limpiar checkpoint
                self.state_machine.cleanup_checkpoint()
                
                return True
            else:
                # Mover a error
                error_path = os.path.join(self.error_dir, filename)
                shutil.move(processing_path, error_path)
                rpa_logger.log_error(f"Error procesando archivo: {filename}")
                return False
                
        except Exception as e:
            rpa_logger.log_error(f"Error procesando {filename}: {str(e)}")
            
            # Mover a error si aún está en procesando
            if os.path.exists(os.path.join(self.processing_dir, filename)):
                error_path = os.path.join(self.error_dir, filename)
                shutil.move(os.path.join(self.processing_dir, filename), error_path)
            
            return False
    
    def _execute_rpa_workflow(self, file_path: str, order_data: Dict) -> bool:
        """
        Ejecuta el workflow completo de RPA usando la máquina de estados
        
        Args:
            file_path: Ruta al archivo en procesamiento
            order_data: Datos de la orden
            
        Returns:
            True si el workflow fue exitoso
        """
        try:
            # PASO 1: Conectar al escritorio remoto
            event = self.state_machine.execute_current_state(file_path=file_path, order_data=order_data)
            if not self.state_machine.trigger_event(event):
                return False
            
            # PASO 2: Abrir/detectar SAP
            if self.state_machine.current_state == RPAState.OPENING_SAP:
                event = self.state_machine.execute_current_state(file_path=file_path, order_data=order_data)
                if not self.state_machine.trigger_event(event):
                    return False
            
            # PASO 3: Navegar al módulo específico (implementado en clases derivadas)
            if hasattr(self, '_navigate_to_module'):
                if not self._navigate_to_module():
                    return False
            
            # PASO 4: Procesar los datos específicos del módulo
            if not self._process_module_data(order_data):
                return False
            
            # PASO 5: Tomar screenshot y finalizar
            if not self._finalize_processing(file_path):
                return False
            
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error en workflow RPA: {str(e)}")
            return False
    
    @abstractmethod
    def _process_module_data(self, order_data: Dict) -> bool:
        """
        Procesa los datos específicos del módulo (debe implementarse en clases derivadas)
        
        Args:
            order_data: Datos de la orden
            
        Returns:
            True si el procesamiento fue exitoso
        """
        pass
    
    def _finalize_processing(self, file_path: str) -> bool:
        """Finaliza el procesamiento tomando screenshot y subiendo a Google Drive"""
        try:
            # Tomar screenshot
            screenshot_path = self._take_screenshot(file_path)
            
            if screenshot_path and self.google_drive:
                # Subir a Google Drive
                try:
                    self.google_drive.upload_file(screenshot_path)
                    rpa_logger.log_action("Archivo subido a Google Drive exitosamente")
                except Exception as e:
                    rpa_logger.log_error(f"Error subiendo a Google Drive: {str(e)}")
            
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error en finalización: {str(e)}")
            return False
    
    def _take_screenshot(self, file_path: str) -> Optional[str]:
        """Toma screenshot del resultado del procesamiento"""
        try:
            filename = os.path.basename(file_path).replace('.json', '.png')
            screenshot_path = os.path.join(os.path.dirname(file_path), filename)
            
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            rpa_logger.log_action(f"Screenshot guardado: {filename}")
            return screenshot_path
            
        except Exception as e:
            rpa_logger.log_error(f"Error tomando screenshot: {str(e)}")
            return None
    
    def connect_to_remote_desktop(self) -> bool:
        """Conecta al escritorio remoto usando el sistema de visión"""
        try:
            rpa_logger.log_action("Conectando al escritorio remoto...", "Iniciando conexión")
            
            # Usar el método del sistema de visión existente
            from rpa.rpa_with_state_machine import RPAWithStateMachine
            rpa_instance = RPAWithStateMachine()
            
            return rpa_instance.get_remote_desktop()
            
        except Exception as e:
            rpa_logger.log_error(f"Error conectando al escritorio remoto: {str(e)}")
            return False
    
    def detect_sap_desktop(self) -> bool:
        """Detecta si el escritorio SAP está visible"""
        try:
            return self.vision.is_sap_desktop_visible()
        except Exception as e:
            rpa_logger.log_error(f"Error detectando escritorio SAP: {str(e)}")
            return False
    
    def open_sap(self) -> bool:
        """Abre SAP Business One"""
        try:
            from rpa.rpa_with_state_machine import RPAWithStateMachine
            rpa_instance = RPAWithStateMachine()
            
            return rpa_instance.open_sap()
            
        except Exception as e:
            rpa_logger.log_error(f"Error abriendo SAP: {str(e)}")
            return False
    
    def get_pending_count(self) -> int:
        """Obtiene el número de archivos pendientes"""
        try:
            if not os.path.exists(self.pending_dir):
                return 0
            
            pending_files = glob.glob(os.path.join(self.pending_dir, "*.json"))
            return len(pending_files)
            
        except Exception as e:
            self.logger.error(f"Error obteniendo conteo de pendientes: {e}")
            return 0
    
    def get_status_summary(self) -> Dict[str, int]:
        """Obtiene un resumen del estado de procesamiento"""
        try:
            summary = {
                'pending': self._count_files(self.pending_dir),
                'processing': self._count_files(self.processing_dir),
                'completed': self._count_files(self.completed_dir),
                'error': self._count_files(self.error_dir)
            }
            return summary
            
        except Exception as e:
            self.logger.error(f"Error obteniendo resumen: {e}")
            return {'pending': 0, 'processing': 0, 'completed': 0, 'error': 0}
    
    def _count_files(self, directory: str) -> int:
        """Cuenta archivos JSON en un directorio"""
        try:
            if not os.path.exists(directory):
                return 0
            
            files = glob.glob(os.path.join(directory, "*.json"))
            return len(files)
            
        except Exception:
            return 0