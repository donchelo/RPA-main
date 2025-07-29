# Sistema de Logs MVP para RPA

## Descripción

Este sistema de logs MVP (Minimum Viable Product) proporciona un sistema de logging robusto y organizado para el módulo RPA. Incluye rotación automática de archivos, diferentes niveles de logging, y métodos específicos para acciones RPA.

## Características

### ✅ Funcionalidades Implementadas

- **Logging estructurado** con timestamps y contexto
- **Rotación automática** de archivos (máximo 5 archivos de 10MB cada uno)
- **Múltiples niveles** de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Métodos específicos** para acciones RPA:
  - `log_action()` - Para acciones específicas del RPA
  - `log_error()` - Para errores con contexto
  - `log_performance()` - Para métricas de rendimiento
- **Logging dual**: Archivo + Consola
- **Configuración centralizada** en `log_config.py`

### 📁 Estructura de Archivos

```
rpa/
├── logger.py          # Sistema principal de logs
├── log_config.py      # Configuración del sistema
├── test_logger.py     # Script de pruebas
├── README_LOGS.md     # Esta documentación
└── logs/              # Directorio de archivos de log (se crea automáticamente)
    ├── rpa.log        # Log principal
    ├── rpa.log.1      # Archivos de rotación
    └── ...
```

## Uso

### Importación Básica

```python
from rpa.logger import rpa_logger

# Logging básico
rpa_logger.info("Mensaje informativo")
rpa_logger.debug("Mensaje de debug")
rpa_logger.warning("Advertencia")
rpa_logger.error("Error")
rpa_logger.critical("Error crítico")
```

### Logging Específico para RPA

```python
# Logging de acciones
rpa_logger.log_action("Carga de NIT", "NIT: 12345678-9")
rpa_logger.log_action("Procesamiento de items", "Total: 5 items")

# Logging de errores con contexto
rpa_logger.log_error("Error al conectar con SAP", "Conexión remota fallida")

# Logging de rendimiento
rpa_logger.log_performance("Carga de datos", 2.5)  # 2.5 segundos
```

### Ejemplo de Integración en Métodos RPA

```python
def load_nit(self, nit):
    start_time = time.time()
    rpa_logger.log_action("Iniciando carga de NIT", f"NIT: {nit}")
    
    try:
        # ... código de carga ...
        
        duration = time.time() - start_time
        rpa_logger.log_performance("Carga de NIT", duration)
        rpa_logger.log_action("NIT cargado exitosamente", f"NIT: {nit}")
        
    except Exception as e:
        rpa_logger.log_error(f"Error al cargar NIT: {str(e)}", f"NIT: {nit}")
        raise
```

## Configuración

### Modificar Configuración

Edita `log_config.py` para personalizar:

```python
# Tamaño máximo de archivo (10MB por defecto)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Número de archivos de respaldo (5 por defecto)
BACKUP_COUNT = 5

# Nivel de logging por defecto
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Niveles de Logging por Módulo

```python
MODULE_LOG_LEVELS = {
    "RPA": "INFO",
    "RPA.vision": "DEBUG",
    "RPA.json_parser": "INFO"
}
```

## Pruebas

### Ejecutar Pruebas del Sistema

```bash
cd rpa
python test_logger.py
```

Este script ejecutará:
- ✅ Pruebas de logging básico
- ✅ Pruebas de logging de acciones
- ✅ Pruebas de logging de errores
- ✅ Pruebas de logging de rendimiento
- ✅ Simulación completa de flujo RPA

### Verificar Archivos Generados

Después de ejecutar las pruebas, revisa el directorio `logs/`:

```bash
ls -la logs/
cat logs/rpa.log
```

## Formato de Logs

### Estructura de Mensajes

```
2024-01-15 14:30:25 - RPA - INFO - log_action:45 - ACTION: Iniciando carga de NIT | DETAILS: NIT: 12345678-9
2024-01-15 14:30:27 - RPA - INFO - log_performance:52 - PERFORMANCE: Carga de NIT completed in 2.50 seconds
2024-01-01 14:30:28 - RPA - ERROR - log_error:39 - ERROR: Error al conectar con SAP | CONTEXT: Conexión remota fallida
```

### Campos del Log

- **Timestamp**: Fecha y hora exacta
- **Logger Name**: Nombre del logger (RPA)
- **Level**: Nivel del mensaje (INFO, ERROR, etc.)
- **Function**: Función que generó el log
- **Line**: Número de línea
- **Message**: Mensaje principal
- **Context**: Información adicional (opcional)

## Monitoreo y Mantenimiento

### Verificar Tamaño de Archivos

```bash
du -h logs/
```

### Limpiar Logs Antiguos

```bash
# Mantener solo los últimos 5 archivos
find logs/ -name "rpa.log.*" -mtime +30 -delete
```

### Análisis de Logs

```bash
# Ver errores
grep "ERROR" logs/rpa.log

# Ver acciones específicas
grep "ACTION" logs/rpa.log

# Ver métricas de rendimiento
grep "PERFORMANCE" logs/rpa.log
```

## Integración con el Sistema Existente

El sistema de logs está completamente integrado con el código RPA existente:

- ✅ Reemplaza el logging básico anterior
- ✅ Mantiene compatibilidad con el código existente
- ✅ Agrega funcionalidades avanzadas
- ✅ No requiere cambios en la lógica de negocio

## Ventajas del Sistema MVP

1. **Simplicidad**: Fácil de usar y entender
2. **Robustez**: Rotación automática y manejo de errores
3. **Flexibilidad**: Configuración centralizada
4. **Específico**: Métodos dedicados para RPA
5. **Escalable**: Fácil de extender para necesidades futuras

## Próximos Pasos (Futuras Mejoras)

- [ ] Dashboard web para visualización de logs
- [ ] Alertas automáticas por email/Slack
- [ ] Análisis de tendencias de rendimiento
- [ ] Integración con sistemas de monitoreo externos
- [ ] Logs estructurados en JSON para análisis avanzado 