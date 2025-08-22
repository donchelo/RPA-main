# 🤖 CLAUDE.md - Guía Completa del Sistema RPA TAMAPRINT

## 📄 Descripción del Proyecto

**Sistema RPA TAMAPRINT** es una solución de automatización robusta que procesa órdenes de venta en SAP Business One de manera completamente automática. El sistema utiliza una arquitectura basada en máquina de estados con integración de visión computacional, OCR y subida automática a Google Drive.

### 🎯 Propósito Principal
Automatizar completamente el flujo: `Archivo JSON` → `Procesamiento SAP` → `Captura` → `Google Drive`

## 🏗️ Arquitectura del Sistema

### 🔧 Componentes Principales

1. **Main Controller** (`main.py`):
   - Punto de entrada del sistema
   - Programador de ejecución cada 10 minutos
   - Manejo de errores críticos del sistema

2. **State Machine** (`rpa/state_machine.py`):
   - Estados: IDLE, CONNECTING_REMOTE_DESKTOP, OPENING_SAP, NAVIGATING_TO_SALES_ORDER, LOADING_NIT, LOADING_ORDER, LOADING_DATE, LOADING_ITEMS, TAKING_SCREENSHOT, MOVING_JSON, POSITIONING_MOUSE, UPLOADING_TO_GOOGLE_DRIVE, COMPLETED, ERROR, RETRYING
   - Eventos: START_PROCESSING, REMOTE_DESKTOP_CONNECTED, SAP_OPENED, etc.
   - Control de flujo robusto con manejo de errores y reintentos

3. **RPA Controller** (`rpa/rpa_with_state_machine.py`):
   - Integración de máquina de estados con lógica RPA
   - Manejo de contexto de procesamiento
   - Coordinación de todos los subsistemas

4. **State Handlers** (`rpa/rpa_state_handlers.py`):
   - Manejadores específicos para cada estado
   - Lógica de negocio para cada paso del proceso
   - Integración con sistemas externos

5. **Vision System** (`rpa/vision/`):
   - Template matching con OpenCV
   - OCR con Tesseract y EasyOCR
   - Detección robusta de elementos SAP
   - Sistema híbrido de respaldo

6. **Google Drive Integration** (`rpa/google_drive_oauth_uploader.py`):
   - Autenticación OAuth automática
   - Subida automática de archivos originales (PDF + PNG)
   - Carpeta de destino configurable

## ⚙️ Configuración (`config.yaml`)

### 🕒 Delays Críticos
```yaml
delays:
  after_click: 1.0          # Espera después de clic
  after_input: 1.0          # Espera después de input
  after_item_code: 2.0      # Espera después del código
  sap_startup: 25.0         # Tiempo startup SAP
  sap_double_click: 10.0    # Espera tras doble clic SAP
```

### 🎯 Template Matching
```yaml
template_matching:
  default_confidence: 0.8   # Umbral por defecto
  high_confidence: 0.9      # Alta confianza
  sap_icon_confidence: 0.7  # Específico para SAP
  timeout: 10.0             # Timeout para encontrar
```

### 🗂️ Google Drive
```yaml
google_drive:
  enabled: true
  folder_id: "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
  upload_original_files: true
  upload_screenshots: false
```

### 🧭 Navegación SAP
```yaml
navigation:
  tabs_after_nit: 3         # Tabs después del NIT
  tabs_after_order: 4       # Tabs después de orden
  tabs_after_date: 4        # Tabs después de fecha
  tabs_after_quantity_next_item: 3
```

## 🔄 Flujo de Estados Detallado

### 1. **IDLE** → **CONNECTING_REMOTE_DESKTOP**
- Busca archivos JSON en `./data/outputs_json/`
- Conecta a escritorio remoto (20.96.6.64)
- **Éxito**: → OPENING_SAP
- **Error**: → ERROR (con reintento)

### 2. **OPENING_SAP**
- Detecta y abre SAP Business One
- Template matching + OCR de respaldo
- **Timeout**: 25 segundos configurables
- **Éxito**: → NAVIGATING_TO_SALES_ORDER

### 3. **NAVIGATING_TO_SALES_ORDER**
- Navega: Módulos → Ventas → Orden de Venta
- Detección robusta de menús
- **Éxito**: → LOADING_NIT

