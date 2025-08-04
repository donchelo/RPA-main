# SISTEMA DE LOGS MEJORADO - RPA

## **DESCRIPCIÓN GENERAL**

El sistema de logs mejorado para RPA proporciona capacidades avanzadas de logging, monitoreo, métricas y análisis. Este sistema reemplaza el logger básico anterior con funcionalidades empresariales.

## **CARACTERÍSTICAS PRINCIPALES**

### **🔍 Logging Estructurado**
- **Logs JSON**: Formato estructurado para análisis automatizado
- **Contexto enriquecido**: Información adicional en cada entrada de log
- **Múltiples archivos**: Separación por tipo (principal, errores, rendimiento, estructurado)

### **📊 Métricas Avanzadas**
- **Tracking de operaciones**: Duración, éxito/fallo, frecuencia
- **Métricas de sesión**: Estadísticas globales del sistema
- **Historial de errores**: Últimos 100 errores con contexto completo

### **🚨 Sistema de Alertas**
- **Alertas automáticas**: Basadas en umbrales configurables
- **Prevención de spam**: Cooldown entre alertas del mismo tipo
- **Clasificación de severidad**: HIGH, MEDIUM, LOW

### **📈 Dashboard y Monitoreo**
- **Dashboard visual**: Gráficos de rendimiento y estado
- **Monitoreo en tiempo real**: Análisis continuo de logs
- **Base de datos SQLite**: Almacenamiento persistente de métricas

### **🛠️ Utilidades de Mantenimiento**
- **Compresión automática**: Logs antiguos comprimidos con gzip
- **Limpieza inteligente**: Eliminación de logs muy antiguos
- **Análisis de patrones**: Detección de problemas recurrentes

## **ARQUITECTURA DEL SISTEMA**

### **Componentes Principales:**

1. **RPALogger** (`rpa/logger.py`): Sistema de logging principal
2. **RPAMetrics** (`rpa/logger.py`): Gestión de métricas
3. **RPAAlertManager** (`rpa/logger.py`): Sistema de alertas
4. **LogMonitor** (`rpa/log_monitor.py`): Monitoreo en tiempo real
5. **LogDashboard** (`rpa/log_monitor.py`): Dashboard visual
6. **LogUtils** (`rpa/log_utils.py`): Utilidades de mantenimiento

### **Flujo de Datos:**
```
Operación RPA → RPALogger → Múltiples Handlers → Archivos + Métricas + Alertas
```

## **ARCHIVOS DE LOG**

### **Tipos de Archivos:**

1. **`rpa.log`**: Log principal (formato legible)
2. **`rpa_errors.log`**: Solo errores y críticos
3. **`rpa_performance.log`**: Métricas de rendimiento
4. **`rpa_structured.log`**: Logs en formato JSON
5. **`rpa_metrics.log`**: Métricas del sistema

### **Rotación de Archivos:**
- **Principal**: 10MB, 5 backups
- **Errores**: 5MB, 3 backups
- **Rendimiento**: 5MB, 3 backups
- **Estructurado**: 15MB, 7 backups
- **Métricas**: 3MB, 2 backups

## **USO DEL SISTEMA**

### **Logging Básico:**
```python
from rpa.logger import rpa_logger

# Logging simple
rpa_logger.info("Mensaje informativo")
rpa_logger.error("Error crítico")

# Logging con contexto
rpa_logger.info("Operación completada", {
    'operation': 'load_nit',
    'duration': 2.5,
    'success': True
})
```

### **Logging de Acciones:**
```python
# Iniciar acción
start_time = rpa_logger.log_action(
    "Carga de NIT", 
    "NIT: 12345678-9", 
    "load_nit"
)

# Completar acción
rpa_logger.log_action_complete(
    "Carga de NIT", 
    start_time, 
    True,  # éxito
    "NIT cargado exitosamente", 
    "load_nit"
)
```

### **Logging de Errores:**
```python
rpa_logger.log_error(
    "Error de conexión SAP", 
    "Timeout en conexión", 
    "sap_connection"
)
```

