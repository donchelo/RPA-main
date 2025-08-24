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
from rpa.modules.sales_order import SalesOrderHandler
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


class RPAUnifiedInterface:
    """Interfaz unificada para todos los módulos RPA"""
    
    def __init__(self):
        self.vision = Vision()
        self.config = ConfigManager()
        self.current_module = None
        self.current_handler = None
        
        # Registrar módulos disponibles
        self.modules = {
            ModuleType.SALES_ORDER: ModuleInfo(
                name="Órdenes de Venta",
                description="Automatización de órdenes de venta en SAP Business One",
                handler_class=SalesOrderHandler,
                config_file="rpa/modules/sales_order/sales_order_config.yaml",
                test_scripts=["test_sales_order.py"],
                status="ready"
            ),
            ModuleType.PRODUCTION_ORDER: ModuleInfo(
                name="Órdenes de Producción", 
                description="Automatización de órdenes de producción en SAP Business One",
                handler_class=ProductionOrderHandler,
                config_file="rpa/modules/production_order/production_order_config.yaml",
                test_scripts=["test_production_order.py"],
                status="ready"
            )
        }
    
    def get_available_modules(self) -> List[ModuleType]:
        """Retorna la lista de módulos disponibles"""
        return list(self.modules.keys())
    
    def get_module_info(self, module_type: ModuleType) -> Optional[ModuleInfo]:
        """Obtiene información de un módulo específico"""
        return self.modules.get(module_type)
    
    def select_module(self, module_type: ModuleType) -> bool:
        """Selecciona un módulo para usar"""
        try:
            if module_type not in self.modules:
                rpa_logger.error(f"Módulo {module_type.value} no encontrado")
                return False
            
            module_info = self.modules[module_type]
            
            # Crear instancia del handler
            self.current_handler = module_info.handler_class(self.vision, self.config)
            self.current_module = module_type
            
            rpa_logger.info(f"✅ Módulo seleccionado: {module_info.name}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error seleccionando módulo {module_type.value}: {e}")
            return False
    
    def get_current_module(self) -> Optional[ModuleType]:
        """Retorna el módulo actualmente seleccionado"""
        return self.current_module
    
    def get_current_handler(self):
        """Retorna el handler del módulo actual"""
        return self.current_handler
    
    def process_file(self, file_path: str, module_type: ModuleType) -> bool:
        """Procesa un archivo JSON con el módulo especificado"""
        try:
            # Seleccionar módulo si no está seleccionado
            if self.current_module != module_type:
                if not self.select_module(module_type):
                    return False
            
            # Cargar datos del archivo
            if not os.path.exists(file_path):
                rpa_logger.error(f"Archivo no encontrado: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Procesar según el tipo de módulo
            if module_type == ModuleType.SALES_ORDER:
                return self.current_handler.process_sales_order(data)
            elif module_type == ModuleType.PRODUCTION_ORDER:
                return self.current_handler.process_production_order(data)
            else:
                rpa_logger.error(f"Tipo de módulo no soportado: {module_type.value}")
                return False
                
        except Exception as e:
            rpa_logger.error(f"Error procesando archivo {file_path}: {e}")
            return False
    
    def test_module(self, module_type: ModuleType) -> bool:
        """Ejecuta pruebas de un módulo específico"""
        try:
            if not self.select_module(module_type):
                return False
            
            return self.current_handler.test_module()
            
        except Exception as e:
            rpa_logger.error(f"Error probando módulo {module_type.value}: {e}")
            return False
    
    def get_module_status(self, module_type: ModuleType) -> Dict[str, Any]:
        """Obtiene el estado de un módulo"""
        try:
            if not self.select_module(module_type):
                return {"status": "error", "message": "No se pudo seleccionar el módulo"}
            
            module_info = self.modules[module_type]
            handler_info = self.current_handler.get_module_info()
            
            return {
                "status": "ready",
                "module_info": module_info,
                "handler_info": handler_info,
                "config_file": module_info.config_file,
                "test_scripts": module_info.test_scripts
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def validate_data(self, data: Dict[str, Any], module_type: ModuleType) -> bool:
        """Valida datos para un módulo específico"""
        try:
            if not self.select_module(module_type):
                return False
            
            # Validar según el tipo de módulo
            if module_type == ModuleType.SALES_ORDER:
                return self.current_handler._validate_sales_data(data)
            elif module_type == ModuleType.PRODUCTION_ORDER:
                return self.current_handler._validate_production_data(data)
            else:
                rpa_logger.error(f"Tipo de módulo no soportado para validación: {module_type.value}")
                return False
                
        except Exception as e:
            rpa_logger.error(f"Error validando datos: {e}")
            return False
    
    def get_supported_fields(self, module_type: ModuleType) -> List[str]:
        """Obtiene los campos soportados por un módulo"""
        try:
            if not self.select_module(module_type):
                return []
            
            handler_info = self.current_handler.get_module_info()
            return handler_info.get("supported_fields", [])
            
        except Exception as e:
            rpa_logger.error(f"Error obteniendo campos soportados: {e}")
            return []
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de procesamiento"""
        return {
            "current_module": self.current_module.value if self.current_module else None,
            "available_modules": [m.value for m in self.get_available_modules()],
            "total_modules": len(self.modules)
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
                modules = interface.get_available_modules()
                for module_type in modules:
                    module_info = interface.get_module_info(module_type)
                    status_icon = "✅" if module_info.status == "ready" else "⚠️"
                    print(f"{status_icon} {module_info.name} ({module_type.value})")
                    print(f"   {module_info.description}")
                    print(f"   Estado: {module_info.status}")
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
                module_type = interface.current_module
                
                result = interface.process_file(file_path, module_type)
                print(f"\n📊 RESULTADO:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            
            elif choice == "5":
                if interface.current_module is None:
                    print("❌ No hay módulo seleccionado")
                    continue
                
                print("\n🧪 TIPOS DE PRUEBA:")
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                test_choice = input("Selecciona tipo de prueba (1-2): ").strip()
                test_map = {"1": ModuleType.SALES_ORDER, "2": ModuleType.PRODUCTION_ORDER}
                
                if test_choice in test_map:
                    print("🚀 Ejecutando prueba...")
                    result = interface.test_module(test_map[test_choice])
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
                    # The original optimize_module method was removed from the new_code,
                    # so this part of the menu will now be empty or require a new implementation.
                    # For now, we'll just print a placeholder message.
                    print("Optimización no disponible en esta versión.")
                    # result = interface.optimize_module(module_map[module_choice]) # This line is removed
                    # print(f"\n📊 RESULTADO:")
                    # print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print("❌ Opción inválida")
            
            elif choice == "7":
                status = interface.get_processing_stats()
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
