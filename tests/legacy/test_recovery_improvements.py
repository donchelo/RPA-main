"""
Tests básicos para validar las mejoras de recovery implementadas en Etapa 1
"""
import unittest
import json
import os
import time
from unittest.mock import Mock, patch, MagicMock
from rpa.error_handler import ErrorHandler, ErrorContext, ErrorType, ErrorSeverity, RecoveryStrategy
from rpa.state_machine import StateMachine, RPAState, RPAEvent, StateContext


class TestRecoveryImprovements(unittest.TestCase):
    """Tests para las nuevas funcionalidades de recovery"""
    
    def setUp(self):
        """Setup para cada test"""
        self.error_handler = ErrorHandler()
        self.state_machine = StateMachine()
        
    def tearDown(self):
        """Cleanup después de cada test"""
        # Limpiar archivos de checkpoint de prueba
        test_files = [
            "checkpoint_test_file.json",
            "checkpoint_test_file.json.json"
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_checkpoint_creation(self):
        """Test que verifica la creación de checkpoints"""
        # Setup
        self.state_machine.context.current_file = "test_file.json"
        self.state_machine.current_state = RPAState.LOADING_NIT
        
        # Ejecutar
        result = self.state_machine.save_checkpoint()
        
        # Verificar
        self.assertTrue(result)
        checkpoint_file = f"checkpoint_{os.path.basename('test_file.json')}.json"
        self.assertTrue(os.path.exists(checkpoint_file))
        
        # Verificar contenido del checkpoint
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
        
        self.assertEqual(checkpoint_data['current_file'], "test_file.json")
        self.assertEqual(checkpoint_data['current_state'], "loading_nit")
        self.assertIsInstance(checkpoint_data['timestamp'], float)
        
        # Cleanup
        os.remove(checkpoint_file)
    
    def test_checkpoint_resume(self):
        """Test que verifica la restauración desde checkpoint"""
        # Crear un checkpoint de prueba
        checkpoint_data = {
            'current_file': 'test_file.json',
            'current_state': 'loading_order',
            'retry_count': 1,
            'max_retries': 3,
            'error_message': None,
            'last_successful_state': 'loading_nit',
            'timestamp': time.time(),
            'processing_stats': {'test': 'data'}
        }
        
        checkpoint_file = "checkpoint_test_file.json.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f)
        
        # Ejecutar
        result = self.state_machine.try_resume_from_checkpoint("test_file.json")
        
        # Verificar
        self.assertTrue(result)
        self.assertEqual(self.state_machine.current_state, RPAState.LOADING_ORDER)
        self.assertEqual(self.state_machine.context.retry_count, 1)
        self.assertEqual(self.state_machine.context.current_file, 'test_file.json')
    
    def test_checkpoint_expiration(self):
        """Test que verifica que checkpoints expirados se eliminen"""
        # Crear checkpoint expirado (más de 1 hora)
        old_timestamp = time.time() - 3700  # 1 hora 1 minuto atrás
        checkpoint_data = {
            'current_file': 'test_file.json',
            'current_state': 'loading_nit',
            'retry_count': 0,
            'max_retries': 3,
            'error_message': None,
            'last_successful_state': None,
            'timestamp': old_timestamp,
            'processing_stats': {}
        }
        
        checkpoint_file = "checkpoint_test_file.json.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f)
        
        # Ejecutar
        result = self.state_machine.try_resume_from_checkpoint("test_file.json")
        
        # Verificar
        self.assertFalse(result)
        self.assertFalse(os.path.exists(checkpoint_file))  # Debe haberse eliminado
    
    def test_circuit_breaker_activation(self):
        """Test que verifica la activación del circuit breaker"""
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_operation"
        )
        
        # Simular 5 fallos consecutivos
        for i in range(5):
            self.error_handler._record_failure(context)
        
        # Verificar que circuit breaker está activo
        is_open = self.error_handler._is_circuit_breaker_open(context)
        self.assertTrue(is_open)
        
        # Verificar que el contador es correcto
        consecutive_count = self.error_handler.consecutive_failures.get(ErrorType.TEMPLATE_MATCHING.value, 0)
        self.assertEqual(consecutive_count, 5)
    
    def test_circuit_breaker_reset_on_success(self):
        """Test que verifica el reset del circuit breaker en caso de éxito"""
        context = ErrorContext(
            error_type=ErrorType.WINDOW_CONNECTION,
            severity=ErrorSeverity.HIGH,
            operation="test_operation"
        )
        
        # Simular fallos y luego un éxito
        for i in range(3):
            self.error_handler._record_failure(context)
        
        # Verificar que hay fallos registrados
        consecutive_count = self.error_handler.consecutive_failures.get(ErrorType.WINDOW_CONNECTION.value, 0)
        self.assertEqual(consecutive_count, 3)
        
        # Registrar éxito
        self.error_handler._record_success(context)
        
        # Verificar que se reseteó
        consecutive_count = self.error_handler.consecutive_failures.get(ErrorType.WINDOW_CONNECTION.value, 0)
        self.assertEqual(consecutive_count, 0)
    
    @patch('pyautogui.screenshot')
    def test_template_recovery_validation(self, mock_screenshot):
        """Test que verifica la validación de template recovery"""
        # Setup mock
        mock_screenshot.return_value = MagicMock()  # Simular captura exitosa
        
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_template_validation"
        )
        
        # Ejecutar validación
        result = RecoveryStrategy.validate_template_recovery(context)
        
        # Verificar
        self.assertTrue(result)
        mock_screenshot.assert_called_once()
    
    @patch('pyautogui.getWindowsWithTitle')
    def test_window_recovery_validation(self, mock_get_windows):
        """Test que verifica la validación de window recovery"""
        # Setup mock - simular ventana activa
        mock_window = MagicMock()
        mock_window.isActive = True
        mock_get_windows.return_value = [mock_window]
        
        context = ErrorContext(
            error_type=ErrorType.WINDOW_CONNECTION,
            severity=ErrorSeverity.HIGH,
            operation="test_window_validation"
        )
        
        # Ejecutar validación
        result = RecoveryStrategy.validate_window_recovery(context)
        
        # Verificar
        self.assertTrue(result)
        mock_get_windows.assert_called()
    
    @patch('pyautogui.screenshot')
    def test_timeout_recovery_validation(self, mock_screenshot):
        """Test que verifica la validación de timeout recovery"""
        # Setup mock - simular respuesta rápida
        mock_screenshot.return_value = MagicMock()
        
        context = ErrorContext(
            error_type=ErrorType.TIMEOUT_ERROR,
            severity=ErrorSeverity.MEDIUM,
            operation="test_timeout_validation"
        )
        
        # Ejecutar validación
        result = RecoveryStrategy.validate_timeout_recovery(context)
        
        # Verificar
        self.assertTrue(result)
        mock_screenshot.assert_called_once()
    
    def test_manual_circuit_breaker_reset(self):
        """Test que verifica el reset manual del circuit breaker"""
        context = ErrorContext(
            error_type=ErrorType.SAP_NAVIGATION,
            severity=ErrorSeverity.MEDIUM,
            operation="test_operation"
        )
        
        # Simular fallos hasta activar circuit breaker
        for i in range(6):
            self.error_handler._record_failure(context)
        
        # Verificar que está activo
        self.assertTrue(self.error_handler._is_circuit_breaker_open(context))
        
        # Reset manual
        self.error_handler.reset_circuit_breaker(ErrorType.SAP_NAVIGATION)
        
        # Verificar que se reseteó
        self.assertFalse(self.error_handler._is_circuit_breaker_open(context))
    
    def test_integration_recovery_with_validation(self):
        """Test de integración que verifica recovery + validación"""
        # Este test simula un flujo completo de error, recovery y validación
        
        context = ErrorContext(
            error_type=ErrorType.DATA_PROCESSING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_integration",
            retry_count=0,
            max_retries=3
        )
        
        # Simular excepción
        test_exception = Exception("Test error for integration")
        
        # Mock de las estrategias para controlar el resultado
        with patch.dict(self.error_handler.recovery_strategies, {ErrorType.DATA_PROCESSING: Mock(return_value=True)}) as mock_strategies, \
             patch.dict(self.error_handler.validation_strategies, {ErrorType.DATA_PROCESSING: Mock(return_value=True)}) as mock_validations:
            
            # Ejecutar handle_error
            result = self.error_handler.handle_error(test_exception, context)
            
            # Verificar que todo funcionó
            self.assertTrue(result)
            # Verificar que las estrategias fueron llamadas
            mock_strategies[ErrorType.DATA_PROCESSING].assert_called_once_with(context)
            mock_validations[ErrorType.DATA_PROCESSING].assert_called_once_with(context)


def run_recovery_tests():
    """Función para ejecutar todos los tests"""
    print("=== EJECUTANDO TESTS DE RECOVERY IMPROVEMENTS ===")
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRecoveryImprovements)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print(f"\n=== RESUMEN DE TESTS ===")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Éxitos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.failures:
        print("\nFALLOS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nERRORES:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_recovery_tests()
    exit(0 if success else 1)