#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Order Handler
Manejador de órdenes de producción para RPA
"""

import os
import json
import glob
import shutil
from datetime import datetime
import logging

class ProductionOrderHandler:
    def __init__(self):
        """Inicializa el handler de órdenes de producción"""
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.pending_dir = os.path.join(self.project_root, "data", "outputs_json", "production_order", "01_Pendiente")
        self.processing_dir = os.path.join(self.project_root, "data", "outputs_json", "production_order", "02_Procesando")
        self.completed_dir = os.path.join(self.project_root, "data", "outputs_json", "production_order", "03_Completado")
        self.error_dir = os.path.join(self.project_root, "data", "outputs_json", "production_order", "04_Error")
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def process_pending_orders(self):
        """Procesa las órdenes de producción pendientes"""
        try:
            self.logger.info("Iniciando procesamiento de órdenes de producción...")
            
            # Verificar que existe el directorio de pendientes
            if not os.path.exists(self.pending_dir):
                self.logger.warning(f"Directorio de pendientes no encontrado: {self.pending_dir}")
                return "No hay archivos pendientes para procesar"
            
            # Obtener archivos pendientes
            pending_files = glob.glob(os.path.join(self.pending_dir, "*.json"))
            
            if not pending_files:
                self.logger.info("No hay archivos pendientes para procesar")
                return "No hay archivos pendientes"
            
            self.logger.info(f"Encontrados {len(pending_files)} archivos pendientes")
            
            processed_count = 0
            error_count = 0
            
            for file_path in pending_files:
                try:
                    # Mover a procesando
                    filename = os.path.basename(file_path)
                    processing_path = os.path.join(self.processing_dir, filename)
                    
                    # Crear directorio si no existe
                    os.makedirs(self.processing_dir, exist_ok=True)
                    
                    # Mover archivo
                    shutil.move(file_path, processing_path)
                    
                    self.logger.info(f"Procesando archivo: {filename}")
                    
                    # Simular procesamiento
                    self._process_production_order(processing_path)
                    
                    # Mover a completado
                    completed_path = os.path.join(self.completed_dir, filename)
                    os.makedirs(self.completed_dir, exist_ok=True)
                    shutil.move(processing_path, completed_path)
                    
                    self.logger.info(f"Archivo procesado exitosamente: {filename}")
                    processed_count += 1
                    
                except Exception as e:
                    self.logger.error(f"Error procesando archivo {filename}: {e}")
                    
                    # Mover a error
                    error_path = os.path.join(self.error_dir, filename)
                    os.makedirs(self.error_dir, exist_ok=True)
                    
                    if os.path.exists(processing_path):
                        shutil.move(processing_path, error_path)
                    elif os.path.exists(file_path):
                        shutil.move(file_path, error_path)
                    
                    error_count += 1
            
            result = f"Procesamiento completado: {processed_count} exitosos, {error_count} errores"
            self.logger.info(result)
            return result
            
        except Exception as e:
            error_msg = f"Error en procesamiento: {e}"
            self.logger.error(error_msg)
            return error_msg
    
    def _process_production_order(self, file_path):
        """Procesa una orden de producción específica"""
        try:
            # Leer archivo JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                order_data = json.load(f)
            
            self.logger.info(f"Procesando orden de producción: {order_data.get('order_number', 'N/A')}")
            
            # Simular procesamiento de SAP
            # Aquí iría la lógica real de navegación en SAP para producción
            
            # Agregar timestamp de procesamiento
            order_data['processed_at'] = datetime.now().isoformat()
            order_data['status'] = 'completed'
            
            # Guardar archivo actualizado
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(order_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Orden de producción procesada exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error procesando orden de producción: {e}")
            raise
    
    def get_pending_count(self):
        """Obtiene el número de archivos pendientes"""
        try:
            if not os.path.exists(self.pending_dir):
                return 0
            
            pending_files = glob.glob(os.path.join(self.pending_dir, "*.json"))
            return len(pending_files)
            
        except Exception as e:
            self.logger.error(f"Error obteniendo conteo de pendientes: {e}")
            return 0
    
    def get_status_summary(self):
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
    
    def _count_files(self, directory):
        """Cuenta archivos en un directorio"""
        try:
            if not os.path.exists(directory):
                return 0
            
            files = glob.glob(os.path.join(directory, "*.json"))
            return len(files)
            
        except Exception:
            return 0
