#!/usr/bin/env python3
"""
Interfaz Unificada RPA - Sistema Centralizado de Automatización
Integra todos los módulos RPA en una sola interfaz fácil de usar
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.config_manager import ConfigManager
from rpa.simple_logger import rpa_logger
from rpa.modules.production_order import ProductionOrderHandler


class ModuleType(Enum):
    """Tipos de módulos disponibles"""
    SALES_ORDER = "sales_order"
    PRODUCTION_ORDER = "production_order"


@dataclass
class ModuleInfo:
    """Información de un módulo RPA"""
    name: str
    description: str
    handler_class: Any
    config_file: str
    test_scripts: List[str]
    status: str = "ready"


class SalesOrderHandler:
    """Handler para el módulo de órdenes de venta (implementación existente)"""
    
    def __init__(self, vision_system: Vision, config: ConfigManager):
        self.vision = vision_system
        self.config = config
        # Importar la clase RPA existente que maneja órdenes de venta
        from rpa.rpa_with_state_machine import RPAWithStateMachine
        self.rpa = RPAWithStateMachine()
    
    def process_sales_order(self, data: Dict[str, Any], auto_confirm: bool = False) -> bool:
        """Procesa una orden de venta usando la implementación existente"""
        try:
            rpa_logger.info("🚀 Iniciando procesamiento de orden de venta")
            
            # Validar datos requeridos
            required_fields = ['comprador', 'orden', 'items']
            for field in required_fields:
                if field not in data:
                    rpa_logger.error(f"Campo requerido faltante: {field}")
                    return False
            
            # Navegar a SAP y abrir orden de ventas
            if not self.rpa.open_sap_orden_de_ventas():
                rpa_logger.error("No se pudo abrir SAP orden de ventas")
                return False
            
            # Cargar NIT del comprador
            nit = data['comprador'].get('nit')
            if not nit:
                rpa_logger.error("NIT del comprador no encontrado")
                return False
            
            self.rpa.load_nit(nit)
            
            # Cargar número de orden
            numero_orden = data['orden'].get('numero')
            if not numero_orden:
                rpa_logger.error("Número de orden no encontrado")
                return False
            
            self.rpa.load_orden_compra(numero_orden)
            
            # Cargar fechas
            fecha_entrega = data['orden'].get('fecha_entrega')
            fecha_documento = data['orden'].get('fecha_documento')
            if not fecha_entrega:
                rpa_logger.error("Fecha de entrega no encontrada")
                return False
            
            self.rpa.load_fecha_entrega(fecha_entrega, fecha_documento)
            
            # Cargar items
            items = data.get('items', [])
            if not items:
                rpa_logger.error("No se encontraron items para cargar")
                return False
            
            self.rpa.load_items(items)
            
            # Tomar screenshot final
            rpa_logger.info("📸 Tomando screenshot final...")
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"./screenshots/ventas_final_{timestamp}.png"
                
                # Crear directorio si no existe
                os.makedirs("./screenshots", exist_ok=True)
                
                screenshot.save(screenshot_path)
                rpa_logger.info(f"✅ Screenshot guardado: {screenshot_path}")
            except Exception as e:
                rpa_logger.warning(f"⚠️ Error tomando screenshot: {e}")
            
            rpa_logger.info("✅ Orden de venta procesada exitosamente")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error procesando orden de venta: {e}")
            return False


class RPAUnifiedInterface:
    """Interfaz unificada para todos los módulos RPA"""
    
    def __init__(self):
        self.vision = Vision()
        self.config = ConfigManager()
        self.modules: Dict[ModuleType, ModuleInfo] = {}
        self.current_module: Optional[ModuleType] = None
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Inicializa todos los módulos disponibles"""
        self.modules = {
            ModuleType.SALES_ORDER: ModuleInfo(
                name="Órdenes de Venta",
                description="Automatización de creación de órdenes de venta en SAP (implementación existente)",
                handler_class=SalesOrderHandler,
                config_file="config.yaml",
                test_scripts=[
                    "test_flujo_completo_corregido.py",
                    "test_flujo_final_corregido.py"
                ],
                status="ready"
            ),
            ModuleType.PRODUCTION_ORDER: ModuleInfo(
                name="Órdenes de Producción",
                description="Automatización de creación de órdenes de producción en SAP",
                handler_class=ProductionOrderHandler,
                config_file="rpa/modules/production_order/production_order_config.yaml",
                test_scripts=[
                    "test_produccion_real.py",
                    "test_produccion_ficticia.py",
                    "test_rapido_produccion.py"
                ],
                status="ready"
            ),

        }
    
    def list_modules(self) -> Dict[str, Any]:
        """Lista todos los módulos disponibles con su estado"""
        modules_info = {}
        
        for module_type, module_info in self.modules.items():
            modules_info[module_type.value] = {
                "name": module_info.name,
                "description": module_info.description,
                "status": module_info.status,
                "config_file": module_info.config_file,
                "test_scripts": module_info.test_scripts
            }
        
        return modules_info
    
    def get_module_status(self, module_type: ModuleType) -> Dict[str, Any]:
        """Obtiene el estado detallado de un módulo específico"""
        if module_type not in self.modules:
            return {"error": "Módulo no encontrado"}
        
        module_info = self.modules[module_type]
        
        # Verificar si el archivo de configuración existe
        config_exists = os.path.exists(module_info.config_file)
        
        # Verificar si los scripts de prueba existen
        test_scripts_status = {}
        for script in module_info.test_scripts:
            test_scripts_status[script] = os.path.exists(script)
        
        return {
            "name": module_info.name,
            "description": module_info.description,
            "status": module_info.status,
            "config_file": {
                "path": module_info.config_file,
                "exists": config_exists
            },
            "test_scripts": test_scripts_status,
            "handler_available": module_info.handler_class is not None
        }
    
    def select_module(self, module_type: ModuleType) -> bool:
        """Selecciona un módulo para usar"""
        if module_type not in self.modules:
            rpa_logger.error(f"Módulo {module_type.value} no encontrado")
            return False
        
        module_info = self.modules[module_type]
        
        if module_info.status != "ready":
            rpa_logger.error(f"Módulo {module_info.name} no está listo (status: {module_info.status})")
            return False
        
        if module_info.handler_class is None:
            rpa_logger.error(f"Handler para {module_info.name} no está implementado")
            return False
        
        self.current_module = module_type
        rpa_logger.info(f"✅ Módulo seleccionado: {module_info.name}")
        return True
    
    def get_current_module_handler(self):
        """Obtiene el handler del módulo actualmente seleccionado"""
        if self.current_module is None:
            rpa_logger.error("No hay módulo seleccionado")
            return None
        
        module_info = self.modules[self.current_module]
        
        if module_info.handler_class is None:
            rpa_logger.error(f"Handler no disponible para {module_info.name}")
            return None
        
        return module_info.handler_class(self.vision, self.config)
    
    def process_file(self, file_path: str, auto_confirm: bool = False) -> Dict[str, Any]:
        """Procesa un archivo JSON con el módulo seleccionado"""
        if self.current_module is None:
            return {"error": "No hay módulo seleccionado"}
        
        try:
            # Cargar datos del archivo
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Obtener handler del módulo
            handler = self.get_current_module_handler()
            if handler is None:
                return {"error": "No se pudo obtener el handler del módulo"}
            
            # Procesar según el tipo de módulo
            if self.current_module == ModuleType.SALES_ORDER:
                success = handler.process_sales_order(data, auto_confirm)
                return {
                    "success": success,
                    "module": "sales_order",
                    "file": file_path,
                    "message": "Orden de venta procesada" if success else "Error procesando orden de venta"
                }
            
            elif self.current_module == ModuleType.PRODUCTION_ORDER:
                success = handler.process_production_order(data, auto_click_crear=not auto_confirm)
                return {
                    "success": success,
                    "module": "production_order",
                    "file": file_path,
                    "message": "Orden de producción procesada" if success else "Error procesando orden de producción"
                }
            
            else:
                return {"error": f"Módulo {self.current_module.value} no soportado para procesamiento"}
                
        except FileNotFoundError:
            return {"error": f"Archivo no encontrado: {file_path}"}
        except json.JSONDecodeError:
            return {"error": f"Archivo JSON inválido: {file_path}"}
        except Exception as e:
            return {"error": f"Error procesando archivo: {str(e)}"}
    
    def run_test(self, test_type: str = "real") -> Dict[str, Any]:
        """Ejecuta una prueba del módulo seleccionado"""
        if self.current_module is None:
            return {"error": "No hay módulo seleccionado"}
        
        module_info = self.modules[self.current_module]
        
        # Determinar script de prueba
        test_script = None
        if test_type == "real":
            test_script = next((s for s in module_info.test_scripts if "real" in s or "flujo" in s), None)
        elif test_type == "ficticio":
            test_script = next((s for s in module_info.test_scripts if "fictici" in s), None)
        elif test_type == "rapido":
            test_script = next((s for s in module_info.test_scripts if "rapido" in s), None)
        
        if not test_script or not os.path.exists(test_script):
            return {"error": f"Script de prueba '{test_type}' no encontrado"}
        
        try:
            # Ejecutar script de prueba
            import subprocess
            result = subprocess.run([sys.executable, test_script], 
                                  capture_output=True, text=True, timeout=300)
            
            return {
                "success": result.returncode == 0,
                "script": test_script,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"error": f"Prueba excedió el tiempo límite (5 minutos)"}
        except Exception as e:
            return {"error": f"Error ejecutando prueba: {str(e)}"}
    
    def optimize_module(self, module_type: ModuleType) -> Dict[str, Any]:
        """Optimiza la configuración de un módulo específico"""
        if module_type == ModuleType.PRODUCTION_ORDER:
            try:
                import subprocess
                result = subprocess.run([sys.executable, "optimizar_produccion.py"], 
                                      capture_output=True, text=True, timeout=60)
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "return_code": result.returncode
                }
            except Exception as e:
                return {"error": f"Error optimizando módulo: {str(e)}"}
        else:
            return {"error": f"Optimización no disponible para {module_type.value}"}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado general del sistema"""
        return {
            "current_module": self.current_module.value if self.current_module else None,
            "modules_available": len([m for m in self.modules.values() if m.status == "ready"]),
            "modules_total": len(self.modules),
            "vision_system": "ready",
            "config_manager": "ready",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }


def main():
    """Función principal - Interfaz de línea de comandos"""
    print("🚀 INTERFAZ UNIFICADA RPA")
    print("=" * 50)
    
    interface = RPAUnifiedInterface()
    
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Listar módulos disponibles")
        print("2. Ver estado de un módulo")
        print("3. Seleccionar módulo")
        print("4. Procesar archivo JSON")
        print("5. Ejecutar prueba")
        print("6. Optimizar módulo")
        print("7. Estado del sistema")
        print("8. Salir")
        
        try:
            choice = input("\n🎯 Selecciona una opción (1-8): ").strip()
            
            if choice == "1":
                print("\n📦 MÓDULOS DISPONIBLES:")
                modules = interface.list_modules()
                for module_id, module_info in modules.items():
                    status_icon = "✅" if module_info["status"] == "ready" else "⚠️"
                    print(f"{status_icon} {module_info['name']} ({module_id})")
                    print(f"   {module_info['description']}")
                    print(f"   Estado: {module_info['status']}")
                    print()
            
            elif choice == "2":
                print("\n🔍 VER ESTADO DE MÓDULO:")
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    status = interface.get_module_status(module_map[module_choice])
                    print(f"\n📊 ESTADO DEL MÓDULO:")
                    print(json.dumps(status, indent=2, ensure_ascii=False))
                else:
                    print("❌ Opción inválida")
            
            elif choice == "3":
                print("\n🎯 SELECCIONAR MÓDULO:")
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    success = interface.select_module(module_map[module_choice])
                    if success:
                        print("✅ Módulo seleccionado exitosamente")
                    else:
                        print("❌ Error seleccionando módulo")
                else:
                    print("❌ Opción inválida")
            
            elif choice == "4":
                if interface.current_module is None:
                    print("❌ No hay módulo seleccionado")
                    continue
                
                file_path = input("📁 Ruta del archivo JSON: ").strip()
                auto_confirm = input("🤖 Confirmación automática? (s/n): ").strip().lower() == 's'
                
                result = interface.process_file(file_path, auto_confirm)
                print(f"\n📊 RESULTADO:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            
            elif choice == "5":
                if interface.current_module is None:
                    print("❌ No hay módulo seleccionado")
                    continue
                
                print("\n🧪 TIPOS DE PRUEBA:")
                print("1. Prueba real")
                print("2. Prueba ficticia")
                print("3. Prueba rápida")
                
                test_choice = input("Selecciona tipo de prueba (1-3): ").strip()
                test_map = {"1": "real", "2": "ficticio", "3": "rapido"}
                
                if test_choice in test_map:
                    print("🚀 Ejecutando prueba...")
                    result = interface.run_test(test_map[test_choice])
                    print(f"\n📊 RESULTADO:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print("❌ Opción inválida")
            
            elif choice == "6":
                print("\n⚡ OPTIMIZAR MÓDULO:")
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    print("🔧 Optimizando módulo...")
                    result = interface.optimize_module(module_map[module_choice])
                    print(f"\n📊 RESULTADO:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print("❌ Opción inválida")
            
            elif choice == "7":
                status = interface.get_system_status()
                print(f"\n📊 ESTADO DEL SISTEMA:")
                print(json.dumps(status, indent=2, ensure_ascii=False))
            
            elif choice == "8":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
