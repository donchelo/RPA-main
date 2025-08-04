"""
Tests para sistema de manejo de errores - FASE 2
Tests de componentes críticos (Mediano + Alto impacto)
"""

import unittest
import time
from unittest.mock import patch, MagicMock, call
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rpa.error_handler import (
    ErrorHandler, ErrorType, ErrorSeverity, ErrorContext,
    RecoveryStrategy, with_error_handling,
    handle_template_error, handle_window_error, handle_sap_error
)


class TestErrorContext(unittest.TestCase):
    """Tests para ErrorContext dataclass"""
    
    def test_error_context_creation(self):
        """Test: Creación de contexto de error"""
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="find_sap_icon",
            file_name="test.json",
            item_index=1,
            retry_count=0,
            max_retries=3
        )
        
        self.assertEqual(context.error_type, ErrorType.TEMPLATE_MATCHING)
        self.assertEqual(context.severity, ErrorSeverity.MEDIUM)
        self.assertEqual(context.operation, "find_sap_icon")
        self.assertEqual(context.file_name, "test.json")
        self.assertEqual(context.item_index, 1)
        self.assertEqual(context.retry_count, 0)
        self.assertEqual(context.max_retries, 3)
    
    def test_error_context_defaults(self):
        """Test: Valores por defecto de ErrorContext"""
        context = ErrorContext(
            error_type=ErrorType.SYSTEM_ERROR,
            severity=ErrorSeverity.LOW,
            operation="test_operation"
        )
        
        self.assertIsNone(context.file_name)
        self.assertIsNone(context.item_index)
        self.assertEqual(context.retry_count, 0)
        self.assertEqual(context.max_retries, 3)
        self.assertIsNone(context.additional_info)


class TestRecoveryStrategy(unittest.TestCase):
    """Tests para estrategias de recuperación"""
    
    @patch('time.sleep')
    @patch('rpa.error_handler.get_delay')
    def test_timeout_recovery(self, mock_get_delay, mock_sleep):
        """Test: Estrategia de recuperación de timeout"""
        mock_get_delay.side_effect = lambda key: {'long': 2.0, 'sap_startup': 30.0}.get(key, 1.0)
        
        context = ErrorContext(
            error_type=ErrorType.TIMEOUT_ERROR,
            severity=ErrorSeverity.MEDIUM,
            operation="sap_startup",
            retry_count=1
        )
        
        result = RecoveryStrategy.timeout_recovery(context)
        
        self.assertTrue(result)
        mock_sleep.assert_called_once_with(4.0)  # 2.0 * (2^1)
    
    @patch('pyautogui.hotkey')
    @patch('time.sleep')
    @patch('rpa.error_handler.get_delay')
    def test_sap_navigation_recovery(self, mock_get_delay, mock_sleep, mock_hotkey):
        """Test: Estrategia de recuperación de navegación SAP"""
        mock_get_delay.side_effect = lambda key: {'short': 0.5, 'navigation_wait': 2.0}.get(key, 1.0)
        
        context = ErrorContext(
            error_type=ErrorType.SAP_NAVIGATION,
            severity=ErrorSeverity.MEDIUM,
            operation="open_ventas_menu",
            retry_count=0
        )
        
        result = RecoveryStrategy.sap_navigation_recovery(context)
        
        self.assertTrue(result)
        mock_hotkey.assert_called_once_with('esc')
        self.assertEqual(mock_sleep.call_count, 2)  # Una para esc, otra para wait
    
    @patch('pyautogui.hotkey')
    @patch('time.sleep')
    @patch('rpa.error_handler.get_delay')
    def test_data_processing_recovery(self, mock_get_delay, mock_sleep, mock_hotkey):
        """Test: Estrategia de recuperación de procesamiento de datos"""
        mock_get_delay.return_value = 1.0
        
        context = ErrorContext(
            error_type=ErrorType.DATA_PROCESSING,
            severity=ErrorSeverity.MEDIUM,
            operation="load_nit",
            retry_count=0
        )
        
        result = RecoveryStrategy.data_processing_recovery(context)
        
        self.assertTrue(result)
        # Verificar secuencia: Ctrl+A, Delete, Sleep
        expected_calls = [call('ctrl', 'a'), call('delete')]
        mock_hotkey.assert_has_calls(expected_calls)
        mock_sleep.assert_called()
    
    @patch('pyautogui.screenshot')
    @patch('time.sleep')
    @patch('rpa.error_handler.get_delay')
    def test_template_matching_recovery(self, mock_get_delay, mock_sleep, mock_screenshot):
        """Test: Estrategia de recuperación de template matching"""
        mock_get_delay.return_value = 1.0
        mock_screenshot.return_value = MagicMock()
        
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="find_sap_icon",
            retry_count=1
        )
        
        result = RecoveryStrategy.template_matching_recovery(context)
        
        self.assertTrue(result)
        mock_sleep.assert_called_with(2.0)  # base_delay * (retry_count + 1)
        mock_screenshot.assert_called_once()


