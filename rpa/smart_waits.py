"""
Sistema de esperas inteligentes para RPA
Reemplaza time.sleep() hardcodeados con waits condicionales y adaptativos
"""

import time
import pyautogui
from typing import Callable, Optional, Any, Tuple
from rpa.config_manager import get_delay
from rpa.simple_logger import rpa_logger


class SmartWaits:
    """Clase para manejo de esperas inteligentes en RPA"""
    
    def __init__(self):
        self.last_action_time = 0
        self.adaptive = True
        
    def wait_for_element(self,
                        check_function: Callable[[], bool],
                        timeout: float = None,
                        check_interval: float = 0.1,
                        description: str = "elemento") -> bool:
        """
        Espera hasta que un elemento esté disponible o se agote el timeout
        
        Args:
            check_function: Función que retorna True cuando el elemento está listo
            timeout: Tiempo máximo de espera en segundos
            check_interval: Intervalo between verificaciones
            description: Descripción del elemento para logging
        
        Returns:
            True si el elemento apareció, False si timeout
        """
        if timeout is None:
            timeout = get_delay('medium') or 2.0
            
        start_time = time.time()
        checks_made = 0
        
        rpa_logger.info(f"Esperando {description} (timeout: {timeout}s)")
        
        while time.time() - start_time < timeout:
            try:
                if check_function():
                    elapsed = time.time() - start_time
                    rpa_logger.info(f"{description} encontrado después de {elapsed:.2f}s ({checks_made} verificaciones)")
                    return True
            except Exception as e:
                rpa_logger.warning(f"Error verificando {description}: {str(e)}")
            
            checks_made += 1
            time.sleep(check_interval)
        
        rpa_logger.warning(f"Timeout esperando {description} después de {timeout}s ({checks_made} verificaciones)")
        return False
    
    def wait_for_template(self,
                         template_image,
                         confidence: float = 0.8,
                         timeout: float = None,
                         description: str = "template") -> Optional[Tuple[int, int]]:
        """
        Espera hasta que aparezca un template en pantalla
        
        Args:
            template_image: Imagen template a buscar
            confidence: Umbral de confianza
            timeout: Tiempo máximo de espera
            description: Descripción para logging
        
        Returns:
            Coordenadas del template encontrado o None si timeout
        """
        from rpa.vision.template_matcher import template_matcher
        
        if timeout is None:
            timeout = get_delay('long') or 3.0
        
        def check_template():
            return template_matcher.find_template(template_image, confidence=confidence)
        
        rpa_logger.info(f"Esperando template: {description}")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            coordinates = check_template()
            if coordinates:
                elapsed = time.time() - start_time
                rpa_logger.info(f"Template {description} encontrado en {elapsed:.2f}s en {coordinates}")
                return coordinates
            time.sleep(0.1)
        
        rpa_logger.warning(f"Timeout esperando template {description} después de {timeout}s")
        return None
    
    def wait_for_window_active(self,
                              window_title: str,
                              timeout: float = None) -> bool:
        """
        Espera hasta que una ventana específica esté activa
        
        Args:
            window_title: Título de la ventana
            timeout: Tiempo máximo de espera
        
        Returns:
            True si la ventana se activó, False si timeout
        """
        if timeout is None:
            timeout = get_delay('window_activation') or 5.0
        
        def check_window():
            try:
                windows = pyautogui.getWindowsWithTitle(window_title)
                return len(windows) > 0 and windows[0].isActive
            except:
                return False
        
        return self.wait_for_element(
            check_window,
            timeout,
            0.2,
            f"ventana '{window_title}' activa"
        )
    
    def adaptive_wait(self, operation_type: str, base_delay: float = None):
        """
        Espera adaptativa basada en el tipo de operación y rendimiento histórico
        
        Args:
            operation_type: Tipo de operación (input, click, navigation, etc.)
            base_delay: Delay base, si no se especifica usa configuración
        """
        if base_delay is None:
            delay_key = f"after_{operation_type}"
            base_delay = get_delay(delay_key) or get_delay('medium') or 1.0
        
        # Si es adaptativo, ajustar basado en el rendimiento reciente
        if self.adaptive:
            # Ajuste simple basado en tiempo desde última acción
            time_since_last = time.time() - self.last_action_time
            if time_since_last < 0.5:  # Acciones muy rápidas, puede necesitar más tiempo
                adjusted_delay = base_delay * 1.2
            elif time_since_last > 3.0:  # Sistema puede estar lento
                adjusted_delay = base_delay * 1.5
            else:
                adjusted_delay = base_delay
        else:
            adjusted_delay = base_delay
        
        # Mínimo y máximo razonables
        adjusted_delay = max(0.1, min(adjusted_delay, 5.0))
        
        rpa_logger.debug(f"Espera adaptativa para {operation_type}: {adjusted_delay:.2f}s")
        time.sleep(adjusted_delay)
        self.last_action_time = time.time()
    
    def wait_for_user_input_processed(self, delay_type: str = "after_input"):
        """Espera específica después de entrada de usuario"""
        delay = get_delay(delay_type) or 1.0
        rpa_logger.debug(f"Esperando procesamiento de entrada: {delay}s")
        time.sleep(delay)
    
    def wait_for_click_processed(self, delay_type: str = "after_click"):
        """Espera específica después de clic"""
        delay = get_delay(delay_type) or 1.0
        rpa_logger.debug(f"Esperando procesamiento de clic: {delay}s")
        time.sleep(delay)
    
    def wait_for_navigation(self, delay_type: str = "navigation_wait"):
        """Espera específica para navegación"""
        delay = get_delay(delay_type) or 2.0
        rpa_logger.debug(f"Esperando navegación: {delay}s")
        time.sleep(delay)
    
    def wait_for_system_startup(self, system_name: str = "SAP", delay_type: str = "sap_startup"):
        """Espera para startup de sistemas pesados"""
        delay = get_delay(delay_type) or 30.0
        rpa_logger.info(f"Esperando startup de {system_name}: {delay}s")
        time.sleep(delay)
    
    def smart_tab_wait(self, tabs_count: int, operation_context: str = ""):
        """
        Espera inteligente después de navegación por tabs
        
        Args:
            tabs_count: Número de tabs presionados
            operation_context: Contexto de la operación para logging
        """
        # Delay base por tab
        base_delay_per_tab = get_delay('after_tab') or 0.5
        total_delay = base_delay_per_tab * tabs_count
        
        # Ajuste por contexto
        if "nit" in operation_context.lower():
            total_delay *= 1.2  # NIT puede requerir más tiempo
        elif "item" in operation_context.lower():
            total_delay *= 1.1  # Items pueden requerir procesamiento adicional
        
        rpa_logger.debug(f"Espera inteligente después de {tabs_count} tabs ({operation_context}): {total_delay:.2f}s")
        time.sleep(total_delay)
    
    def conditional_wait(self,
                        condition_function: Callable[[], bool],
                        timeout: float,
                        success_delay: float = 0.5,
                        failure_delay: float = 2.0,
                        description: str = "condición") -> bool:
        """
        Espera condicional con diferentes delays según resultado
        
        Args:
            condition_function: Función que retorna True/False
            timeout: Timeout máximo
            success_delay: Delay adicional si la condición se cumple
            failure_delay: Delay adicional si la condición falla
            description: Descripción para logging
        
        Returns:
            True si la condición se cumplió, False si timeout
        """
        if self.wait_for_element(condition_function, timeout, 0.1, description):
            if success_delay > 0:
                rpa_logger.debug(f"Condición cumplida, esperando {success_delay}s adicionales")
                time.sleep(success_delay)
            return True
        else:
            if failure_delay > 0:
                rpa_logger.debug(f"Condición no cumplida, esperando {failure_delay}s para recuperación")
                time.sleep(failure_delay)
            return False


# Instancia global
smart_waits = SmartWaits()

# Funciones de conveniencia
def wait_for_element(check_function, timeout=None, description="elemento"):
    """Función de conveniencia para esperar elementos"""
    return smart_waits.wait_for_element(check_function, timeout, description=description)

def wait_for_template(template_image, confidence=0.8, timeout=None, description="template"):
    """Función de conveniencia para esperar templates"""
    return smart_waits.wait_for_template(template_image, confidence, timeout, description)

def adaptive_wait(operation_type, base_delay=None):
    """Función de conveniencia para esperas adaptativas"""
    smart_waits.adaptive_wait(operation_type, base_delay)

def smart_sleep(delay_type):
    """Reemplazo inteligente para time.sleep() con configuración"""
    delay = get_delay(delay_type) or 1.0
    time.sleep(delay)