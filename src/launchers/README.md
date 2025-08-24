# 🚀 Launchers del Sistema RPA

## 📋 Descripción
Esta carpeta contiene todos los launchers del sistema RPA, organizados por funcionalidad y versión.

## 🎯 Launchers Principales

### `rpa_launcher_v3_final.py`
**Launcher principal del sistema**
- Versión más estable y completa
- Incluye todas las funcionalidades del sistema
- Manejo robusto de errores
- Logging completo
- **Uso recomendado para producción**

### `launcher_ventas_mejorado.py`
**Launcher específico para ventas**
- Optimizado para procesamiento de órdenes de venta
- Configuración específica para SAP Business One
- Interfaz simplificada para usuarios de ventas
- **Uso recomendado para equipo de ventas**

## 📁 Estructura

```
src/launchers/
├── rpa_launcher_v3_final.py          # Launcher principal
├── rpa_launcher_v3_final.bat         # Script batch principal
├── launcher_ventas_mejorado.py       # Launcher de ventas
├── launcher_ventas_funcional.bat     # Script batch ventas
├── launcher_ventas_mejorado.bat      # Script batch ventas mejorado
└── legacy/                           # Versiones anteriores
    ├── launcher_completo.py
    ├── launcher_definitivo.py
    ├── launcher_ultra_simple.py
    ├── rpa_launcher.py
    ├── rpa_launcher_v2.py
    ├── rpa_launcher_v3.py
    ├── rpa_launcher_v3_simple.py
    ├── rpa_launcher_v3_robust.py
    └── *.bat                         # Scripts batch legacy
```

## 🚀 Cómo Usar

### Ejecutar Launcher Principal
```bash
# Desde la raíz del proyecto
python src/launchers/rpa_launcher_v3_final.py

# O usando el script batch
src\launchers\rpa_launcher_v3_final.bat
```

### Ejecutar Launcher de Ventas
```bash
# Desde la raíz del proyecto
python src/launchers/launcher_ventas_mejorado.py

# O usando el script batch
src\launchers\launcher_ventas_mejorado.bat
```

## ⚙️ Configuración

### Variables de Entorno
Los launchers utilizan las siguientes variables de entorno:
- `RPA_CONFIG_PATH`: Ruta al archivo de configuración
- `RPA_LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `RPA_ENVIRONMENT`: Entorno de ejecución (DEV, TEST, PROD)

### Archivos de Configuración
- `config.yaml`: Configuración principal del sistema
- `rpa/modules/*/config.yaml`: Configuraciones específicas por módulo

## 🔧 Características

### Launcher Principal (`rpa_launcher_v3_final.py`)
- ✅ Detección automática de SAP
- ✅ Navegación inteligente
- ✅ Procesamiento de órdenes de venta y producción
- ✅ Integración con Google Drive
- ✅ Sistema de logging completo
- ✅ Manejo de errores robusto
- ✅ Configuración externa
- ✅ Tests automáticos

### Launcher de Ventas (`launcher_ventas_mejorado.py`)
- ✅ Interfaz simplificada
- ✅ Configuración específica para ventas
- ✅ Validación de datos mejorada
- ✅ Reportes de procesamiento
- ✅ Integración con SAP Business One

## 🐛 Troubleshooting

### Problemas Comunes

#### "No se encuentra el módulo RPA"
```bash
# Verificar que estás en la raíz del proyecto
cd /path/to/RPA-main
python src/launchers/rpa_launcher_v3_final.py
```

#### "Error de configuración"
```bash
# Verificar archivo de configuración
python src/utils/check_dependencies.py
```

#### "SAP no encontrado"
```bash
# Ejecutar diagnóstico
python debug/diagnostico_problema.py
```

## 📊 Métricas

### Rendimiento
- **Tiempo de inicio**: ~5-10 segundos
- **Memoria utilizada**: ~50-100MB
- **Archivos procesados por hora**: 40-60
- **Tasa de éxito**: >95%

### Logs
- **Ubicación**: `logs/`
- **Rotación**: Automática diaria
- **Niveles**: DEBUG, INFO, WARNING, ERROR
- **Formato**: JSON estructurado

## 🔄 Actualizaciones

### Versiones Legacy
Los launchers en la carpeta `legacy/` se mantienen por compatibilidad:
- No se recomienda su uso en producción
- Útiles para debugging y comparación
- Pueden contener funcionalidades experimentales

### Migración
Para migrar de versiones anteriores:
1. Revisar cambios en `docs/technical/MIGRATION_GUIDE.md`
2. Actualizar configuraciones según sea necesario
3. Ejecutar tests de compatibilidad
4. Migrar gradualmente

## 📞 Soporte

Para problemas con los launchers:
1. Revisar logs en `logs/`
2. Ejecutar diagnósticos en `debug/`
3. Consultar documentación en `docs/`
4. Contactar al equipo de desarrollo
