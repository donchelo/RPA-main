# 🤖 AI4U | Sistema RPA TAMAPRINT v3.0

## 📋 Descripción

Sistema de Automatización Robótica de Procesos (RPA) para SAP Business One con **arquitectura modular unificada**. Permite seleccionar entre dos módulos principales:

- **🛒 Módulo de Órdenes de Venta**: Automatización de órdenes de venta en SAP
- **🏭 Módulo de Órdenes de Producción**: Automatización de órdenes de producción en SAP

## ✨ Características Principales

### 🎯 Interfaz Unificada
- **Selección de módulos**: Interfaz gráfica que permite elegir entre ventas y producción
- **Control centralizado**: Gestión unificada de ambos módulos
- **Monitoreo en tiempo real**: Logs y estado del sistema
- **Branding AI4U**: Interfaz profesional con identidad de marca

### 🔧 Arquitectura Modular
- **Módulos independientes**: Cada módulo tiene su propia lógica y configuración
- **Handlers especializados**: Clases específicas para cada tipo de proceso
- **Configuración modular**: Archivos de configuración separados por módulo
- **Reutilización de componentes**: Sistema de visión y configuración compartido

### 📊 Funcionalidades Avanzadas
- **Detección visual híbrida**: Template matching + OCR
- **Manejo robusto de errores**: Recuperación automática y reintentos
- **Integración con Google Drive**: Subida automática de archivos
- **Logging detallado**: Registro completo de operaciones
- **Screenshots automáticos**: Capturas de confirmación

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- SAP Business One
- Conexión a escritorio remoto (IP: 20.96.6.64)
- Tesseract OCR instalado

### Instalación
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ai4u/rpa-tamaprINT.git
   cd rpa-tamaprINT
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar credenciales**:
   - Copiar archivos de credenciales OAuth a la carpeta raíz
   - Configurar `config.yaml` según tu entorno

4. **Verificar estructura de carpetas**:
   ```
   data/
   ├── outputs_json/
   │   ├── 01_Pendiente/
   │   ├── 02_Procesando/
   │   ├── 03_Completado/
   │   ├── 04_Error/
   │   └── 05_Archivado/
   ├── inputs/
   └── temp/
   ```

## 🎮 Uso del Sistema

### Inicio Rápido
1. **Ejecutar el launcher**:
   ```bash
   python rpa_launcher_v3.py
   ```
   O usar el archivo batch:
   ```bash
   rpa_launcher_v3.bat
   ```

2. **Seleccionar módulo**:
   - Hacer clic en "Seleccionar Módulo de Ventas" o "Seleccionar Módulo de Producción"
   - Verificar que el módulo esté activo en el panel derecho

3. **Iniciar sistema**:
   - Hacer clic en "▶️ INICIAR SISTEMA"
   - El sistema comenzará a monitorear archivos automáticamente

### Procesamiento Manual
1. **Procesar archivo individual**:
   - Seleccionar módulo
   - Hacer clic en "📁 PROCESAR ARCHIVO"
   - Elegir archivo JSON
   - El sistema procesará el archivo inmediatamente

2. **Probar módulo**:
   - Seleccionar módulo
   - Hacer clic en "🧪 PROBAR MÓDULO"
   - El sistema ejecutará una prueba de navegación

## 📦 Estructura de Módulos

### 🛒 Módulo de Órdenes de Venta
**Ubicación**: `rpa/modules/sales_order/`

**Funcionalidades**:
- Navegación automática a módulo de ventas
- Carga de NIT del cliente
- Ingreso de número de orden de compra
- Procesamiento de items y cantidades
- Screenshots de confirmación

**Archivos de configuración**:
- `sales_order_config.yaml`: Configuración específica del módulo
- Imágenes de referencia en `rpa/vision/reference_images/`

**Campos soportados**:
```json
{
  "comprador": {
    "nit": "string",
    "nombre": "string"
  },
  "orden_compra": "string",
  "fecha_entrega": "DD/MM/YYYY",
  "items": [
    {
      "codigo": "string",
      "cantidad": "number",
      "precio_unitario": "number"
    }
  ]
}
```

### 🏭 Módulo de Órdenes de Producción
**Ubicación**: `rpa/modules/production_order/`

**Funcionalidades**:
- Navegación automática a módulo de producción
- Creación de órdenes de fabricación
- Ingreso de artículo, pedido interno y cantidad
- Configuración de fecha de finalización
- Screenshots de confirmación

**Archivos de configuración**:
- `production_order_config.yaml`: Configuración específica del módulo
- Imágenes de referencia en `rpa/vision/reference_images/production/`

**Campos soportados**:
```json
{
  "numero_articulo": "string",
  "numero_pedido_interno": "string",
  "cantidad": "number",
  "fecha_finalizacion": "DD/MM/YYYY",
  "unidad_medida": "string",
  "centro_trabajo": "string"
}
```

