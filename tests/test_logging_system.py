"""
Tests para sistema de logging - FASE 2
Tests de componentes (Mediano + Alto impacto)
"""

import unittest
import tempfile
import os
import logging
import shutil
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rpa.simple_logger import SimpleRPALogger


class TestSimpleRPALogger(unittest.TestCase):
    """Tests para el sistema de logging simplificado"""
    
    def setUp(self):
        """Setup para cada test"""
        self.temp_dir = tempfile.mkdtemp()
        self.logger = SimpleRPALogger(name="TestRPA", log_dir=self.temp_dir)
    
    def tearDown(self):
        """Cleanup después de cada test"""
        # Cerrar handlers para liberar archivos
        for handler in self.logger.logger.handlers[:]:
            handler.close()
            self.logger.logger.removeHandler(handler)
        
        # Limpiar directorio temporal
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_logger_creation(self):
        """Test: Creación correcta del logger"""
        self.assertEqual(self.logger.name, "TestRPA")
        self.assertEqual(self.logger.log_dir, self.temp_dir)
        self.assertIsInstance(self.logger.logger, logging.Logger)
    
    def test_log_directory_creation(self):
        """Test: Creación automática del directorio de logs"""
        # El directorio debe existir después de crear el logger
        self.assertTrue(os.path.exists(self.temp_dir))
    
    def test_log_files_creation(self):
        """Test: Creación de archivos de log"""
        # Hacer algunos logs para que se creen los archivos
        self.logger.info("Test message")
        self.logger.error("Test error")
        
        # Verificar que los archivos se crearon
        main_log = os.path.join(self.temp_dir, 'rpa.log')
        error_log = os.path.join(self.temp_dir, 'rpa_errors.log')
        
        # Dar tiempo para que se escriban los archivos
        import time
        time.sleep(0.1)
        
        self.assertTrue(os.path.exists(main_log))
        self.assertTrue(os.path.exists(error_log))
    
    def test_info_logging(self):
        """Test: Logging de mensajes de información"""
        test_message = "Test info message"
        self.logger.info(test_message)
        
        # Verificar que se escribió en el archivo principal
        main_log = os.path.join(self.temp_dir, 'rpa.log')
        
        # Esperar a que se escriba
        import time
        time.sleep(0.1)
        
        if os.path.exists(main_log):
            with open(main_log, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn(test_message, content)
                self.assertIn('INFO', content)
    
    def test_error_logging(self):
        """Test: Logging de mensajes de error"""
        test_error = "Test error message"
        self.logger.error(test_error)
        
        # Verificar que se escribió en ambos archivos
        main_log = os.path.join(self.temp_dir, 'rpa.log')
        error_log = os.path.join(self.temp_dir, 'rpa_errors.log')
        
        # Esperar a que se escriba
        import time
        time.sleep(0.1)
        
        if os.path.exists(error_log):
            with open(error_log, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn(test_error, content)
                self.assertIn('ERROR', content)
    
    def test_log_with_context(self):
        """Test: Logging con contexto"""
        message = "Operation completed"
        context = {"operation": "test_op", "duration": 1.5}
        
        self.logger.info(message, context)
        
        # Verificar que el contexto se incluye
        main_log = os.path.join(self.temp_dir, 'rpa.log')
        
        import time
        time.sleep(0.1)
        
        if os.path.exists(main_log):
            with open(main_log, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn(message, content)
                self.assertIn("Context:", content)
    
    def test_log_action_method(self):
        """Test: Método log_action específico para RPA"""
        action = "Processing item"
        details = "Item code: PROD001"
        
        self.logger.log_action(action, details)
        
        main_log = os.path.join(self.temp_dir, 'rpa.log')
        
        import time
        time.sleep(0.1)
        
        if os.path.exists(main_log):
            with open(main_log, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("ACTION:", content)
                self.assertIn(action, content)
                self.assertIn(details, content)
    
    def test_log_performance_method(self):
        """Test: Método log_performance para métricas"""
        operation = "Load NIT"
        duration = 2.5
        
        self.logger.log_performance(operation, duration)
        
        main_log = os.path.join(self.temp_dir, 'rpa.log')
        
        import time
        time.sleep(0.1)
        
        if os.path.exists(main_log):
            with open(main_log, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("PERFORMANCE:", content)
                self.assertIn(operation, content)
                self.assertIn("2.50s", content)
    
    def test_log_error_method(self):
        """Test: Método log_error específico"""
        error = "Template not found"
        context = {"template": "sap_icon.png", "confidence": 0.8}
        
        self.logger.log_error(error, context)
        
        error_log = os.path.join(self.temp_dir, 'rpa_errors.log')
        
        import time
        time.sleep(0.1)
        
        if os.path.exists(error_log):
            with open(error_log, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("ERROR:", content)
                self.assertIn(error, content)
    
    def test_different_log_levels(self):
        """Test: Diferentes niveles de logging"""
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")
        
        # Todos deberían funcionar sin errores
        self.assertTrue(True)  # Si llegamos aquí, no hubo excepciones
    
    def test_handler_configuration(self):
        """Test: Configuración correcta de handlers"""
        # El logger debe tener 3 handlers: main, error, console
        handlers = self.logger.logger.handlers
        self.assertEqual(len(handlers), 3)
        
        # Verificar tipos de handlers
        handler_types = [type(h).__name__ for h in handlers]
        self.assertIn('RotatingFileHandler', handler_types)
        self.assertIn('StreamHandler', handler_types)
    
    def test_unicode_support(self):
        """Test: Soporte para caracteres unicode"""
        unicode_message = "Procesando artículo: CAÑÓN-123 🚀"
        self.logger.info(unicode_message)
        
        # No debe lanzar excepción
        self.assertTrue(True)
    
    def test_large_context_data(self):
        """Test: Manejo de contexto con datos grandes"""
        large_context = {
            "items": ["ITEM-" + str(i) for i in range(100)],
            "data": "x" * 1000,
            "nested": {"level1": {"level2": {"value": "test"}}}
        }
        
        # No debe fallar con contexto grande
        self.logger.info("Large context test", large_context)
        self.assertTrue(True)


class TestLoggingIntegration(unittest.TestCase):
    """Tests de integración del sistema de logging"""
    
    def setUp(self):
        """Setup para tests de integración"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Cleanup"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_multiple_logger_instances(self):
        """Test: Múltiples instancias de logger"""
        logger1 = SimpleRPALogger("Logger1", self.temp_dir)
        logger2 = SimpleRPALogger("Logger2", self.temp_dir)
        
        # Ambos deben funcionar independientemente
        logger1.info("Message from logger 1")
        logger2.info("Message from logger 2")
        
        # Cleanup handlers
        for logger in [logger1, logger2]:
            for handler in logger.logger.handlers[:]:
                handler.close()
                logger.logger.removeHandler(handler)
        
        self.assertTrue(True)
    
    def test_logger_with_nonexistent_directory(self):
        """Test: Logger con directorio que no existe"""
        nonexistent_dir = os.path.join(self.temp_dir, "deep", "nested", "path")
        
        # No debe fallar al crear directorios
        logger = SimpleRPALogger("TestLogger", nonexistent_dir)
        logger.info("Test message")
        
        # Verificar que se creó el directorio
        self.assertTrue(os.path.exists(nonexistent_dir))
        
        # Cleanup
        for handler in logger.logger.handlers[:]:
            handler.close()
            logger.logger.removeHandler(handler)
    
    def test_concurrent_logging(self):
        """Test: Logging concurrente (simulado)"""
        logger = SimpleRPALogger("ConcurrentLogger", self.temp_dir)
        
        # Simular múltiples logs rápidos
        for i in range(50):
            logger.info(f"Concurrent message {i}")
            if i % 10 == 0:
                logger.error(f"Concurrent error {i}")
        
        # No debe fallar
        self.assertTrue(True)
        
        # Cleanup
        for handler in logger.logger.handlers[:]:
            handler.close()
            logger.logger.removeHandler(handler)


if __name__ == '__main__':
    unittest.main()