#!/usr/bin/env python3
"""
Tests unitarios para el módulo de órdenes de producción
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpa.modules.production_order import ProductionOrderHandler
from rpa.vision.main import Vision


class TestProductionOrderHandler(unittest.TestCase):
    """Tests para ProductionOrderHandler"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_vision = Mock(spec=Vision)
        self.mock_config = Mock()
        self.mock_config.get.return_value = 1.0  # Valor por defecto para delays
        
        # Mock de la configuración de producción
        self.mock_production_config = {
            'navigation': {
                'alt_m_delay': 0.5,
                'p_key_delay': 1.0,
                'mouse_click_delay': 2.0
            },
            'form_fields': {
                'articulo_tabs': 2,
                'pedido_interno_tabs': 3,
                'cantidad_tabs': 2,
                'fecha_finalizacion_tabs': 3
            },
            'validation': {
                'max_cantidad': 999999,
                'formato_fecha': 'DD/MM/YYYY'
            },
            'template_matching': {
                'orden_fabricacion_button_confidence': 0.8,
                'field_confidence': 0.85
            },
            'timeouts': {
                'navigation_timeout': 10.0,
                'field_input_timeout': 5.0
            }
        }
        
        # Crear handler con mocks
        with patch.object(ProductionOrderHandler, '_load_production_config', return_value=self.mock_production_config):
            self.handler = ProductionOrderHandler(self.mock_vision, self.mock_config)
    
    def test_validate_form_data_valid(self):
        """Test validación de datos válidos"""
        valid_data = {
            'numero_articulo': 'ART-001',
            'numero_pedido_interno': 'PI-001',
            'cantidad': 100,
            'fecha_finalizacion': '15/12/2024'
        }
        
        result = self.handler.validate_form_data(valid_data)
        self.assertTrue(result)
    
    def test_validate_form_data_missing_field(self):
        """Test validación con campo faltante"""
        invalid_data = {
            'numero_articulo': 'ART-001',
            'numero_pedido_interno': 'PI-001',
            'cantidad': 100
            # fecha_finalizacion faltante
        }
        
        result = self.handler.validate_form_data(invalid_data)
        self.assertFalse(result)
    
    def test_validate_form_data_invalid_quantity(self):
        """Test validación con cantidad inválida"""
        invalid_data = {
            'numero_articulo': 'ART-001',
            'numero_pedido_interno': 'PI-001',
            'cantidad': -5,  # Cantidad negativa
            'fecha_finalizacion': '15/12/2024'
        }
        
        result = self.handler.validate_form_data(invalid_data)
        self.assertFalse(result)
    
    def test_validate_form_data_invalid_date_format(self):
        """Test validación con formato de fecha inválido"""
        invalid_data = {
            'numero_articulo': 'ART-001',
            'numero_pedido_interno': 'PI-001',
            'cantidad': 100,
            'fecha_finalizacion': '2024-12-15'  # Formato incorrecto
        }
        
        result = self.handler.validate_form_data(invalid_data)
        self.assertFalse(result)
    
    def test_load_articulo_success(self):
        """Test carga exitosa de artículo"""
        with patch('pyautogui.press') as mock_press, \
             patch('pyautogui.write') as mock_write, \
             patch('time.sleep') as mock_sleep:
            
            result = self.handler.load_articulo('ART-001')
            
            self.assertTrue(result)
            # Verificar que se presionó tab el número correcto de veces
            self.assertEqual(mock_press.call_count, 2)  # articulo_tabs = 2
            # Verificar que se escribió el artículo
            mock_write.assert_called_once_with('ART-001')
    
    def test_load_pedido_interno_success(self):
        """Test carga exitosa de pedido interno"""
        with patch('pyautogui.press') as mock_press, \
             patch('pyautogui.write') as mock_write, \
             patch('time.sleep') as mock_sleep:
            
            result = self.handler.load_pedido_interno('PI-001')
            
            self.assertTrue(result)
            # Verificar que se presionó tab el número correcto de veces
            self.assertEqual(mock_press.call_count, 3)  # pedido_interno_tabs = 3
            # Verificar que se escribió el pedido interno
            mock_write.assert_called_once_with('PI-001')
    
    def test_load_cantidad_success(self):
        """Test carga exitosa de cantidad"""
        with patch('pyautogui.press') as mock_press, \
             patch('pyautogui.write') as mock_write, \
             patch('time.sleep') as mock_sleep:
            
            result = self.handler.load_cantidad(100)
            
            self.assertTrue(result)
            # Verificar que se presionó tab el número correcto de veces
            self.assertEqual(mock_press.call_count, 2)  # cantidad_tabs = 2
            # Verificar que se escribió la cantidad como string
            mock_write.assert_called_once_with('100')
    
    def test_load_fecha_finalizacion_success(self):
        """Test carga exitosa de fecha de finalización"""
        with patch('pyautogui.press') as mock_press, \
             patch('pyautogui.write') as mock_write, \
             patch('time.sleep') as mock_sleep:
            
            result = self.handler.load_fecha_finalizacion('15/12/2024')
            
            self.assertTrue(result)
            # Verificar que se presionó tab el número correcto de veces
            self.assertEqual(mock_press.call_count, 3)  # fecha_finalizacion_tabs = 3
            # Verificar que se escribió la fecha
            mock_write.assert_called_once_with('15/12/2024')
    
    def test_navigate_to_production_success(self):
        """Test navegación exitosa a producción"""
        self.mock_vision.find_and_click.return_value = True
        
        with patch('pyautogui.hotkey') as mock_hotkey, \
             patch('pyautogui.press') as mock_press, \
             patch('time.sleep') as mock_sleep:
            
            result = self.handler.navigate_to_production()
            
            self.assertTrue(result)
            # Verificar que se presionó Alt+M
            mock_hotkey.assert_called_once_with('alt', 'm')
            # Verificar que se presionó P
            mock_press.assert_called_once_with('p')
            # Verificar que se buscó el botón de orden de fabricación
            self.mock_vision.find_and_click.assert_called_once()
    
    def test_navigate_to_production_failure(self):
        """Test navegación fallida a producción"""
        self.mock_vision.find_and_click.return_value = False
        
        with patch('pyautogui.hotkey') as mock_hotkey, \
             patch('pyautogui.press') as mock_press, \
             patch('time.sleep') as mock_sleep:
            
            result = self.handler.navigate_to_production()
            
            self.assertFalse(result)
    
    def test_process_production_order_success_without_auto_click(self):
        """Test procesamiento exitoso sin auto-click en crear"""
        test_data = {
            'numero_articulo': 'ART-001',
            'numero_pedido_interno': 'PI-001',
            'cantidad': 100,
            'fecha_finalizacion': '15/12/2024'
        }
        
        with patch.object(self.handler, 'load_articulo', return_value=True), \
             patch.object(self.handler, 'load_pedido_interno', return_value=True), \
             patch.object(self.handler, 'load_cantidad', return_value=True), \
             patch.object(self.handler, 'load_fecha_finalizacion', return_value=True):
            
            result = self.handler.process_production_order(test_data, auto_click_crear=False)
            
            self.assertTrue(result)
            # Verificar que NO se llamó click_crear_button
            self.assertFalse(hasattr(self.handler, 'click_crear_button') or 
                           getattr(self.handler, 'click_crear_button', None) is not None)
    
    def test_process_production_order_success_with_auto_click(self):
        """Test procesamiento exitoso con auto-click en crear"""
        test_data = {
            'numero_articulo': 'ART-001',
            'numero_pedido_interno': 'PI-001',
            'cantidad': 100,
            'fecha_finalizacion': '15/12/2024'
        }
        
        with patch.object(self.handler, 'load_articulo', return_value=True), \
             patch.object(self.handler, 'load_pedido_interno', return_value=True), \
             patch.object(self.handler, 'load_cantidad', return_value=True), \
             patch.object(self.handler, 'load_fecha_finalizacion', return_value=True), \
             patch.object(self.handler, 'click_crear_button', return_value=True):
            
            result = self.handler.process_production_order(test_data, auto_click_crear=True)
            
            self.assertTrue(result)
            # Verificar que se llamó click_crear_button
            self.handler.click_crear_button.assert_called_once()
    
    def test_process_production_order_validation_failure(self):
        """Test procesamiento fallido por validación"""
        invalid_data = {
            'numero_articulo': 'ART-001',
            # Datos incompletos
        }
        
        result = self.handler.process_production_order(invalid_data)
        
        self.assertFalse(result)


