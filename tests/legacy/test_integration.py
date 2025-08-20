"""
Tests de integración para verificar que los componentes trabajan juntos correctamente
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_framework import RPATestCase


class IntegrationTests(RPATestCase):
    """Tests de integración para flujos completos"""
    
    def setUp(self):
        super().setUp()
        self.sample_json_data = {
            "comprador": {"nit": "900123456"},
            "orden_compra": "OC-2024-001",
            "fecha_entrega": "31/12/2024",
            "items": [
                {"codigo": "PROD001", "cantidad": "10"},
                {"codigo": "PROD002", "cantidad": "5"}
            ]
        }
    
    @patch('rpa.main.pyautogui')
    @patch('rpa.main.vision')
    @patch('rpa.main.smart_sleep')
    def test_complete_data_loading_flow(self, mock_sleep, mock_vision, mock_pyautogui):
        """Test del flujo completo de carga de datos"""
        from rpa.main import RPA
        
        # Configurar mocks
        mock_vision.save_template = Mock()
        mock_pyautogui.screenshot.return_value = Mock()
        mock_pyautogui.typewrite = Mock()
        mock_pyautogui.hotkey = Mock()
        
        rpa = RPA()
        
        # Ejecutar flujo completo
        with patch.object(rpa, 'take_totals_screenshot'), \
             patch.object(rpa, 'move_json_to_processed', return_value=True):
            rpa.data_loader(self.sample_json_data, "test.json")
        
        # Verificar que se llamaron las funciones principales
        mock_pyautogui.typewrite.assert_called()
        mock_pyautogui.hotkey.assert_called()
        
        # Verificar cantidad de llamadas (NIT + Orden + Fecha + 2 Items)
        self.assertGreaterEqual(mock_pyautogui.typewrite.call_count, 5)
    
    @patch('rpa.vision.template_matcher.cv2')
    @patch('rpa.vision.template_matcher.pyautogui')
    def test_vision_system_integration(self, mock_pyautogui, mock_cv2):
        """Test de integración del sistema de visión"""
        # Configurar mocks para template matching exitoso
        mock_cv2.matchTemplate.return_value = Mock()
        mock_cv2.minMaxLoc.return_value = (0.1, 0.9, (10, 10), (100, 100))
        mock_pyautogui.screenshot.return_value = Mock()
        
        # Configurar mock para imagen
        mock_image = Mock()
        mock_image.shape = (50, 50, 3)
        mock_cv2.imread.return_value = mock_image
        
        from rpa.vision.main import Vision
        vision = Vision()
        
        # Test múltiples funciones de detección
        sap_coords = vision.get_sap_coordinates()
        
        self.assertIsNotNone(sap_coords)
        self.assertIsInstance(sap_coords, tuple)
        
        # Verificar que se llamaron las funciones de OpenCV
        mock_cv2.matchTemplate.assert_called()
        mock_cv2.minMaxLoc.assert_called()


class QuickTests(RPATestCase):
    """Tests rápidos para verificación básica"""
    
    def test_imports_work(self):
        """Test que todas las importaciones funcionen"""
        try:
            from rpa.main import RPA
            from rpa.config_manager import ConfigManager
            from rpa.simple_logger import rpa_logger
            from rpa.smart_waits import SmartWaits
            from rpa.error_handler import ErrorHandler
            from rpa.vision.template_matcher import TemplateMatcher
            self.assertTrue(True, "Todas las importaciones exitosas")
        except ImportError as e:
            self.fail(f"Error de importación: {e}")
    
    def test_basic_functionality(self):
        """Test funcionalidad básica sin dependencias externas"""
        from rpa.config_manager import ConfigManager
        from rpa.simple_logger import SimpleRPALogger
        from rpa.smart_waits import SmartWaits
        
        # Test ConfigManager
        config = ConfigManager('nonexistent.yaml')  # Usa defaults
        self.assertIsNotNone(config.get('delays.short', 0.5))
        
        # Test Logger
        logger = SimpleRPALogger()
        self.assertIsNotNone(logger.logger)
        
        # Test SmartWaits
        waits = SmartWaits()
        self.assertIsNotNone(waits)
    
    def test_json_data_structure(self):
        """Test estructura de datos JSON"""
        sample_data = {
            "comprador": {"nit": "900123456"},
            "orden_compra": "OC-2024-001",
            "fecha_entrega": "31/12/2024",
            "items": [
                {"codigo": "PROD001", "cantidad": "10"}
            ]
        }
        
        # Verificar campos requeridos
        required_fields = ['comprador', 'orden_compra', 'fecha_entrega', 'items']
        for field in required_fields:
            self.assertIn(field, sample_data, f"Campo requerido faltante: {field}")
        
        # Verificar NIT
        self.assertIn('nit', sample_data['comprador'])
        self.assertTrue(sample_data['comprador']['nit'].strip())
        
        # Verificar items
        self.assertIsInstance(sample_data['items'], list)
        self.assertGreater(len(sample_data['items']), 0)
        
        for item in sample_data['items']:
            self.assertIn('codigo', item)
            self.assertIn('cantidad', item)


if __name__ == '__main__':
    print("Ejecutando Tests de Integración...")
    unittest.main(verbosity=2)