### 4. **LOADING_NIT**
- Carga NIT del comprador desde JSON
- Navegación por teclado (3 tabs configurables)
- **Éxito**: → LOADING_ORDER

### 5. **LOADING_ORDER**
- Carga orden de compra
- Navegación (4 tabs configurables)
- **Éxito**: → LOADING_DATE

### 6. **LOADING_DATE**
- Carga fecha de entrega (formato DD/MM/YYYY)
- **Éxito**: → LOADING_ITEMS

### 7. **LOADING_ITEMS**
- Procesa cada item del JSON:
  - Código del artículo
  - Cantidad
  - Navegación al siguiente item
- **Éxito**: → TAKING_SCREENSHOT

### 8. **TAKING_SCREENSHOT**
- Captura pantalla de validación
- Guarda como PNG con nombre del archivo
- **Éxito**: → MOVING_JSON

### 9. **MOVING_JSON**
- Mueve archivo a `./data/outputs_json/Procesados/`
- **Éxito**: → POSITIONING_MOUSE

### 10. **POSITIONING_MOUSE**
- Posiciona mouse en botón "Agregar y cerrar"
- **Éxito**: → UPLOADING_TO_GOOGLE_DRIVE

### 11. **UPLOADING_TO_GOOGLE_DRIVE** (NUEVO)
- Sube PDF y PNG originales a Google Drive
- Carpeta: "Terminados" (ID configurable)
- **Éxito**: → COMPLETED

### 12. **COMPLETED**
- Logs de estadísticas completas
- Reset de contexto
- **Siempre**: → IDLE

## 📁 Estructura de Archivos

```
RPA-main/
├── 📄 main.py                          # Punto de entrada
├── 📄 config.yaml                      # Configuración principal
├── 📄 requirements.txt                 # Dependencias
├── 📁 rpa/
│   ├── 📄 rpa_with_state_machine.py    # RPA principal
│   ├── 📄 state_machine.py             # Máquina de estados
│   ├── 📄 rpa_state_handlers.py        # Manejadores
│   ├── 📄 google_drive_oauth_uploader.py # Google Drive
│   ├── 📄 simple_logger.py             # Logger
│   ├── 📄 config_manager.py            # Gestión config
│   ├── 📄 smart_waits.py               # Esperas inteligentes
│   └── 📁 vision/
│       ├── 📄 main.py                  # Sistema visión
│       ├── 📄 template_matcher.py      # Template matching
│       └── 📁 reference_images/        # Imágenes referencia
├── 📁 data/
│   └── 📁 outputs_json/
│       ├── 📁 (archivos JSON a procesar)
│       └── 📁 Procesados/              # Archivos completados
├── 📁 tests/                          # Tests unitarios
├── 📁 logs/                           # Logs del sistema
└── 📁 scripts/                        # Scripts utilidad
```

## 🔧 Dependencias Críticas

### 🖼️ Visión Computacional
```python
opencv-python==4.10.0.84    # Template matching
pillow==11.0.0               # Manipulación imágenes
numpy==2.1.3                 # Arrays numéricos
```

### 🔤 OCR (Optical Character Recognition)
```python
pytesseract==0.3.10          # Tesseract wrapper
easyocr==1.7.0               # EasyOCR alternativo
```

### 🤖 Automatización UI
```python
PyAutoGUI==0.9.54            # Control mouse/teclado
PyGetWindow==0.0.9           # Gestión ventanas
pyperclip==1.9.0             # Manejo clipboard
```

### ☁️ Google Drive
```python
google-auth==2.23.4          # Autenticación Google
google-auth-oauthlib==1.1.0  # OAuth flow
google-api-python-client==2.108.0 # API Google Drive
```

### ⏰ Programación
```python
schedule==1.2.2              # Programador tareas
PyYAML==6.0.2                # Configuración YAML
```

## 💾 Formato de Archivos JSON

### 📋 Estructura Requerida
```json
{
  "comprador": {
    "nit": "900123456"
  },
  "orden_compra": "OC-2024-001",
  "fecha_entrega": "31/12/2024",
  "items": [
    {
      "codigo": "PROD001",
      "cantidad": "10"
    }
  ]
}
```

