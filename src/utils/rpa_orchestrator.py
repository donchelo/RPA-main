#!/usr/bin/env python3
"""
Orquestador Central RPA - Sistema de Gestión Unificada
Coordina todos los módulos RPA y proporciona una interfaz centralizada
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
from rpa.state_machine import StateMachine, RPAState, RPAEvent, StateContext
from rpa_unified_interface import RPAUnifiedInterface, ModuleType


class ProcessType(Enum):
    """Tipos de procesos disponibles"""
    SINGLE_FILE = "single_file"
    BATCH_PROCESSING = "batch_processing"
    MONITORING = "monitoring"
    TESTING = "testing"


@dataclass
class ProcessRequest:
    """Solicitud de procesamiento"""
    module_type: ModuleType
    file_path: str
    auto_confirm: bool = False
    priority: int = 1
    metadata: Dict[str, Any] = None


@dataclass
class ProcessResult:
    """Resultado de un proceso"""
    success: bool
    module_type: ModuleType
    file_path: str
    start_time: float
    end_time: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


class RPAOrchestrator:
    """Orquestador central para todos los módulos RPA"""
    
    def __init__(self):
        self.interface = RPAUnifiedInterface()
        self.state_machine = StateMachine()
        self.vision = Vision()
        self.config = ConfigManager()
        
        # Cola de procesos
        self.process_queue: List[ProcessRequest] = []
        self.processed_files: List[ProcessResult] = []
        self.failed_files: List[ProcessResult] = []
        
        # Estadísticas
        self.stats = {
            "total_processed": 0,
            "total_successful": 0,
            "total_failed": 0,
            "total_duration": 0.0,
            "start_time": time.time()
        }
    
    def add_process_request(self, request: ProcessRequest) -> bool:
        """Agrega una solicitud de procesamiento a la cola"""
        try:
            # Validar que el archivo existe
            if not os.path.exists(request.file_path):
                rpa_logger.error(f"Archivo no encontrado: {request.file_path}")
                return False
            
            # Validar que el módulo está disponible
            if not self.interface.select_module(request.module_type):
                rpa_logger.error(f"Módulo {request.module_type.value} no disponible")
                return False
            
            # Agregar a la cola
            self.process_queue.append(request)
            rpa_logger.info(f"✅ Solicitud agregada: {request.file_path} ({request.module_type.value})")
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error agregando solicitud: {e}")
            return False
    
    def process_single_file(self, request: ProcessRequest) -> ProcessResult:
        """Procesa un archivo individual"""
        start_time = time.time()
        result = ProcessResult(
            success=False,
            module_type=request.module_type,
            file_path=request.file_path,
            start_time=start_time,
            end_time=start_time,
            metadata=request.metadata or {}
        )
        
        try:
            rpa_logger.info(f"🚀 Procesando: {request.file_path}")
            
            # Seleccionar módulo
            if not self.interface.select_module(request.module_type):
                result.error_message = f"Módulo {request.module_type.value} no disponible"
                return result
            
            # Procesar archivo
            process_result = self.interface.process_file(request.file_path, request.auto_confirm)
            
            # Actualizar resultado
            result.success = process_result.get("success", False)
            result.end_time = time.time()
            
            if not result.success:
                result.error_message = process_result.get("error", "Error desconocido")
                rpa_logger.error(f"❌ Error procesando {request.file_path}: {result.error_message}")
            else:
                rpa_logger.info(f"✅ Procesado exitosamente: {request.file_path} ({result.duration:.2f}s)")
            
            return result
            
        except Exception as e:
            result.end_time = time.time()
            result.error_message = str(e)
            rpa_logger.error(f"❌ Excepción procesando {request.file_path}: {e}")
            return result
    
    def process_batch(self, requests: List[ProcessRequest]) -> List[ProcessResult]:
        """Procesa un lote de archivos"""
        results = []
        
        rpa_logger.info(f"🔄 Iniciando procesamiento por lotes: {len(requests)} archivos")
        
        for i, request in enumerate(requests, 1):
            rpa_logger.info(f"📋 Procesando {i}/{len(requests)}: {request.file_path}")
            
            result = self.process_single_file(request)
            results.append(result)
            
            # Actualizar estadísticas
            self.stats["total_processed"] += 1
            if result.success:
                self.stats["total_successful"] += 1
                self.processed_files.append(result)
            else:
                self.stats["total_failed"] += 1
                self.failed_files.append(result)
            
            self.stats["total_duration"] += result.duration
            
            # Pausa entre archivos para evitar sobrecarga
            if i < len(requests):
                time.sleep(1.0)
        
        rpa_logger.info(f"✅ Procesamiento por lotes completado: {len(results)} archivos")
        return results
    
    def monitor_directory(self, directory: str, module_type: ModuleType, 
                         file_pattern: str = "*.json", auto_confirm: bool = False) -> None:
        """Monitorea un directorio para procesar archivos automáticamente"""
        rpa_logger.info(f"👁️ Iniciando monitoreo: {directory}")
        
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class FileHandler(FileSystemEventHandler):
                def __init__(self, orchestrator, module_type, auto_confirm):
                    self.orchestrator = orchestrator
                    self.module_type = module_type
                    self.auto_confirm = auto_confirm
                
                def on_created(self, event):
                    if not event.is_directory and event.src_path.endswith('.json'):
                        rpa_logger.info(f"📁 Nuevo archivo detectado: {event.src_path}")
                        
                        request = ProcessRequest(
                            module_type=self.module_type,
                            file_path=event.src_path,
                            auto_confirm=self.auto_confirm
                        )
                        
                        # Procesar después de un pequeño delay para asegurar que el archivo esté completo
                        time.sleep(2.0)
                        self.orchestrator.add_process_request(request)
            
            # Configurar observador
            event_handler = FileHandler(self, module_type, auto_confirm)
            observer = Observer()
            observer.schedule(event_handler, directory, recursive=False)
            observer.start()
            
            rpa_logger.info(f"✅ Monitoreo iniciado en: {directory}")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                rpa_logger.info("🛑 Monitoreo detenido")
            
            observer.join()
            
        except ImportError:
            rpa_logger.error("❌ watchdog no instalado. Instalar con: pip install watchdog")
        except Exception as e:
            rpa_logger.error(f"❌ Error en monitoreo: {e}")
    
    def run_tests(self, module_type: ModuleType, test_type: str = "real") -> Dict[str, Any]:
        """Ejecuta pruebas para un módulo específico"""
        rpa_logger.info(f"🧪 Ejecutando pruebas: {module_type.value} ({test_type})")
        
        if not self.interface.select_module(module_type):
            return {"error": f"Módulo {module_type.value} no disponible"}
        
        result = self.interface.run_test(test_type)
        
        if result.get("success"):
            rpa_logger.info(f"✅ Pruebas exitosas: {module_type.value}")
        else:
            rpa_logger.error(f"❌ Pruebas fallidas: {module_type.value}")
        
        return result
    
    def optimize_system(self) -> Dict[str, Any]:
        """Optimiza todo el sistema RPA"""
        rpa_logger.info("⚡ Iniciando optimización del sistema")
        
        results = {}
        
        # Optimizar módulo de producción
        if ModuleType.PRODUCTION_ORDER in self.interface.modules:
            results["production_order"] = self.interface.optimize_module(ModuleType.PRODUCTION_ORDER)
        
        # TODO: Agregar optimización para otros módulos cuando estén disponibles
        
        rpa_logger.info("✅ Optimización del sistema completada")
        return results
    
    def get_system_health(self) -> Dict[str, Any]:
        """Obtiene el estado de salud del sistema"""
        return {
            "orchestrator": {
                "status": "running",
                "queue_size": len(self.process_queue),
                "processed_files": len(self.processed_files),
                "failed_files": len(self.failed_files)
            },
            "interface": self.interface.get_system_status(),
            "statistics": {
                "total_processed": self.stats["total_processed"],
                "total_successful": self.stats["total_successful"],
                "total_failed": self.stats["total_failed"],
                "success_rate": (self.stats["total_successful"] / max(self.stats["total_processed"], 1)) * 100,
                "average_duration": self.stats["total_duration"] / max(self.stats["total_processed"], 1),
                "uptime": time.time() - self.stats["start_time"]
            },
            "modules": self.interface.list_modules(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_report(self, output_file: str = "rpa_report.json") -> bool:
        """Genera un reporte completo del sistema"""
        try:
            report = {
                "system_health": self.get_system_health(),
                "processed_files": [
                    {
                        "file": result.file_path,
                        "module": result.module_type.value,
                        "success": result.success,
                        "duration": result.duration,
                        "error": result.error_message
                    }
                    for result in self.processed_files
                ],
                "failed_files": [
                    {
                        "file": result.file_path,
                        "module": result.module_type.value,
                        "error": result.error_message,
                        "duration": result.duration
                    }
                    for result in self.failed_files
                ],
                "queue": [
                    {
                        "file": request.file_path,
                        "module": request.module_type.value,
                        "priority": request.priority
                    }
                    for request in self.process_queue
                ]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            rpa_logger.info(f"✅ Reporte generado: {output_file}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"❌ Error generando reporte: {e}")
            return False


def main():
    """Función principal - Interfaz de línea de comandos del orquestador"""
    print("🎼 ORQUESTADOR CENTRAL RPA")
    print("=" * 50)
    
    orchestrator = RPAOrchestrator()
    
    while True:
        print("\n🎯 MENÚ DEL ORQUESTADOR")
        print("1. Estado del sistema")
        print("2. Procesar archivo individual")
        print("3. Procesar lote de archivos")
        print("4. Monitorear directorio")
        print("5. Ejecutar pruebas")
        print("6. Optimizar sistema")
        print("7. Generar reporte")
        print("8. Salir")
        
        try:
            choice = input("\n🎼 Selecciona una opción (1-8): ").strip()
            
            if choice == "1":
                health = orchestrator.get_system_health()
                print(f"\n📊 ESTADO DEL SISTEMA:")
                print(json.dumps(health, indent=2, ensure_ascii=False))
            
            elif choice == "2":
                print("\n📁 PROCESAR ARCHIVO INDIVIDUAL:")
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    file_path = input("📁 Ruta del archivo JSON: ").strip()
                    auto_confirm = input("🤖 Confirmación automática? (s/n): ").strip().lower() == 's'
                    
                    request = ProcessRequest(
                        module_type=module_map[module_choice],
                        file_path=file_path,
                        auto_confirm=auto_confirm
                    )
                    
                    result = orchestrator.process_single_file(request)
                    print(f"\n📊 RESULTADO:")
                    print(f"✅ Éxito: {result.success}")
                    print(f"⏱️ Duración: {result.duration:.2f}s")
                    if result.error_message:
                        print(f"❌ Error: {result.error_message}")
                else:
                    print("❌ Opción inválida")
            
            elif choice == "3":
                print("\n📦 PROCESAR LOTE DE ARCHIVOS:")
                directory = input("📁 Directorio con archivos JSON: ").strip()
                
                if not os.path.exists(directory):
                    print("❌ Directorio no encontrado")
                    continue
                
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    auto_confirm = input("🤖 Confirmación automática? (s/n): ").strip().lower() == 's'
                    
                    # Buscar archivos JSON
                    json_files = list(Path(directory).glob("*.json"))
                    
                    if not json_files:
                        print("❌ No se encontraron archivos JSON")
                        continue
                    
                    print(f"📋 Encontrados {len(json_files)} archivos")
                    
                    requests = []
                    for json_file in json_files:
                        request = ProcessRequest(
                            module_type=module_map[module_choice],
                            file_path=str(json_file),
                            auto_confirm=auto_confirm
                        )
                        requests.append(request)
                    
                    results = orchestrator.process_batch(requests)
                    
                    successful = sum(1 for r in results if r.success)
                    print(f"\n📊 RESULTADO DEL LOTE:")
                    print(f"✅ Exitosos: {successful}/{len(results)}")
                    print(f"❌ Fallidos: {len(results) - successful}")
                    
                else:
                    print("❌ Opción inválida")
            
            elif choice == "4":
                print("\n👁️ MONITOREAR DIRECTORIO:")
                directory = input("📁 Directorio a monitorear: ").strip()
                
                if not os.path.exists(directory):
                    print("❌ Directorio no encontrado")
                    continue
                
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    auto_confirm = input("🤖 Confirmación automática? (s/n): ").strip().lower() == 's'
                    
                    print("👁️ Iniciando monitoreo... (Ctrl+C para detener)")
                    orchestrator.monitor_directory(directory, module_map[module_choice], auto_confirm=auto_confirm)
                else:
                    print("❌ Opción inválida")
            
            elif choice == "5":
                print("\n🧪 EJECUTAR PRUEBAS:")
                print("1. Órdenes de Venta")
                print("2. Órdenes de Producción")
                
                module_choice = input("Selecciona módulo (1-2): ").strip()
                module_map = {
                    "1": ModuleType.SALES_ORDER,
                    "2": ModuleType.PRODUCTION_ORDER
                }
                
                if module_choice in module_map:
                    print("1. Prueba real")
                    print("2. Prueba ficticia")
                    print("3. Prueba rápida")
                    
                    test_choice = input("Selecciona tipo de prueba (1-3): ").strip()
                    test_map = {"1": "real", "2": "ficticio", "3": "rapido"}
                    
                    if test_choice in test_map:
                        result = orchestrator.run_tests(module_map[module_choice], test_map[test_choice])
                        print(f"\n📊 RESULTADO:")
                        print(json.dumps(result, indent=2, ensure_ascii=False))
                    else:
                        print("❌ Opción inválida")
                else:
                    print("❌ Opción inválida")
            
            elif choice == "6":
                print("⚡ Optimizando sistema...")
                results = orchestrator.optimize_system()
                print(f"\n📊 RESULTADO:")
                print(json.dumps(results, indent=2, ensure_ascii=False))
            
            elif choice == "7":
                output_file = input("📄 Nombre del archivo de reporte (rpa_report.json): ").strip()
                if not output_file:
                    output_file = "rpa_report.json"
                
                success = orchestrator.generate_report(output_file)
                if success:
                    print(f"✅ Reporte generado: {output_file}")
                else:
                    print("❌ Error generando reporte")
            
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
