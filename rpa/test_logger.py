#!/usr/bin/env python3
"""
Script de prueba para el sistema de logs MVP de RPA
"""

import time
import random
from logger import rpa_logger

def test_basic_logging():
    """Prueba el logging básico"""
    print("=== Prueba de logging básico ===")
    
    rpa_logger.info("Iniciando pruebas del sistema de logs")
    rpa_logger.debug("Mensaje de debug - solo visible en archivo")
    rpa_logger.warning("Advertencia: esto es una prueba")
    rpa_logger.error("Error simulado para pruebas")
    rpa_logger.critical("Error crítico simulado")

def test_action_logging():
    """Prueba el logging de acciones específicas"""
    print("=== Prueba de logging de acciones ===")
    
    rpa_logger.log_action("Inicio de sesión SAP", "Usuario: admin")
    rpa_logger.log_action("Navegación a módulo ventas", "Menú: Ventas > Órdenes")
    rpa_logger.log_action("Carga de datos de cliente", "NIT: 12345678-9")
    rpa_logger.log_action("Procesamiento de items", "Total: 5 items")

def test_error_logging():
    """Prueba el logging de errores"""
    print("=== Prueba de logging de errores ===")
    
    try:
        # Simular un error
        raise ValueError("Error simulado para pruebas de logging")
    except Exception as e:
        rpa_logger.log_error(f"Error en procesamiento: {str(e)}", "Contexto: prueba de errores")

def test_performance_logging():
    """Prueba el logging de rendimiento"""
    print("=== Prueba de logging de rendimiento ===")
    
    # Simular operaciones con diferentes duraciones
    operations = [
        ("Carga de NIT", 2.5),
        ("Procesamiento de items", 8.3),
        ("Guardado de orden", 1.2),
        ("Conexión remota", 5.7)
    ]
    
    for operation, duration in operations:
        rpa_logger.log_performance(operation, duration)
        time.sleep(0.1)  # Pequeña pausa para diferenciar timestamps

def test_simulation():
    """Simula un flujo completo de RPA con logging"""
    print("=== Simulación de flujo RPA completo ===")
    
    rpa_logger.log_action("Iniciando simulación RPA", "Proceso completo de orden de ventas")
    
    # Simular pasos del proceso
    steps = [
        ("Conexión al escritorio remoto", 3.2),
        ("Apertura de SAP", 4.1),
        ("Navegación a módulo ventas", 2.8),
        ("Carga de datos del cliente", 1.5),
        ("Procesamiento de 3 items", 12.3),
        ("Guardado de orden", 2.1),
        ("Cierre de SAP", 1.8)
    ]
    
    total_start_time = time.time()
    
    for step_name, step_duration in steps:
        step_start = time.time()
        rpa_logger.log_action(f"Iniciando: {step_name}", "Paso del proceso RPA")
        
        # Simular duración del paso
        time.sleep(0.1)  # Solo para la simulación
        
        step_actual_duration = time.time() - step_start
        rpa_logger.log_performance(step_name, step_actual_duration)
        rpa_logger.log_action(f"Completado: {step_name}", "Paso exitoso")
    
    total_duration = time.time() - total_start_time
    rpa_logger.log_performance("Proceso RPA completo", total_duration)
    rpa_logger.log_action("Simulación RPA completada", "Todos los pasos exitosos")

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema de logs MVP para RPA")
    print("=" * 60)
    
    try:
        test_basic_logging()
        print()
        
        test_action_logging()
        print()
        
        test_error_logging()
        print()
        
        test_performance_logging()
        print()
        
        test_simulation()
        print()
        
        print("✅ Todas las pruebas completadas exitosamente")
        print("📁 Revisa el directorio 'logs' para ver los archivos generados")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")
        rpa_logger.log_error(f"Error en pruebas: {str(e)}", "Función main")

if __name__ == "__main__":
    main() 