class TestErrorHandler(unittest.TestCase):
    """Tests para la clase ErrorHandler principal"""
    
    def setUp(self):
        """Setup para cada test"""
        self.error_handler = ErrorHandler()
    
    def test_error_handler_initialization(self):
        """Test: Inicialización correcta del ErrorHandler"""
        self.assertIsInstance(self.error_handler.error_counts, dict)
        self.assertIsInstance(self.error_handler.recovery_strategies, dict)
        
        # Verificar que tiene estrategias para tipos principales
        self.assertIn(ErrorType.TEMPLATE_MATCHING, self.error_handler.recovery_strategies)
        self.assertIn(ErrorType.WINDOW_CONNECTION, self.error_handler.recovery_strategies)
        self.assertIn(ErrorType.SAP_NAVIGATION, self.error_handler.recovery_strategies)
    
    def test_should_attempt_recovery_logic(self):
        """Test: Lógica de si debe intentar recuperación"""
        # No recuperar errores críticos
        critical_context = ErrorContext(
            error_type=ErrorType.SYSTEM_ERROR,
            severity=ErrorSeverity.CRITICAL,
            operation="test_op"
        )
        self.assertFalse(self.error_handler._should_attempt_recovery(critical_context))
        
        # No recuperar si excede reintentos
        max_retries_context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_op",
            retry_count=3,
            max_retries=3
        )
        self.assertFalse(self.error_handler._should_attempt_recovery(max_retries_context))
        
        # Sí recuperar en caso normal
        normal_context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_op",
            retry_count=1,
            max_retries=3
        )
        self.assertTrue(self.error_handler._should_attempt_recovery(normal_context))
    
    @patch('rpa.error_handler.rpa_logger')
    def test_log_error_functionality(self, mock_logger):
        """Test: Funcionalidad de logging de errores"""
        exception = ValueError("Test error")
        context = ErrorContext(
            error_type=ErrorType.DATA_PROCESSING,
            severity=ErrorSeverity.HIGH,
            operation="load_nit",
            file_name="test.json"
        )
        
        self.error_handler._log_error(exception, context)
        
        # Verificar que se llamó al logger con nivel correcto
        mock_logger.error.assert_called_once()
        
        # Verificar conteo de errores
        error_key = "data_processing_load_nit"
        self.assertEqual(self.error_handler.error_counts[error_key], 1)
    
    @patch('rpa.error_handler.rpa_logger')
    def test_handle_error_with_recovery_success(self, mock_logger):
        """Test: Manejo de error con recuperación exitosa"""
        exception = Exception("Template not found")
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="find_sap_icon",
            retry_count=0,
            max_retries=3
        )
        
        # Mock de estrategia de recuperación exitosa
        with patch.object(self.error_handler, '_attempt_recovery', return_value=True):
            result = self.error_handler.handle_error(exception, context)
        
        self.assertTrue(result)
        mock_logger.info.assert_called_with("Recuperación exitosa para find_sap_icon")
    
    @patch('rpa.error_handler.rpa_logger')
    def test_handle_error_with_recovery_failure(self, mock_logger):
        """Test: Manejo de error con recuperación fallida"""
        exception = Exception("Critical system error")
        context = ErrorContext(
            error_type=ErrorType.SYSTEM_ERROR,
            severity=ErrorSeverity.CRITICAL,
            operation="system_startup",
            retry_count=0,
            max_retries=3
        )
        
        result = self.error_handler.handle_error(exception, context)
        
        # Errores críticos no deben intentar recuperación
        self.assertFalse(result)
    
    def test_error_statistics(self):
        """Test: Estadísticas de errores"""
        # Simular algunos errores
        context1 = ErrorContext(ErrorType.TEMPLATE_MATCHING, ErrorSeverity.MEDIUM, "op1")
        context2 = ErrorContext(ErrorType.SAP_NAVIGATION, ErrorSeverity.MEDIUM, "op2")
        
        with patch('rpa.error_handler.rpa_logger'):
            self.error_handler._log_error(Exception("Error 1"), context1)
            self.error_handler._log_error(Exception("Error 2"), context1)  # Mismo tipo
            self.error_handler._log_error(Exception("Error 3"), context2)  # Diferente tipo
        
        stats = self.error_handler.get_error_statistics()
        
        self.assertEqual(stats["template_matching_op1"], 2)
        self.assertEqual(stats["sap_navigation_op2"], 1)
    
    def test_reset_error_counts(self):
        """Test: Reinicio de contadores de errores"""
        # Agregar algunos errores
        self.error_handler.error_counts["test_error"] = 5
        
        with patch('rpa.error_handler.rpa_logger'):
            self.error_handler.reset_error_counts()
        
        self.assertEqual(len(self.error_handler.error_counts), 0)


