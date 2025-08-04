import logging
import os
import json
import time
import threading
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from collections import defaultdict, deque
import traceback
import sys

class RPAMetrics:
    """Clase para manejar métricas de rendimiento del RPA"""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
            'errors': 0,
            'last_execution': None,
            'success_rate': 0.0
        })
        self.recent_errors = deque(maxlen=100)
        self.session_start = time.time()
    
    def record_operation(self, operation, duration, success=True):
        """Registra una operación con su duración y resultado"""
        metric = self.metrics[operation]
        metric['count'] += 1
        metric['total_time'] += duration
        metric['min_time'] = min(metric['min_time'], duration)
        metric['max_time'] = max(metric['max_time'], duration)
        metric['last_execution'] = datetime.now()
        
        if not success:
            metric['errors'] += 1
        
        # Calcular tasa de éxito
        if metric['count'] > 0:
            metric['success_rate'] = ((metric['count'] - metric['errors']) / metric['count']) * 100
    
    def record_error(self, error_type, error_message, context=None):
        """Registra un error con contexto"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message,
            'context': context,
            'traceback': traceback.format_exc()
        }
        self.recent_errors.append(error_record)
    
    def get_operation_stats(self, operation):
        """Obtiene estadísticas de una operación específica"""
        metric = self.metrics[operation]
        if metric['count'] == 0:
            return None
        
        return {
            'operation': operation,
            'count': metric['count'],
            'avg_time': metric['total_time'] / metric['count'],
            'min_time': metric['min_time'] if metric['min_time'] != float('inf') else 0,
            'max_time': metric['max_time'],
            'errors': metric['errors'],
            'success_rate': metric['success_rate'],
            'last_execution': metric['last_execution'].isoformat() if metric['last_execution'] else None
        }
    
    def get_session_stats(self):
        """Obtiene estadísticas de la sesión actual"""
        session_duration = time.time() - self.session_start
        total_operations = sum(m['count'] for m in self.metrics.values())
        total_errors = sum(m['errors'] for m in self.metrics.values())
        
        return {
            'session_duration': session_duration,
            'total_operations': total_operations,
            'total_errors': total_errors,
            'overall_success_rate': ((total_operations - total_errors) / total_operations * 100) if total_operations > 0 else 0,
            'recent_errors_count': len(self.recent_errors)
        }

class RPAAlertManager:
    """Gestor de alertas para el sistema RPA"""
    
    def __init__(self, logger):
        self.logger = logger
        self.alert_thresholds = {
            'error_rate': 0.1,  # 10% de errores
            'response_time': 30.0,  # 30 segundos
            'consecutive_errors': 3,  # 3 errores consecutivos
            'session_duration': 3600  # 1 hora
        }
        self.consecutive_errors = 0
        self.last_alert_time = {}
    
    def check_alert_conditions(self, operation, duration, success, error_message=None):
        """Verifica condiciones de alerta y genera alertas si es necesario"""
        alerts = []
        
        # Verificar errores consecutivos
        if not success:
            self.consecutive_errors += 1
            if self.consecutive_errors >= self.alert_thresholds['consecutive_errors']:
                alert = {
                    'type': 'CONSECUTIVE_ERRORS',
                    'message': f'Demasiados errores consecutivos: {self.consecutive_errors}',
                    'severity': 'HIGH',
                    'operation': operation
                }
                alerts.append(alert)
        else:
            self.consecutive_errors = 0
        
        # Verificar tiempo de respuesta
        if duration > self.alert_thresholds['response_time']:
            alert = {
                'type': 'SLOW_RESPONSE',
                'message': f'Operación lenta: {duration:.2f}s > {self.alert_thresholds["response_time"]}s',
                'severity': 'MEDIUM',
                'operation': operation,
                'duration': duration
            }
            alerts.append(alert)
        
        # Generar alertas
        for alert in alerts:
            self._send_alert(alert)
    
    def _send_alert(self, alert):
        """Envía una alerta"""
        current_time = time.time()
        alert_key = f"{alert['type']}_{alert['operation']}"
        
        # Evitar spam de alertas (mínimo 5 minutos entre alertas del mismo tipo)
        if alert_key in self.last_alert_time:
            if current_time - self.last_alert_time[alert_key] < 300:  # 5 minutos
                return
        
        self.last_alert_time[alert_key] = current_time
        
        # Log de alerta
        alert_message = f"ALERTA [{alert['severity']}]: {alert['type']} - {alert['message']}"
        if alert['severity'] == 'HIGH':
            self.logger.critical(alert_message)
        elif alert['severity'] == 'MEDIUM':
            self.logger.warning(alert_message)
        else:
            self.logger.info(alert_message)

class StructuredFormatter(logging.Formatter):
    """Formateador estructurado para logs JSON"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.thread,
            'process': record.process
        }
        
        # Agregar campos adicionales si existen
        if hasattr(record, 'context'):
            log_entry['context'] = record.context
        if hasattr(record, 'metrics'):
            log_entry['metrics'] = record.metrics
        if hasattr(record, 'operation'):
            log_entry['operation'] = record.operation
        
        return json.dumps(log_entry, ensure_ascii=False)

