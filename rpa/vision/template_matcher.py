"""
Módulo consolidado para template matching
Elimina duplicación de código y centraliza la lógica de reconocimiento de imágenes
"""

import cv2
import numpy as np
import pyautogui
import logging
from typing import Optional, Tuple, Dict, Any
from rpa.config_manager import get_confidence, get_delay

# Configurar logger
logger = logging.getLogger(__name__)


class TemplateMatcher:
    """Clase centralizada para operaciones de template matching"""
    
    def __init__(self):
        self.screenshot_cache = {}
        self.template_cache = {}
    
    def find_template(self, 
                     template_image: np.ndarray, 
                     target_image: Optional[np.ndarray] = None,
                     confidence: float = None,
                     offset: Tuple[int, int] = (0, 0),
                     search_region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int]]:
        """
        Método genérico para template matching que reemplaza todos los métodos duplicados
        
        Args:
            template_image: Imagen template a buscar
            target_image: Imagen donde buscar (si es None, toma screenshot)
            confidence: Umbral de confianza (si es None, usa el por defecto)
            offset: Offset para ajustar el punto central (x, y)
            search_region: Región de búsqueda (x, y, width, height)
        
        Returns:
            Tupla con coordenadas (x, y) del centro del match, o None si no se encuentra
        """
        if template_image is None:
            logger.error("Template image is None")
            return None
        
        # Usar screenshot actual si no se proporciona target_image
        if target_image is None:
            target_image = self._get_current_screenshot()
        
        if target_image is None:
            logger.error("No se pudo obtener target image")
            return None
        
        # Usar confianza por defecto si no se especifica
        if confidence is None:
            confidence = get_confidence('default')
        
        # Aplicar región de búsqueda si se especifica
        if search_region:
            x, y, w, h = search_region
            target_image = target_image[y:y+h, x:x+w]
            region_offset = (x, y)
        else:
            region_offset = (0, 0)
        
        try:
            # Realizar template matching
            result = cv2.matchTemplate(target_image, template_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            logger.debug(f"Template matching - Confianza: {max_val:.3f}, Umbral: {confidence}")
            
            # Verificar si se encontró match con suficiente confianza
            if max_val >= confidence:
                # Calcular coordenadas del centro
                template_h, template_w = template_image.shape[:2]
                center_x = max_loc[0] + template_w // 2 + offset[0] + region_offset[0]
                center_y = max_loc[1] + template_h // 2 + offset[1] + region_offset[1]
                
                logger.info(f"Template encontrado en ({center_x}, {center_y}) con confianza {max_val:.3f}")
                return (center_x, center_y)
            else:
                logger.warning(f"Template no encontrado. Confianza: {max_val:.3f} < {confidence}")
                return None
                
        except Exception as e:
            logger.error(f"Error en template matching: {str(e)}")
            return None
    
    def find_template_with_timeout(self,
                                  template_image: np.ndarray,
                                  timeout: float = None,
                                  confidence: float = None,
                                  check_interval: float = 0.1) -> Optional[Tuple[int, int]]:
        """
        Busca un template con timeout, útil para esperar que aparezcan elementos
        
        Args:
            template_image: Imagen template a buscar
            timeout: Tiempo máximo de espera en segundos
            confidence: Umbral de confianza
            check_interval: Intervalo entre verificaciones
        
        Returns:
            Coordenadas del match o None si timeout
        """
        import time
        
        if timeout is None:
            timeout = get_delay('template_timeout') or 10.0
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            coordinates = self.find_template(template_image, confidence=confidence)
            if coordinates:
                return coordinates
            time.sleep(check_interval)
        
        logger.warning(f"Template no encontrado después de {timeout} segundos")
        return None
    
    def find_multiple_templates(self, 
                              templates: Dict[str, np.ndarray],
                              confidence: float = None) -> Dict[str, Optional[Tuple[int, int]]]:
        """
        Busca múltiples templates en una sola captura de pantalla
        
        Args:
            templates: Diccionario con nombre -> imagen template
            confidence: Umbral de confianza común
        
        Returns:
            Diccionario con nombre -> coordenadas (o None si no se encuentra)
        """
        target_image = self._get_current_screenshot()
        if target_image is None:
            return {name: None for name in templates.keys()}
        
        results = {}
        for name, template in templates.items():
            results[name] = self.find_template(template, target_image, confidence)
        
        return results
    
    def _get_current_screenshot(self) -> Optional[np.ndarray]:
        """Obtiene screenshot actual y lo convierte a formato OpenCV"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            return screenshot_cv
        except Exception as e:
            logger.error(f"Error tomando screenshot: {str(e)}")
            return None
    
    def load_template_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Carga una imagen template desde archivo con caché
        
        Args:
            image_path: Ruta al archivo de imagen
        
        Returns:
            Imagen cargada o None si error
        """
        if image_path in self.template_cache:
            return self.template_cache[image_path]
        
        try:
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if image is not None:
                self.template_cache[image_path] = image
                logger.debug(f"Template cargado y almacenado en caché: {image_path}")
            else:
                logger.error(f"No se pudo cargar la imagen: {image_path}")
            return image
        except Exception as e:
            logger.error(f"Error cargando imagen {image_path}: {str(e)}")
            return None
    
    def clear_cache(self):
        """Limpia el caché de templates e imágenes"""
        self.screenshot_cache.clear()
        self.template_cache.clear()
        logger.info("Caché de templates limpiado")
    
    def get_template_info(self, template_image: np.ndarray) -> Dict[str, Any]:
        """Obtiene información sobre un template"""
        if template_image is None:
            return {}
        
        height, width = template_image.shape[:2]
        channels = template_image.shape[2] if len(template_image.shape) > 2 else 1
        
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'dtype': str(template_image.dtype)
        }


# Instancia global del matcher
template_matcher = TemplateMatcher()

# Funciones de conveniencia para compatibilidad con código existente
def find_template(template_image: np.ndarray, 
                 confidence: float = None, 
                 timeout: float = None) -> Optional[Tuple[int, int]]:
    """Función de conveniencia para template matching simple"""
    if timeout:
        return template_matcher.find_template_with_timeout(template_image, timeout, confidence)
    else:
        return template_matcher.find_template(template_image, confidence=confidence)

def load_template(image_path: str) -> Optional[np.ndarray]:
    """Función de conveniencia para cargar templates"""
    return template_matcher.load_template_image(image_path)