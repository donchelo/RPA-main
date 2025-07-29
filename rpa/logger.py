import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class RPALogger:
    def __init__(self, name="RPA", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        self.setup_logger()
    
    def setup_logger(self):
        """Configura el sistema de logging con rotación de archivos"""
        # Crear directorio de logs si no existe
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Configurar el logger principal
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicación de handlers
        if self.logger.handlers:
            return
        
        # Handler para archivo con rotación (máximo 5 archivos de 10MB cada uno)
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato personalizado
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregar handlers al logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Registra un mensaje de nivel INFO"""
        self.logger.info(message)
    
    def debug(self, message):
        """Registra un mensaje de nivel DEBUG"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Registra un mensaje de nivel WARNING"""
        self.logger.warning(message)
    
    def error(self, message):
        """Registra un mensaje de nivel ERROR"""
        self.logger.error(message)
    
    def critical(self, message):
        """Registra un mensaje de nivel CRITICAL"""
        self.logger.critical(message)
    
    def log_action(self, action, details=None):
        """Método específico para logging de acciones RPA"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"ACTION: {action}"
        if details:
            message += f" | DETAILS: {details}"
        self.info(message)
    
    def log_error(self, error, context=None):
        """Método específico para logging de errores"""
        message = f"ERROR: {error}"
        if context:
            message += f" | CONTEXT: {context}"
        self.error(message)
    
    def log_performance(self, operation, duration):
        """Método para logging de rendimiento"""
        self.info(f"PERFORMANCE: {operation} completed in {duration:.2f} seconds")

# Instancia global del logger
rpa_logger = RPALogger() 