import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rpa.state_machine import StateMachine, RPAState, RPAEvent, StateContext
from rpa.rpa_state_handlers import RPAStateHandlers


class TestStateMachine(unittest.TestCase):
    """Tests para la máquina de estados del RPA"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.state_machine = StateMachine()
    
    def test_initial_state(self):
        """Verifica que el estado inicial sea IDLE"""
        self.assertEqual(self.state_machine.get_current_state(), RPAState.IDLE)
    
    def test_valid_transition(self):
        """Verifica que las transiciones válidas funcionen correctamente"""
        # Transición de IDLE a CONNECTING_REMOTE_DESKTOP
        success = self.state_machine.trigger_event(RPAEvent.START_PROCESSING)
        self.assertTrue(success)
        self.assertEqual(self.state_machine.get_current_state(), RPAState.CONNECTING_REMOTE_DESKTOP)
    
    def test_invalid_transition(self):
        """Verifica que las transiciones inválidas sean rechazadas"""
        # Intentar una transición inválida desde IDLE
        success = self.state_machine.trigger_event(RPAEvent.SAP_OPENED)
        self.assertFalse(success)
        self.assertEqual(self.state_machine.get_current_state(), RPAState.IDLE)
    
    def test_full_happy_path(self):
        """Verifica el flujo completo exitoso"""
        events_sequence = [
            RPAEvent.START_PROCESSING,
            RPAEvent.REMOTE_DESKTOP_CONNECTED,
            RPAEvent.SAP_OPENED,
            RPAEvent.SALES_ORDER_OPENED,
            RPAEvent.NIT_LOADED,
            RPAEvent.ORDER_LOADED,
            RPAEvent.DATE_LOADED,
            RPAEvent.ITEMS_LOADED,
            RPAEvent.SCROLLED_TO_TOTALS,
            RPAEvent.SCREENSHOT_TAKEN,
            RPAEvent.JSON_MOVED
        ]
        
        expected_states = [
            RPAState.CONNECTING_REMOTE_DESKTOP,
            RPAState.OPENING_SAP,
            RPAState.NAVIGATING_TO_SALES_ORDER,
            RPAState.LOADING_NIT,
            RPAState.LOADING_ORDER,
            RPAState.LOADING_DATE,
            RPAState.LOADING_ITEMS,
            RPAState.SCROLLING_TO_TOTALS,
            RPAState.TAKING_SCREENSHOT,
            RPAState.MOVING_JSON,
            RPAState.COMPLETED
        ]
        
        for event, expected_state in zip(events_sequence, expected_states):
            success = self.state_machine.trigger_event(event)
            self.assertTrue(success, f"Transición falló para evento: {event.value}")
            self.assertEqual(
                self.state_machine.get_current_state(), 
                expected_state,
                f"Estado incorrecto después del evento: {event.value}"
            )
    
    def test_error_handling(self):
        """Verifica el manejo de errores y reintentos"""
        # Avanzar a un estado intermedio
        self.state_machine.trigger_event(RPAEvent.START_PROCESSING)
        self.state_machine.trigger_event(RPAEvent.REMOTE_DESKTOP_CONNECTED)
        
        # Simular error
        success = self.state_machine.trigger_event(RPAEvent.SAP_FAILED)
        self.assertTrue(success)
        self.assertEqual(self.state_machine.get_current_state(), RPAState.ERROR)
        
        # Verificar reintento
        context = self.state_machine.get_context()
        context.retry_count = 1
        context.max_retries = 3
        
        success = self.state_machine.trigger_event(RPAEvent.RETRY)
        self.assertTrue(success)
        self.assertEqual(self.state_machine.get_current_state(), RPAState.RETRYING)
    
    def test_context_management(self):
        """Verifica que el contexto se maneje correctamente"""
        test_file = "test_file.json"
        test_data = {"test": "data"}
        
        success = self.state_machine.start_processing(test_file, test_data)
        self.assertTrue(success)
        
        context = self.state_machine.get_context()
        self.assertEqual(context.current_file, test_file)
        self.assertEqual(context.current_data, test_data)
        self.assertEqual(context.retry_count, 0)
        self.assertIsNotNone(context.start_time)
    
    def test_state_info(self):
        """Verifica que get_state_info retorne información correcta"""
        info = self.state_machine.get_state_info()
        
        self.assertIn('current_state', info)
        self.assertIn('available_events', info)
        self.assertIn('context', info)
        
        self.assertEqual(info['current_state'], RPAState.IDLE.value)
        self.assertIsInstance(info['available_events'], list)
    
    def test_can_transition_to(self):
        """Verifica la funcionalidad can_transition_to"""
        # Desde IDLE, debería poder ir a START_PROCESSING
        self.assertTrue(self.state_machine.can_transition_to(RPAEvent.START_PROCESSING))
        
        # Desde IDLE, no debería poder ir a SAP_OPENED
        self.assertFalse(self.state_machine.can_transition_to(RPAEvent.SAP_OPENED))
    
    def test_get_available_events(self):
        """Verifica que se retornen los eventos disponibles correctos"""
        available_events = self.state_machine.get_available_events()
        self.assertIn(RPAEvent.START_PROCESSING, available_events)
        
        # Cambiar estado y verificar nuevos eventos disponibles
        self.state_machine.trigger_event(RPAEvent.START_PROCESSING)
        available_events = self.state_machine.get_available_events()
        self.assertIn(RPAEvent.REMOTE_DESKTOP_CONNECTED, available_events)
        self.assertIn(RPAEvent.REMOTE_DESKTOP_FAILED, available_events)
    
    def test_reset(self):
        """Verifica que el reset funcione correctamente"""
        # Avanzar a un estado diferente
        self.state_machine.start_processing("test.json", {"test": "data"})
        self.assertNotEqual(self.state_machine.get_current_state(), RPAState.IDLE)
        
        # Resetear
        self.state_machine.reset()
        self.assertEqual(self.state_machine.get_current_state(), RPAState.IDLE)
        
        # Verificar que el contexto también se reinició
        context = self.state_machine.get_context()
        self.assertIsNone(context.current_file)
        self.assertIsNone(context.current_data)
        self.assertEqual(context.retry_count, 0)


class TestRPAStateHandlers(unittest.TestCase):
    """Tests para los manejadores de estado del RPA"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_rpa = Mock()
        self.state_handlers = RPAStateHandlers(self.mock_rpa)
        self.context = StateContext()
        self.context.current_file = "test_file.json"
        self.context.current_data = {
            "comprador": {"nit": "12345"},
            "orden_compra": "OC-123",
            "fecha_entrega": "2024-12-31",
            "items": [{"codigo": "ITEM1", "cantidad": 10}]
        }
    
    def test_handle_connecting_remote_desktop_success(self):
        """Verifica el manejo exitoso de conexión a escritorio remoto"""
        self.mock_rpa.get_remote_desktop.return_value = True
        
        result = self.state_handlers.handle_connecting_remote_desktop(self.context)
        
        self.assertEqual(result, RPAEvent.REMOTE_DESKTOP_CONNECTED)
        self.mock_rpa.get_remote_desktop.assert_called_once()
    
    def test_handle_connecting_remote_desktop_failure(self):
        """Verifica el manejo de fallo en conexión a escritorio remoto"""
        self.mock_rpa.get_remote_desktop.return_value = False
        
        result = self.state_handlers.handle_connecting_remote_desktop(self.context)
        
        self.assertEqual(result, RPAEvent.REMOTE_DESKTOP_FAILED)
        self.mock_rpa.get_remote_desktop.assert_called_once()
    
    def test_handle_opening_sap_success(self):
        """Verifica el manejo exitoso de apertura de SAP"""
        self.mock_rpa.open_sap.return_value = True
        
        result = self.state_handlers.handle_opening_sap(self.context)
        
        self.assertEqual(result, RPAEvent.SAP_OPENED)
        self.mock_rpa.open_sap.assert_called_once()
    
    def test_handle_loading_nit_success(self):
        """Verifica el manejo exitoso de carga de NIT"""
        result = self.state_handlers.handle_loading_nit(self.context)
        
        self.assertEqual(result, RPAEvent.NIT_LOADED)
        self.mock_rpa.load_nit.assert_called_once_with("12345")
    
    def test_handle_loading_nit_missing_data(self):
        """Verifica el manejo de datos faltantes en carga de NIT"""
        self.context.current_data = {}
        
        result = self.state_handlers.handle_loading_nit(self.context)
        
        self.assertEqual(result, RPAEvent.NIT_FAILED)
        self.mock_rpa.load_nit.assert_not_called()
    
    def test_handle_loading_order_success(self):
        """Verifica el manejo exitoso de carga de orden"""
        result = self.state_handlers.handle_loading_order(self.context)
        
        self.assertEqual(result, RPAEvent.ORDER_LOADED)
        self.mock_rpa.load_orden_compra.assert_called_once_with("OC-123")
    
    def test_handle_loading_date_success(self):
        """Verifica el manejo exitoso de carga de fecha"""
        result = self.state_handlers.handle_loading_date(self.context)
        
        self.assertEqual(result, RPAEvent.DATE_LOADED)
        self.mock_rpa.load_fecha_entrega.assert_called_once_with("2024-12-31")
    
    def test_handle_loading_items_success(self):
        """Verifica el manejo exitoso de carga de items"""
        result = self.state_handlers.handle_loading_items(self.context)
        
        self.assertEqual(result, RPAEvent.ITEMS_LOADED)
        self.mock_rpa.load_items.assert_called_once_with([{"codigo": "ITEM1", "cantidad": 10}])
    
    def test_handle_scrolling_success(self):
        """Verifica el manejo exitoso de scroll"""
        self.mock_rpa.scroll_to_bottom.return_value = True
        
        result = self.state_handlers.handle_scrolling_to_totals(self.context)
        
        self.assertEqual(result, RPAEvent.SCROLLED_TO_TOTALS)
        self.mock_rpa.scroll_to_bottom.assert_called_once()
    
    def test_handle_screenshot_success(self):
        """Verifica el manejo exitoso de captura de pantalla"""
        self.mock_rpa.take_totals_screenshot.return_value = True
        
        result = self.state_handlers.handle_taking_screenshot(self.context)
        
        self.assertEqual(result, RPAEvent.SCREENSHOT_TAKEN)
        self.mock_rpa.take_totals_screenshot.assert_called_once_with("test_file.json")
    
    def test_handle_moving_json_success(self):
        """Verifica el manejo exitoso de movimiento de JSON"""
        self.mock_rpa.move_json_to_processed.return_value = True
        self.mock_rpa.validate_files_for_makecom.return_value = {"ready_for_makecom": True}
        
        result = self.state_handlers.handle_moving_json(self.context)
        
        self.assertEqual(result, RPAEvent.JSON_MOVED)
        self.mock_rpa.move_json_to_processed.assert_called_once_with("test_file.json")
        self.mock_rpa.validate_files_for_makecom.assert_called_once_with("test_file.json")
    
    def test_handle_moving_json_validation_failed(self):
        """Verifica el manejo de validación fallida en movimiento de JSON"""
        self.mock_rpa.move_json_to_processed.return_value = True
        self.mock_rpa.validate_files_for_makecom.return_value = {"ready_for_makecom": False}
        
        result = self.state_handlers.handle_moving_json(self.context)
        
        self.assertEqual(result, RPAEvent.JSON_FAILED)
    
    def test_exception_handling(self):
        """Verifica que las excepciones se manejen correctamente"""
        self.mock_rpa.get_remote_desktop.side_effect = Exception("Test error")
        
        result = self.state_handlers.handle_connecting_remote_desktop(self.context)
        
        self.assertEqual(result, RPAEvent.REMOTE_DESKTOP_FAILED)


