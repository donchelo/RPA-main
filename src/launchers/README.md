# 🚀 Launchers del Sistema RPA

## 📋 Descripción
Esta carpeta contiene todos los launchers del sistema RPA, organizados por funcionalidad y versión.

## 🎯 Launchers Principales

### `launcher_ventas.py` 🛒
**Launcher específico para órdenes de venta**
- Interfaz dedicada para procesamiento de órdenes de venta
- Optimizado para SAP Business One - módulo de ventas
- Configuración específica para ventas
- **Uso recomendado para equipo de ventas**

### `launcher_produccion.py` 🏭
**Launcher específico para órdenes de producción**
- Interfaz dedicada para procesamiento de órdenes de producción
- Optimizado para SAP Business One - módulo de producción
- Configuración específica para producción
- **Uso recomendado para equipo de producción**

### `rpa_launcher_v3_final.py` 🔧
**Launcher unificado (legacy)**
- Versión que permite seleccionar entre módulos
- Incluye todas las funcionalidades del sistema
- Manejo robusto de errores
- **Uso recomendado para administradores**

## 📁 Estructura

```
src/launchers/
├── launcher_ventas.py              # Launcher específico para ventas
├── launcher_ventas.bat             # Script batch para ventas
├── launcher_produccion.py          # Launcher específico para producción
├── launcher_produccion.bat         # Script batch para producción
├── rpa_launcher_v3_final.py        # Launcher unificado (legacy)
├── rpa_launcher_v3_final.bat       # Script batch unificado
└── legacy/                         # Versiones anteriores
    ├── launcher_completo.py
    ├── launcher_definitivo.py
    ├── launcher_ultra_simple.py
    ├── launcher_ventas_mejorado.py
    ├── rpa_launcher.py
    ├── rpa_launcher_v2.py
    ├── rpa_launcher_v3.py
    ├── rpa_launcher_v3_simple.py
    ├── rpa_launcher_v3_robust.py
    └── *.bat                         # Scripts batch legacy
```

## 🚀 Cómo Usar

### Ejecutar Launcher de Ventas
```bash
# Desde la raíz del proyecto
python src/launchers/launcher_ventas.py

# O usando el script batch
src\launchers\launcher_ventas.bat
```

### Ejecutar Launcher de Producción
```bash
# Desde la raíz del proyecto
python src/launchers/launcher_produccion.py

# O usando el script batch
src\launchers\launcher_produccion.bat
```

### Ejecutar Launcher Unificado (Legacy)
```bash
# Desde la raíz del proyecto
python src/launchers/rpa_launcher_v3_final.py

# O usando el script batch
src\launchers\rpa_launcher_v3_final.bat
```

## ⚙️ Configuración

### Variables de Entorno
Los launchers utilizan las siguientes variables de entorno:
- `RPA_CONFIG_PATH`: Ruta al archivo de configuración
- `RPA_LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `RPA_ENVIRONMENT`: Entorno de ejecución (DEV, TEST, PROD)

### Archivos de Configuración
- `config.yaml`: Configuración principal del sistema
- `rpa/modules/sales_order/sales_order_config.yaml`: Configuración específica de ventas
- `rpa/modules/production_order/production_order_config.yaml`: Configuración específica de producción

## 🔧 Características por Launcher

### Launcher de Ventas (`launcher_ventas.py`)
- ✅ Interfaz específica para ventas
- ✅ Configuración optimizada para órdenes de venta
- ✅ Validación de datos de ventas
- ✅ Reportes específicos de ventas
- ✅ Integración con SAP Business One - Ventas
- ✅ Gestión de archivos JSON de ventas

### Launcher de Producción (`launcher_produccion.py`)
- ✅ Interfaz específica para producción
- ✅ Configuración optimizada para órdenes de producción
- ✅ Validación de datos de producción
- ✅ Reportes específicos de producción
- ✅ Integración con SAP Business One - Producción
- ✅ Gestión de archivos JSON de producción

### Launcher Unificado (`rpa_launcher_v3_final.py`)
- ✅ Selección de módulos (ventas/producción)
- ✅ Detección automática de SAP
- ✅ Navegación inteligente
- ✅ Procesamiento de ambos tipos de órdenes
- ✅ Integración con Google Drive
- ✅ Sistema de logging completo
- ✅ Manejo de errores robusto

## 🐛 Troubleshooting

### Problemas Comunes

#### "No se encuentra el módulo RPA"
```bash
# Verificar que estás en la raíz del proyecto
cd /path/to/RPA-main
python src/launchers/launcher_ventas.py
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

#### "Módulo específico no encontrado"
```bash
# Verificar que el módulo existe
ls rpa/modules/sales_order/
ls rpa/modules/production_order/
```

## 📊 Métricas

### Rendimiento por Launcher
| Launcher | Tiempo de inicio | Memoria | Archivos/hora | Tasa de éxito |
|----------|------------------|---------|---------------|---------------|
| **Ventas** | ~3-5 segundos | ~30-50MB | 50-70 | >98% |
| **Producción** | ~3-5 segundos | ~30-50MB | 40-60 | >95% |
| **Unificado** | ~5-10 segundos | ~50-100MB | 40-60 | >95% |

### Logs
- **Ubicación**: `logs/`
- **Rotación**: Automática diaria
- **Niveles**: DEBUG, INFO, WARNING, ERROR
- **Formato**: JSON estructurado

## 🔄 Migración y Uso

### Recomendaciones de Uso
1. **Para equipo de ventas**: Usar `launcher_ventas.py`
2. **Para equipo de producción**: Usar `launcher_produccion.py`
3. **Para administradores**: Usar `rpa_launcher_v3_final.py`

### Migración desde Versiones Anteriores
Para migrar de versiones anteriores:
1. Revisar cambios en `docs/technical/MIGRATION_GUIDE.md`
2. Actualizar configuraciones según sea necesario
3. Ejecutar tests de compatibilidad
4. Migrar gradualmente al launcher específico correspondiente

## 📞 Soporte

### Para problemas con los launchers:
1. Revisar logs en `logs/`
2. Ejecutar diagnósticos en `debug/`
3. Consultar documentación en `docs/`
4. Contactar al equipo de desarrollo

### Contacto por tipo de problema:
- **Ventas**: Equipo de ventas + documentación en `docs/guides/`
- **Producción**: Equipo de producción + documentación en `docs/guides/`
- **Técnico**: Equipo de desarrollo + documentación en `docs/technical/`
