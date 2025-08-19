"""
Sistema de Navegación Automática - RPA TAMAPRINT
Fase 2: Navegación inteligente entre pantallas
"""

import pyautogui
import time
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass
from rpa.screen_detector import ScreenState, screen_detector
from rpa.simple_logger import rpa_logger
from rpa.smart_waits import smart_sleep, adaptive_wait
from rpa.config_manager import get_delay


@dataclass
class NavigationStep:
    """Paso de navegación"""
    action: str
    target: str
    expected_state: ScreenState
    timeout: int = 10
    retries: int = 3


class NavigationPlanner:
    """Planificador de navegación automática"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_state = ScreenState.UNKNOWN
        
        # Configurar PyAutoGUI para ser más seguro
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Definir rutas de navegación
        self.navigation_routes = {
            # Desde cualquier estado a Remote Desktop
            ScreenState.UNKNOWN: [
                NavigationStep("maximize_remote_desktop", "Remote Desktop", ScreenState.REMOTE_DESKTOP),
                NavigationStep("connect_remote_desktop", "Remote Desktop", ScreenState.REMOTE_DESKTOP)
            ],
            
            # Desde Remote Desktop a SAP Desktop
            ScreenState.REMOTE_DESKTOP: [
                NavigationStep("open_sap", "SAP Desktop", ScreenState.SAP_DESKTOP),
                NavigationStep("wait_sap_load", "SAP Desktop", ScreenState.SAP_DESKTOP)
            ],
            
            # Desde SAP Desktop a Sales Order Form
            ScreenState.SAP_DESKTOP: [
                NavigationStep("navigate_to_sales_order", "Sales Order Form", ScreenState.SALES_ORDER_FORM),
                NavigationStep("wait_form_load", "Sales Order Form", ScreenState.SALES_ORDER_FORM)
            ]
        }
    
    def navigate_to_target_state(self, target_state: ScreenState, max_attempts: int = 3) -> bool:
        """
        Navega automáticamente al estado objetivo
        
        Args:
            target_state: Estado al que queremos llegar
            max_attempts: Número máximo de intentos
            
        Returns:
            True si se logró llegar al estado objetivo
        """
        rpa_logger.log_action(
            "INICIANDO NAVEGACIÓN",
            f"Objetivo: {target_state.value}, Máximo intentos: {max_attempts}"
        )
        
        for attempt in range(max_attempts):
            self.logger.info(f"Intento {attempt + 1}/{max_attempts} para llegar a {target_state.value}")
            
            # Detectar estado actual
            detection_result = screen_detector.detect_current_screen()
            self.current_state = detection_result.state
            
            self.logger.info(f"Estado actual detectado: {self.current_state.value} (confianza: {detection_result.confidence:.3f})")
            
            # Si ya estamos en el estado objetivo
            if self.current_state == target_state:
                self.logger.info(f"Ya estamos en el estado objetivo: {target_state.value}")
                return True
            
            # Si hay error en la detección, intentar recuperar
            if self.current_state == ScreenState.ERROR:
                self.logger.warning("Error en detección, intentando recuperar...")
                self._recover_from_error()
                continue
            
            # Si estado desconocido, intentar navegar a Remote Desktop
            if self.current_state == ScreenState.UNKNOWN:
                self.logger.info("Estado desconocido, intentando navegar a Remote Desktop...")
                if self._navigate_to_remote_desktop():
                    continue
                else:
                    self.logger.error("No se pudo navegar a Remote Desktop")
                    return False
            
            # Navegar al estado objetivo
            if self._execute_navigation_plan(target_state):
                # Verificar que llegamos al estado objetivo
                if screen_detector.verify_screen_state(target_state, max_attempts=2):
                    self.logger.info(f"✅ Navegación exitosa a {target_state.value}")
                    return True
                else:
                    self.logger.warning(f"No se pudo confirmar llegada a {target_state.value}")
            
            # Esperar antes del siguiente intento
            if attempt < max_attempts - 1:
                smart_sleep(3)
        
        self.logger.error(f"❌ No se pudo llegar a {target_state.value} después de {max_attempts} intentos")
        return False
    
    def _execute_navigation_plan(self, target_state: ScreenState) -> bool:
        """Ejecuta el plan de navegación hacia el estado objetivo"""
        
        # Obtener ruta de navegación
        route = self._get_navigation_route(target_state)
        if not route:
            self.logger.error(f"No se encontró ruta de navegación para {target_state.value}")
            return False
        
        self.logger.info(f"Ejecutando ruta de navegación con {len(route)} pasos")
        
        # Ejecutar cada paso
        for step in route:
            if not self._execute_navigation_step(step):
                self.logger.error(f"Fallo en paso: {step.action}")
                return False
        
        return True
    
    def _get_navigation_route(self, target_state: ScreenState) -> List[NavigationStep]:
        """Obtiene la ruta de navegación hacia el estado objetivo"""
        
        # Si estamos en estado desconocido, ir a Remote Desktop primero
        if self.current_state == ScreenState.UNKNOWN:
            return self.navigation_routes[ScreenState.UNKNOWN]
        
        # Construir ruta paso a paso
        route = []
        current = self.current_state
        
        while current != target_state:
            if current in self.navigation_routes:
                route.extend(self.navigation_routes[current])
                # El siguiente estado sería el objetivo del último paso
                if route:
                    current = route[-1].expected_state
                else:
                    break
            else:
                self.logger.error(f"No hay ruta definida desde {current.value}")
                break
        
        return route
    
    def _execute_navigation_step(self, step: NavigationStep) -> bool:
        """Ejecuta un paso de navegación específico"""
        
        self.logger.info(f"Ejecutando: {step.action} -> {step.target}")
        rpa_logger.log_action("NAVEGACIÓN", f"{step.action} -> {step.target}")
        
        for retry in range(step.retries):
            try:
                # Ejecutar acción específica
                if step.action == "maximize_remote_desktop":
                    success = self._maximize_remote_desktop()
                elif step.action == "connect_remote_desktop":
                    success = self._connect_remote_desktop()
                elif step.action == "open_sap":
                    success = self._open_sap()
                elif step.action == "wait_sap_load":
                    success = self._wait_sap_load()
                elif step.action == "navigate_to_sales_order":
                    success = self._navigate_to_sales_order()
                elif step.action == "wait_form_load":
                    success = self._wait_form_load()
                else:
                    self.logger.error(f"Acción no reconocida: {step.action}")
                    return False
                
                if success:
                    # Verificar que llegamos al estado esperado
                    if screen_detector.verify_screen_state(step.expected_state, max_attempts=1):
                        self.current_state = step.expected_state
                        return True
                    else:
                        self.logger.warning(f"Acción exitosa pero no se confirmó estado {step.expected_state.value}")
                
                # Esperar antes del siguiente intento
                if retry < step.retries - 1:
                    smart_sleep(2)
                    
            except Exception as e:
                self.logger.error(f"Error en paso {step.action}: {e}")
                if retry < step.retries - 1:
                    smart_sleep(2)
        
        return False
    
    def _maximize_remote_desktop(self) -> bool:
        """Maximiza la ventana de Remote Desktop"""
        try:
            # Buscar ventana de Remote Desktop
            window_title = "Conexión a Escritorio remoto"
            
            # Intentar maximizar usando Alt+Space, M
            pyautogui.hotkey('alt', 'space')
            smart_sleep(0.5)
            pyautogui.press('m')
            smart_sleep(0.5)
            
            # Alternativa: usar F11 para pantalla completa
            pyautogui.press('f11')
            smart_sleep(1)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error maximizando Remote Desktop: {e}")
            return False
    
    def _connect_remote_desktop(self) -> bool:
        """Conecta a Remote Desktop"""
        try:
            # Simular clic en botón de conexión (generalmente en el centro)
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            
            pyautogui.click(center_x, center_y)
            smart_sleep(3)  # Esperar conexión
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error conectando Remote Desktop: {e}")
            return False
    
    def _open_sap(self) -> bool:
        """Abre SAP desde Remote Desktop"""
        try:
            # Buscar y hacer clic en el icono de SAP
            # Usar template matching para encontrar el icono
            from rpa.vision.main import Vision
            vision = Vision()
            
            # Buscar icono de SAP
            sap_icon_coords = vision.get_sap_icon_coordinates()
            if sap_icon_coords:
                pyautogui.click(sap_icon_coords)
                smart_sleep(5)  # Esperar que SAP se abra
                return True
            else:
                self.logger.error("No se encontró el icono de SAP")
                return False
                
        except Exception as e:
            self.logger.error(f"Error abriendo SAP: {e}")
            return False
    
    def _wait_sap_load(self) -> bool:
        """Espera a que SAP termine de cargar"""
        try:
            # Esperar hasta 30 segundos para que SAP cargue
            for i in range(30):
                if screen_detector.verify_screen_state(ScreenState.SAP_DESKTOP, max_attempts=1):
                    return True
                smart_sleep(1)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error esperando carga de SAP: {e}")
            return False
    
    def _navigate_to_sales_order(self) -> bool:
        """Navega al formulario de órdenes de venta"""
        try:
            from rpa.vision.main import Vision
            vision = Vision()
            
            # Hacer clic en menú de módulos
            modulos_coords = vision.get_modulos_menu_coordinates()
            if modulos_coords:
                pyautogui.click(modulos_coords)
                smart_sleep(1)
            
            # Hacer clic en menú de ventas
            ventas_coords = vision.get_ventas_menu_coordinates()
            if ventas_coords:
                pyautogui.click(ventas_coords)
                smart_sleep(1)
            
            # Hacer clic en órdenes de venta
            ordenes_coords = vision.get_ventas_order_coordinates()
            if ordenes_coords:
                pyautogui.click(ordenes_coords)
                smart_sleep(3)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error navegando a órdenes de venta: {e}")
            return False
    
    def _wait_form_load(self) -> bool:
        """Espera a que el formulario de órdenes cargue"""
        try:
            # Esperar hasta 15 segundos para que el formulario cargue
            for i in range(15):
                if screen_detector.verify_screen_state(ScreenState.SALES_ORDER_FORM, max_attempts=1):
                    return True
                smart_sleep(1)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error esperando carga del formulario: {e}")
            return False
    
    def _navigate_to_remote_desktop(self) -> bool:
        """Navega a Remote Desktop desde cualquier estado"""
        try:
            # Buscar ventana de Remote Desktop
            window_title = "Conexión a Escritorio remoto"
            
            # Intentar activar la ventana
            pyautogui.hotkey('alt', 'tab')
            smart_sleep(1)
            
            # Verificar si estamos en Remote Desktop
            if screen_detector.verify_screen_state(ScreenState.REMOTE_DESKTOP, max_attempts=1):
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error navegando a Remote Desktop: {e}")
            return False
    
    def _recover_from_error(self) -> bool:
        """Intenta recuperarse de un error de detección"""
        try:
            self.logger.info("Intentando recuperación...")
            
            # Tomar screenshot y guardarlo para debugging
            screen_detector.detect_current_screen(save_screenshot=True)
            
            # Intentar navegar a Remote Desktop
            return self._navigate_to_remote_desktop()
            
        except Exception as e:
            self.logger.error(f"Error en recuperación: {e}")
            return False


# Instancia global del planificador
navigation_planner = NavigationPlanner()
