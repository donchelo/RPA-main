"""
Handler específico para el módulo de órdenes de producción
"""

import os
import time
import yaml
from typing import Dict, Any, Optional, List
import pyautogui
from ...vision.main import Vision
from ...config_manager import ConfigManager
from ...simple_logger import rpa_logger
from ...state_machine import RPAEvent, RPAState


class ProductionOrderHandler:
    """Manejador específico para órdenes de producción"""
    
    def __init__(self, vision_system: Vision, config: ConfigManager):
        self.vision = vision_system
        self.config = config
        self.production_config = self._load_production_config()
        
    def _load_production_config(self) -> Dict[str, Any]:
        """Cargar configuración específica del módulo de producción"""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            'production_order_config.yaml'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
                return config_data.get('production_order', {})
        except Exception as e:
            rpa_logger.error(f"Error cargando configuración de producción: {e}")
            return {}
    
    def navigate_to_production(self) -> bool:
        """Navega al módulo de producción y abre orden de fabricación"""
        try:
            rpa_logger.info("🔄 Navegando al módulo de producción...")
            
            # 1. Presionar Alt+M para abrir módulos
            pyautogui.hotkey('alt', 'm')
            time.sleep(self.production_config.get('navigation', {}).get('alt_m_delay', 0.5))
            
            # 2. Presionar P para ir a producción
            pyautogui.press('p')
            time.sleep(self.production_config.get('navigation', {}).get('p_key_delay', 1.0))
            
            # 3. Buscar y hacer clic en "Orden de Fabricación"
            try:
                import cv2
                import numpy as np
                
                # Tomar screenshot y buscar la imagen del botón
                screenshot = pyautogui.screenshot()
                screenshot_np = np.array(screenshot)
                screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
                
                # Cargar imagen de referencia del botón
                button_ref = cv2.imread('./rpa/vision/reference_images/production/sap_orden_fabricacion_button.png', cv2.IMREAD_COLOR)
                
                if button_ref is not None:
                    # Buscar coincidencia
                    result = cv2.matchTemplate(screenshot_cv, button_ref, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    
                    confidence_threshold = self.production_config.get('template_matching', {}).get('orden_fabricacion_button_confidence', 0.8)
                    
                    if max_val > confidence_threshold:
                        # Calcular centro del elemento encontrado
                        w = button_ref.shape[1]
                        h = button_ref.shape[0]
                        center_x = max_loc[0] + w // 2
                        center_y = max_loc[1] + h // 2
                        
                        # Hacer clic en el centro
                        pyautogui.click(center_x, center_y)
                        orden_fabricacion_found = True
                        rpa_logger.info(f"✅ Botón de orden de fabricación encontrado (confianza: {max_val:.3f})")
                    else:
                        orden_fabricacion_found = False
                        rpa_logger.error(f"❌ Botón de orden de fabricación no encontrado (confianza: {max_val:.3f})")
                else:
                    orden_fabricacion_found = False
                    rpa_logger.error("❌ Imagen de referencia del botón no encontrada")
                    
            except Exception as e:
                orden_fabricacion_found = False
                rpa_logger.error(f"❌ Error buscando botón de orden de fabricación: {e}")
            
            if not orden_fabricacion_found:
                rpa_logger.error("❌ No se pudo encontrar el botón de orden de fabricación")
                return False
                
            time.sleep(self.production_config.get('navigation', {}).get('mouse_click_delay', 2.0))
            rpa_logger.info("✅ Navegación a producción completada")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error navegando a producción: {e}")
            return False
    
    def process_production_order(self, data: Dict[str, Any]) -> bool:
        """Procesa una orden de producción completa"""
        try:
            rpa_logger.info("🚀 Iniciando procesamiento de orden de producción")
            
            # Validar datos requeridos
            if not self._validate_production_data(data):
                return False
            
            # Navegar al módulo de producción
            if not self.navigate_to_production():
                return False
            
            # Buscar botón "Crear" y hacer clic
            if not self._click_create_button():
                return False
            
            # Cargar artículo
            numero_articulo = data.get('numero_articulo')
            if not numero_articulo:
                rpa_logger.error("❌ Número de artículo no encontrado")
                return False
            
            if not self._load_articulo(numero_articulo):
                return False
            
            # Cargar pedido interno
            numero_pedido_interno = data.get('numero_pedido_interno')
            if not numero_pedido_interno:
                rpa_logger.error("❌ Número de pedido interno no encontrado")
                return False
            
            if not self._load_pedido_interno(numero_pedido_interno):
                return False
            
            # Cargar cantidad
            cantidad = data.get('cantidad')
            if not cantidad:
                rpa_logger.error("❌ Cantidad no encontrada")
                return False
            
            if not self._load_cantidad(cantidad):
                return False
            
            # Cargar fecha de finalización
            fecha_finalizacion = data.get('fecha_finalizacion')
            if not fecha_finalizacion:
                rpa_logger.error("❌ Fecha de finalización no encontrada")
                return False
            
            if not self._load_fecha_finalizacion(fecha_finalizacion):
                return False
            
            # Tomar screenshot final
            if not self._take_screenshot():
                return False
            
            rpa_logger.info("✅ Orden de producción procesada exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error procesando orden de producción: {e}")
            return False
    
    def _click_create_button(self) -> bool:
        """Busca y hace clic en el botón 'Crear'"""
        try:
            import cv2
            import numpy as np
            
            # Tomar screenshot
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Buscar botón crear
            crear_button_ref = cv2.imread('./rpa/vision/reference_images/production/sap_produccion_crear_button.png', cv2.IMREAD_COLOR)
            
            if crear_button_ref is not None:
                result = cv2.matchTemplate(screenshot_cv, crear_button_ref, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                confidence_threshold = self.production_config.get('template_matching', {}).get('field_confidence', 0.8)
                
                if max_val > confidence_threshold:
                    w = crear_button_ref.shape[1]
                    h = crear_button_ref.shape[0]
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2
                    
                    pyautogui.click(center_x, center_y)
                    rpa_logger.info(f"✅ Botón crear encontrado y clickeado (confianza: {max_val:.3f})")
                    return True
                else:
                    rpa_logger.error(f"❌ Botón crear no encontrado (confianza: {max_val:.3f})")
                    return False
            else:
                rpa_logger.error("❌ Imagen de referencia del botón crear no encontrada")
                return False
                
        except Exception as e:
            rpa_logger.error(f"❌ Error buscando botón crear: {e}")
            return False
    
    def _load_articulo(self, numero_articulo: str) -> bool:
        """Carga el número de artículo en el campo correspondiente"""
        try:
            # Navegar al campo artículo
            tabs = self.production_config.get('form_fields', {}).get('articulo_tabs', 2)
            for _ in range(tabs):
                pyautogui.press('tab')
            
            # Escribir el número de artículo
            pyautogui.write(str(numero_articulo))
            time.sleep(self.production_config.get('form_fields', {}).get('field_input_delay', 0.5))
            
            rpa_logger.info(f"✅ Artículo cargado: {numero_articulo}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando artículo: {e}")
            return False
    
    def _load_pedido_interno(self, numero_pedido: str) -> bool:
        """Carga el número de pedido interno"""
        try:
            # Navegar al campo pedido interno
            tabs = self.production_config.get('form_fields', {}).get('pedido_interno_tabs', 3)
            for _ in range(tabs):
                pyautogui.press('tab')
            
            # Escribir el número de pedido
            pyautogui.write(str(numero_pedido))
            time.sleep(self.production_config.get('form_fields', {}).get('field_input_delay', 0.5))
            
            rpa_logger.info(f"✅ Pedido interno cargado: {numero_pedido}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando pedido interno: {e}")
            return False
    
    def _load_cantidad(self, cantidad: int) -> bool:
        """Carga la cantidad en el campo correspondiente"""
        try:
            # Navegar al campo cantidad
            tabs = self.production_config.get('form_fields', {}).get('cantidad_tabs', 2)
            for _ in range(tabs):
                pyautogui.press('tab')
            
            # Escribir la cantidad
            pyautogui.write(str(cantidad))
            time.sleep(self.production_config.get('form_fields', {}).get('field_input_delay', 0.5))
            
            rpa_logger.info(f"✅ Cantidad cargada: {cantidad}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando cantidad: {e}")
            return False
    
    def _load_fecha_finalizacion(self, fecha: str) -> bool:
        """Carga la fecha de finalización"""
        try:
            # Navegar al campo fecha
            tabs = self.production_config.get('form_fields', {}).get('fecha_finalizacion_tabs', 3)
            for _ in range(tabs):
                pyautogui.press('tab')
            
            # Escribir la fecha
            pyautogui.write(fecha)
            time.sleep(self.production_config.get('form_fields', {}).get('field_input_delay', 0.5))
            
            rpa_logger.info(f"✅ Fecha de finalización cargada: {fecha}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando fecha de finalización: {e}")
            return False
    
    def _take_screenshot(self) -> bool:
        """Toma un screenshot del formulario completado"""
        try:
            # Crear directorio de screenshots si no existe
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            # Tomar screenshot
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"production_order_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            rpa_logger.info(f"✅ Screenshot guardado: {filepath}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error tomando screenshot: {e}")
            return False
    
    def _validate_production_data(self, data: Dict[str, Any]) -> bool:
        """Valida que los datos de la orden de producción sean correctos"""
        required_fields = ['numero_articulo', 'numero_pedido_interno', 'cantidad', 'fecha_finalizacion']
        
        for field in required_fields:
            if field not in data:
                rpa_logger.error(f"❌ Campo requerido faltante: {field}")
                return False
        
        # Validar cantidad
        cantidad = data.get('cantidad')
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            rpa_logger.error("❌ Cantidad debe ser un número positivo")
            return False
        
        # Validar fecha
        fecha = data.get('fecha_finalizacion')
        if not fecha or len(fecha) != 10:  # DD/MM/YYYY
            rpa_logger.error("❌ Formato de fecha inválido (debe ser DD/MM/YYYY)")
            return False
        
        return True
    
    def get_module_info(self) -> Dict[str, Any]:
        """Retorna información del módulo"""
        return {
            "name": "Órdenes de Producción",
            "description": "Automatización de órdenes de producción en SAP Business One",
            "version": "1.0.0",
            "status": "ready",
            "supported_fields": [
                "numero_articulo",
                "numero_pedido_interno",
                "cantidad",
                "fecha_finalizacion",
                "unidad_medida",
                "centro_trabajo"
            ]
        }
    
    def test_module(self) -> bool:
        """Ejecuta pruebas del módulo"""
        try:
            rpa_logger.info("🧪 Iniciando pruebas del módulo de producción...")
            
            # Probar navegación
            if not self.navigate_to_production():
                rpa_logger.error("❌ Prueba de navegación falló")
                return False
            
            rpa_logger.info("✅ Pruebas del módulo de producción completadas")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error en pruebas del módulo: {e}")
            return False
