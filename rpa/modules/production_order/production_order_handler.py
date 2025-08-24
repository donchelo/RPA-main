"""
Handler específico para el módulo de órdenes de producción
"""

import os
import time
import yaml
from typing import Dict, Any, Optional
import pyautogui
from ...vision.main import Vision
from ...config_manager import ConfigManager
from ...simple_logger import rpa_logger
from ...state_machine import RPAEvent


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
    
    def load_articulo(self, numero_articulo: str) -> bool:
        """Carga el número de artículo en el formulario"""
        try:
            rpa_logger.info(f"🔄 Cargando artículo: {numero_articulo}")
            
            # Buscar el campo artículo usando template matching
            try:
                import cv2
                import numpy as np
                
                # Tomar screenshot y buscar la imagen del campo artículo
                screenshot = pyautogui.screenshot()
                screenshot_np = np.array(screenshot)
                screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
                
                # Cargar imagen de referencia del campo artículo
                field_ref = cv2.imread('./rpa/vision/reference_images/production/sap_articulo_field.png', cv2.IMREAD_COLOR)
                
                if field_ref is not None:
                    # Buscar coincidencia
                    result = cv2.matchTemplate(screenshot_cv, field_ref, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    
                    confidence_threshold = self.production_config.get('template_matching', {}).get('field_confidence', 0.8)
                    
                    if max_val > confidence_threshold:
                        # Calcular centro del elemento encontrado
                        w = field_ref.shape[1]
                        h = field_ref.shape[0]
                        center_x = max_loc[0] + w // 2
                        center_y = max_loc[1] + h // 2
                        
                        # Hacer clic en el centro del campo
                        pyautogui.click(center_x, center_y)
                        rpa_logger.info(f"✅ Campo artículo encontrado (confianza: {max_val:.3f})")
                    else:
                        rpa_logger.warning(f"⚠️ Campo artículo no encontrado claramente (confianza: {max_val:.3f})")
                        # Fallback: usar TAB
                        pyautogui.press('tab')
                        time.sleep(0.1)
                else:
                    rpa_logger.warning("⚠️ Imagen de referencia del campo artículo no encontrada")
                    # Fallback: usar TAB
                    pyautogui.press('tab')
                    time.sleep(0.1)
                    
            except Exception as e:
                rpa_logger.warning(f"⚠️ Error buscando campo artículo: {e}")
                # Fallback: usar TAB
                pyautogui.press('tab')
                time.sleep(0.1)
            
            # Escribir el número de artículo
            pyautogui.write(numero_articulo)
            time.sleep(self.config.get('delays', {}).get('after_input', 0.5))
            
            rpa_logger.info(f"✅ Artículo cargado: {numero_articulo}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando artículo: {e}")
            return False
    
    def load_pedido_interno(self, numero_pedido: str) -> bool:
        """Carga el número de pedido interno"""
        try:
            rpa_logger.info(f"🔄 Cargando pedido interno: {numero_pedido}")
            
            # Navegar al campo pedido interno: TAB+TAB
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            
            pyautogui.write(numero_pedido)
            time.sleep(self.config.get('delays', {}).get('after_input', 0.5))
            
            rpa_logger.info(f"✅ Pedido interno cargado: {numero_pedido}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando pedido interno: {e}")
            return False
    
    def load_cantidad(self, cantidad: int) -> bool:
        """Carga la cantidad"""
        try:
            rpa_logger.info(f"🔄 Cargando cantidad: {cantidad}")
            
            # Validar cantidad
            max_cantidad = self.production_config.get('validation', {}).get('max_cantidad', 999999)
            if cantidad > max_cantidad:
                rpa_logger.warning(f"⚠️ Cantidad {cantidad} excede el máximo permitido {max_cantidad}")
            
            # Navegar al campo cantidad: TAB+TAB
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            
            pyautogui.write(str(cantidad))
            time.sleep(self.config.get('delays', {}).get('after_input', 0.5))
            
            rpa_logger.info(f"✅ Cantidad cargada: {cantidad}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando cantidad: {e}")
            return False
    
    def load_fecha_finalizacion(self, fecha: str) -> bool:
        """Carga la fecha de finalización"""
        try:
            rpa_logger.info(f"🔄 Cargando fecha de finalización: {fecha}")
            
            # Validar formato de fecha
            formato_esperado = self.production_config.get('validation', {}).get('formato_fecha', 'DD/MM/YYYY')
            if len(fecha.split('/')) != 3:
                rpa_logger.warning(f"⚠️ Formato de fecha {fecha} no coincide con el esperado {formato_esperado}")
            
            # Navegar al campo fecha: TAB+TAB+TAB+TAB+TAB+TAB+TAB (7 TABs)
            for _ in range(7):
                pyautogui.press('tab')
                time.sleep(0.1)
            
            pyautogui.write(fecha)
            time.sleep(self.config.get('delays', {}).get('after_input', 0.5))
            
            rpa_logger.info(f"✅ Fecha de finalización cargada: {fecha}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error cargando fecha de finalización: {e}")
            return False
    
    def click_crear_button(self) -> bool:
        """Hace clic en el botón crear para finalizar la orden"""
        try:
            rpa_logger.info("🔄 Haciendo clic en botón crear...")
            
            # Buscar y hacer clic en el botón crear
            try:
                import cv2
                import numpy as np
                
                # Tomar screenshot y buscar la imagen del botón
                screenshot = pyautogui.screenshot()
                screenshot_np = np.array(screenshot)
                screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
                
                # Cargar imagen de referencia del botón
                button_ref = cv2.imread('./rpa/vision/reference_images/production/sap_produccion_crear_button.png', cv2.IMREAD_COLOR)
                
                if button_ref is not None:
                    # Buscar coincidencia
                    result = cv2.matchTemplate(screenshot_cv, button_ref, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    
                    confidence_threshold = self.production_config.get('template_matching', {}).get('field_confidence', 0.85)
                    
                    if max_val > confidence_threshold:
                        # Calcular centro del elemento encontrado
                        w = button_ref.shape[1]
                        h = button_ref.shape[0]
                        center_x = max_loc[0] + w // 2
                        center_y = max_loc[1] + h // 2
                        
                        # Hacer clic en el centro
                        pyautogui.click(center_x, center_y)
                        crear_button_found = True
                        rpa_logger.info(f"✅ Botón crear encontrado (confianza: {max_val:.3f})")
                    else:
                        crear_button_found = False
                        rpa_logger.error(f"❌ Botón crear no encontrado (confianza: {max_val:.3f})")
                else:
                    crear_button_found = False
                    rpa_logger.error("❌ Imagen de referencia del botón crear no encontrada")
                    
            except Exception as e:
                crear_button_found = False
                rpa_logger.error(f"❌ Error buscando botón crear: {e}")
            
            if not crear_button_found:
                rpa_logger.error("❌ No se pudo encontrar el botón crear")
                return False
            
            time.sleep(self.config.get('delays', {}).get('after_click', 1.0))
            rpa_logger.info("✅ Botón crear presionado exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error haciendo clic en botón crear: {e}")
            return False
    
    def validate_form_data(self, data: Dict[str, Any]) -> bool:
        """Valida los datos del formulario antes de procesarlos"""
        try:
            required_fields = ['numero_articulo', 'numero_pedido_interno', 'cantidad', 'fecha_finalizacion']
            
            for field in required_fields:
                if field not in data or not data[field]:
                    rpa_logger.error(f"❌ Campo requerido faltante: {field}")
                    return False
            
            # Validar cantidad
            cantidad = data.get('cantidad')
            if not isinstance(cantidad, (int, float)) or cantidad <= 0:
                rpa_logger.error(f"❌ Cantidad inválida: {cantidad}")
                return False
            
            # Validar fecha
            fecha = data.get('fecha_finalizacion')
            if not fecha or len(fecha.split('/')) != 3:
                rpa_logger.error(f"❌ Formato de fecha inválido: {fecha}")
                return False
            
            rpa_logger.info("✅ Validación de datos completada")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error validando datos: {e}")
            return False
    
    def process_production_order(self, data: Dict[str, Any], auto_click_crear: bool = False) -> bool:
        """Procesa una orden de producción completa"""
        try:
            rpa_logger.info("🚀 Iniciando procesamiento de orden de producción")
            
            # Validar datos
            if not self.validate_form_data(data):
                return False
            
            # Cargar cada campo en el orden correcto:
            # 1. Artículo (busca imagen y hace clic)
            if not self.load_articulo(data['numero_articulo']):
                return False
            
            # 2. Cantidad (TAB+TAB)
            if not self.load_cantidad(data['cantidad']):
                return False
            
            # 3. Fecha de finalización (TAB+TAB+TAB+TAB+TAB+TAB+TAB)
            if not self.load_fecha_finalizacion(data['fecha_finalizacion']):
                return False
            
            # 4. Pedido interno (TAB+TAB)
            if not self.load_pedido_interno(data['numero_pedido_interno']):
                return False
            
            # 5. Screenshot antes de crear
            rpa_logger.info("📸 Tomando screenshot antes de crear...")
            try:
                screenshot = pyautogui.screenshot()
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"./screenshots/produccion_antes_crear_{timestamp}.png"
                
                # Crear directorio si no existe
                os.makedirs("./screenshots", exist_ok=True)
                
                screenshot.save(screenshot_path)
                rpa_logger.info(f"✅ Screenshot guardado: {screenshot_path}")
            except Exception as e:
                rpa_logger.warning(f"⚠️ Error tomando screenshot: {e}")
            
            # Finalizar con botón crear (opcional)
            if auto_click_crear:
                if not self.click_crear_button():
                    return False
                rpa_logger.info("🎉 Orden de producción procesada y creada exitosamente")
            else:
                rpa_logger.info("✅ Formulario completado - Esperando decisión manual del usuario")
                rpa_logger.info("💡 El formulario está listo. Puedes hacer clic en 'Crear' o 'Borrar' manualmente.")
            
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error procesando orden de producción: {e}")
            return False