### **Logging de Rendimiento:**
```python
rpa_logger.log_performance(
    "Procesamiento de items", 
    15.5, 
    {
        'items_count': 5,
        'avg_time_per_item': 3.1
    }
)
```

## **MÉTRICAS Y ANÁLISIS**

### **Obtener Métricas:**
```python
# Resumen completo
metrics = rpa_logger.get_metrics_summary()

# Estadísticas de sesión
session_stats = metrics['session_stats']
print(f"Operaciones totales: {session_stats['total_operations']}")
print(f"Tasa de éxito: {session_stats['overall_success_rate']:.1f}%")

# Estadísticas por operación
for operation, stats in metrics['operation_stats'].items():
    if stats:
        print(f"{operation}: {stats['avg_time']:.2f}s promedio")
```

### **Análisis de Patrones:**
```python
from rpa.log_utils import LogUtils

utils = LogUtils()
analysis = utils.analyze_log_patterns(24)  # Últimas 24 horas

# Errores más frecuentes
for error_type, count in analysis['error_patterns'].items():
    print(f"{error_type}: {count} veces")

# Operaciones más lentas
for operation, durations in analysis['performance_patterns'].items():
    avg_duration = sum(durations) / len(durations)
    print(f"{operation}: {avg_duration:.2f}s promedio")
```

## **MONITOREO Y DASHBOARD**

### **Iniciar Monitor:**
```python
from rpa.log_monitor import LogMonitor, LogDashboard

# Crear monitor
monitor = LogMonitor()
monitor.start_monitoring()

# Crear dashboard
dashboard = LogDashboard(monitor)
fig = dashboard.create_dashboard()
dashboard.save_dashboard("dashboard.png")
```

### **Ejecutar Monitor Independiente:**
```bash
python rpa/log_monitor.py
```

## **UTILIDADES DE MANTENIMIENTO**

### **Comprimir Logs Antiguos:**
```python
from rpa.log_utils import LogUtils

utils = LogUtils()
compressed_count = utils.compress_old_logs(7)  # Logs de más de 7 días
print(f"Archivos comprimidos: {compressed_count}")
```

### **Limpiar Logs Muy Antiguos:**
```python
cleaned_count = utils.cleanup_old_logs(30)  # Logs de más de 30 días
print(f"Archivos eliminados: {cleaned_count}")
```

### **Generar Reporte:**
```python
report = utils.generate_log_report('daily')  # daily, weekly, hourly
print(f"Recomendaciones: {len(report['recommendations'])}")
```

### **Exportar Logs:**
```python
success = utils.export_logs_to_json("export.json", 24)  # Últimas 24 horas
```

### **Comandos de Línea:**
```bash
# Comprimir logs
python rpa/log_utils.py --action compress --days 7

# Limpiar logs
python rpa/log_utils.py --action cleanup --days 30

# Analizar patrones
python rpa/log_utils.py --action analyze --hours 24

# Generar reporte
python rpa/log_utils.py --action report --report-type daily

# Exportar logs
python rpa/log_utils.py --action export --output logs_export.json --hours 24
```

## **CONFIGURACIÓN AVANZADA**

### **Archivo de Configuración:**
```json
{
  "log_dir": "logs",
  "log_level": "INFO",
  "files": {
    "main": "rpa.log",
    "error": "rpa_errors.log",
    "performance": "rpa_performance.log",
    "structured": "rpa_structured.log",
    "metrics": "rpa_metrics.log"
  },
  "alerts": {
    "error_rate_threshold": 0.1,
    "response_time_threshold": 30.0,
    "consecutive_errors_threshold": 3,
    "alert_cooldown": 300
  },
  "metrics": {
    "enable_performance_tracking": true,
    "enable_error_tracking": true,
    "metrics_summary_interval": 3600
  }
}
```

### **Umbrales de Alerta:**
- **Error Rate**: 10% de errores
- **Response Time**: 30 segundos
- **Consecutive Errors**: 3 errores consecutivos
- **Alert Cooldown**: 5 minutos entre alertas

## **PRUEBAS DEL SISTEMA**

### **Ejecutar Pruebas:**
```bash
python rpa/test_enhanced_logger.py
```

