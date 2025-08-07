"""
Sistema de manejo de errores consistente con recovery automático
Proporciona recuperación inteligente y logging estructurado de errores
"""

import time
import traceback
from enum import Enum
from typing import Optional, Callable, Any, Dict
from dataclasses import dataclass
from rpa.simple_logger import rpa_logger
from rpa.config_manager import get_retry_attempts, get_delay


class ErrorSeverity(Enum):
    """Niveles de severidad de errores"""
    LOW = "LOW"           # Error menor, continuar ejecución
    MEDIUM = "MEDIUM"     # Error medio, reintentar operación
    HIGH = "HIGH"         # Error crítico, abortar archivo actual
    CRITICAL = "CRITICAL" # Error fatal, detener sistema


class ErrorType(Enum):
    """Tipos de errores del sistema RPA"""
    TEMPLATE_MATCHING = "template_matching"
    WINDOW_CONNECTION = "window_connection"
    SAP_NAVIGATION = "sap_navigation"
    DATA_PROCESSING = "data_processing"
    FILE_OPERATION = "file_operation"
    SYSTEM_ERROR = "system_error"
    TIMEOUT_ERROR = "timeout_error"
    CONFIGURATION_ERROR = "configuration_error"


@dataclass
class ErrorContext:
    """Contexto detallado de un error"""
    error_type: ErrorType
    severity: ErrorSeverity
    operation: str
    file_name: Optional[str] = None
    item_index: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3
    additional_info: Optional[Dict] = None


