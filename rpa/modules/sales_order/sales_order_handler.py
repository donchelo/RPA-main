"""
Handler específico para el módulo de órdenes de venta
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
from ...rpa_with_state_machine import RPAWithStateMachine


class SalesOrderHandler:
    """Manejador específico para órdenes de venta"""
    
    def __init__(self, vision_system: Vision, config: ConfigManager):
        self.vision = vision_system
        self.config = config
        self.sales_config = self._load_sales_config()
        # Usar la implementación existente del RPA
        self.rpa = RPAWithStateMachine()
        
    def _load_sales_config(self) -> Dict[str, Any]:
        """Cargar configuración específica del módulo de ventas"""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            'sales_order_config.yaml'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
                return config_data.get('sales_order', {})
        except Exception as e:
            rpa_logger.error(f"Error cargando configuración de ventas: {e}")
            return {}
    
    def navigate_to_sales_order(self) -> bool:
        """Navega al módulo de ventas y abre orden de venta"""
        try:
            rpa_logger.info("🔄 Navegando al módulo de ventas...")
            
            # Asumir que SAP ya está abierto y maximizado
            # Solo conectar al escritorio remoto
            success = self.rpa.get_remote_desktop()
            if not success:
                rpa_logger.error("❌ No se pudo conectar al escritorio remoto")
                return False
            
            # Ir directamente a la navegación de módulos (asumiendo que SAP ya está abierto)
            if not self.rpa.open_sap_orden_de_ventas():
                rpa_logger.error("❌ No se pudo abrir orden de ventas")
                return False
            
            rpa_logger.info("✅ Navegación a ventas completada")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error navegando a ventas: {e}")
            return False
    
    def process_sales_order(self, data: Dict[str, Any]) -> bool:
        """Procesa una orden de venta completa"""
        try:
            rpa_logger.info("🚀 Iniciando procesamiento de orden de venta")
            
            # Validar datos requeridos
            if not self._validate_sales_data(data):
                return False
            
            # Navegar al módulo de ventas
            if not self.navigate_to_sales_order():
                return False
            
            # Cargar NIT del comprador
            nit = data.get('comprador', {}).get('nit')
            if not nit:
                rpa_logger.error("❌ NIT del comprador no encontrado")
                return False
            
            if not self.rpa.load_nit(nit):
                rpa_logger.error("❌ Error cargando NIT")
                return False
            
            # Cargar número de orden
            orden_compra = data.get('orden_compra')
            if not orden_compra:
                rpa_logger.error("❌ Número de orden no encontrado")
                return False
            
            if not self.rpa.load_orden_compra(orden_compra):
                rpa_logger.error("❌ Error cargando orden de compra")
                return False
            
            # Cargar fecha de entrega
            fecha_entrega = data.get('fecha_entrega')
            if not fecha_entrega:
                rpa_logger.error("❌ Fecha de entrega no encontrada")
                return False
            
            if not self.rpa.load_fecha_entrega(fecha_entrega):
                rpa_logger.error("❌ Error cargando fecha de entrega")
                return False
            
            # Cargar items
            items = data.get('items', [])
            if not items:
                rpa_logger.error("❌ No se encontraron items para cargar")
                return False
            
            if not self.rpa.load_items(items):
                rpa_logger.error("❌ Error cargando items")
                return False
            
            # Tomar screenshot final
            if not self.rpa.take_screenshot():
                rpa_logger.error("❌ Error tomando screenshot")
                return False
            
            rpa_logger.info("✅ Orden de venta procesada exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error procesando orden de venta: {e}")
            return False
    
    def _validate_sales_data(self, data: Dict[str, Any]) -> bool:
        """Valida que los datos de la orden de venta sean correctos"""
        required_fields = ['comprador', 'orden_compra', 'fecha_entrega', 'items']
        
        for field in required_fields:
            if field not in data:
                rpa_logger.error(f"❌ Campo requerido faltante: {field}")
                return False
        
        # Validar comprador
        comprador = data.get('comprador', {})
        if not comprador.get('nit'):
            rpa_logger.error("❌ NIT del comprador es requerido")
            return False
        
        # Validar items
        items = data.get('items', [])
        if not items:
            rpa_logger.error("❌ Al menos un item es requerido")
            return False
        
        for i, item in enumerate(items):
            if not item.get('codigo'):
                rpa_logger.error(f"❌ Código del item {i+1} es requerido")
                return False
            if not item.get('cantidad'):
                rpa_logger.error(f"❌ Cantidad del item {i+1} es requerida")
                return False
        
        return True
    
    def get_module_info(self) -> Dict[str, Any]:
        """Retorna información del módulo"""
        return {
            "name": "Órdenes de Venta",
            "description": "Automatización de órdenes de venta en SAP Business One",
            "version": "1.0.0",
            "status": "ready",
            "supported_fields": [
                "comprador.nit",
                "comprador.nombre", 
                "orden_compra",
                "fecha_entrega",
                "items.codigo",
                "items.cantidad",
                "items.precio_unitario"
            ]
        }
    
    def test_module(self) -> bool:
        """Ejecuta pruebas del módulo"""
        try:
            rpa_logger.info("🧪 Iniciando pruebas del módulo de ventas...")
            
            # Probar navegación
            if not self.navigate_to_sales_order():
                rpa_logger.error("❌ Prueba de navegación falló")
                return False
            
            rpa_logger.info("✅ Pruebas del módulo de ventas completadas")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error en pruebas del módulo: {e}")
            return False
