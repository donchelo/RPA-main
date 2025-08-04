"""
Tests para ConfigManager - FASE 1
Tests básicos de configuración (Fácil + Alto impacto)
"""

import unittest
import tempfile
import os
import yaml
from unittest.mock import patch, mock_open
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rpa.config_manager import ConfigManager, get_delay, get_confidence, get_navigation_tabs, get_retry_attempts


class TestConfigManager(unittest.TestCase):
    """Tests para el gestor de configuración"""
    
    def setUp(self):
        """Setup para cada test"""
        self.test_config = {
            'delays': {
                'short': 0.5,
                'medium': 1.0,
                'after_input': 1.5,
                'sap_startup': 30.0
            },
            'template_matching': {
                'default_confidence': 0.8,
                'high_confidence': 0.9,
                'timeout': 10.0
            },
            'navigation': {
                'tabs_after_nit': 3,
                'tabs_after_order': 4
            },
            'retries': {
                'max_sap_open_attempts': 3,
                'max_remote_desktop_attempts': 5
            }
        }
    
    def test_load_valid_config(self):
        """Test: Cargar configuración válida"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_file = f.name
        
        try:
            config_manager = ConfigManager(temp_file)
            self.assertEqual(config_manager.get('delays.short'), 0.5)
            self.assertEqual(config_manager.get('template_matching.default_confidence'), 0.8)
        finally:
            os.unlink(temp_file)
    
    def test_get_with_dot_notation(self):
        """Test: Acceso con notación de puntos"""
        config_manager = ConfigManager()
        config_manager.config = self.test_config
        
        self.assertEqual(config_manager.get('delays.medium'), 1.0)
        self.assertEqual(config_manager.get('template_matching.timeout'), 10.0)
        self.assertEqual(config_manager.get('navigation.tabs_after_nit'), 3)
    
    def test_get_with_default_value(self):
        """Test: Valor por defecto cuando clave no existe"""
        config_manager = ConfigManager()
        config_manager.config = self.test_config
        
        # Clave que no existe
        result = config_manager.get('nonexistent.key', 'default_value')
        self.assertEqual(result, 'default_value')
    
    def test_get_nonexistent_key_raises_error(self):
        """Test: Error cuando clave no existe y no hay default"""
        config_manager = ConfigManager()
        config_manager.config = self.test_config
        
        with self.assertRaises(KeyError):
            config_manager.get('nonexistent.key')
    
    def test_get_delays_method(self):
        """Test: Método get_delays()"""
        config_manager = ConfigManager()
        config_manager.config = self.test_config
        
        delays = config_manager.get_delays()
        self.assertEqual(delays['short'], 0.5)
        self.assertEqual(delays['medium'], 1.0)
        self.assertEqual(delays['sap_startup'], 30.0)
    
    def test_get_template_config_method(self):
        """Test: Método get_template_config()"""
        config_manager = ConfigManager()
        config_manager.config = self.test_config
        
        template_config = config_manager.get_template_config()
        self.assertEqual(template_config['default_confidence'], 0.8)
        self.assertEqual(template_config['timeout'], 10.0)
    
    def test_validate_config_success(self):
        """Test: Validación exitosa de configuración"""
        config_manager = ConfigManager()
        config_manager.config = self.test_config
        
        result = config_manager.validate_config()
        self.assertTrue(result)
    
    def test_validate_config_missing_keys(self):
        """Test: Validación falla con claves faltantes"""
        incomplete_config = {'delays': {'short': 0.5}}
        config_manager = ConfigManager()
        config_manager.config = incomplete_config
        
        result = config_manager.validate_config()
        self.assertFalse(result)
    
    def test_convenience_functions(self):
        """Test: Funciones de conveniencia"""
        # Mock del config global
        with patch('rpa.config_manager.config') as mock_config:
            mock_config.get.side_effect = lambda key, default=None: {
                'delays.short': 0.5,
                'delays.after_input': 1.5,
                'template_matching.default_confidence': 0.8,
                'navigation.tabs_after_nit': 3,
                'retries.max_sap_open_attempts': 3
            }.get(key, default)
            
            # Test get_delay
            self.assertEqual(get_delay('short'), 0.5)
            self.assertEqual(get_delay('after_input'), 1.5)
            self.assertEqual(get_delay('nonexistent'), 1.0)  # default
            
            # Test get_confidence
            self.assertEqual(get_confidence('default'), 0.8)
            self.assertEqual(get_confidence('nonexistent'), 0.8)  # default
            
            # Test get_navigation_tabs
            self.assertEqual(get_navigation_tabs('after_nit'), 3)
            self.assertEqual(get_navigation_tabs('nonexistent'), 1)  # default
            
            # Test get_retry_attempts
            self.assertEqual(get_retry_attempts('sap_open'), 3)
            self.assertEqual(get_retry_attempts('nonexistent'), 3)  # default


class TestConfigManagerErrorHandling(unittest.TestCase):
    """Tests para manejo de errores en ConfigManager"""
    
    def test_load_nonexistent_file(self):
        """Test: Cargar archivo que no existe usa configuración por defecto"""
        config_manager = ConfigManager('nonexistent_file.yaml')
        
        # Debe cargar configuración por defecto
        self.assertIsInstance(config_manager.config, dict)
        self.assertIn('delays', config_manager.config)
        self.assertIn('template_matching', config_manager.config)
    
    def test_load_invalid_yaml(self):
        """Test: Cargar YAML inválido usa configuración por defecto"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")  # YAML inválido
            temp_file = f.name
        
        try:
            config_manager = ConfigManager(temp_file)
            # Debe cargar configuración por defecto
            self.assertIsInstance(config_manager.config, dict)
            self.assertIn('delays', config_manager.config)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()