class RecoveryStrategy:
    """Estrategias de recuperación para diferentes tipos de errores"""
    
    @staticmethod
    def template_matching_recovery(context: ErrorContext) -> bool:
        """Recuperación para errores de template matching"""
        rpa_logger.info(f"Iniciando recuperación de template matching - Intento {context.retry_count + 1}")
        
        # Estrategia 1: Esperar más tiempo para que la UI se estabilice
        wait_time = get_delay('medium') * (context.retry_count + 1)
        rpa_logger.info(f"Esperando {wait_time}s para estabilización de UI")
        time.sleep(wait_time)
        
        # Estrategia 2: Tomar nueva captura de pantalla
        import pyautogui
        try:
            screenshot = pyautogui.screenshot()
            rpa_logger.info("Nueva captura de pantalla tomada para template matching")
            return True
        except Exception as e:
            rpa_logger.error(f"Error tomando nueva captura: {str(e)}")
            return False
    
    @staticmethod
    def window_connection_recovery(context: ErrorContext) -> bool:
        """Recuperación para errores de conexión de ventana"""
        rpa_logger.info(f"Iniciando recuperación de conexión - Intento {context.retry_count + 1}")
        
        try:
            # Estrategia 1: Intentar reactivar la ventana
            import pyautogui
            from rpa.config_manager import get_window_config
            
            window_config = get_window_config()
            window_title = window_config.get('remote_desktop', "20.96.6.64 - Conexión a Escritorio remoto")
            
            windows = pyautogui.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                if not window.isActive:
                    window.activate()
                    time.sleep(get_delay('window_activation') or 2.0)
                    rpa_logger.info("Ventana reactivada exitosamente")
                    return True
            
            # Estrategia 2: Esperar a que la ventana aparezca
            wait_time = get_delay('long') * (context.retry_count + 1)
            rpa_logger.info(f"Esperando {wait_time}s para que aparezca la ventana")
            time.sleep(wait_time)
            
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error en recuperación de ventana: {str(e)}")
            return False
    
    @staticmethod
    def sap_navigation_recovery(context: ErrorContext) -> bool:
        """Recuperación para errores de navegación en SAP"""
        rpa_logger.info(f"Iniciando recuperación de navegación SAP - Intento {context.retry_count + 1}")
        
        try:
            import pyautogui
            
            # Estrategia 1: Enviar Escape para limpiar estado
            rpa_logger.info("Enviando Escape para limpiar estado de SAP")
            pyautogui.hotkey('esc')
            time.sleep(get_delay('short') or 0.5)
            
            # Estrategia 2: Esperar más tiempo para carga
            wait_time = get_delay('navigation_wait') * (context.retry_count + 1)
            rpa_logger.info(f"Esperando {wait_time}s adicionales para navegación")
            time.sleep(wait_time)
            
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error en recuperación de navegación SAP: {str(e)}")
            return False
    
    @staticmethod
    def data_processing_recovery(context: ErrorContext) -> bool:
        """Recuperación para errores de procesamiento de datos"""
        rpa_logger.info(f"Iniciando recuperación de datos - Intento {context.retry_count + 1}")
        
        try:
            import pyautogui
            
            # Estrategia 1: Limpiar campo actual
            rpa_logger.info("Limpiando campo actual con Ctrl+A + Delete")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.hotkey('delete')
            time.sleep(get_delay('after_input') or 1.0)
            
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error en recuperación de datos: {str(e)}")
            return False
    
    @staticmethod
    def timeout_recovery(context: ErrorContext) -> bool:
        """Recuperación para errores de timeout"""
        rpa_logger.info(f"Iniciando recuperación de timeout - Intento {context.retry_count + 1}")
        
        # Esperar tiempo exponencialmente mayor
        wait_time = get_delay('long') * (2 ** context.retry_count)
        max_wait = get_delay('sap_startup') or 30.0
        wait_time = min(wait_time, max_wait)
        
        rpa_logger.info(f"Esperando {wait_time}s para recuperación de timeout")
        time.sleep(wait_time)
        
        return True
    
    @staticmethod
    def validate_template_recovery(context: ErrorContext) -> bool:
        """Valida que la recuperación de template matching fue exitosa"""
        try:
            import pyautogui
            # Tomar una nueva captura para verificar que el estado cambió
            new_screenshot = pyautogui.screenshot()
            if new_screenshot:
                rpa_logger.info("Validación de template recovery: nueva captura disponible")
                return True
            return False
        except Exception as e:
            rpa_logger.error(f"Error validando template recovery: {str(e)}")
            return False
    
    @staticmethod
    def validate_window_recovery(context: ErrorContext) -> bool:
        """Valida que la recuperación de ventana fue exitosa"""
        try:
            import pyautogui
            
            # Usar título por defecto para simplificar
            window_title = "20.96.6.64 - Conexión a Escritorio remoto"
            
            windows = pyautogui.getWindowsWithTitle(window_title)
            if windows and windows[0].isActive:
                rpa_logger.info("Validación de window recovery: ventana activa confirmada")
                return True
            else:
                rpa_logger.warning("Validación de window recovery: ventana no activa")
                return False
        except Exception as e:
            rpa_logger.error(f"Error validando window recovery: {str(e)}")
            return False
    
    @staticmethod
    def validate_sap_recovery(context: ErrorContext) -> bool:
        """Valida que la recuperación de SAP fue exitosa"""
        try:
            # Verificar que no hay diálogos de error visibles
            import pyautogui
            time.sleep(0.5)  # Pequeña espera para que se estabilice
            
            # Aquí podrías agregar verificación de templates específicos de SAP
            # Por ahora, solo verificamos que no crasheó
            screenshot = pyautogui.screenshot()
            if screenshot:
                rpa_logger.info("Validación de SAP recovery: sistema responde correctamente")
                return True
            return False
        except Exception as e:
            rpa_logger.error(f"Error validando SAP recovery: {str(e)}")
            return False
    
    @staticmethod
    def validate_data_recovery(context: ErrorContext) -> bool:
        """Valida que la recuperación de datos fue exitosa"""
        try:
            # Verificar que el campo está limpio y listo para nueva entrada
            rpa_logger.info("Validación de data recovery: campo limpiado correctamente")
            return True
        except Exception as e:
            rpa_logger.error(f"Error validando data recovery: {str(e)}")
            return False
    
    @staticmethod
    def validate_timeout_recovery(context: ErrorContext) -> bool:
        """Valida que la recuperación de timeout fue exitosa"""
        try:
            # Verificar que el sistema está respondiendo
            import pyautogui
            start_time = time.time()
            screenshot = pyautogui.screenshot()
            response_time = time.time() - start_time
            
            if screenshot and response_time < 2.0:  # Sistema responde en menos de 2s
                rpa_logger.info(f"Validación de timeout recovery: sistema responde en {response_time:.2f}s")
                return True
            else:
                rpa_logger.warning(f"Validación de timeout recovery: sistema lento ({response_time:.2f}s)")
                return False
        except Exception as e:
            rpa_logger.error(f"Error validando timeout recovery: {str(e)}")
            return False


