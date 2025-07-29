"""
Configuración del sistema de logs para RPA
"""

import os
from datetime import datetime

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

# Configuración de niveles por módulo
MODULE_LOG_LEVELS = {
    "RPA": "INFO",
    "RPA.vision": "DEBUG",
    "RPA.json_parser": "INFO"
}

def get_log_config():
    """Retorna la configuración del sistema de logs"""
    return {
        "log_dir": LOG_DIR,
        "log_level": LOG_LEVEL,
        "max_file_size": MAX_FILE_SIZE,
        "backup_count": BACKUP_COUNT,
        "log_format": LOG_FORMAT,
        "date_format": DATE_FORMAT,
        "rpa_log_file": RPA_LOG_FILE,
        "error_log_file": ERROR_LOG_FILE,
        "performance_log_file": PERFORMANCE_LOG_FILE,
        "module_log_levels": MODULE_LOG_LEVELS
    }

def setup_log_directory():
    """Crea el directorio de logs si no existe"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"Directorio de logs creado: {LOG_DIR}")

def get_timestamp():
    """Retorna el timestamp actual formateado"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_log_message(level, message, context=None):
    """Formatea un mensaje de log con contexto opcional"""
    timestamp = get_timestamp()
    formatted_message = f"[{timestamp}] {level}: {message}"
    if context:
        formatted_message += f" | Context: {context}"
    return formatted_message 