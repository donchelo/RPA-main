"""
Constantes globales para el sistema RPA
Centraliza configuraciones y elimina números mágicos del código
"""

# Configuración de ventanas
REMOTE_DESKTOP_WINDOW = "20.96.6.64 - Conexión a Escritorio remoto"

# Tiempos de espera (en segundos)
class Delays:
    VERY_SHORT = 0.1
    SHORT = 0.5
    MEDIUM = 1.0
    LONG = 2.0
    VERY_LONG = 3.0
    
    # Específicos para operaciones
    AFTER_INPUT = 1.0
    AFTER_CLICK = 1.0
    AFTER_TAB = 0.5
    AFTER_NIT = 2.0
    AFTER_ORDER = 1.0
    AFTER_DATE = 1.0
    AFTER_ITEM_CODE = 3.0
    AFTER_QUANTITY = 2.0
    
    # Esperas largas para carga
    SAP_STARTUP = 30.0
    SCREENSHOT_WAIT = 1.0
    NAVIGATION_WAIT = 2.0
    WINDOW_ACTIVATION = 2.0
    SAP_DOUBLE_CLICK = 10.0

# Configuración de directorios
class Paths:
    DATA_JSON = './data/outputs_json'
    PROCESSED_JSON = './data/outputs_json/Procesados'
    REFERENCE_IMAGES = './rpa/vision/reference_images'
    INSERTED_ORDERS = './rpa/vision/reference_images/inserted_orders'
    TEMPLATE_IMAGE = './rpa/vision/reference_images/template.png'
    SAP_DESKTOP = './rpa/vision/reference_images/sap_desktop.png'
    REMOTE_DESKTOP = './rpa/vision/reference_images/remote_desktop.png'
    SAP_ORDER_TEMPLATE = './rpa/vision/reference_images/sap_orden_de_ventas_template.png'

# Configuración de template matching
class TemplateMatching:
    DEFAULT_CONFIDENCE = 0.8
    LOW_CONFIDENCE = 0.5
    HIGH_CONFIDENCE = 0.9
    SAP_ICON_CONFIDENCE = 0.7
    SCROLLBAR_CONFIDENCE = 0.8
    
# Configuración de reintentos
class Retries:
    MAX_SAP_OPEN_ATTEMPTS = 3
    MAX_REMOTE_DESKTOP_ATTEMPTS = 3
    RETRY_DELAY = 5
    
# Configuración de navegación por teclado
class Navigation:
    TABS_AFTER_NIT = 3
    TABS_AFTER_ORDER = 4
    TABS_AFTER_DATE = 4
    TABS_BEFORE_QUANTITY = 2
    TABS_AFTER_QUANTITY_NEXT_ITEM = 3
    TABS_AFTER_LAST_QUANTITY = 1

# Configuración de archivos
class FileConfig:
    VALID_EXTENSIONS = ['.json']
    EXCLUDE_PREFIXES = ['.', 'desktop.ini']
    EXCLUDE_SUFFIXES = ['.tmp']

# Configuración de logging
class LogConfig:
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    BACKUP_COUNT = 3
    ERROR_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    ERROR_BACKUP_COUNT = 2

# Tesseract configuration
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración OCR
class OCRConfig:
    TESSERACT_CONFIG = r'--oem 3 --psm 6'
    EASYOCR_LANGUAGES = ['en']
    EASYOCR_GPU = False

# Palabras clave para detección de totales
TOTALES_KEYWORDS = [
    "Total antes del descuento",
    "Descuento", 
    "Gastos adicionales",
    "Redondeo",
    "Impuesto",
    "Total del documento",
    "Total antes",
    "Total documento"
]

# Configuración de ventana
class WindowConfig:
    ACTIVATION_WAIT = 2.0
    MAXIMIZE_SHORTCUT_WAIT = 0.5

# Configuración de sistema
class SystemConfig:
    MAIN_LOOP_INTERVAL = 10  # segundos
    SCHEDULE_INTERVAL = 10   # minutos
    ERROR_RECOVERY_WAIT = 30 # segundos
    
# Mensajes de estado
class Messages:
    SYSTEM_STARTUP = "=== SISTEMA RPA TAMAPRINT ==="
    SYSTEM_ACTIVE = "Sistema RPA activo. Presiona Ctrl+C para detener."
    SYSTEM_MONITORING = "Sistema RPA en espera - monitoreando nuevos archivos JSON..."
    SYSTEM_STOPPED = "Sistema RPA detenido por el usuario."
    NEXT_EXECUTION = "Proceso RPA completado, esperando próxima ejecución en 10 minutos"