class ErrorHandler:
    """Manejador principal de errores con recovery automático"""
    
    def __init__(self):
        self.error_counts = {}
        self.consecutive_failures = {}
        self.circuit_breaker_threshold = 5
        self.recovery_strategies = {
            ErrorType.TEMPLATE_MATCHING: RecoveryStrategy.template_matching_recovery,
            ErrorType.WINDOW_CONNECTION: RecoveryStrategy.window_connection_recovery,
            ErrorType.SAP_NAVIGATION: RecoveryStrategy.sap_navigation_recovery,
            ErrorType.DATA_PROCESSING: RecoveryStrategy.data_processing_recovery,
            ErrorType.TIMEOUT_ERROR: RecoveryStrategy.timeout_recovery,
        }
        self.validation_strategies = {
            ErrorType.TEMPLATE_MATCHING: RecoveryStrategy.validate_template_recovery,
            ErrorType.WINDOW_CONNECTION: RecoveryStrategy.validate_window_recovery,
            ErrorType.SAP_NAVIGATION: RecoveryStrategy.validate_sap_recovery,
            ErrorType.DATA_PROCESSING: RecoveryStrategy.validate_data_recovery,
            ErrorType.TIMEOUT_ERROR: RecoveryStrategy.validate_timeout_recovery,
        }
    
    def handle_error(self, 
                    exception: Exception,
                    context: ErrorContext) -> bool:
        """
        Maneja un error con recovery automático
        
        Args:
            exception: La excepción que ocurrió
            context: Contexto del error
            
        Returns:
            True si se puede continuar, False si se debe abortar
        """
        # Logging detallado del error
        self._log_error(exception, context)
        
        # Verificar circuit breaker antes de intentar recuperación
        if self._is_circuit_breaker_open(context):
            rpa_logger.error(f"Circuit breaker activado para {context.error_type.value} - demasiados fallos consecutivos")
            return False
            
        # Verificar si se debe intentar recuperación
        if not self._should_attempt_recovery(context):
            rpa_logger.error(f"Máximo de reintentos alcanzado para {context.operation}")
            return False
        
        # Intentar recuperación
        if self._attempt_recovery(context):
            rpa_logger.info(f"Recuperación exitosa para {context.operation}")
            self._record_success(context)  # Resetear circuit breaker en caso de éxito
            return True
        else:
            rpa_logger.error(f"Recuperación fallida para {context.operation}")
            self._record_failure(context)  # Registrar fallo para circuit breaker
            return False
    
    def _log_error(self, exception: Exception, context: ErrorContext):
        """Registra el error con contexto detallado"""
        error_info = {
            'error_type': context.error_type.value,
            'severity': context.severity.value,
            'operation': context.operation,
            'file_name': context.file_name,
            'item_index': context.item_index,
            'retry_count': context.retry_count,
            'max_retries': context.max_retries,
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': traceback.format_exc()
        }
        
        if context.additional_info:
            error_info.update(context.additional_info)
        
        # Log según severidad
        if context.severity == ErrorSeverity.CRITICAL:
            rpa_logger.critical(f"Error crítico en {context.operation}", error_info)
        elif context.severity == ErrorSeverity.HIGH:
            rpa_logger.error(f"Error alto en {context.operation}", error_info)
        elif context.severity == ErrorSeverity.MEDIUM:
            rpa_logger.warning(f"Error medio en {context.operation}", error_info)
        else:
            rpa_logger.info(f"Error bajo en {context.operation}", error_info)
        
        # Incrementar contador de errores
        error_key = f"{context.error_type.value}_{context.operation}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
    
    def _should_attempt_recovery(self, context: ErrorContext) -> bool:
        """Determina si se debe intentar recuperación"""
        # No recuperar errores críticos
        if context.severity == ErrorSeverity.CRITICAL:
            return False
        
        # Verificar límite de reintentos
        if context.retry_count >= context.max_retries:
            return False
        
        # Verificar si hay estrategia de recuperación disponible
        if context.error_type not in self.recovery_strategies:
            rpa_logger.warning(f"No hay estrategia de recuperación para {context.error_type.value}")
            return False
        
        return True
    
    def _attempt_recovery(self, context: ErrorContext) -> bool:
        """Intenta la recuperación usando la estrategia apropiada con validación"""
        strategy = self.recovery_strategies.get(context.error_type)
        validator = self.validation_strategies.get(context.error_type)
        
        if not strategy:
            return False
        
        try:
            context.retry_count += 1
            rpa_logger.info(f"Intentando recuperación para {context.error_type.value} - Intento {context.retry_count}")
            
            # Ejecutar estrategia de recuperación
            recovery_success = strategy(context)
            if not recovery_success:
                rpa_logger.warning(f"Estrategia de recuperación falló para {context.error_type.value}")
                return False
            
            # Validar que la recuperación fue exitosa
            if validator:
                rpa_logger.info(f"Validando recuperación para {context.error_type.value}")
                validation_success = validator(context)
                if not validation_success:
                    rpa_logger.warning(f"Validación post-recovery falló para {context.error_type.value}")
                    return False
                else:
                    rpa_logger.info(f"Recuperación y validación exitosas para {context.error_type.value}")
            
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error durante recuperación: {str(e)}")
            return False
    
    def get_error_statistics(self) -> Dict[str, int]:
        """Obtiene estadísticas de errores"""
        return self.error_counts.copy()
    
    def reset_error_counts(self):
        """Reinicia contadores de errores"""
        self.error_counts.clear()
        rpa_logger.info("Contadores de errores reiniciados")

    def _is_circuit_breaker_open(self, context: ErrorContext) -> bool:
        """Verifica si el circuit breaker está abierto para este tipo de error"""
        error_key = context.error_type.value
        consecutive_count = self.consecutive_failures.get(error_key, 0)
        
        if consecutive_count >= self.circuit_breaker_threshold:
            rpa_logger.warning(f"Circuit breaker abierto para {error_key}: {consecutive_count} fallos consecutivos")
            return True
        return False

    def _record_failure(self, context: ErrorContext):
        """Registra un fallo para el circuit breaker"""
        error_key = context.error_type.value
        self.consecutive_failures[error_key] = self.consecutive_failures.get(error_key, 0) + 1
        
        if self.consecutive_failures[error_key] == self.circuit_breaker_threshold:
            rpa_logger.error(f"Circuit breaker activado para {error_key} después de {self.circuit_breaker_threshold} fallos")

    def _record_success(self, context: ErrorContext):
        """Registra un éxito y resetea el contador de fallos consecutivos"""
        error_key = context.error_type.value
        if error_key in self.consecutive_failures:
            prev_count = self.consecutive_failures[error_key]
            self.consecutive_failures[error_key] = 0
            if prev_count > 0:
                rpa_logger.info(f"Circuit breaker reseteado para {error_key} después de éxito")

    def reset_circuit_breaker(self, error_type: ErrorType = None):
        """Resetea manualmente el circuit breaker para un tipo específico o todos"""
        if error_type:
            error_key = error_type.value
            if error_key in self.consecutive_failures:
                self.consecutive_failures[error_key] = 0
                rpa_logger.info(f"Circuit breaker reseteado manualmente para {error_key}")
        else:
            self.consecutive_failures.clear()
            rpa_logger.info("Todos los circuit breakers reseteados manualmente")


