#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sales Order Handler
Manejador de órdenes de venta para RPA con funcionalidad completa de navegación SAP
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

class SalesOrderHandler(BaseRPAHandler):
    def __init__(self):
        """Inicializa el handler de órdenes de venta con funcionalidad completa"""
        super().__init__("sales_order")
        
        # Cargar configuración específica del módulo
        self.config_file = os.path.join(self.project_root, "rpa", "modules", "sales_order", "sales_order_config.yaml")
        
        rpa_logger.log_action("SalesOrderHandler inicializado con funcionalidad completa", "Listo para procesar órdenes de venta")
    
    # Hereda process_pending_orders de BaseRPAHandler
    
    def _navigate_to_module(self) -> bool:
        """Navega al módulo de órdenes de venta en SAP"""
        try:
            rpa_logger.log_action("Navegando al módulo de órdenes de venta", "Alt+M → V → Buscar Órdenes de Venta")
            
            # PASO 1: Abrir menú de módulos (Alt+M)
            rpa_logger.log_action("Presionando Alt+M para abrir menú de módulos")
            pyautogui.hotkey('alt', 'm')
            time.sleep(get_delay('navigation_wait') or 2.0)
            
            # PASO 2: Ir a Ventas (V)
            rpa_logger.log_action("Presionando V para ir a módulo de Ventas")
            pyautogui.press('v')
            time.sleep(get_delay('navigation_wait') or 2.0)
            
            # PASO 3: Buscar y hacer clic en "Órdenes de Venta" usando visión computacional
            rpa_logger.log_action("Buscando opción de Órdenes de Venta en el menú")
            
            # Buscar imagen de órdenes de venta en el menú
            ventas_menu_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "sap_ventas_order_menu.png")
            if os.path.exists(ventas_menu_path):
                template = self.template_matcher.load_template_image(ventas_menu_path)
                if template is not None:
                    coordinates = self.template_matcher.find_template_with_timeout(template, timeout=10.0)
                    if coordinates:
                        rpa_logger.log_action(f"Órdenes de Venta encontrada, haciendo clic", f"Coordenadas: {coordinates}")
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(get_delay('form_load_delay') or 3.0)
                        
                        # Verificar que se abrió la forma de órdenes de venta
                        return self._verify_sales_form_opened()
                    else:
                        rpa_logger.log_error("No se encontró la opción de Órdenes de Venta en el menú")
                else:
                    rpa_logger.log_error("No se pudo cargar el template de menú de órdenes de venta")
            
            # Si no encuentra la imagen, intentar con la tecla O como fallback
            rpa_logger.log_action("Fallback: Presionando O para órdenes de venta")
            pyautogui.press('o')
            time.sleep(get_delay('form_load_delay') or 3.0)
            
            return self._verify_sales_form_opened()
            
        except Exception as e:
            rpa_logger.log_error(f"Error navegando al módulo de ventas: {str(e)}")
            return False
    
    def _verify_sales_form_opened(self) -> bool:
        """Verifica que la forma de órdenes de venta esté abierta"""
        try:
            # Verificar que la forma de órdenes de venta está abierta usando visión computacional
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "sap_orden_de_ventas_template.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template is not None:
                    coordinates = self.template_matcher.find_template_with_timeout(template, timeout=10.0)
                    if coordinates:
                        rpa_logger.log_action("Forma de órdenes de venta detectada correctamente", f"Coordenadas: {coordinates}")
                        return True
                    else:
                        rpa_logger.log_error("Template de órdenes de venta no encontrado en pantalla")
                else:
                    rpa_logger.log_error("No se pudo cargar el template de órdenes de venta")
            else:
                rpa_logger.log_error(f"Archivo template no existe: {template_path}")
            
            rpa_logger.log_error("No se pudo verificar que la forma de órdenes de venta esté abierta")
            return False
            
        except Exception as e:
            rpa_logger.log_error(f"Error verificando forma de órdenes de venta: {str(e)}")
            return False
    
    def _process_module_data(self, order_data: Dict) -> bool:
        """Procesa los datos específicos de la orden de venta en SAP"""
        try:
            rpa_logger.log_action("Procesando datos de orden de venta", f"Orden: {order_data.get('orden_compra', 'N/A')}")
            
            # PASO 1: Ingresar NIT del comprador
            if not self._fill_nit_field(order_data.get('comprador', {}).get('nit', '')):
                return False
            
            # PASO 2: Ingresar número de orden de compra
            if not self._fill_order_field(order_data.get('orden_compra', '')):
                return False
            
            # PASO 3: Ingresar fecha de entrega
            if not self._fill_date_field(order_data.get('fecha_entrega', '')):
                return False
            
            # PASO 4: Procesar items de la orden
            if not self._process_order_items(order_data.get('items', [])):
                return False
            
            # PASO 5: Finalizar la orden
            if not self._finalize_order():
                return False
            
            rpa_logger.log_action("Datos de orden de venta procesados exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error procesando datos de orden de venta: {str(e)}")
            return False
    
    def _fill_nit_field(self, nit: str) -> bool:
        """Llena el campo NIT del comprador"""
        try:
            if not nit:
                rpa_logger.log_error("NIT no proporcionado")
                return False
            
            rpa_logger.log_action(f"Ingresando NIT: {nit}")
            
            # Buscar el campo NIT usando visión computacional
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "client_field.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Ingresar NIT
            pyautogui.write(nit)
            
            # Navegar al siguiente campo (configurado en YAML)
            for _ in range(3):  # nit_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"NIT ingresado correctamente: {nit}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando NIT: {str(e)}")
            return False
    
    def _fill_order_field(self, order_number: str) -> bool:
        """Llena el campo de número de orden de compra"""
        try:
            if not order_number:
                rpa_logger.log_error("Número de orden no proporcionado")
                return False
            
            rpa_logger.log_action(f"Ingresando orden de compra: {order_number}")
            
            # Buscar campo de orden de compra
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "orden_compra.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Ingresar número de orden
            pyautogui.write(order_number)
            
            # Navegar al siguiente campo
            for _ in range(4):  # orden_compra_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"Orden de compra ingresada correctamente: {order_number}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando orden de compra: {str(e)}")
            return False
    
    def _fill_date_field(self, delivery_date: str) -> bool:
        """Llena el campo de fecha de entrega"""
        try:
            if not delivery_date:
                rpa_logger.log_error("Fecha de entrega no proporcionada")
                return False
            
            rpa_logger.log_action(f"Ingresando fecha de entrega: {delivery_date}")
            
            # Buscar campo de fecha
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "fecha_entrega.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            # Limpiar campo y ingresar fecha
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(delivery_date)
            
            # Navegar al siguiente campo
            for _ in range(4):  # fecha_entrega_tabs del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            rpa_logger.log_action(f"Fecha de entrega ingresada correctamente: {delivery_date}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ingresando fecha de entrega: {str(e)}")
            return False
    
    def _process_order_items(self, items: list) -> bool:
        """Procesa todos los items de la orden"""
        try:
            if not items:
                rpa_logger.log_error("No hay items para procesar")
                return False
            
            rpa_logger.log_action(f"Procesando {len(items)} items de la orden")
            
            # Buscar el primer artículo
            template_path = os.path.join(self.project_root, "rpa", "vision", "reference_images", "primer_articulo.png")
            if os.path.exists(template_path):
                template = self.template_matcher.load_template_image(template_path)
                if template:
                    coordinates = self.template_matcher.find_template(template)
                    if coordinates:
                        pyautogui.click(coordinates[0], coordinates[1])
                        time.sleep(0.5)
            
            for i, item in enumerate(items):
                rpa_logger.log_action(f"Procesando item {i+1}/{len(items)}: {item.get('codigo', 'N/A')}")
                
                # Ingresar código del artículo
                if 'codigo' in item:
                    pyautogui.write(item['codigo'])
                    
                    # Navegar a cantidad
                    for _ in range(2):  # item_code_tabs del config
                        pyautogui.press('tab')
                        time.sleep(0.1)
                    
                    # Ingresar cantidad
                    if 'cantidad' in item:
                        pyautogui.write(str(item['cantidad']))
                    
                    # Si no es el último item, navegar al siguiente
                    if i < len(items) - 1:
                        for _ in range(3):  # tabs para próximo item
                            pyautogui.press('tab')
                            time.sleep(0.1)
            
            rpa_logger.log_action("Todos los items procesados exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error procesando items: {str(e)}")
            return False
    
    def _finalize_order(self) -> bool:
        """Finaliza y graba la orden de venta"""
        try:
            rpa_logger.log_action("Finalizando orden de venta")
            
            # Navegar al final de los totales
            for _ in range(2):  # tabs_after_last_quantity del config
                pyautogui.press('tab')
                time.sleep(0.1)
            
            # Grabar la orden (Ctrl+S o botón específico)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(get_delay('long') or 2.0)
            
            rpa_logger.log_action("Orden de venta finalizada exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error finalizando orden: {str(e)}")
            return False
    
    # Hereda get_pending_count, get_status_summary y _count_files de BaseRPAHandler