class TestErrorHandlerDecorator(unittest.TestCase):
    """Tests para el decorador with_error_handling"""
    
    def test_decorator_success_case(self):
        """Test: Decorador en caso de éxito"""
        @with_error_handling(ErrorType.TEMPLATE_MATCHING, ErrorSeverity.MEDIUM)
        def successful_function():
            return "success"
        
        result = successful_function()
        self.assertEqual(result, "success")
    
    @patch('rpa.error_handler.error_handler')
    @patch('rpa.error_handler.get_retry_attempts')
    def test_decorator_with_retries(self, mock_get_retry, mock_error_handler):
        """Test: Decorador con reintentos"""
        mock_get_retry.return_value = 2
        mock_error_handler.handle_error.return_value = True  # Recuperación exitosa
        
        call_count = 0
        
        @with_error_handling(ErrorType.TEMPLATE_MATCHING, ErrorSeverity.MEDIUM)
        def failing_then_succeeding_function():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("First attempt fails")
            return "success on retry"
        
        result = failing_then_succeeding_function()
        self.assertEqual(result, "success on retry")
        self.assertEqual(call_count, 2)
    
    @patch('rpa.error_handler.error_handler')
    @patch('rpa.error_handler.get_retry_attempts')
    def test_decorator_max_retries_exceeded(self, mock_get_retry, mock_error_handler):
        """Test: Decorador cuando se exceden reintentos máximos"""
        mock_get_retry.return_value = 1
        mock_error_handler.handle_error.return_value = False  # Recuperación falla
        
        @with_error_handling(ErrorType.TEMPLATE_MATCHING, ErrorSeverity.MEDIUM)
        def always_failing_function():
            raise Exception("Always fails")
        
        with self.assertRaises(Exception):
            always_failing_function()


class TestConvenienceFunctions(unittest.TestCase):
    """Tests para funciones de conveniencia"""
    
    @patch('rpa.error_handler.error_handler')
    def test_handle_template_error(self, mock_error_handler):
        """Test: Función de conveniencia para errores de template"""
        mock_error_handler.handle_error.return_value = True
        
        exception = Exception("Template not found")
        result = handle_template_error(exception, "find_sap_icon")
        
        self.assertTrue(result)
        mock_error_handler.handle_error.assert_called_once()
        
        # Verificar que se creó el contexto correcto
        call_args = mock_error_handler.handle_error.call_args
        exception_arg, context_arg = call_args[0]
        
        self.assertEqual(context_arg.error_type, ErrorType.TEMPLATE_MATCHING)
        self.assertEqual(context_arg.severity, ErrorSeverity.MEDIUM)
        self.assertEqual(context_arg.operation, "find_sap_icon")
    
    @patch('rpa.error_handler.error_handler')
    def test_handle_window_error(self, mock_error_handler):
        """Test: Función de conveniencia para errores de ventana"""
        mock_error_handler.handle_error.return_value = True
        
        exception = Exception("Window not found")
        result = handle_window_error(exception, "get_remote_desktop")
        
        self.assertTrue(result)
        
        # Verificar contexto
        call_args = mock_error_handler.handle_error.call_args
        context_arg = call_args[0][1]
        
        self.assertEqual(context_arg.error_type, ErrorType.WINDOW_CONNECTION)
        self.assertEqual(context_arg.severity, ErrorSeverity.HIGH)
        self.assertEqual(context_arg.operation, "get_remote_desktop")
    
    @patch('rpa.error_handler.error_handler')
    def test_handle_sap_error(self, mock_error_handler):
        """Test: Función de conveniencia para errores de SAP"""
        mock_error_handler.handle_error.return_value = True
        
        exception = Exception("SAP navigation failed")
        result = handle_sap_error(exception, "open_ventas_menu")
        
        self.assertTrue(result)
        
        # Verificar contexto
        call_args = mock_error_handler.handle_error.call_args
        context_arg = call_args[0][1]
        
        self.assertEqual(context_arg.error_type, ErrorType.SAP_NAVIGATION)
        self.assertEqual(context_arg.severity, ErrorSeverity.MEDIUM)
        self.assertEqual(context_arg.operation, "open_ventas_menu")


if __name__ == '__main__':
    unittest.main()