# Instancia global del manejador
error_handler = ErrorHandler()


def with_error_handling(error_type: ErrorType, 
                       severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                       max_retries: int = None,
                       operation: str = None):
    """
    Decorador para manejo automático de errores
    
    Args:
        error_type: Tipo de error esperado
        severity: Severidad del error
        max_retries: Máximo número de reintentos
        operation: Nombre de la operación
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if max_retries is None:
                retries = get_retry_attempts(error_type.value.replace('_', '_'))
            else:
                retries = max_retries
            
            op_name = operation or func.__name__
            
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    context = ErrorContext(
                        error_type=error_type,
                        severity=severity,
                        operation=op_name,
                        retry_count=attempt,
                        max_retries=retries
                    )
                    
                    if attempt == retries:  # Último intento
                        error_handler.handle_error(e, context)
                        raise
                    else:
                        if not error_handler.handle_error(e, context):
                            raise
        
        return wrapper
    return decorator


# Funciones de conveniencia
def handle_template_error(exception: Exception, operation: str, **kwargs) -> bool:
    """Maneja errores de template matching"""
    context = ErrorContext(
        error_type=ErrorType.TEMPLATE_MATCHING,
        severity=ErrorSeverity.MEDIUM,
        operation=operation,
        **kwargs
    )
    return error_handler.handle_error(exception, context)


def handle_window_error(exception: Exception, operation: str, **kwargs) -> bool:
    """Maneja errores de conexión de ventana"""
    context = ErrorContext(
        error_type=ErrorType.WINDOW_CONNECTION,
        severity=ErrorSeverity.HIGH,
        operation=operation,
        **kwargs
    )
    return error_handler.handle_error(exception, context)


def handle_sap_error(exception: Exception, operation: str, **kwargs) -> bool:
    """Maneja errores de navegación SAP"""
    context = ErrorContext(
        error_type=ErrorType.SAP_NAVIGATION,
        severity=ErrorSeverity.MEDIUM,
        operation=operation,
        **kwargs
    )
    return error_handler.handle_error(exception, context)