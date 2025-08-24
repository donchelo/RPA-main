# 🔧 GUÍA TÉCNICA DETALLADA - COMPONENTES RPA

## 📋 INFORMACIÓN TÉCNICA ESPECÍFICA PARA AGENTES FUTUROS

---

## 🧠 COMPONENTES PRINCIPALES - ANÁLISIS DETALLADO

### 1️⃣ **RPAWithStateMachine** - Controlador Principal

**Ubicación**: `rpa/rpa_with_state_machine.py`

**Responsabilidades**:
- Orquestar todo el flujo de procesamiento
- Manejar la máquina de estados
- Coordinar entre componentes
- Gestionar reintentos automáticos

**Métodos Clave**:
```python
def run(self):
    """Método principal que ejecuta el ciclo completo"""
    # 1. Escanea archivos JSON
    # 2. Procesa cada archivo con máquina de estados
    # 3. Maneja errores y reintentos

def process_single_file(self, file_path: str, data: dict) -> bool:
    """Procesa un archivo JSON individual"""
    # Maneja el flujo completo para un archivo
```

**Puntos de Atención**:
- Usa `StateMachine` para control de flujo
- Cada estado tiene su propio manejador en `RPAStateHandlers`
- Manejo automático de errores con reintentos

---

### 2️⃣ **StateMachine** - Máquina de Estados

**Ubicación**: `rpa/state_machine.py`

**Estados Definidos**:
```python
class RPAState(Enum):
    IDLE = "idle"                           # Estado inicial
    CONNECTING_REMOTE_DESKTOP = "connecting_remote_desktop"
    OPENING_SAP = "opening_sap"
    NAVIGATING_TO_SALES_ORDER = "navigating_to_sales_order"
    LOADING_NIT = "loading_nit"
    LOADING_ORDER = "loading_order"
    LOADING_DATE = "loading_date"
    LOADING_ITEMS = "loading_items"
    TAKING_SCREENSHOT = "taking_screenshot"
    MOVING_JSON = "moving_json"
    POSITIONING_MOUSE = "positioning_mouse"
    COMPLETED = "completed"
    ERROR = "error"
    RETRYING = "retrying"
```

**Transiciones Automáticas**:
```python
# Éxito: Estado actual → Siguiente estado
# Error: Estado actual → ERROR → RETRYING (hasta 3 intentos)
# Máximo reintentos: ERROR → COMPLETED (marcar como fallido)
```

**Contexto de Estado**:
```python
@dataclass
class StateContext:
    current_file: Optional[str] = None      # Archivo actual
    current_data: Optional[Dict] = None     # Datos del JSON
    retry_count: int = 0                    # Contador de reintentos
    max_retries: int = 3                    # Máximo reintentos
    error_message: Optional[str] = None     # Mensaje de error
    start_time: Optional[float] = None      # Tiempo de inicio
    last_successful_state: Optional[RPAState] = None
    processing_stats: Dict[str, Any] = None # Estadísticas
```

---

### 3️⃣ **Vision System** - Sistema de Visión Híbrido

**Ubicación**: `rpa/vision/main.py`

**Componentes**:
- **Template Matcher**: Detección rápida con OpenCV
- **OCR Engine**: Backup robusto con Tesseract + EasyOCR

**Métodos Principales**:
```python
def get_sap_coordinates_robust(self):
    """Detección híbrida del icono de SAP"""
    # 1. Intenta template matching
    # 2. Si falla, usa OCR como backup

def get_client_coordinates(self):
    """Obtiene coordenadas del campo cliente"""
    # Usa offset específico para precisión

def get_orden_coordinates(self):
    """Obtiene coordenadas del campo orden"""
    # Offset específico para orden de compra
```

**Imágenes de Referencia Críticas**:
```python
# Cargadas en __init__
self.sap_icon_image = cv2.imread('./rpa/vision/reference_images/sap_icon.png')
self.sap_orden_de_ventas_template_image = cv2.imread('./rpa/vision/reference_images/sap_orden_de_ventas_template.png')
self.client_field_image = cv2.imread('./rpa/vision/reference_images/client_field.png')
self.orden_compra_image = cv2.imread('./rpa/vision/reference_images/orden_compra.png')
self.fecha_entrega_image = cv2.imread('./rpa/vision/reference_images/fecha_entrega.png')
self.primer_articulo_image = cv2.imread('./rpa/vision/reference_images/primer_articulo.png')
```

---

### 4️⃣ **SmartWaits** - Esperas Inteligentes

**Ubicación**: `rpa/smart_waits.py`