class RPALogger:
    """Sistema de logging avanzado para RPA"""
    
    def __init__(self, name="RPA", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        self.metrics = RPAMetrics()
        self.alert_manager = None  # Se inicializa después del setup
        self.setup_logger()
        self.alert_manager = RPAAlertManager(self)
    
    def setup_logger(self):
        """Configura el sistema de logging con múltiples handlers y formatos"""
        # Crear directorio de logs si no existe
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Configurar el logger principal
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicación de handlers
        if self.logger.handlers:
            return
        
        # 1. Handler principal con rotación (formato legible)
        main_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        main_handler.setLevel(logging.INFO)
        
        # 2. Handler para errores separado
        error_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa_errors.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        # 3. Handler para logs estructurados (JSON)
        json_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa_structured.log'),
            maxBytes=15*1024*1024,  # 15MB
            backupCount=7,
            encoding='utf-8'
        )
        json_handler.setLevel(logging.DEBUG)
        
        # 4. Handler para métricas de rendimiento
        performance_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rpa_performance.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        performance_handler.setLevel(logging.INFO)
        
        # 5. Handler para consola (solo INFO y superior)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Configurar filtros
        class ErrorFilter(logging.Filter):
            def filter(self, record):
                return record.levelno >= logging.ERROR
        
        class PerformanceFilter(logging.Filter):
            def filter(self, record):
                return hasattr(record, 'metrics') or 'PERFORMANCE' in record.getMessage()
        
        error_handler.addFilter(ErrorFilter())
        performance_handler.addFilter(PerformanceFilter())
        
        # Formateadores
        readable_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        json_formatter = StructuredFormatter()
        
        # Aplicar formateadores
        main_handler.setFormatter(readable_formatter)
        error_handler.setFormatter(readable_formatter)
        console_handler.setFormatter(readable_formatter)
        json_handler.setFormatter(json_formatter)
        performance_handler.setFormatter(readable_formatter)
        
        # Agregar handlers al logger
        self.logger.addHandler(main_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(json_handler)
        self.logger.addHandler(performance_handler)
        self.logger.addHandler(console_handler)
    
    def _log_with_context(self, level, message, context=None, metrics=None, operation=None):
        """Método interno para logging con contexto"""
        record = self.logger.makeRecord(
            self.name, level, __file__, 0, message, (), None
        )
        
        if context:
            record.context = context
        if metrics:
            record.metrics = metrics
        if operation:
            record.operation = operation
        
        self.logger.handle(record)
    
    def info(self, message, context=None):
        """Registra un mensaje de nivel INFO"""
        self._log_with_context(logging.INFO, message, context)
    
    def debug(self, message, context=None):
        """Registra un mensaje de nivel DEBUG"""
        self._log_with_context(logging.DEBUG, message, context)
    
    def warning(self, message, context=None):
        """Registra un mensaje de nivel WARNING"""
        self._log_with_context(logging.WARNING, message, context)
    
    def error(self, message, context=None):
        """Registra un mensaje de nivel ERROR"""
        self._log_with_context(logging.ERROR, message, context)
    
    def critical(self, message, context=None):
        """Registra un mensaje de nivel CRITICAL"""
        self._log_with_context(logging.CRITICAL, message, context)
    
    def log_action(self, action, details=None, operation=None):
        """Método específico para logging de acciones RPA"""
        start_time = time.time()
        
        # Log de inicio de acción
        self.info(f"ACTION_START: {action}", {
            'action': action,
            'details': details,
            'operation': operation,
            'timestamp': datetime.now().isoformat()
        })
        
        return start_time
    
    def log_action_complete(self, action, start_time, success=True, details=None, operation=None):
        """Completa el logging de una acción con métricas"""
        duration = time.time() - start_time
        
        # Registrar métricas
        if operation:
            self.metrics.record_operation(operation, duration, success)
        
        # Verificar alertas
        if self.alert_manager:
            self.alert_manager.check_alert_conditions(operation or action, duration, success)
        
        # Log de finalización
        status = "SUCCESS" if success else "FAILED"
        self.info(f"ACTION_COMPLETE: {action} - {status} ({duration:.2f}s)", {
            'action': action,
            'status': status,
            'duration': duration,
            'details': details,
            'operation': operation
        })
        
        # Log de rendimiento
        self._log_with_context(
            logging.INFO,
            f"PERFORMANCE: {action} completed in {duration:.2f} seconds",
            {'duration': duration, 'operation': operation},
            {'duration': duration, 'operation': operation},
            operation
        )
    
    def log_error(self, error, context=None, operation=None):
        """Método específico para logging de errores"""
        # Registrar error en métricas
        if operation:
            self.metrics.record_error(operation, str(error), context)
        
        # Log del error
        self.error(f"ERROR: {error}", {
            'error': str(error),
            'context': context,
            'operation': operation,
            'traceback': traceback.format_exc()
        })
    
    def log_performance(self, operation, duration, additional_metrics=None):
        """Método para logging de rendimiento con métricas adicionales"""
        metrics = {
            'duration': duration,
            'operation': operation,
            'timestamp': datetime.now().isoformat()
        }
        
        if additional_metrics:
            metrics.update(additional_metrics)
        
        self._log_with_context(
            logging.INFO,
            f"PERFORMANCE: {operation} completed in {duration:.2f} seconds",
            metrics,
            metrics,
            operation
        )
    
    def get_metrics_summary(self):
        """Obtiene un resumen de métricas del sistema"""
        return {
            'session_stats': self.metrics.get_session_stats(),
            'operation_stats': {
                op: self.metrics.get_operation_stats(op)
                for op in self.metrics.metrics.keys()
            },
            'recent_errors': list(self.metrics.recent_errors)[-10:]  # Últimos 10 errores
        }
    
    def log_metrics_summary(self):
        """Registra un resumen de métricas"""
        summary = self.get_metrics_summary()
        self.info("METRICS_SUMMARY", summary)
    
    def cleanup_old_logs(self, days_to_keep=30):
        """Limpia logs antiguos"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleaned_files = 0
        
        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if file_time < cutoff_date:
                    try:
                        os.remove(filepath)
                        cleaned_files += 1
                        self.info(f"Log file cleaned: {filename}")
                    except Exception as e:
                        self.error(f"Error cleaning log file {filename}: {e}")
        
        return cleaned_files

# Instancia global del logger
rpa_logger = RPALogger() 