### **Pruebas Incluidas:**
1. **Logging Mejorado**: Prueba de logging con contexto
2. **Escenarios de Error**: Simulación de diferentes tipos de error
3. **Monitoreo de Rendimiento**: Prueba de métricas de rendimiento
4. **Utilidades de Logs**: Prueba de mantenimiento y análisis

## **MONITOREO DE SALUD**

### **Verificar Estado:**
```python
from rpa.log_config import get_health_status

health = get_health_status()
print(f"Configuración válida: {health['config_valid']}")
print(f"Directorio escribible: {health['log_directory_writable']}")
```

### **Métricas del Sistema:**
- **CPU Usage**: Monitoreo de uso de CPU
- **Memory Usage**: Monitoreo de uso de memoria
- **Disk Usage**: Monitoreo de uso de disco
- **Log File Count**: Número de archivos de log
- **Total Log Size**: Tamaño total de logs

## **BEST PRACTICES**

### **Para Desarrolladores:**
1. **Usar contexto**: Siempre incluir información relevante en logs
2. **Clasificar operaciones**: Usar nombres consistentes para operaciones
3. **Manejar errores**: Registrar errores con contexto completo
4. **Monitorear rendimiento**: Usar métricas para optimizar

### **Para Operadores:**
1. **Revisar alertas**: Monitorear alertas automáticas
2. **Analizar patrones**: Usar análisis para identificar problemas
3. **Mantener logs**: Ejecutar limpieza y compresión regularmente
4. **Generar reportes**: Crear reportes periódicos

### **Para Mantenimiento:**
1. **Configurar rotación**: Ajustar tamaños y backups según necesidades
2. **Monitorear espacio**: Verificar uso de disco regularmente
3. **Actualizar umbrales**: Ajustar alertas según experiencia
4. **Backup de configuración**: Mantener copias de configuración

## **TROUBLESHOOTING**

### **Problemas Comunes:**

#### **1. Logs no se escriben**
- **Causa**: Permisos de directorio
- **Solución**: Verificar permisos de escritura en `logs/`

#### **2. Dashboard no se genera**
- **Causa**: Dependencias faltantes
- **Solución**: Instalar `matplotlib` y `psutil`

#### **3. Métricas no se actualizan**
- **Causa**: Base de datos corrupta
- **Solución**: Eliminar `log_metrics.db` y reiniciar

#### **4. Alertas no funcionan**
- **Causa**: Umbrales mal configurados
- **Solución**: Verificar configuración de alertas

### **Comandos de Diagnóstico:**
```bash
# Verificar salud del sistema
python -c "from rpa.log_config import get_health_status; print(get_health_status())"

# Verificar métricas
python -c "from rpa.logger import rpa_logger; print(rpa_logger.get_metrics_summary())"

# Analizar patrones
python rpa/log_utils.py --action analyze --hours 1
```

## **MIGRACIÓN DESDE EL SISTEMA ANTERIOR**

### **Cambios Principales:**
1. **Nuevos métodos**: `log_action()`, `log_action_complete()`
2. **Contexto enriquecido**: Parámetro `context` en todos los métodos
3. **Métricas automáticas**: Tracking automático de rendimiento
4. **Alertas inteligentes**: Sistema de alertas basado en umbrales

### **Compatibilidad:**
- Los métodos antiguos siguen funcionando
- Los logs existentes se mantienen
- Migración gradual recomendada

## **CONTACTO Y SOPORTE**

### **Información del Sistema:**
- **Versión**: Enhanced Logger v2.0
- **Última actualización**: Agosto 2025
- **Responsable**: Equipo de Automatización

### **Archivos Críticos:**
- **Logger principal**: `rpa/logger.py`
- **Configuración**: `rpa/log_config.py`
- **Monitor**: `rpa/log_monitor.py`
- **Utilidades**: `rpa/log_utils.py`

---

**NOTA**: Este sistema de logs mejorado proporciona capacidades empresariales para el monitoreo y análisis del sistema RPA. Se recomienda familiarizarse con todas las funcionalidades antes de realizar modificaciones. 