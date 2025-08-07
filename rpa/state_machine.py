from enum import Enum
from typing import Dict, Optional, Callable, Any
import time
from dataclasses import dataclass
from .simple_logger import rpa_logger


class RPAState(Enum):
    """Estados de la máquina de estados del RPA"""
    IDLE = "idle"
    CONNECTING_REMOTE_DESKTOP = "connecting_remote_desktop"
    OPENING_SAP = "opening_sap"
    NAVIGATING_TO_SALES_ORDER = "navigating_to_sales_order"
    LOADING_NIT = "loading_nit"
    LOADING_ORDER = "loading_order"
    LOADING_DATE = "loading_date"
    LOADING_ITEMS = "loading_items"
    TAKING_SCREENSHOT = "taking_screenshot"
    MOVING_JSON = "moving_json"
    COMPLETED = "completed"
    ERROR = "error"
    RETRYING = "retrying"


class RPAEvent(Enum):
    """Eventos que pueden disparar transiciones"""
    START_PROCESSING = "start_processing"
    REMOTE_DESKTOP_CONNECTED = "remote_desktop_connected"
    REMOTE_DESKTOP_FAILED = "remote_desktop_failed"
    SAP_OPENED = "sap_opened"
    SAP_FAILED = "sap_failed"
    SALES_ORDER_OPENED = "sales_order_opened"
    SALES_ORDER_FAILED = "sales_order_failed"
    NIT_LOADED = "nit_loaded"
    NIT_FAILED = "nit_failed"
    ORDER_LOADED = "order_loaded"
    ORDER_FAILED = "order_failed"
    DATE_LOADED = "date_loaded"
    DATE_FAILED = "date_failed"
    ITEMS_LOADED = "items_loaded"
    ITEMS_FAILED = "items_failed"
    SCREENSHOT_TAKEN = "screenshot_taken"
    SCREENSHOT_FAILED = "screenshot_failed"
    JSON_MOVED = "json_moved"
    JSON_FAILED = "json_failed"
    PROCESS_COMPLETED = "process_completed"
    ERROR_OCCURRED = "error_occurred"
    RETRY = "retry"
    MAX_RETRIES_REACHED = "max_retries_reached"
    RESET = "reset"


@dataclass
class StateContext:
    """Contexto que mantiene el estado actual del procesamiento"""
    current_file: Optional[str] = None
    current_data: Optional[Dict] = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    start_time: Optional[float] = None
    last_successful_state: Optional[RPAState] = None
    processing_stats: Dict[str, Any] = None

    def __post_init__(self):
        if self.processing_stats is None:
            self.processing_stats = {}


