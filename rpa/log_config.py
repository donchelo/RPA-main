"""
Configuración avanzada del sistema de logs para RPA
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configuración básica
LOG_DIR = "logs"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5

# Configuración de formato
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Configuración de archivos específicos
RPA_LOG_FILE = "rpa.log"
ERROR_LOG_FILE = "rpa_errors.log"
PERFORMANCE_LOG_FILE = "rpa_performance.log"
STRUCTURED_LOG_FILE = "rpa_structured.log"
METRICS_LOG_FILE = "rpa_metrics.log"

# Configuración de niveles por módulo
MODULE_LOG_LEVELS = {
    "RPA": "INFO",
    "RPA.vision": "DEBUG",
    "RPA.json_parser": "INFO",
    "RPA.metrics": "INFO"
}

# Configuración de alertas
ALERT_CONFIG = {
    'error_rate_threshold': 0.1,  # 10% de errores
    'response_time_threshold': 30.0,  # 30 segundos
    'consecutive_errors_threshold': 3,  # 3 errores consecutivos
    'session_duration_threshold': 3600,  # 1 hora
    'alert_cooldown': 300,  # 5 minutos entre alertas del mismo tipo
    'max_recent_errors': 100  # Máximo 100 errores recientes
}

# Configuración de métricas
METRICS_CONFIG = {
    'enable_performance_tracking': True,
    'enable_error_tracking': True,
    'enable_session_tracking': True,
    'metrics_summary_interval': 3600,  # 1 hora
    'cleanup_old_logs_days': 30,
    'max_metrics_history': 1000
}

# Configuración de rotación de archivos
ROTATION_CONFIG = {
    'main_log': {
        'max_bytes': 10 * 1024 * 1024,  # 10MB
        'backup_count': 5
    },
    'error_log': {
        'max_bytes': 5 * 1024 * 1024,  # 5MB
        'backup_count': 3
    },
    'performance_log': {
        'max_bytes': 5 * 1024 * 1024,  # 5MB
        'backup_count': 3
    },
    'structured_log': {
        'max_bytes': 15 * 1024 * 1024,  # 15MB
        'backup_count': 7
    },
    'metrics_log': {
        'max_bytes': 3 * 1024 * 1024,  # 3MB
        'backup_count': 2
    }
}

# Configuración de compresión
COMPRESSION_CONFIG = {
    'enable_compression': True,
    'compress_after_days': 7,  # Comprimir logs después de 7 días
    'compression_level': 6  # Nivel de compresión (1-9)
}

# Configuración de monitoreo
MONITORING_CONFIG = {
    'enable_health_checks': True,
    'health_check_interval': 300,  # 5 minutos
    'disk_space_threshold': 0.9,  # 90% de uso del disco
    'memory_usage_threshold': 0.8,  # 80% de uso de memoria
    'log_file_size_threshold': 50 * 1024 * 1024  # 50MB
}

class LogConfig:
    """Clase para manejar la configuración de logs"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "log_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo o usa valores por defecto"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config file: {e}")
        
        # Configuración por defecto
        return {
            'log_dir': LOG_DIR,
            'log_level': LOG_LEVEL,
            'max_file_size': MAX_FILE_SIZE,
            'backup_count': BACKUP_COUNT,
            'log_format': LOG_FORMAT,
            'date_format': DATE_FORMAT,
            'files': {
                'main': RPA_LOG_FILE,
                'error': ERROR_LOG_FILE,
                'performance': PERFORMANCE_LOG_FILE,
                'structured': STRUCTURED_LOG_FILE,
                'metrics': METRICS_LOG_FILE
            },
            'module_levels': MODULE_LOG_LEVELS,
            'alerts': ALERT_CONFIG,
            'metrics': METRICS_CONFIG,
            'rotation': ROTATION_CONFIG,
            'compression': COMPRESSION_CONFIG,
            'monitoring': MONITORING_CONFIG
        }
    
    def save_config(self):
        """Guarda la configuración actual en archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Establece un valor de configuración"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_log_file_path(self, file_type: str) -> str:
        """Obtiene la ruta completa de un archivo de log"""
        log_dir = self.get('log_dir', LOG_DIR)
        filename = self.get(f'files.{file_type}', f'rpa_{file_type}.log')
        return os.path.join(log_dir, filename)
    
    def get_rotation_config(self, file_type: str) -> Dict[str, Any]:
        """Obtiene la configuración de rotación para un tipo de archivo"""
        return self.get(f'rotation.{file_type}', {
            'max_bytes': 10 * 1024 * 1024,
            'backup_count': 5
        })

def get_log_config() -> Dict[str, Any]:
    """Retorna la configuración del sistema de logs"""
    config = LogConfig()
    return config.config

def setup_log_directory():
    """Crea el directorio de logs si no existe"""
    log_dir = get_log_config().get('log_dir', LOG_DIR)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Directorio de logs creado: {log_dir}")

def get_timestamp():
    """Retorna el timestamp actual formateado"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_log_message(level: str, message: str, context: Optional[Dict] = None) -> str:
    """Formatea un mensaje de log con contexto opcional"""
    timestamp = get_timestamp()
    formatted_message = f"[{timestamp}] {level}: {message}"
    if context:
        formatted_message += f" | Context: {json.dumps(context, ensure_ascii=False)}"
    return formatted_message

