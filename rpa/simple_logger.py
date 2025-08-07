"""
Sistema de logging simplificado para RPA
Reemplaza el sistema complejo anterior con una versión ligera y eficiente
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class SimpleRPALogger:
    """Logger simplificado para RPA con funcionalidades esenciales"""
    
    def __init__(self, name="RPA", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        self.setup_logger()
    
    def setup_logger(self):
        """Configura el logger con handlers básicos pero eficientes"""
        # Crear directorio de logs si no existe
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Configurar el logger principal
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicación de handlers
        if self.logger.handlers:
            return
        
        # Handler principal con rotación
        main_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        main_handler.setLevel(logging.INFO)
        
        # Handler para errores
        error_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa_errors.log'),
            maxBytes=2*1024*1024,  # 2MB
            backupCount=2,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formateador simple y claro
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Aplicar formateadores
        main_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregar handlers
        self.logger.addHandler(main_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message, context=None):
        """Registra mensaje de información"""
        if context:
            if isinstance(context, dict):
                context_str = " | ".join([f"{k}: {v}" for k, v in context.items()])
            else:
                context_str = str(context)
            message = f"{message} | Context: {context_str}"
        self.logger.info(message)
    
    def debug(self, message, context=None):
        """Registra mensaje de debug"""
        if context:
            if isinstance(context, dict):
                context_str = " | ".join([f"{k}: {v}" for k, v in context.items()])
            else:
                context_str = str(context)
            message = f"{message} | Context: {context_str}"
        self.logger.debug(message)
    
    def warning(self, message, context=None):
        """Registra mensaje de advertencia"""
        if context:
            if isinstance(context, dict):
                context_str = " | ".join([f"{k}: {v}" for k, v in context.items()])
            else:
                context_str = str(context)
            message = f"{message} | Context: {context_str}"
        self.logger.warning(message)
    
    def error(self, message, context=None):
        """Registra mensaje de error"""
        if context:
            if isinstance(context, dict):
                context_str = " | ".join([f"{k}: {v}" for k, v in context.items()])
            else:
                context_str = str(context)
            message = f"{message} | Context: {context_str}"
        self.logger.error(message)
    
    def critical(self, message, context=None):
        """Registra mensaje crítico"""
        if context:
            if isinstance(context, dict):
                context_str = " | ".join([f"{k}: {v}" for k, v in context.items()])
            else:
                context_str = str(context)
            message = f"{message} | Context: {context_str}"
        self.logger.critical(message)
    
    def log_action(self, action, details=None):
        """Método específico para logging de acciones RPA"""
        context = {'action': action, 'timestamp': datetime.now().isoformat()}
        if details:
            context['details'] = details
        self.info(f"ACTION: {action}", context)
    
    def log_error(self, error, context=None):
        """Método específico para logging de errores"""
        error_context = {'error': str(error), 'timestamp': datetime.now().isoformat()}
        if context:
            if isinstance(context, dict):
                error_context.update(context)
            else:
                error_context['context'] = str(context)
        self.error(f"ERROR: {error}", error_context)
    
    def log_performance(self, operation, duration):
        """Método para logging de rendimiento"""
        context = {
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        self.info(f"PERFORMANCE: {operation} completed in {duration:.2f}s", context)


# Instancia global del logger
rpa_logger = SimpleRPALogger()