class StateMachine:
    """Máquina de estados para el proceso RPA"""
    
    def __init__(self):
        self.current_state = RPAState.IDLE
        self.context = StateContext()
        self.state_handlers: Dict[RPAState, Callable] = {}
        self.transitions: Dict[RPAState, Dict[RPAEvent, RPAState]] = {}
        self.state_entry_callbacks: Dict[RPAState, Callable] = {}
        self.state_exit_callbacks: Dict[RPAState, Callable] = {}
        self._setup_transitions()
        
    def _setup_transitions(self):
        """Define las transiciones válidas entre estados"""
        self.transitions = {
            RPAState.IDLE: {
                RPAEvent.START_PROCESSING: RPAState.CONNECTING_REMOTE_DESKTOP,
            },
            
            RPAState.CONNECTING_REMOTE_DESKTOP: {
                RPAEvent.REMOTE_DESKTOP_CONNECTED: RPAState.OPENING_SAP,
                RPAEvent.REMOTE_DESKTOP_FAILED: RPAState.ERROR,
            },
            
            RPAState.OPENING_SAP: {
                RPAEvent.SAP_OPENED: RPAState.NAVIGATING_TO_SALES_ORDER,
                RPAEvent.SAP_FAILED: RPAState.ERROR,
            },
            
            RPAState.NAVIGATING_TO_SALES_ORDER: {
                RPAEvent.SALES_ORDER_OPENED: RPAState.LOADING_NIT,
                RPAEvent.SALES_ORDER_FAILED: RPAState.ERROR,
            },
            
            RPAState.LOADING_NIT: {
                RPAEvent.NIT_LOADED: RPAState.LOADING_ORDER,
                RPAEvent.NIT_FAILED: RPAState.ERROR,
            },
            
            RPAState.LOADING_ORDER: {
                RPAEvent.ORDER_LOADED: RPAState.LOADING_DATE,
                RPAEvent.ORDER_FAILED: RPAState.ERROR,
            },
            
            RPAState.LOADING_DATE: {
                RPAEvent.DATE_LOADED: RPAState.LOADING_ITEMS,
                RPAEvent.DATE_FAILED: RPAState.ERROR,
            },
            
            RPAState.LOADING_ITEMS: {
                RPAEvent.ITEMS_LOADED: RPAState.TAKING_SCREENSHOT,
                RPAEvent.ITEMS_FAILED: RPAState.ERROR,
            },
            
            RPAState.TAKING_SCREENSHOT: {
                RPAEvent.SCREENSHOT_TAKEN: RPAState.MOVING_JSON,
                RPAEvent.SCREENSHOT_FAILED: RPAState.ERROR,
            },
            
            RPAState.MOVING_JSON: {
                RPAEvent.JSON_MOVED: RPAState.COMPLETED,
                RPAEvent.JSON_FAILED: RPAState.ERROR,
            },
            
            RPAState.ERROR: {
                RPAEvent.RETRY: RPAState.RETRYING,
                RPAEvent.MAX_RETRIES_REACHED: RPAState.IDLE,
                RPAEvent.RESET: RPAState.IDLE,
            },
            
            RPAState.RETRYING: {
                RPAEvent.START_PROCESSING: RPAState.CONNECTING_REMOTE_DESKTOP,
            },
            
            RPAState.COMPLETED: {
                RPAEvent.START_PROCESSING: RPAState.CONNECTING_REMOTE_DESKTOP,
                RPAEvent.RESET: RPAState.IDLE,
            },
        }

    def register_state_handler(self, state: RPAState, handler: Callable):
        """Registra un manejador para un estado específico"""
        self.state_handlers[state] = handler
        
    def register_entry_callback(self, state: RPAState, callback: Callable):
        """Registra un callback que se ejecuta al entrar a un estado"""
        self.state_entry_callbacks[state] = callback
        
    def register_exit_callback(self, state: RPAState, callback: Callable):
        """Registra un callback que se ejecuta al salir de un estado"""
        self.state_exit_callbacks[state] = callback

    def trigger_event(self, event: RPAEvent, **kwargs) -> bool:
        """Dispara un evento y ejecuta la transición correspondiente"""
        try:
            # Verificar si la transición es válida
            if self.current_state not in self.transitions:
                rpa_logger.log_error(
                    f"No hay transiciones definidas para el estado: {self.current_state.value}",
                    f"Evento: {event.value}"
                )
                return False
                
            if event not in self.transitions[self.current_state]:
                rpa_logger.log_error(
                    f"Transición inválida: {event.value} desde estado {self.current_state.value}",
                    "Transición no permitida"
                )
                return False

            # Obtener el nuevo estado
            new_state = self.transitions[self.current_state][event]
            old_state = self.current_state

            # Ejecutar callback de salida del estado anterior
            if old_state in self.state_exit_callbacks:
                try:
                    self.state_exit_callbacks[old_state](self.context, **kwargs)
                except Exception as e:
                    rpa_logger.log_error(f"Error en callback de salida del estado {old_state.value}: {str(e)}")

            # Cambiar el estado
            self.current_state = new_state
            
            # Log de transición
            rpa_logger.log_action(
                f"Transición de estado ejecutada",
                f"De: {old_state.value} → A: {new_state.value} (Evento: {event.value})"
            )

            # Ejecutar callback de entrada del nuevo estado
            if new_state in self.state_entry_callbacks:
                try:
                    self.state_entry_callbacks[new_state](self.context, **kwargs)
                except Exception as e:
                    rpa_logger.log_error(f"Error en callback de entrada del estado {new_state.value}: {str(e)}")

            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error ejecutando transición: {str(e)}", f"Evento: {event.value}")
            return False

    def execute_current_state(self, **kwargs) -> Optional[RPAEvent]:
        """Ejecuta la lógica del estado actual y retorna el próximo evento"""
        if self.current_state in self.state_handlers:
            try:
                return self.state_handlers[self.current_state](self.context, **kwargs)
            except Exception as e:
                rpa_logger.log_error(
                    f"Error ejecutando estado {self.current_state.value}: {str(e)}",
                    "Error en ejecución de estado"
                )
                self.context.error_message = str(e)
                return RPAEvent.ERROR_OCCURRED
        else:
            rpa_logger.log_error(
                f"No hay manejador registrado para el estado: {self.current_state.value}",
                "Manejador faltante"
            )
            return RPAEvent.ERROR_OCCURRED

    def get_current_state(self) -> RPAState:
        """Retorna el estado actual"""
        return self.current_state

    def get_context(self) -> StateContext:
        """Retorna el contexto actual"""
        return self.context

    def reset(self):
        """Reinicia la máquina de estados"""
        self.current_state = RPAState.IDLE
        self.context = StateContext()
        rpa_logger.log_action("Máquina de estados reiniciada", "Estado: IDLE")

    def can_transition_to(self, event: RPAEvent) -> bool:
        """Verifica si se puede ejecutar una transición desde el estado actual"""
        return (self.current_state in self.transitions and 
                event in self.transitions[self.current_state])

    def get_available_events(self) -> list[RPAEvent]:
        """Retorna los eventos disponibles desde el estado actual"""
        if self.current_state in self.transitions:
            return list(self.transitions[self.current_state].keys())
        return []

    def get_state_info(self) -> Dict[str, Any]:
        """Retorna información completa del estado actual"""
        return {
            'current_state': self.current_state.value,
            'available_events': [event.value for event in self.get_available_events()],
            'context': {
                'current_file': self.context.current_file,
                'retry_count': self.context.retry_count,
                'max_retries': self.context.max_retries,
                'error_message': self.context.error_message,
                'last_successful_state': self.context.last_successful_state.value if self.context.last_successful_state else None,
            }
        }

    def handle_error(self, error_message: str):
        """Maneja errores y decide si reintentar o fallar"""
        self.context.error_message = error_message
        self.context.retry_count += 1
        
        rpa_logger.log_error(
            f"Error en estado {self.current_state.value}: {error_message}",
            f"Intento {self.context.retry_count}/{self.context.max_retries}"
        )
        
        if self.context.retry_count < self.context.max_retries:
            return self.trigger_event(RPAEvent.RETRY)
        else:
            rpa_logger.log_error(
                f"Máximo número de reintentos alcanzado para {self.context.current_file}",
                f"Reintentos: {self.context.retry_count}"
            )
            return self.trigger_event(RPAEvent.MAX_RETRIES_REACHED)

    def start_processing(self, file_name: str, data: Dict):
        """Inicia el procesamiento de un archivo"""
        self.context.current_file = file_name
        self.context.current_data = data
        self.context.retry_count = 0
        self.context.error_message = None
        self.context.start_time = time.time()
        self.context.processing_stats = {}
        
        rpa_logger.log_action(
            f"Iniciando procesamiento con máquina de estados",
            f"Archivo: {file_name}"
        )
        
        return self.trigger_event(RPAEvent.START_PROCESSING)

    def complete_processing(self):
        """Marca el procesamiento como completado"""
        if self.context.start_time:
            total_time = time.time() - self.context.start_time
            rpa_logger.log_performance(
                f"Procesamiento completado para {self.context.current_file}",
                total_time
            )
        
        return self.trigger_event(RPAEvent.PROCESS_COMPLETED)