**Funcionalidades**:
```python
def wait_for_element(self, check_function, timeout=None, description="elemento"):
    """Espera hasta que un elemento esté disponible"""
    # Espera condicional con timeout configurable

def wait_for_template(self, template_image, confidence=0.8, timeout=None):
    """Espera hasta que aparezca un template"""
    # Espera específica para template matching

def adaptive_wait(self, operation_type, base_delay=None):
    """Espera adaptativa según condiciones"""
    # Ajusta tiempos según el contexto
```

**Configuración desde YAML**:
```yaml
delays:
  after_input: 1.0      # Espera después de escribir
  after_click: 1.0      # Espera después de clic
  sap_startup: 25.0     # Espera para startup de SAP
  after_nit: 2.0        # Espera después de cargar NIT
  after_order: 1.0      # Espera después de cargar orden
  after_date: 1.0       # Espera después de cargar fecha
  after_item_code: 2.0  # Espera después de código
  after_quantity: 2.0   # Espera después de cantidad
```

---

### 5️⃣ **ConfigManager** - Gestor de Configuración

**Ubicación**: `rpa/config_manager.py`

**Funcionalidades**:
```python
def get(self, key_path: str, default: Any = None) -> Any:
    """Obtiene configuración usando notación de puntos"""
    # Ejemplo: get('delays.after_input') → 1.0

def reload_config(self):
    """Recarga configuración sin reiniciar"""
    # Útil para cambios en tiempo de ejecución
```

**Funciones de Acceso Rápido**:
```python
# Importadas directamente para uso rápido
from rpa.config_manager import (
    get_delay,           # get_delay('after_input')
    get_navigation_tabs, # get_navigation_tabs('after_nit')
    get_retry_attempts,  # get_retry_attempts('max_sap_open_attempts')
    get_confidence,      # get_confidence('sap_icon')
    get_timeout          # get_timeout('template_matching')
)
```

---

### 6️⃣ **SimpleLogger** - Sistema de Logging

**Ubicación**: `rpa/simple_logger.py`

**Características**:
- **Rotación automática**: 5MB principal, 2MB errores
- **Múltiples handlers**: Archivo principal, errores, consola
- **Contexto automático**: Incluye función y línea de código

**Métodos Principales**:
```python
def log_action(self, action: str, details: str = ""):
    """Registra acciones del RPA"""
    # Para tracking de operaciones

def log_error(self, error: str, context: str = ""):
    """Registra errores con contexto"""
    # Para debugging y troubleshooting

def log_performance(self, operation: str, duration: float):
    """Registra métricas de rendimiento"""
    # Para optimización
```

**Archivos de Log**:
- `logs/rpa.log` - Log principal
- `logs/rpa_errors.log` - Solo errores
- Rotación automática con backup

---

## 🔧 CONFIGURACIONES CRÍTICAS

### ⚙️ **Template Matching**

```yaml
template_matching:
  default_confidence: 0.8    # Umbral general
  low_confidence: 0.5        # Para casos difíciles
  high_confidence: 0.9       # Para elementos críticos
  sap_icon_confidence: 0.7   # Específico para SAP
  timeout: 10.0              # Timeout en segundos
```

### ⌨️ **Navegación por Teclado**

```yaml
navigation:
  tabs_after_nit: 3          # Tabs después del NIT
  tabs_after_order: 4        # Tabs después de orden
  tabs_after_date: 4         # Tabs después de fecha
  tabs_before_quantity: 2    # Tabs antes de cantidad
  tabs_after_quantity_next_item: 3  # Tabs para siguiente artículo
  tabs_after_last_quantity: 1       # Tabs después del último artículo
```

### 🔄 **Sistema de Reintentos**

```yaml
retries:
  max_sap_open_attempts: 3   # Intentos para abrir SAP
  max_remote_desktop_attempts: 3  # Intentos para RDP
  retry_delay: 5             # Segundos entre reintentos
```

---

## 🚨 MANEJO DE ERRORES ESPECÍFICO

### 🛡️ **Tipos de Error Definidos**

```python
class ErrorType(Enum):
    TEMPLATE_ERROR = "template_error"      # Template matching falló
    WINDOW_ERROR = "window_error"          # Ventana no encontrada
    SAP_ERROR = "sap_error"                # Error en SAP
    NAVIGATION_ERROR = "navigation_error"  # Error de navegación
    CONFIG_ERROR = "config_error"          # Error de configuración
    SYSTEM_ERROR = "system_error"          # Error del sistema
```

### 🔄 **Estrategias de Recuperación**

```python
# Template Error → OCR Backup
if template_fails:
    coordinates = vision.ocr_fallback()

# Window Error → Reintento
if window_not_found:
    retry_with_delay()

# SAP Error → Reinicio de SAP
if sap_error:
    restart_sap_process()

# Navigation Error → Ajuste de tabs
if navigation_fails:
    adjust_tab_count()
```

---

## 📊 FORMATO DE DATOS Y VALIDACIONES

### 📄 **Estructura JSON Esperada**

