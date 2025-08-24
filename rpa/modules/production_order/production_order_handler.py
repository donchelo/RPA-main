#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Order Handler
Manejador de órdenes de producción para RPA con funcionalidad completa de navegación SAP
"""

import os
import sys
import time
from typing import Dict, Optional

# Agregar el directorio del módulo base al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_rpa_handler import BaseRPAHandler
from rpa.simple_logger import rpa_logger
from rpa.config_manager import get_delay
import pyautogui

class ProductionOrderHandler(BaseRPAHandler):
    def __init__(self):
        """Inicializa el handler de órdenes de producción con funcionalidad completa"""
        super().__init__("production_order")
        
        # Cargar configuración específica del módulo
        self.config_file = os.path.join(self.project_root, "rpa", "modules", "production_order", "production_order_config.yaml")
        
        rpa_logger.log_action("ProductionOrderHandler inicializado con funcionalidad completa", "Listo para procesar órdenes de producción")
    
    # Hereda process_pending_orders de BaseRPAHandler
    
    def _navigate_to_module(self) -> bool:
        """Navega al módulo de órdenes de producción en SAP"""
        try:
            rpa_logger.log_action("Navegando al módulo de órdenes de producción", "Alt+M → P")
            
            # PASO 1: Abrir menú de módulos (Alt+M)
            pyautogui.hotkey('alt', 'm')
            time.sleep(get_delay('navigation_wait') or 2.0)
            
            # PASO 2: Ir a Producción (P)
            pyautogui.press('p')
            time.sleep(get_delay('form_load_delay') or 3.0)
            
            # Verificar que el módulo de producción está abierto usando visión computacional
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "produccion_form.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template is not None:
                    coordinates = self.template_matcher.find_template_with_timeout(template, timeout=10.0)
                    if coordinates:
                        rpa_logger.log_action("Módulo de producción detectado correctamente", f"Coordenadas: {coordinates}")
                        return True
            
            # Si no encontramos el template específico, buscar el menú de producción
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "produccion_menu.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template is not None:
                    coordinates = self.template_matcher.find_template_with_timeout(template, timeout=10.0)
                    if coordinates:
                        rpa_logger.log_action("Menú de producción detectado correctamente", f"Coordenadas: {coordinates}")
                        # Ahora navegar a órdenes de fabricación
                        return self._navigate_to_production_orders()
            
            rpa_logger.log_error("No se pudo verificar que el módulo de producción esté abierto")
            return False
            
        except Exception as e:
            rpa_logger.log_error(f"Error navegando al módulo de producción: {str(e)}")
            return False
    
    def _navigate_to_production_orders(self) -> bool:
        """Navega específicamente a órdenes de fabricación"""
        try:
            rpa_logger.log_action("Navegando a órdenes de fabricación")
            
            # Buscar y hacer clic en el botón de órdenes de fabricación
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "orden_fabricacion_button.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template_with_timeout(template, timeout=10.0)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(get_delay('form_load_delay') or 3.0)
                        
                        # Verificar que se abrió la forma de órdenes de fabricación
                        return self._verify_production_form_opened()
            
            return False
            
        except Exception as e:
            rpa_logger.log_error(f"Error navegando a órdenes de fabricación: {str(e)}")
            return False
    
    def _verify_production_form_opened(self) -> bool:
        """Verifica que la forma de órdenes de fabricación esté abierta"""
        try:
            # Buscar elementos específicos de la forma de producción
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "articulo_field.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template_with_timeout(template, timeout=5.0)
                    if coordinates:
                        rpa_logger.log_action("Forma de órdenes de fabricación verificada correctamente")
                        return True
            
            rpa_logger.log_error("No se pudo verificar que la forma de órdenes de fabricación esté abierta")
            return False
            
        except Exception as e:
            rpa_logger.log_error(f"Error verificando forma de producción: {str(e)}")
            return False
    
    def _process_module_data(self, order_data: Dict) -> bool:
        """Procesa los datos específicos de la orden de producción en SAP"""
        try:
            rpa_logger.log_action("Procesando datos de orden de producción", f"Artículo: {order_data.get('articulo', 'N/A')}")
            
            # PASO 1: Ingresar artículo
            if not self._fill_articulo_field(order_data.get('articulo', '')):
                return False
            
            # PASO 2: Ingresar pedido interno
            if not self._fill_pedido_interno_field(order_data.get('pedido_interno', '')):
                return False
            
            # PASO 3: Ingresar cantidad
            if not self._fill_cantidad_field(order_data.get('cantidad', '')):
                return False
            
            # PASO 4: Ingresar fecha de finalización
            if not self._fill_fecha_finalizacion_field(order_data.get('fecha_finalizacion', '')):
                return False
            
            # PASO 5: Crear la orden de fabricación
            if not self._create_production_order():
                return False
            
            rpa_logger.log_action("Datos de orden de producción procesados exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error procesando datos de orden de producción: {str(e)}")
            return False
    
    def _fill_articulo_field(self, articulo: str) -> bool:
        """Llena el campo de artículo"""
        try:
            if not articulo:
                rpa_logger.log_error("Artículo no proporcionado")
                return False
            
            rpa_logger.log_action(f"Ingresando artículo: {articulo}")
            
            # Buscar el campo artículo usando visión computacional
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "articulo_field.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Ingresar artículo
            pyautogui.write(articulo)
            
            # Navegar al siguiente campo (configurado en YAML)
            for _ in range(2):  # articulo_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"Artículo ingresado correctamente: {articulo}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando artículo: {str(e)}")
            return False
    
    def _fill_pedido_interno_field(self, pedido_interno: str) -> bool:
        """Llena el campo de pedido interno"""
        try:
            if not pedido_interno:
                rpa_logger.log_error("Pedido interno no proporcionado")
                return False
            
            rpa_logger.log_action(f"Ingresando pedido interno: {pedido_interno}")
            
            # Buscar campo de pedido interno
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "pedido_interno_field.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Ingresar pedido interno
            pyautogui.write(pedido_interno)
            
            # Navegar al siguiente campo
            for _ in range(3):  # pedido_interno_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"Pedido interno ingresado correctamente: {pedido_interno}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando pedido interno: {str(e)}")
            return False
    
    def _fill_cantidad_field(self, cantidad: str) -> bool:
        """Llena el campo de cantidad"""
        try:
            if not cantidad:
                rpa_logger.log_error("Cantidad no proporcionada")
                return False
            
            rpa_logger.log_action(f"Ingresando cantidad: {cantidad}")
            
            # Buscar campo de cantidad
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "cantidad_field.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Limpiar campo y ingresar cantidad
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(str(cantidad))
            
            # Navegar al siguiente campo
            for _ in range(2):  # cantidad_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"Cantidad ingresada correctamente: {cantidad}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando cantidad: {str(e)}")
            return False
    
    def _fill_fecha_finalizacion_field(self, fecha_finalizacion: str) -> bool:
        """Llena el campo de fecha de finalización"""
        try:
            if not fecha_finalizacion:
                rpa_logger.log_error("Fecha de finalización no proporcionada")
                return False
            
            rpa_logger.log_action(f"Ingresando fecha de finalización: {fecha_finalizacion}")
            
            # Buscar campo de fecha de finalización
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "fecha_finalizacion_field.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Limpiar campo y ingresar fecha
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(fecha_finalizacion)
            
            # Navegar al siguiente campo
            for _ in range(3):  # fecha_finalizacion_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"Fecha de finalización ingresada correctamente: {fecha_finalizacion}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando fecha de finalización: {str(e)}")
            return False
    
    def _create_production_order(self) -> bool:
        """Crea y graba la orden de fabricación"""
        try:
            rpa_logger.log_action("Creando orden de fabricación")
            
            # Buscar y hacer clic en el botón crear
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "production", "crear_button.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(get_delay('long') or 2.0)
            else:
                # Si no hay botón específico, usar Ctrl+S
                pyautogui.hotkey('ctrl', 's')
                time.sleep(get_delay('long') or 2.0)
            
            rpa_logger.log_action("Orden de fabricación creada exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error creando orden de fabricación: {str(e)}")
            return False
    
    # Hereda get_pending_count, get_status_summary y _count_files de BaseRPAHandler