### ✅ Validaciones Automáticas
- **NIT**: Numérico, longitud válida
- **Orden**: Alfanumérico, no vacío
- **Fecha**: DD/MM/YYYY válida
- **Items**: Array con código y cantidad
- **Códigos**: No vacíos, formatos válidos

## 🚨 Sistema de Logging

### 📊 Tipos de Log
1. **rpa.log**: Log principal del sistema
2. **rpa_errors.log**: Solo errores críticos
3. **rpa_performance.log**: Métricas de rendimiento
4. **rpa_vision.log**: Debug del sistema de visión

### 🔍 Niveles de Debug
```yaml
development:
  enable_debug_screenshots: false  # Capturas debug
  enable_detailed_logging: false   # Logs detallados
  enable_performance_metrics: true # Métricas rendimiento
```

## 🛠️ Testing y Validación

### 🧪 Tests Disponibles
- **test_state_machine.py**: Tests máquina de estados
- **test_config_manager.py**: Tests configuración
- **test_error_handler.py**: Tests manejo errores
- **tests/legacy/**: Tests versiones anteriores

### 🔬 Scripts de Diagnóstico
- **diagnose_sap_detection.py**: Diagnostica detección SAP
- **diagnose_sap_navigation.py**: Diagnostica navegación
- **verificar_google_drive.py**: Diagnostica Google Drive

## 🚀 Comandos de Ejecución

### ▶️ Ejecución Normal
```bash
python main.py
```

### 🧪 Ejecución de Tests
```bash
python run_state_machine_tests.py
python tests/test_state_machine.py
```

### 🔍 Diagnóstico
```bash
python diagnose_sap_detection.py
python verificar_google_drive.py
```

### 📊 Monitoreo en Tiempo Real
```powershell
Get-Content ./logs/rpa.log -Wait
Get-Content ./logs/rpa_errors.log -Wait
```

## ⚡ Optimizaciones de Rendimiento

### 🎯 Template Matching Optimizado
- Cache de templates cargados
- Búsqueda por regiones específicas
- Fallback automático a OCR
- Timeouts configurables

### 🧠 Esperas Inteligentes
- Esperas adaptativas según contexto
- Configuración externa sin hardcoding
- Optimización por tipo de operación

### 📈 Métricas Típicas
- **Tiempo por artículo**: 12-18 segundos
- **Archivos por hora**: 40-60 (cada 10 min)
- **Tasa de éxito**: >95% con reintentos
- **Uso memoria**: ~100MB

## 🔐 Seguridad y Credenciales

### 🔑 Autenticación Google Drive
- OAuth 2.0 flow automático
- Tokens guardados en `token.pickle`
- Credenciales en `oauth_credentials.json`
- Scope limitado: `drive.file`

### 🛡️ Archivos Sensibles (.gitignore)
```
token.pickle
oauth_credentials.json
credentials/
*.log
debug_screenshots/
```

## 🚨 Troubleshooting

### ❌ Errores Comunes

#### "Ventana escritorio remoto no encontrada"
```bash
# Solución:
1. Verificar conexión a 20.96.6.64
2. Activar ventana manualmente
3. Ajustar nombre en config.yaml: windows.remote_desktop
```

#### "SAP Business One no detectado"
```bash
# Solución:
1. Actualizar reference_images/sap_icon.png
2. Ajustar sap_icon_confidence en config.yaml
3. Ejecutar diagnose_sap_detection.py
```

#### "Google Drive upload failed"
```bash
# Solución:
1. Revisar oauth_credentials.json
2. Eliminar token.pickle para re-autorizar
3. Verificar folder_id en config.yaml
4. Ejecutar verificar_google_drive.py
```

#### "Template matching timeout"
```bash
# Solución:
1. Aumentar template_matching.timeout
2. Actualizar imágenes de referencia
3. Habilitar debug_screenshots
4. Revisar confidence thresholds
```

### 🔧 Comandos de Diagnóstico
```bash
# Ver estado del sistema
python -c "from rpa.config_manager import config; print(config.validate_config())"

# Test componentes individuales
python -c "from rpa.vision.main import Vision; v=Vision(); print('Vision OK')"

# Verificar Google Drive
python verificar_google_drive_api.py

# Ver archivos pendientes
ls ./data/outputs_json/*.json

# Limpiar logs antiguos
del .\logs\*.log

# Reiniciar sistema completo
taskkill /f /im python.exe
python main.py
```

## 🔄 Migración y Actualizaciones

### 📝 Historial de Versiones
- **v1.0**: Sistema RPA básico
- **v1.5**: Refactorización con módulos
- **v2.0**: Máquina de estados
- **v2.5**: Integración Google Drive (actual)

### 🚀 Para Nuevas Funcionalidades

#### Agregar Nuevo Estado
```python
# 1. En state_machine.py
class RPAState(Enum):
    NEW_STATE = "new_state"

# 2. En rpa_state_handlers.py
def handle_new_state(self, context, **kwargs):
    # Lógica del nuevo estado
    return RPAEvent.NEW_EVENT_SUCCESS

# 3. Registrar en rpa_with_state_machine.py
self.state_machine.register_state_handler(
    RPAState.NEW_STATE, 
    self.state_handlers.handle_new_state
)
```

#### Agregar Nueva Configuración
```yaml
# En config.yaml
new_feature:
  enabled: true
  timeout: 30.0
  max_retries: 3
```

```python
# En código
from rpa.config_manager import get_config
enabled = get_config('new_feature.enabled', False)
```

## 👥 Información para Desarrolladores

### 🧩 Patrón de Arquitectura
- **Estado**: Representa donde está el proceso
- **Evento**: Trigger para cambio de estado
- **Contexto**: Información compartida entre estados
- **Handler**: Lógica específica de cada estado

### 📚 APIs Importantes

#### State Machine
```python
# Obtener estado actual
current = rpa.state_machine.get_current_state()

# Disparar evento
rpa.state_machine.trigger_event(RPAEvent.START_PROCESSING)

# Obtener contexto
context = rpa.state_machine.get_context()
```

#### Vision System
```python
# Template matching
coordinates = vision.find_sap_icon_coordinates()

# OCR
text = vision.ocr_text_in_region(x, y, width, height)
```

#### Configuration
```python
# Obtener configuración
delay = get_delay('after_click')
confidence = get_confidence('sap_icon')
tabs = get_navigation_tabs('after_nit')
```

### 🎯 Mejores Prácticas
1. **Siempre usar configuración externa** (`config.yaml`)
2. **Manejar errores con try/catch y logging**
3. **Validar inputs antes de procesar**
4. **Usar esperas inteligentes, no `time.sleep()` fijos**
5. **Actualizar reference images cuando SAP cambie**
6. **Tests unitarios para nuevos features**

## 📞 Soporte y Contacto

### 🆘 En Caso de Emergencia
1. **Revisar logs**: `./logs/rpa.log` y `./logs/rpa_errors.log`
2. **Ejecutar diagnósticos**: Scripts en `/scripts/debug/`
3. **Verificar config**: `config.yaml` formato válido
4. **Reiniciar limpio**: Matar Python + reiniciar
5. **Validar conectividad**: RDP y SAP operativos

### 📊 Información del Sistema
- **Versión Actual**: 2.5 (Con Google Drive)
- **Python Requerido**: 3.8+
- **SO Soportado**: Windows 10/11
- **SAP Version**: Business One
- **Última Actualización**: Agosto 2024

---

## 🏆 Características Destacadas del Sistema

✅ **Máquina de Estados Robusta** - Control de flujo infalible  
✅ **Integración Google Drive** - Subida automática de archivos  
✅ **Sistema Visión Híbrido** - Template matching + OCR backup  
✅ **Configuración 100% Externa** - Sin valores hardcoded  
✅ **Logging Estructurado** - Debug y monitoreo completo  
✅ **Recuperación de Errores** - Reintentos automáticos  
✅ **Tests Comprehensivos** - Validación de cada componente  
✅ **Performance Optimizado** - Cache y esperas inteligentes  

**⚡ Sistema probado en producción, robusto y completamente automatizado ⚡**

---

*Este documento debe ser mantenido actualizado con cada cambio significativo al sistema. Para modificaciones, contactar al equipo de desarrollo.*