class TestStateIntegration(unittest.TestCase):
    """Tests de integración para la máquina de estados completa"""
    
    def setUp(self):
        """Configuración inicial para tests de integración"""
        self.state_machine = StateMachine()
        self.mock_rpa = Mock()
        self.state_handlers = RPAStateHandlers(self.mock_rpa)
        
        # Configurar todos los métodos mock para retornar éxito
        self.mock_rpa.get_remote_desktop.return_value = True
        self.mock_rpa.open_sap.return_value = True
        self.mock_rpa.open_sap_orden_de_ventas.return_value = True
        self.mock_rpa.scroll_to_bottom.return_value = True
        self.mock_rpa.take_totals_screenshot.return_value = True
        self.mock_rpa.move_json_to_processed.return_value = True
        self.mock_rpa.validate_files_for_makecom.return_value = {"ready_for_makecom": True}
        
        # Registrar handlers
        for state in RPAState:
            if hasattr(self.state_handlers, f'handle_{state.value}'):
                handler_method = getattr(self.state_handlers, f'handle_{state.value}')
                self.state_machine.register_state_handler(state, handler_method)
    
    @patch('rpa.rpa_state_handlers.rpa_logger')
    def test_complete_workflow_simulation(self, mock_logger):
        """Simula un flujo de trabajo completo"""
        test_data = {
            "comprador": {"nit": "12345"},
            "orden_compra": "OC-123",
            "fecha_entrega": "2024-12-31",
            "items": [{"codigo": "ITEM1", "cantidad": 10}]
        }
        
        # Iniciar procesamiento
        success = self.state_machine.start_processing("test.json", test_data)
        self.assertTrue(success)
        
        # Simular ejecución completa
        max_iterations = 20
        iteration = 0
        
        while (self.state_machine.get_current_state() not in [RPAState.COMPLETED, RPAState.IDLE] 
               and iteration < max_iterations):
            iteration += 1
            current_state = self.state_machine.get_current_state()
            
            # Ejecutar estado actual
            next_event = self.state_machine.execute_current_state()
            
            if next_event is None:
                break
            
            # Ejecutar transición
            self.state_machine.trigger_event(next_event)
        
        # Verificar que llegamos al estado completado
        self.assertEqual(self.state_machine.get_current_state(), RPAState.COMPLETED)
        self.assertLess(iteration, max_iterations, "El workflow no completó en tiempo razonable")
        
        # Verificar que se llamaron los métodos correctos
        self.mock_rpa.get_remote_desktop.assert_called()
        self.mock_rpa.open_sap.assert_called()
        self.mock_rpa.open_sap_orden_de_ventas.assert_called()
        self.mock_rpa.load_nit.assert_called_with("12345")
        self.mock_rpa.load_orden_compra.assert_called_with("OC-123")
        self.mock_rpa.load_fecha_entrega.assert_called_with("2024-12-31")
        self.mock_rpa.load_items.assert_called_with([{"codigo": "ITEM1", "cantidad": 10}])


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Ejecutar tests
    unittest.main(verbosity=2)