"""
Tests para validación de datos JSON - FASE 1
Tests de validación de entrada (Fácil + Alto impacto)
"""

import unittest
import json
import tempfile
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class DataValidator:
    """Clase helper para validar datos JSON del RPA"""
    
    @staticmethod
    def validate_json_structure(data):
        """Valida que el JSON tenga la estructura esperada"""
        required_keys = ['comprador', 'orden_compra', 'fecha_entrega', 'items']
        
        for key in required_keys:
            if key not in data:
                return False, f"Clave requerida faltante: {key}"
        
        # Validar estructura del comprador
        if 'nit' not in data['comprador']:
            return False, "NIT faltante en comprador"
        
        # Validar que items sea una lista
        if not isinstance(data['items'], list):
            return False, "Items debe ser una lista"
        
        # Validar cada item
        for i, item in enumerate(data['items']):
            if 'codigo' not in item or 'cantidad' not in item:
                return False, f"Item {i} faltante codigo o cantidad"
        
        return True, "Estructura válida"
    
    @staticmethod
    def validate_nit(nit):
        """Valida formato del NIT"""
        if not nit:
            return False, "NIT vacío"
        
        nit_str = str(nit).strip()
        
        if not nit_str:
            return False, "NIT vacío después de limpiar"
        
        if not nit_str.isdigit():
            return False, "NIT debe contener solo números"
        
        if len(nit_str) < 8 or len(nit_str) > 12:
            return False, "NIT debe tener entre 8 y 12 dígitos"
        
        return True, "NIT válido"
    
    @staticmethod
    def validate_fecha(fecha):
        """Valida formato de fecha DD/MM/YYYY"""
        if not fecha:
            return False, "Fecha vacía"
        
        try:
            # Verificar formato DD/MM/YYYY
            parts = fecha.split('/')
            if len(parts) != 3:
                return False, "Formato debe ser DD/MM/YYYY"
            
            day, month, year = parts
            
            # Validar rangos
            if not (1 <= int(day) <= 31):
                return False, "Día debe estar entre 1 y 31"
            
            if not (1 <= int(month) <= 12):
                return False, "Mes debe estar entre 1 y 12"
            
            if not (2020 <= int(year) <= 2030):
                return False, "Año debe estar entre 2020 y 2030"
            
            return True, "Fecha válida"
            
        except ValueError:
            return False, "Fecha contiene valores no numéricos"
    
    @staticmethod
    def validate_orden_compra(orden):
        """Valida formato de orden de compra"""
        if not orden:
            return False, "Orden de compra vacía"
        
        orden_str = str(orden).strip()
        
        if not orden_str:
            return False, "Orden de compra vacía después de limpiar"
        
        if len(orden_str) < 3:
            return False, "Orden de compra muy corta"
        
        if len(orden_str) > 50:
            return False, "Orden de compra muy larga"
        
        return True, "Orden de compra válida"
    
    @staticmethod
    def validate_item_codigo(codigo):
        """Valida código de artículo"""
        if not codigo:
            return False, "Código de artículo vacío"
        
        codigo_str = str(codigo).strip()
        
        if not codigo_str:
            return False, "Código vacío después de limpiar"
        
        if len(codigo_str) < 2:
            return False, "Código muy corto"
        
        if len(codigo_str) > 30:
            return False, "Código muy largo"
        
        return True, "Código válido"
    
    @staticmethod
    def validate_item_cantidad(cantidad):
        """Valida cantidad de artículo"""
        if not cantidad:
            return False, "Cantidad vacía"
        
        try:
            cantidad_num = float(cantidad)
            
            if cantidad_num <= 0:
                return False, "Cantidad debe ser mayor a 0"
            
            if cantidad_num > 10000:
                return False, "Cantidad demasiado grande"
            
            return True, "Cantidad válida"
            
        except (ValueError, TypeError):
            return False, "Cantidad debe ser un número"


class TestDataValidation(unittest.TestCase):
    """Tests para validación de datos JSON"""
    
    def setUp(self):
        """Setup para cada test"""
        self.valid_json = {
            "comprador": {
                "nit": "900123456"
            },
            "orden_compra": "OC-2024-001",
            "fecha_entrega": "31/12/2024",
            "items": [
                {
                    "codigo": "PROD001",
                    "cantidad": "10"
                },
                {
                    "codigo": "PROD002",
                    "cantidad": "5"
                }
            ]
        }
    
    def test_valid_json_structure(self):
        """Test: JSON con estructura válida"""
        is_valid, message = DataValidator.validate_json_structure(self.valid_json)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Estructura válida")
    
    def test_missing_required_keys(self):
        """Test: JSON con claves requeridas faltantes"""
        invalid_json = {"comprador": {"nit": "123"}}
        
        is_valid, message = DataValidator.validate_json_structure(invalid_json)
        self.assertFalse(is_valid)
        self.assertIn("orden_compra", message)
    
    def test_missing_nit_in_comprador(self):
        """Test: JSON sin NIT en comprador"""
        invalid_json = self.valid_json.copy()
        invalid_json["comprador"] = {}
        
        is_valid, message = DataValidator.validate_json_structure(invalid_json)
        self.assertFalse(is_valid)
        self.assertIn("NIT faltante", message)
    
    def test_items_not_list(self):
        """Test: Items no es una lista"""
        invalid_json = self.valid_json.copy()
        invalid_json["items"] = "not a list"
        
        is_valid, message = DataValidator.validate_json_structure(invalid_json)
        self.assertFalse(is_valid)
        self.assertIn("debe ser una lista", message)
    
    def test_item_missing_fields(self):
        """Test: Item sin campos requeridos"""
        invalid_json = self.valid_json.copy()
        invalid_json["items"] = [{"codigo": "PROD001"}]  # Falta cantidad
        
        is_valid, message = DataValidator.validate_json_structure(invalid_json)
        self.assertFalse(is_valid)
        self.assertIn("faltante codigo o cantidad", message)