## 🔧 Configuración

### Archivo de Configuración Principal
`config.yaml` - Configuración global del sistema:
```yaml
delays:
  after_click: 1.0
  after_input: 1.0
  navigation_wait: 2.0

template_matching:
  default_confidence: 0.8
  timeout: 10.0

google_drive:
  enabled: true
  folder_id: "your_folder_id"
```

### Configuración de Módulos
Cada módulo tiene su propio archivo de configuración:

**Ventas**: `rpa/modules/sales_order/sales_order_config.yaml`
**Producción**: `rpa/modules/production_order/production_order_config.yaml`

## 📁 Estructura de Archivos

```
RPA-main/
├── rpa_launcher_v3.py          # Launcher principal v3.0
├── rpa_launcher_v3.bat         # Script batch para Windows
├── config.yaml                 # Configuración global
├── requirements.txt            # Dependencias Python
├── rpa/
│   ├── modules/
│   │   ├── sales_order/        # Módulo de ventas
│   │   │   ├── __init__.py
│   │   │   ├── sales_order_handler.py
│   │   │   └── sales_order_config.yaml
│   │   └── production_order/   # Módulo de producción
│   │       ├── __init__.py
│   │       ├── production_order_handler.py
│   │       └── production_order_config.yaml
│   ├── vision/                 # Sistema de visión
│   ├── config_manager.py       # Gestor de configuración
│   └── simple_logger.py        # Sistema de logging
├── data/
│   └── outputs_json/           # Archivos JSON de entrada/salida
├── screenshots/                # Capturas de pantalla
├── logs/                       # Archivos de log
└── test_*.py                   # Scripts de prueba
```

## 🧪 Pruebas

### Pruebas de Módulos
```bash
# Probar módulo de ventas
python test_sales_order.py

# Probar módulo de producción
python test_production_order.py
```

### Verificación de Requisitos
- Usar la opción "Verificar requisitos" en el menú Herramientas
- Revisar que todas las dependencias estén instaladas
- Verificar que las carpetas necesarias existan

## 📊 Monitoreo y Logs

### Logs del Sistema
- **Ubicación**: Carpeta `logs/`
- **Formato**: Timestamp + nivel + mensaje
- **Rotación**: Automática por tamaño y fecha

### Screenshots
- **Ubicación**: Carpeta `screenshots/`
- **Formato**: `{modulo}_{timestamp}.png`
- **Propósito**: Confirmación visual de operaciones

### Estado del Sistema
- **Interfaz gráfica**: Panel de información en tiempo real
- **Archivos pendientes**: Contador automático
- **Módulo activo**: Indicador del módulo seleccionado

## 🔒 Seguridad

### Credenciales
- **OAuth delegation**: Autenticación segura con Google Drive
- **Archivos de token**: Almacenamiento local de credenciales
- **Sin hardcoding**: No hay credenciales en el código

### Acceso
- **Escritorio remoto**: Conexión segura a SAP
- **Permisos mínimos**: Solo acceso necesario a archivos y SAP

## 🆘 Solución de Problemas

### Problemas Comunes

**1. Error de conexión al escritorio remoto**
- Verificar que la IP 20.96.6.64 sea accesible
- Comprobar que el escritorio remoto esté abierto
- Revisar configuración de red

**2. SAP no se detecta**
- Verificar que SAP Business One esté abierto
- Comprobar que las imágenes de referencia existan
- Revisar configuración de template matching

**3. Error en procesamiento de archivos**
- Verificar formato JSON de los archivos
- Comprobar que los campos requeridos estén presentes
- Revisar logs para detalles específicos

### Logs de Depuración
```bash
# Ver logs en tiempo real
tail -f logs/rpa.log

# Buscar errores específicos
grep "ERROR" logs/rpa.log
```

## 📞 Soporte

### Contacto
- **Email**: hola@ai4u.com.co
- **Empresa**: AI4U - Automatización Inteligente para Ti!

### Documentación Adicional
- **Guía técnica**: `GUIA_TECNICA_DETALLADA.md`
- **Manual de usuario**: `MANUAL_USUARIO_PRODUCCION.md`
- **Changelog**: `docs/changelog/`

## 🔄 Versiones

### v3.0 (Actual)
- ✅ Arquitectura modular unificada
- ✅ Interfaz gráfica con selección de módulos
- ✅ Módulo de órdenes de venta
- ✅ Módulo de órdenes de producción
- ✅ Monitoreo automático
- ✅ Logs detallados

### v2.0
- ✅ Interfaz gráfica básica
- ✅ Integración con Google Drive
- ✅ Sistema de máquina de estados

### v1.0
- ✅ Funcionalidad básica de RPA
- ✅ Procesamiento de órdenes de venta
- ✅ Detección visual

---

**© 2024 AI4U - Automatización Inteligente para Ti!**