```json
{
  "comprador": {
    "nit": "CN800069933",        // Obligatorio: Solo números
    "nombre": "COMODIN S.A.S."   // Opcional
  },
  "orden_compra": "4500223571",  // Obligatorio: Alfanumérico
  "fecha_entrega": "01/09/2025", // Obligatorio: DD/MM/YYYY
  "items": [                     // Obligatorio: Array no vacío
    {
      "codigo": "14010682001",   // Obligatorio: No vacío
      "cantidad": 1408,          // Obligatorio: Número > 0
      "descripcion": "..."       // Opcional
    }
  ],
  "valor_total": 115456          // Opcional: Número
}
```

### ✅ **Validaciones Automáticas**

```python
# Validaciones implementadas en el sistema
- NIT: Solo números, longitud correcta
- Orden: Formato alfanumérico válido
- Fecha: DD/MM/YYYY con validación de fecha real
- Items: Array con al menos un elemento
- Códigos: No vacíos, formato válido
- Cantidades: Números positivos
```

---

## 🔧 COMANDOS DE DEBUG Y TROUBLESHOOTING

### 📋 **Verificación del Sistema**

```bash
# Verificar configuración
python -c "from rpa.config_manager import config; print(config.validate_config())"

# Verificar dependencias
python -c "import cv2, pytesseract, easyocr; print('Dependencias OK')"

# Verificar imágenes de referencia
ls ./rpa/vision/reference_images/*.png

# Verificar logs
tail -n 50 ./logs/rpa.log
```

### 🚨 **Diagnóstico de Errores**

```bash
# Ver errores recientes
grep "ERROR" ./logs/rpa_errors.log | tail -20

# Ver métricas de rendimiento
grep "PERFORMANCE" ./logs/rpa.log | tail -10

# Ver archivos procesados hoy
ls ./data/outputs_json/Procesados/ | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}
```

### 🔧 **Ajustes Rápidos**

```bash
# Aumentar tiempo de espera SAP
# Editar config.yaml: delays.sap_startup: 30.0

# Reducir confianza de template
# Editar config.yaml: template_matching.default_confidence: 0.7

# Aumentar reintentos
# Editar config.yaml: retries.max_sap_open_attempts: 5
```

---

## 🎯 PUNTOS DE EXTENSIÓN

### 🔧 **Agregar Nuevo Estado**

```python
# 1. Definir en state_machine.py
class RPAState(Enum):
    NEW_STATE = "new_state"

# 2. Agregar transiciones
self.transitions[RPAState.NEW_STATE] = {
    RPAEvent.SUCCESS: RPAState.NEXT_STATE,
    RPAEvent.FAILURE: RPAState.ERROR
}

# 3. Crear manejador en rpa_state_handlers.py
def handle_new_state(self, context):
    # Lógica del nuevo estado
    pass

# 4. Registrar en RPAWithStateMachine
self.state_machine.register_state_handler(
    RPAState.NEW_STATE, self.state_handlers.handle_new_state
)
```

### ⚙️ **Agregar Nueva Configuración**

```yaml
# En config.yaml
custom:
  new_feature_enabled: true
  custom_timeout: 20.0
  custom_retries: 5
```

```python
# En código
from rpa.config_manager import get_config
value = get_config('custom.new_feature_enabled', default=False)
```

---

## 📞 INFORMACIÓN TÉCNICA ADICIONAL

### 🔧 **Dependencias Críticas**

```txt
# requirements.txt - Versiones específicas
PyAutoGUI==0.9.54          # Automatización de interfaz
opencv-python==4.10.0.84   # Visión computacional
pytesseract==0.3.10        # OCR principal
easyocr==1.7.0             # OCR backup
schedule==1.2.2            # Programación de tareas
PyYAML==6.0.2              # Configuración YAML
```

### 🌐 **Dependencias Externas**

- **Tesseract OCR**: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **Conexión RDP**: `20.96.6.64`
- **SAP Business One**: Disponible en escritorio remoto
- **Python**: 3.8+ (recomendado 3.9+)

### 📊 **Métricas de Rendimiento Esperadas**

- **Tiempo por artículo**: 12-18 segundos
- **Tiempo por archivo**: 60-90 segundos
- **Archivos por hora**: 40-60
- **Tasa de éxito**: >95%
- **Uso de memoria**: ~100MB
- **CPU**: <10% en uso normal

---

## 🏆 RESUMEN PARA AGENTES FUTUROS

**Este sistema RPA está diseñado con arquitectura modular y configuración externa, permitiendo modificaciones sin tocar código. La máquina de estados garantiza control robusto, mientras que el sistema de visión híbrido asegura detección confiable. El logging estructurado y manejo de errores automático facilitan el debugging y mantenimiento.**

**⚡ Sistema profesional, mantenible y extensible ⚡**
