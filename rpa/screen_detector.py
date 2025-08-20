"""
Sistema de Detección de Estado de Pantalla - RPA TAMAPRINT
Fase 1: Detección básica de las 3 pantallas principales
"""

import cv2
import numpy as np
import pyautogui
import logging
import time
from enum import Enum
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from rpa.vision.template_matcher import template_matcher
from rpa.simple_logger import rpa_logger


class ScreenState(Enum):
    """Estados de pantalla que puede detectar el sistema"""
    UNKNOWN = "unknown"
    REMOTE_DESKTOP = "remote_desktop"
    SAP_DESKTOP = "sap_desktop"
    SALES_ORDER_FORM = "sales_order_form"
    ERROR = "error"


@dataclass
class DetectionResult:
    """Resultado de la detección de pantalla"""
    state: ScreenState
    confidence: float
    details: Dict[str, Any]
    screenshot_path: Optional[str] = None


class ScreenDetector:
    """Sistema de detección de estado de pantalla"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Cargar imágenes de referencia para detección
        self._load_reference_images()
        
        # Configurar umbrales de confianza
        self.confidence_thresholds = {
            ScreenState.REMOTE_DESKTOP: 0.85,
            ScreenState.SAP_DESKTOP: 0.80,
            ScreenState.SALES_ORDER_FORM: 0.85,
        }
        
        # Elementos clave para cada pantalla
        self.detection_elements = {
            ScreenState.REMOTE_DESKTOP: [
                'remote_desktop_title',
                'remote_desktop_controls'
            ],
            ScreenState.SAP_DESKTOP: [
                'sap_icon',
                'sap_modulos_menu_button',
                'sap_desktop_layout'
            ],
            ScreenState.SALES_ORDER_FORM: [
                'client_field',
                'orden_compra_field',
                'fecha_entrega_field',
                'sales_order_template'
            ]
        }
    
    def _load_reference_images(self):
        """Carga las imágenes de referencia para detección"""
        try:
            # Remote Desktop
            self.remote_desktop_image = cv2.imread(
                './rpa/vision/reference_images/remote_desktop.png', 
                cv2.IMREAD_UNCHANGED
            )
            
            # SAP Desktop
            self.sap_desktop_image = cv2.imread(
                './rpa/vision/reference_images/sap_desktop.png', 
                cv2.IMREAD_UNCHANGED
            )
            self.sap_icon_image = cv2.imread(
                './rpa/vision/reference_images/sap_icon.png', 
                cv2.IMREAD_COLOR
            )
            self.sap_modulos_menu_button = cv2.imread(
                './rpa/vision/reference_images/sap_modulos_menu_button.png', 
                cv2.IMREAD_COLOR
            )
            # Nueva imagen de referencia para la interfaz principal de SAP
            self.sap_main_interface_image = cv2.imread(
                './rpa/vision/reference_images/sap_main_interface.png', 
                cv2.IMREAD_COLOR
            )
            
            # Sales Order Form
            self.sales_order_template = cv2.imread(
                './rpa/vision/reference_images/sap_orden_de_ventas_template.png', 
                cv2.IMREAD_UNCHANGED
            )
            self.client_field_image = cv2.imread(
                './rpa/vision/reference_images/client_field.png', 
                cv2.IMREAD_COLOR
            )
            self.orden_compra_image = cv2.imread(
                './rpa/vision/reference_images/orden_compra.png', 
                cv2.IMREAD_COLOR
            )
            self.fecha_entrega_image = cv2.imread(
                './rpa/vision/reference_images/fecha_entrega.png', 
                cv2.IMREAD_COLOR
            )
            
            self.logger.info("Imágenes de referencia cargadas correctamente")
            
        except Exception as e:
            self.logger.error(f"Error cargando imágenes de referencia: {e}")
            raise
    
    def detect_current_screen(self, save_screenshot: bool = False) -> DetectionResult:
        """
        Detecta el estado actual de la pantalla
        
        Args:
            save_screenshot: Si guardar el screenshot para debugging
            
        Returns:
            DetectionResult con el estado detectado y confianza
        """
        try:
            # Tomar screenshot
            screenshot = self._take_screenshot(save_screenshot)
            if screenshot is None:
                return DetectionResult(
                    state=ScreenState.ERROR,
                    confidence=0.0,
                    details={"error": "No se pudo tomar screenshot"}
                )
            
            # Detectar cada estado
            results = {}
            
            # Remote Desktop
            remote_desktop_conf = self._detect_remote_desktop(screenshot)
            results[ScreenState.REMOTE_DESKTOP] = remote_desktop_conf
            
            # SAP Desktop
            sap_desktop_conf = self._detect_sap_desktop(screenshot)
            results[ScreenState.SAP_DESKTOP] = sap_desktop_conf
            
            # Sales Order Form
            sales_order_conf = self._detect_sales_order_form(screenshot)
            results[ScreenState.SALES_ORDER_FORM] = sales_order_conf
            
            # Determinar estado con mayor confianza
            best_state = max(results.items(), key=lambda x: x[1])
            
            # Verificar si la confianza es suficiente
            if best_state[1] >= self.confidence_thresholds.get(best_state[0], 0.8):
                detected_state = best_state[0]
                confidence = best_state[1]
            else:
                detected_state = ScreenState.UNKNOWN
                confidence = best_state[1]
            
            # Crear resultado
            result = DetectionResult(
                state=detected_state,
                confidence=confidence,
                details={
                    "all_confidences": results,
                    "threshold_met": detected_state != ScreenState.UNKNOWN
                },
                screenshot_path=f"./debug_screenshots/detection_{detected_state.value}.png" if save_screenshot else None
            )
            
            self.logger.info(f"Estado detectado: {detected_state.value} (confianza: {confidence:.3f})")
            rpa_logger.log_action(
                "DETECCIÓN DE PANTALLA",
                f"Estado: {detected_state.value}, Confianza: {confidence:.3f}"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error en detección de pantalla: {e}")
            return DetectionResult(
                state=ScreenState.ERROR,
                confidence=0.0,
                details={"error": str(e)}
            )
    
    def _take_screenshot(self, save: bool = False) -> Optional[np.ndarray]:
        """Toma un screenshot de la pantalla actual"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            if save:
                import os
                os.makedirs("./debug_screenshots", exist_ok=True)
                cv2.imwrite(f"./debug_screenshots/screenshot_{int(time.time())}.png", screenshot_np)
            
            return screenshot_np
            
        except Exception as e:
            self.logger.error(f"Error tomando screenshot: {e}")
            return None
    
    def _detect_remote_desktop(self, screenshot: np.ndarray) -> float:
        """Detecta si estamos en la pantalla de Remote Desktop"""
        try:
            # Detectar elementos clave de Remote Desktop
            matches = []
            
            # Buscar imagen de referencia de Remote Desktop
            if self.remote_desktop_image is not None:
                result = cv2.matchTemplate(screenshot, self.remote_desktop_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Buscar elementos específicos de Remote Desktop
            # (Aquí se pueden añadir más elementos específicos)
            
            # Calcular confianza promedio
            if matches:
                return sum(matches) / len(matches)
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error detectando Remote Desktop: {e}")
            return 0.0
    
    def _detect_sap_desktop(self, screenshot: np.ndarray) -> float:
        """Detecta si estamos en la pantalla de SAP Desktop"""
        try:
            matches = []
            
            # Buscar icono de SAP
            if self.sap_icon_image is not None:
                result = cv2.matchTemplate(screenshot, self.sap_icon_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Buscar botón de módulos
            if self.sap_modulos_menu_button is not None:
                result = cv2.matchTemplate(screenshot, self.sap_modulos_menu_button, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Buscar interfaz principal de SAP (nueva imagen de referencia)
            if self.sap_main_interface_image is not None:
                result = cv2.matchTemplate(screenshot, self.sap_main_interface_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
                self.logger.debug(f"Confianza interfaz principal SAP: {max_val:.3f}")
            
            # Buscar layout de SAP Desktop
            if self.sap_desktop_image is not None:
                result = cv2.matchTemplate(screenshot, self.sap_desktop_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Calcular confianza promedio
            if matches:
                return sum(matches) / len(matches)
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error detectando SAP Desktop: {e}")
            return 0.0
    
    def _detect_sales_order_form(self, screenshot: np.ndarray) -> float:
        """Detecta si estamos en el formulario de órdenes de venta"""
        try:
            matches = []
            
            # Buscar template de formulario de órdenes
            if self.sales_order_template is not None:
                result = cv2.matchTemplate(screenshot, self.sales_order_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Buscar campo de cliente
            if self.client_field_image is not None:
                result = cv2.matchTemplate(screenshot, self.client_field_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Buscar campo de orden de compra
            if self.orden_compra_image is not None:
                result = cv2.matchTemplate(screenshot, self.orden_compra_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Buscar campo de fecha de entrega
            if self.fecha_entrega_image is not None:
                result = cv2.matchTemplate(screenshot, self.fecha_entrega_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                matches.append(max_val)
            
            # Calcular confianza promedio
            if matches:
                return sum(matches) / len(matches)
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error detectando formulario de órdenes: {e}")
            return 0.0
    
    def verify_screen_state(self, state: ScreenState, max_attempts: int = 3) -> bool:
        """
        Verifica que realmente estamos en el estado especificado
        
        Args:
            state: Estado a verificar
            max_attempts: Número máximo de intentos
            
        Returns:
            True si el estado se confirma, False en caso contrario
        """
        for attempt in range(max_attempts):
            result = self.detect_current_screen()
            
            if result.state == state and result.confidence >= self.confidence_thresholds.get(state, 0.8):
                self.logger.info(f"Estado {state.value} confirmado en intento {attempt + 1}")
                return True
            
            self.logger.warning(f"Intento {attempt + 1}: Estado esperado {state.value}, detectado {result.state.value}")
            
            if attempt < max_attempts - 1:
                import time
                time.sleep(1)  # Esperar antes del siguiente intento
        
        self.logger.error(f"No se pudo confirmar estado {state.value} después de {max_attempts} intentos")
        return False


# Instancia global del detector
screen_detector = ScreenDetector()