class TestNITValidation(unittest.TestCase):
    """Tests específicos para validación de NIT"""
    
    def test_valid_nit(self):
        """Test: NITs válidos"""
        valid_nits = ["900123456", "12345678901", "987654321"]
        
        for nit in valid_nits:
            is_valid, message = DataValidator.validate_nit(nit)
            self.assertTrue(is_valid, f"NIT {nit} debería ser válido")
    
    def test_empty_nit(self):
        """Test: NIT vacío"""
        invalid_nits = [None, "", "   ", 0]
        
        for nit in invalid_nits:
            is_valid, message = DataValidator.validate_nit(nit)
            self.assertFalse(is_valid, f"NIT {nit} debería ser inválido")
            self.assertIn("vacío", message)
    
    def test_non_numeric_nit(self):
        """Test: NIT con caracteres no numéricos"""
        invalid_nits = ["ABC123456", "900-123-456", "900.123.456", "900 123 456"]
        
        for nit in invalid_nits:
            is_valid, message = DataValidator.validate_nit(nit)
            self.assertFalse(is_valid, f"NIT {nit} debería ser inválido")
            self.assertIn("solo números", message)
    
    def test_nit_length(self):
        """Test: Longitud de NIT"""
        # Muy corto
        is_valid, message = DataValidator.validate_nit("1234567")
        self.assertFalse(is_valid)
        self.assertIn("entre 8 y 12", message)
        
        # Muy largo
        is_valid, message = DataValidator.validate_nit("1234567890123")
        self.assertFalse(is_valid)
        self.assertIn("entre 8 y 12", message)


class TestFechaValidation(unittest.TestCase):
    """Tests para validación de fechas"""
    
    def test_valid_fecha(self):
        """Test: Fechas válidas"""
        valid_fechas = ["31/12/2024", "01/01/2025", "15/06/2023"]
        
        for fecha in valid_fechas:
            is_valid, message = DataValidator.validate_fecha(fecha)
            self.assertTrue(is_valid, f"Fecha {fecha} debería ser válida")
    
    def test_invalid_fecha_format(self):
        """Test: Formato de fecha inválido"""
        invalid_fechas = ["2024-12-31", "31-12-2024", "31/12", "31/12/24"]
        
        for fecha in invalid_fechas:
            is_valid, message = DataValidator.validate_fecha(fecha)
            self.assertFalse(is_valid, f"Fecha {fecha} debería ser inválida")
    
    def test_invalid_fecha_ranges(self):
        """Test: Rangos de fecha inválidos"""
        invalid_fechas = ["32/12/2024", "31/13/2024", "31/12/2019", "31/12/2031"]
        
        for fecha in invalid_fechas:
            is_valid, message = DataValidator.validate_fecha(fecha)
            self.assertFalse(is_valid, f"Fecha {fecha} debería ser inválida")


class TestItemValidation(unittest.TestCase):
    """Tests para validación de items"""
    
    def test_valid_codigo(self):
        """Test: Códigos válidos"""
        valid_codigos = ["PROD001", "ABC-123", "ITEM_X1"]
        
        for codigo in valid_codigos:
            is_valid, message = DataValidator.validate_item_codigo(codigo)
            self.assertTrue(is_valid, f"Código {codigo} debería ser válido")
    
    def test_invalid_codigo(self):
        """Test: Códigos inválidos"""
        invalid_codigos = [None, "", "   ", "A", "A" * 31]
        
        for codigo in invalid_codigos:
            is_valid, message = DataValidator.validate_item_codigo(codigo)
            self.assertFalse(is_valid, f"Código {codigo} debería ser inválido")
    
    def test_valid_cantidad(self):
        """Test: Cantidades válidas"""
        valid_cantidades = ["1", "10.5", "100", "999.99"]
        
        for cantidad in valid_cantidades:
            is_valid, message = DataValidator.validate_item_cantidad(cantidad)
            self.assertTrue(is_valid, f"Cantidad {cantidad} debería ser válida")
    
    def test_invalid_cantidad(self):
        """Test: Cantidades inválidas"""
        invalid_cantidades = [None, "", "0", "-5", "ABC", "10001"]
        
        for cantidad in invalid_cantidades:
            is_valid, message = DataValidator.validate_item_cantidad(cantidad)
            self.assertFalse(is_valid, f"Cantidad {cantidad} debería ser inválida")


if __name__ == '__main__':
    unittest.main()