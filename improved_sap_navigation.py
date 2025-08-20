#!/usr/bin/env python3
"""
Script mejorado para navegación a "Orden de Venta" en SAP
Incluye mejor manejo de errores, tiempos de espera y verificación de estado
"""

import time
import sys
import os
import cv2
import numpy as np
import pyautogui

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.screen_detector import ScreenDetector, ScreenState
from rpa.simple_logger import rpa_logger
from rpa.smart_waits import smart_sleep

class ImprovedSAPNavigation:
    """Navegación mejorada a SAP con mejor manejo de errores"""
    
    def __init__(self):
        self.vision = Vision()
        self.detector = ScreenDetector()
        
        # Configurar PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Tiempos de espera configurables
        self.wait_times = {
            'menu_open': 2.0,      # Tiempo para que se abra un menú
            'menu_navigate': 1.5,  # Tiempo entre navegación de menús
            'page_load': 5.0,      # Tiempo para que cargue una página
            'verification': 3.0    # Tiempo para verificar estado
        }
    
    def navigate_to_sales_order(self, max_attempts: int = 3) -> bool:
        """
        Navega al formulario de órdenes de venta con mejor manejo de errores
        
        Args:
            max_attempts: Número máximo de intentos
            
        Returns:
            True si se logró llegar al formulario
        """
        print("🚀 Iniciando navegación mejorada a Orden de Venta")
        print()
        
        for attempt in range(max_attempts):
            print(f"📋 Intento {attempt + 1}/{max_attempts}")
            
            try:
                # Verificar estado inicial
                if not self._verify_sap_desktop():
                    print("❌ No estamos en SAP Desktop")
                    return False
                
                # Paso 1: Hacer clic en módulos
                if not self._click_modulos_menu():
                    print("❌ No se pudo hacer clic en módulos")
                    continue
                
                # Paso 2: Hacer clic en ventas
                if not self._click_ventas_menu():
                    print("❌ No se pudo hacer clic en ventas")
                    continue
                
                # Paso 3: Hacer clic en orden de venta
                if not self._click_sales_order():
                    print("❌ No se pudo hacer clic en orden de venta")
                    continue
                
                # Paso 4: Verificar que llegamos al formulario
                if self._verify_sales_order_form():
                    print("✅ ¡Navegación exitosa! Llegamos al formulario de órdenes")
                    return True
                else:
                    print("❌ No se detectó el formulario de órdenes")
                    continue
                
            except Exception as e:
                print(f"❌ Error en intento {attempt + 1}: {e}")
                rpa_logger.log_error("NAVEGACIÓN SAP", f"Error en intento {attempt + 1}: {e}")
                
                if attempt < max_attempts - 1:
                    print("⏳ Esperando antes del siguiente intento...")
                    smart_sleep(3)
        
        print("❌ No se pudo completar la navegación después de todos los intentos")
        return False
    
    def _verify_sap_desktop(self) -> bool:
        """Verifica que estamos en SAP Desktop"""
        print("🔍 Verificando que estamos en SAP Desktop...")
        
        result = self.detector.detect_current_screen()
        if result.state == ScreenState.SAP_DESKTOP and result.confidence > 0.7:
            print(f"✅ Confirmado: SAP Desktop (confianza: {result.confidence:.3f})")
            return True
        else:
            print(f"❌ Estado actual: {result.state.value} (confianza: {result.confidence:.3f})")
            return False
    
    def _click_modulos_menu(self) -> bool:
        """Hace clic en el menú de módulos"""
        print("🔍 Buscando botón de módulos...")
        
        modulos_coords = self.vision.get_modulos_menu_coordinates()
        if not modulos_coords:
            print("❌ No se encontró el botón de módulos")
            return False
        
        print(f"✅ Botón de módulos encontrado en {modulos_coords}")
        print("🖱️  Haciendo clic en módulos...")
        
        try:
            pyautogui.click(modulos_coords)
            smart_sleep(self.wait_times['menu_open'])
            
            # Verificar que el menú se abrió
            if self._verify_modulos_menu_opened():
                print("✅ Menú de módulos abierto correctamente")
                return True
            else:
                print("❌ El menú de módulos no se abrió")
                return False
                
        except Exception as e:
            print(f"❌ Error haciendo clic en módulos: {e}")
            return False
    
    def _click_ventas_menu(self) -> bool:
        """Hace clic en el menú de ventas"""
        print("🔍 Buscando menú de ventas...")
        
        ventas_coords = self.vision.get_ventas_menu_coordinates()
        if not ventas_coords:
            print("❌ No se encontró el menú de ventas")
            return False
        
        print(f"✅ Menú de ventas encontrado en {ventas_coords}")
        print("🖱️  Haciendo clic en ventas...")
        
        try:
            pyautogui.click(ventas_coords)
            smart_sleep(self.wait_times['menu_navigate'])
            
            # Verificar que el submenú se abrió
            if self._verify_ventas_menu_opened():
                print("✅ Menú de ventas abierto correctamente")
                return True
            else:
                print("❌ El menú de ventas no se abrió")
                return False
                
        except Exception as e:
            print(f"❌ Error haciendo clic en ventas: {e}")
            return False
    
    def _click_sales_order(self) -> bool:
        """Hace clic en orden de venta"""
        print("🔍 Buscando botón de orden de venta...")
        
        orden_coords = self.vision.get_ventas_order_coordinates()
        if not orden_coords:
            print("❌ No se encontró el botón de orden de venta")
            
            # Intentar con umbral más bajo
            print("🔍 Intentando con umbral más bajo...")
            orden_coords = self._find_sales_order_with_lower_threshold()
            
            if not orden_coords:
                print("❌ No se encontró el botón incluso con umbral bajo")
                return False
        
        print(f"✅ Botón de orden de venta encontrado en {orden_coords}")
        print("🖱️  Haciendo clic en orden de venta...")
        
        try:
            pyautogui.click(orden_coords)
            smart_sleep(self.wait_times['page_load'])
            
            print("✅ Clic en orden de venta realizado")
            return True
            
        except Exception as e:
            print(f"❌ Error haciendo clic en orden de venta: {e}")
            return False
    
    def _find_sales_order_with_lower_threshold(self) -> tuple:
        """Busca el botón de orden de venta con umbral más bajo"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            result = cv2.matchTemplate(screenshot_cv, self.vision.sap_ventas_order_button_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            print(f"   - Confianza máxima: {max_val:.3f}")
            
            if max_val > 0.5:  # Umbral más bajo
                w = self.vision.sap_ventas_order_button_image.shape[1]
                h = self.vision.sap_ventas_order_button_image.shape[0]
                center = (max_loc[0] + w//2, max_loc[1] + h//2)
                print(f"   - Encontrado en: {center}")
                return center
            
            return None
            
        except Exception as e:
            print(f"   ❌ Error en búsqueda con umbral bajo: {e}")
            return None
    
    def _verify_modulos_menu_opened(self) -> bool:
        """Verifica que el menú de módulos se abrió"""
        # Tomar screenshot y buscar elementos del menú
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Buscar el menú de módulos abierto
            if self.vision.sap_modulos_menu_image is not None:
                result = cv2.matchTemplate(screenshot_cv, self.vision.sap_modulos_menu_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                return max_val > 0.6
            
            return True  # Si no hay imagen de referencia, asumir que se abrió
            
        except Exception as e:
            print(f"   ⚠️  Error verificando menú de módulos: {e}")
            return True
    
    def _verify_ventas_menu_opened(self) -> bool:
        """Verifica que el menú de ventas se abrió"""
        # Tomar screenshot y buscar elementos del menú de ventas
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Buscar el menú de ventas abierto
            if self.vision.sap_ventas_order_menu_image is not None:
                result = cv2.matchTemplate(screenshot_cv, self.vision.sap_ventas_order_menu_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                return max_val > 0.6
            
            return True  # Si no hay imagen de referencia, asumir que se abrió
            
        except Exception as e:
            print(f"   ⚠️  Error verificando menú de ventas: {e}")
            return True
    
    def _verify_sales_order_form(self) -> bool:
        """Verifica que llegamos al formulario de órdenes"""
        print("🔍 Verificando que llegamos al formulario de órdenes...")
        
        # Esperar un poco más para que cargue
        smart_sleep(self.wait_times['verification'])
        
        result = self.detector.detect_current_screen()
        if result.state == ScreenState.SALES_ORDER_FORM and result.confidence > 0.7:
            print(f"✅ Confirmado: Formulario de órdenes (confianza: {result.confidence:.3f})")
            return True
        else:
            print(f"❌ Estado actual: {result.state.value} (confianza: {result.confidence:.3f})")
            return False

def main():
    """Función principal"""
    print("🚀 Iniciando navegación mejorada a Orden de Venta en SAP")
    print()
    
    # Crear directorio de debug si no existe
    os.makedirs("./debug_screenshots", exist_ok=True)
    
    # Crear navegador
    navigator = ImprovedSAPNavigation()
    
    # Ejecutar navegación
    success = navigator.navigate_to_sales_order(max_attempts=3)
    
    print()
    if success:
        print("🎉 ¡Navegación completada exitosamente!")
        print("   El sistema llegó al formulario de órdenes de venta")
    else:
        print("⚠️  La navegación no fue exitosa")
        print("   Revisa los logs y screenshots para más detalles")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