class TestProductionOrderHandlerIntegration(unittest.TestCase):
    """Tests de integración para ProductionOrderHandler"""
    
    def setUp(self):
        """Configuración inicial para tests de integración"""
        self.mock_vision = Mock(spec=Vision)
        self.mock_config = Mock()
        self.mock_config.get.return_value = 1.0
        
        # Configuración real de producción
        self.real_production_config = {
            'navigation': {
                'alt_m_delay': 0.5,
                'p_key_delay': 1.0,
                'mouse_click_delay': 2.0
            },
            'form_fields': {
                'articulo_tabs': 2,
                'pedido_interno_tabs': 3,
                'cantidad_tabs': 2,
                'fecha_finalizacion_tabs': 3
            },
            'validation': {
                'max_cantidad': 999999,
                'formato_fecha': 'DD/MM/YYYY'
            },
            'template_matching': {
                'orden_fabricacion_button_confidence': 0.8,
                'field_confidence': 0.85
            },
            'timeouts': {
                'navigation_timeout': 10.0,
                'field_input_timeout': 5.0
            }
        }
        
        with patch.object(ProductionOrderHandler, '_load_production_config', return_value=self.real_production_config):
            self.handler = ProductionOrderHandler(self.mock_vision, self.mock_config)
    
    def test_configuration_loading(self):
        """Test que la configuración se carga correctamente"""
        self.assertEqual(self.handler.production_config, self.real_production_config)
        self.assertEqual(
            self.handler.production_config['form_fields']['articulo_tabs'], 
            2
        )
        self.assertEqual(
            self.handler.production_config['validation']['max_cantidad'], 
            999999
        )
    
    def test_complete_workflow_simulation(self):
        """Simulación del flujo completo sin interacción real"""
        test_data = {
            'numero_articulo': 'ART-INTEGRATION',
            'numero_pedido_interno': 'PI-INTEGRATION-001',
            'cantidad': 250,
            'fecha_finalizacion': '25/12/2024'
        }
        
        # Mock de todos los métodos para simular éxito
        with patch.object(self.handler, 'navigate_to_production', return_value=True), \
             patch.object(self.handler, 'load_articulo', return_value=True), \
             patch.object(self.handler, 'load_pedido_interno', return_value=True), \
             patch.object(self.handler, 'load_cantidad', return_value=True), \
             patch.object(self.handler, 'load_fecha_finalizacion', return_value=True):
            
            # Simular el flujo completo
            result = self.handler.process_production_order(test_data, auto_click_crear=False)
            
            self.assertTrue(result)
            
            # Verificar que se llamaron todos los métodos esperados
            self.handler.navigate_to_production.assert_called_once()
            self.handler.load_articulo.assert_called_once_with('ART-INTEGRATION')
            self.handler.load_pedido_interno.assert_called_once_with('PI-INTEGRATION-001')
            self.handler.load_cantidad.assert_called_once_with(250)
            self.handler.load_fecha_finalizacion.assert_called_once_with('25/12/2024')


if __name__ == '__main__':
    # Crear suite de tests
    test_suite = unittest.TestSuite()
    
    # Agregar tests unitarios
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestProductionOrderHandler))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestProductionOrderHandlerIntegration))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Mostrar resumen
    print(f"\n{'='*60}")
    print(f"RESUMEN DE TESTS")
    print(f"{'='*60}")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Exitosos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.errors:
        print(f"\nErrores encontrados:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    if result.failures:
        print(f"\nFallos encontrados:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.wasSuccessful():
        print(f"\n✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print(f"\n❌ ALGUNOS TESTS FALLARON")