def validate_config() -> bool:
    """Valida la configuración de logs"""
    config = get_log_config()
    
    # Verificar directorio de logs
    log_dir = config.get('log_dir')
    if not log_dir:
        print("ERROR: log_dir no está configurado")
        return False
    
    # Verificar niveles de log válidos
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    log_level = config.get('log_level')
    if log_level not in valid_levels:
        print(f"ERROR: log_level '{log_level}' no es válido. Debe ser uno de: {valid_levels}")
        return False
    
    # Verificar archivos de log
    files = config.get('files', {})
    for file_type, filename in files.items():
        if not filename:
            print(f"ERROR: filename no configurado para {file_type}")
            return False
    
    print("Configuración de logs válida")
    return True

def create_log_config_file():
    """Crea un archivo de configuración de ejemplo"""
    config = LogConfig()
    config.save_config()
    print(f"Archivo de configuración creado: {config.config_file}")

def get_health_status() -> Dict[str, Any]:
    """Obtiene el estado de salud del sistema de logs"""
    config = get_log_config()
    log_dir = config.get('log_dir', LOG_DIR)
    
    health_status = {
        'timestamp': datetime.now().isoformat(),
        'log_directory_exists': os.path.exists(log_dir),
        'log_directory_writable': os.access(log_dir, os.W_OK) if os.path.exists(log_dir) else False,
        'config_valid': validate_config(),
        'files_status': {}
    }
    
    # Verificar archivos de log
    if os.path.exists(log_dir):
        files = config.get('files', {})
        for file_type, filename in files.items():
            file_path = os.path.join(log_dir, filename)
            health_status['files_status'][file_type] = {
                'exists': os.path.exists(file_path),
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                'writable': os.access(file_path, os.W_OK) if os.path.exists(file_path) else False
            }
    
    return health_status

# Funciones de utilidad para métricas
def calculate_disk_usage(log_dir: str) -> float:
    """Calcula el uso de disco del directorio de logs"""
    if not os.path.exists(log_dir):
        return 0.0
    
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(log_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    
    return total_size / (1024 * 1024)  # MB

def get_log_file_info(log_dir: str) -> Dict[str, Any]:
    """Obtiene información detallada de los archivos de log"""
    if not os.path.exists(log_dir):
        return {}
    
    file_info = {}
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            filepath = os.path.join(log_dir, filename)
            stat = os.stat(filepath)
            file_info[filename] = {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
            }
    
    return file_info 