"""
Framework de testing simple pero efectivo para el Sistema RPA
Incluye mocks, assertions y utilidades de testing
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Any, Dict, List, Optional, Callable
import tempfile
import json
import yaml
from contextlib import contextmanager

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class RPATestCase(unittest.TestCase):
    """Clase base para tests del sistema RPA con utilidades comunes"""
    
    def setUp(self):
        """Setup común para todos los tests"""
        self.test_temp_dir = tempfile.mkdtemp()
        self.mock_pyautogui = self._setup_pyautogui_mocks()
        self.mock_cv2 = self._setup_cv2_mocks()
        
    def tearDown(self):
        """Cleanup después de cada test"""
        import shutil
        if os.path.exists(self.test_temp_dir):
            shutil.rmtree(self.test_temp_dir)
    
    def _setup_pyautogui_mocks(self):
        """Configura mocks para pyautogui"""
        mock_pyautogui = Mock()
        mock_pyautogui.screenshot.return_value = Mock()
        mock_pyautogui.position.return_value = (100, 100)
        mock_pyautogui.click = Mock()
        mock_pyautogui.doubleClick = Mock()
        mock_pyautogui.typewrite = Mock()
        mock_pyautogui.hotkey = Mock()
        mock_pyautogui.moveTo = Mock()
        mock_pyautogui.drag = Mock()
        mock_pyautogui.size.return_value = (1920, 1080)
        
        # Mock para getWindowsWithTitle
        mock_window = Mock()
        mock_window.isActive = True
        mock_window.activate = Mock()
        mock_pyautogui.getWindowsWithTitle.return_value = [mock_window]
        
        return mock_pyautogui
    
    def _setup_cv2_mocks(self):
        """Configura mocks para OpenCV"""
        mock_cv2 = Mock()
        mock_cv2.imread.return_value = Mock()
        mock_cv2.matchTemplate.return_value = Mock()
        mock_cv2.minMaxLoc.return_value = (0.1, 0.9, (10, 10), (100, 100))
        mock_cv2.cvtColor.return_value = Mock()
        mock_cv2.TM_CCOEFF_NORMED = 0
        mock_cv2.IMREAD_COLOR = 1
        mock_cv2.IMREAD_UNCHANGED = -1
        mock_cv2.COLOR_RGB2BGR = 4
        return mock_cv2
    
    def create_test_json_file(self, filename: str, data: Dict) -> str:
        """Crea un archivo JSON de test"""
        filepath = os.path.join(self.test_temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath
    
    def create_test_config_file(self, config_data: Dict) -> str:
        """Crea un archivo de configuración YAML de test"""
        filepath = os.path.join(self.test_temp_dir, 'test_config.yaml')
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False)
        return filepath
    
    def assert_called_with_timeout(self, mock_obj, timeout: float = 1.0):
        """Verifica que un mock fue llamado dentro del timeout especificado"""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if mock_obj.called:
                return True
            time.sleep(0.01)
        self.fail(f"Mock {mock_obj} no fue llamado dentro del timeout de {timeout}s")
    
    def assert_log_contains(self, log_mock, message: str):
        """Verifica que el log contiene un mensaje específico"""
        calls = [str(call) for call in log_mock.call_args_list]
        matching_calls = [call for call in calls if message in call]
        self.assertTrue(
            len(matching_calls) > 0,
            f"Log no contiene '{message}'. Llamadas: {calls}"
        )
    
    @contextmanager
    def mock_file_system(self, files: Dict[str, Any]):
        """Context manager para mockear sistema de archivos"""
        original_exists = os.path.exists
        original_listdir = os.listdir
        original_isfile = os.path.isfile
        
        def mock_exists(path):
            return path in files
        
        def mock_listdir(path):
            if path in files and isinstance(files[path], list):
                return files[path]
            return []
        
        def mock_isfile(path):
            return path in files and not isinstance(files[path], list)
        
        with patch('os.path.exists', side_effect=mock_exists), \
             patch('os.listdir', side_effect=mock_listdir), \
             patch('os.path.isfile', side_effect=mock_isfile):
            yield


class ConfigTests(RPATestCase):
    """Tests para el sistema de configuración"""
    
    @patch('rpa.config_manager.yaml.safe_load')
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_config_manager_loads_correctly(self, mock_exists, mock_open, mock_yaml):
        """Test que ConfigManager carga configuración correctamente"""
        mock_exists.return_value = True
        mock_yaml.return_value = {
            'delays': {'short': 0.5, 'medium': 1.0},
            'template_matching': {'default_confidence': 0.8}
        }
        
        from rpa.config_manager import ConfigManager
        config = ConfigManager('test_config.yaml')
        
        self.assertEqual(config.get('delays.short'), 0.5)
        self.assertEqual(config.get('template_matching.default_confidence'), 0.8)
    
    def test_config_validation(self):
        """Test validación de configuración"""
        from rpa.config_manager import ConfigManager
        
        # Crear configuración válida
        valid_config = {
            'delays': {'medium': 1.0, 'sap_startup': 30.0},
            'template_matching': {'default_confidence': 0.8},
            'retries': {'max_sap_open_attempts': 3}
        }
        
        config_file = self.create_test_config_file(valid_config)
        config = ConfigManager(config_file)
        
        self.assertTrue(config.validate_config())
    
    def test_config_default_values(self):
        """Test valores por defecto cuando no existe archivo"""
        from rpa.config_manager import ConfigManager
        
        config = ConfigManager('nonexistent_file.yaml')
        
        # Debe usar valores por defecto
        self.assertIsNotNone(config.get('delays.short'))
        self.assertIsNotNone(config.get('template_matching.default_confidence'))


class TemplateMatcherTests(RPATestCase):
    """Tests para el sistema de template matching"""
    
    @patch('rpa.vision.template_matcher.cv2')
    @patch('rpa.vision.template_matcher.pyautogui')
    def test_find_template_success(self, mock_pyautogui, mock_cv2):
        """Test búsqueda exitosa de template"""
        # Configurar mocks
        mock_cv2.matchTemplate.return_value = Mock()
        mock_cv2.minMaxLoc.return_value = (0.1, 0.9, (10, 10), (100, 100))
        mock_pyautogui.screenshot.return_value = Mock()
        
        # Crear imagen mock
        mock_template = Mock()
        mock_template.shape = (50, 50, 3)
        
        from rpa.vision.template_matcher import TemplateMatcher
        matcher = TemplateMatcher()
        
        result = matcher.find_template(mock_template, confidence=0.8)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
    
    @patch('rpa.vision.template_matcher.cv2')
    @patch('rpa.vision.template_matcher.pyautogui')
    def test_find_template_low_confidence(self, mock_pyautogui, mock_cv2):
        """Test cuando la confianza es muy baja"""
        # Configurar mock con baja confianza
        mock_cv2.matchTemplate.return_value = Mock()
        mock_cv2.minMaxLoc.return_value = (0.1, 0.3, (10, 10), (100, 100))  # Baja confianza
        mock_pyautogui.screenshot.return_value = Mock()
        
        mock_template = Mock()
        mock_template.shape = (50, 50, 3)
        
        from rpa.vision.template_matcher import TemplateMatcher
        matcher = TemplateMatcher()
        
        result = matcher.find_template(mock_template, confidence=0.8)
        
        self.assertIsNone(result)
    
    def test_template_cache(self):
        """Test que el caché de templates funciona"""
        from rpa.vision.template_matcher import TemplateMatcher
        
        matcher = TemplateMatcher()
        
        # Simular carga de template
        test_path = "test_image.png"
        mock_image = Mock()
        
        with patch('cv2.imread', return_value=mock_image):
            result1 = matcher.load_template_image(test_path)
            result2 = matcher.load_template_image(test_path)
        
        # Debe retornar el mismo objeto del caché
        self.assertIs(result1, result2)


class SmartWaitsTests(RPATestCase):
    """Tests para el sistema de esperas inteligentes"""
    
    @patch('time.sleep')
    def test_adaptive_wait(self, mock_sleep):
        """Test esperas adaptativas"""
        from rpa.smart_waits import SmartWaits
        
        waits = SmartWaits()
        waits.adaptive_wait('input', 1.0)
        
        mock_sleep.assert_called()
        # Verificar que se llamó con un tiempo razonable
        call_args = mock_sleep.call_args[0][0]
        self.assertGreater(call_args, 0.1)
        self.assertLess(call_args, 5.0)
    
    @patch('time.time')
    @patch('time.sleep')
    def test_wait_for_element_success(self, mock_sleep, mock_time):
        """Test espera exitosa de elemento"""
        from rpa.smart_waits import SmartWaits
        
        # Simular tiempo
        mock_time.side_effect = [0, 0.5, 1.0]  # 1 segundo total
        
        waits = SmartWaits()
        
        # Función que retorna True en el segundo intento
        call_count = 0
        def check_function():
            nonlocal call_count
            call_count += 1
            return call_count >= 2
        
        result = waits.wait_for_element(check_function, timeout=5.0)
        
        self.assertTrue(result)
    
    @patch('time.time')
    @patch('time.sleep')
    def test_wait_for_element_timeout(self, mock_sleep, mock_time):
        """Test timeout en espera de elemento"""
        from rpa.smart_waits import SmartWaits
        
        # Simular timeout
        mock_time.side_effect = [0, 6.0]  # Supera el timeout de 5s
        
        waits = SmartWaits()
        
        result = waits.wait_for_element(lambda: False, timeout=5.0)
        
        self.assertFalse(result)


class ErrorHandlerTests(RPATestCase):
    """Tests para el sistema de manejo de errores"""
    
    def test_error_context_creation(self):
        """Test creación de contexto de error"""
        from rpa.error_handler import ErrorContext, ErrorType, ErrorSeverity
        
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_operation",
            file_name="test.json"
        )
        
        self.assertEqual(context.error_type, ErrorType.TEMPLATE_MATCHING)
        self.assertEqual(context.severity, ErrorSeverity.MEDIUM)
        self.assertEqual(context.operation, "test_operation")
        self.assertEqual(context.file_name, "test.json")
    
    @patch('rpa.error_handler.rpa_logger')
    def test_error_handler_logs_correctly(self, mock_logger):
        """Test que ErrorHandler registra errores correctamente"""
        from rpa.error_handler import ErrorHandler, ErrorContext, ErrorType, ErrorSeverity
        
        handler = ErrorHandler()
        exception = Exception("Test error")
        context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test_operation"
        )
        
        handler._log_error(exception, context)
        
        # Verificar que se llamó al logger
        mock_logger.warning.assert_called()
    
    def test_should_attempt_recovery(self):
        """Test lógica de decisión de recuperación"""
        from rpa.error_handler import ErrorHandler, ErrorContext, ErrorType, ErrorSeverity
        
        handler = ErrorHandler()
        
        # Error crítico - no debe intentar recuperación
        critical_context = ErrorContext(
            error_type=ErrorType.SYSTEM_ERROR,
            severity=ErrorSeverity.CRITICAL,
            operation="test",
            retry_count=0,
            max_retries=3
        )
        
        self.assertFalse(handler._should_attempt_recovery(critical_context))
        
        # Error medio con reintentos disponibles - debe intentar recuperación
        medium_context = ErrorContext(
            error_type=ErrorType.TEMPLATE_MATCHING,
            severity=ErrorSeverity.MEDIUM,
            operation="test",
            retry_count=1,
            max_retries=3
        )
        
        self.assertTrue(handler._should_attempt_recovery(medium_context))


class RPAMainTests(RPATestCase):
    """Tests para la clase principal RPA"""
    
    @patch('rpa.main.pyautogui')
    @patch('rpa.main.vision')
    def test_rpa_initialization(self, mock_vision, mock_pyautogui):
        """Test inicialización de clase RPA"""
        from rpa.main import RPA
        
        rpa = RPA()
        
        self.assertIsNotNone(rpa.remote_desktop_window)
        self.assertEqual(rpa.remote_desktop_window, "20.96.6.64 - Conexión a Escritorio remoto")
    
    @patch('rpa.main.pyautogui')
    def test_load_nit_validation(self, mock_pyautogui):
        """Test validación de NIT"""
        from rpa.main import RPA
        
        rpa = RPA()
        
        # NIT vacío debe lanzar excepción
        with self.assertRaises(ValueError):
            rpa.load_nit("")
        
        # NIT None debe lanzar excepción
        with self.assertRaises(ValueError):
            rpa.load_nit(None)
    
    def test_json_file_filtering(self):
        """Test filtrado de archivos JSON"""
        # Simular estructura de archivos
        files = {
            './data/outputs_json': [
                'valid.json',
                'another.json',
                '.hidden.json',
                'temp.tmp',
                'desktop.ini',
                'Procesados'  # directorio
            ],
            './data/outputs_json/valid.json': True,
            './data/outputs_json/another.json': True,
            './data/outputs_json/.hidden.json': True,
            './data/outputs_json/temp.tmp': True,
            './data/outputs_json/desktop.ini': True,
            './data/outputs_json/Procesados': []  # es directorio
        }
        
        with self.mock_file_system(files):
            directory = './data/outputs_json'
            filtered_files = [f for f in os.listdir(directory) 
                            if os.path.isfile(os.path.join(directory, f))
                            and f.endswith('.json')
                            and not f.startswith('.')
                            and not f.endswith('.tmp')]
            
            expected_files = ['valid.json', 'another.json']
            self.assertEqual(sorted(filtered_files), sorted(expected_files))


def run_tests():
    """Ejecuta todos los tests"""
    print("Ejecutando Tests del Sistema RPA...")
    print("=" * 50)
    
    # Configurar test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de test
    test_classes = [
        ConfigTests,
        TemplateMatcherTests,  
        SmartWaitsTests,
        ErrorHandlerTests,
        RPAMainTests
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print(f"📊 RESUMEN DE TESTS:")
    print(f"✅ Tests ejecutados: {result.testsRun}")
    print(f"❌ Errores: {len(result.errors)}")
    print(f"⚠️  Fallos: {len(result.failures)}")
    
    if result.errors:
        print(f"\n🔴 ERRORES:")
        for test, error in result.errors:
            print(f"  - {test}: {error.splitlines()[-1]}")
    
    if result.failures:
        print(f"\n🟡 FALLOS:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.splitlines()[-1]}")
    
    success_rate = ((result.testsRun - len(result.errors) - len(result.failures)) / result.testsRun) * 100
    print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)