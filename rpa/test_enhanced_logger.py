"""
Script de prueba para el sistema de logs mejorado RPA
"""

import time
import random
from datetime import datetime, timedelta
import json

from rpa.logger import rpa_logger
from rpa.log_monitor import LogMonitor, LogDashboard
from rpa.log_utils import LogUtils

def test_enhanced_logging():
    """Prueba las nuevas funcionalidades de logging"""
    print("=== PRUEBA DEL SISTEMA DE LOGS MEJORADO ===\n")
    
    # 1. Probar logging con contexto
    print("1. Probando logging con contexto...")
    rpa_logger.info("Iniciando prueba del sistema mejorado", {
        'test_type': 'enhanced_logging',
        'timestamp': datetime.now().isoformat()
    })
    
    # 2. Probar logging de acciones con métricas
    print("2. Probando logging de acciones con métricas...")
    
    # Simular carga de NIT
    start_time = rpa_logger.log_action("Carga de NIT", "NIT: 12345678-9", "load_nit")
    time.sleep(2)  # Simular procesamiento
    rpa_logger.log_action_complete("Carga de NIT", start_time, True, "NIT cargado exitosamente", "load_nit")
    
    # Simular carga de orden de compra
    start_time = rpa_logger.log_action("Carga de orden de compra", "Orden: 4500339540", "load_order")
    time.sleep(1.5)  # Simular procesamiento
    rpa_logger.log_action_complete("Carga de orden de compra", start_time, True, "Orden cargada", "load_order")
    
    # Simular error
    start_time = rpa_logger.log_action("Conexión SAP", "Intentando conectar", "sap_connection")
    time.sleep(1)
    rpa_logger.log_action_complete("Conexión SAP", start_time, False, "Error de conexión", "sap_connection")
    rpa_logger.log_error("Error de conexión SAP", "Timeout en conexión", "sap_connection")
    
    # 3. Probar logging de rendimiento
    print("3. Probando logging de rendimiento...")
    rpa_logger.log_performance("Procesamiento de items", 15.5, {
        'items_count': 5,
        'avg_time_per_item': 3.1
    })
    
    # 4. Probar métricas
    print("4. Probando métricas...")
    metrics_summary = rpa_logger.get_metrics_summary()
    print(f"Resumen de métricas: {json.dumps(metrics_summary, indent=2, ensure_ascii=False)}")
    
    # 5. Probar utilidades de logs
    print("5. Probando utilidades de logs...")
    utils = LogUtils()
    
    # Analizar patrones
    analysis = utils.analyze_log_patterns(1)  # Última hora
    print(f"Análisis de patrones: {json.dumps(analysis, indent=2, ensure_ascii=False)}")
    
    # Generar reporte
    report = utils.generate_log_report('hourly')
    print(f"Reporte generado: {json.dumps(report, indent=2, ensure_ascii=False)}")
    
    # 6. Probar monitor (opcional)
    print("6. Probando monitor de logs...")
    try:
        monitor = LogMonitor()
        dashboard = LogDashboard(monitor)
        
        # Crear dashboard
        fig = dashboard.create_dashboard()
        if fig:
            dashboard.save_dashboard("test_dashboard.png")
            print("Dashboard creado exitosamente: test_dashboard.png")
        
    except Exception as e:
        print(f"Error en monitor: {e}")
    
    print("\n=== PRUEBA COMPLETADA ===")

def test_error_scenarios():
    """Prueba escenarios de error"""
    print("\n=== PRUEBA DE ESCENARIOS DE ERROR ===\n")
    
    # Simular diferentes tipos de errores
    error_scenarios = [
        ("SAP_NOT_FOUND", "Icono de SAP Business One no encontrado"),
        ("RDP_CONNECTION", "Ventana de escritorio remoto no encontrada"),
        ("JSON_PARSING", "Error decodificando archivo JSON"),
        ("TIMEOUT", "Timeout en operación de carga"),
        ("PERMISSION", "Error de permisos al acceder al archivo")
    ]
    
    for error_type, error_message in error_scenarios:
        print(f"Simulando error: {error_type}")
        rpa_logger.log_error(error_message, f"Contexto de {error_type}", error_type.lower())
        time.sleep(0.5)
    
    print("Escenarios de error completados")

def test_performance_monitoring():
    """Prueba monitoreo de rendimiento"""
    print("\n=== PRUEBA DE MONITOREO DE RENDIMIENTO ===\n")
    
    operations = [
        ("Carga de NIT", 2.5),
        ("Carga de orden de compra", 1.8),
        ("Carga de fecha de entrega", 1.2),
        ("Procesamiento de items", 18.5),
        ("Movimiento de archivo", 0.8)
    ]
    
    for operation, duration in operations:
        # Agregar variabilidad
        actual_duration = duration + random.uniform(-0.5, 0.5)
        success = random.random() > 0.1  # 90% de éxito
        
        start_time = rpa_logger.log_action(operation, f"Duración esperada: {duration}s", operation.lower())
        time.sleep(actual_duration)
        rpa_logger.log_action_complete(operation, start_time, success, f"Duración real: {actual_duration:.2f}s", operation.lower())
        
        if not success:
            rpa_logger.log_error(f"Error en {operation}", "Error simulado para prueba", operation.lower())
    
    # Mostrar métricas finales
    metrics = rpa_logger.get_metrics_summary()
    print(f"Métricas finales: {json.dumps(metrics, indent=2, ensure_ascii=False)}")

def test_log_utilities():
    """Prueba utilidades de logs"""
    print("\n=== PRUEBA DE UTILIDADES DE LOGS ===\n")
    
    utils = LogUtils()
    
    # 1. Comprimir logs antiguos (simulado)
    print("1. Comprimiendo logs antiguos...")
    compressed_count = utils.compress_old_logs(7)
    print(f"Archivos comprimidos: {compressed_count}")
    
    # 2. Limpiar logs muy antiguos (simulado)
    print("2. Limpiando logs antiguos...")
    cleaned_count = utils.cleanup_old_logs(30)
    print(f"Archivos eliminados: {cleaned_count}")
    
    # 3. Analizar patrones
    print("3. Analizando patrones...")
    analysis = utils.analyze_log_patterns(24)
    print(f"Patrones encontrados: {len(analysis.get('error_patterns', {}))} tipos de error")
    
    # 4. Generar reporte
    print("4. Generando reporte...")
    report = utils.generate_log_report('daily')
    print(f"Reporte generado con {len(report.get('recommendations', []))} recomendaciones")
    
    # 5. Exportar logs
    print("5. Exportando logs...")
    success = utils.export_logs_to_json("test_export.json", 1)
    print(f"Exportación exitosa: {success}")

def main():
    """Función principal de pruebas"""
    print("Iniciando pruebas del sistema de logs mejorado...\n")
    
    try:
        # Ejecutar pruebas
        test_enhanced_logging()
        test_error_scenarios()
        test_performance_monitoring()
        test_log_utilities()
        
        print("\n=== TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE ===")
        
        # Mostrar resumen final
        final_metrics = rpa_logger.get_metrics_summary()
        print(f"\nResumen final de métricas:")
        print(f"- Operaciones totales: {final_metrics.get('session_stats', {}).get('total_operations', 0)}")
        print(f"- Errores totales: {final_metrics.get('session_stats', {}).get('total_errors', 0)}")
        print(f"- Tasa de éxito: {final_metrics.get('session_stats', {}).get('overall_success_rate', 0):.1f}%")
        
    except Exception as e:
        print(f"Error en las pruebas: {e}")
        rpa_logger.log_error(f"Error en pruebas: {e}", "Función main")

if __name__ == "__main__":
    main() 