"""
Gestor de configuración que carga settings desde config.yaml
Permite modificar comportamientos sin cambiar código
"""

import yaml
import os
from typing import Any, Dict, Optional


class ConfigManager:
    """Maneja la carga y acceso a configuraciones desde archivo YAML"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo YAML"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                print(f"⚠️  Archivo de configuración no encontrado: {self.config_file}")
                return self._get_default_config()
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Configuración por defecto si no se puede cargar el archivo"""
        return {
            'delays': {
                'short': 0.5,
                'medium': 1.0,
                'long': 2.0,
                'after_input': 1.0,
                'sap_startup': 30.0
            },
            'template_matching': {
                'default_confidence': 0.8,
                'timeout': 10.0
            },
            'retries': {
                'max_sap_open_attempts': 3,
                'retry_delay': 5
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración usando notación de puntos
        Ejemplo: get('delays.short') obtiene config['delays']['short']
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise KeyError(f"Configuración no encontrada: {key_path}")
    
    def get_delays(self) -> Dict[str, float]:
        """Obtiene todas las configuraciones de delays"""
        return self.get('delays', {})
    
    def get_paths(self) -> Dict[str, str]:
        """Obtiene todas las rutas de archivos"""
        return self.get('paths', {})
    
    def get_template_config(self) -> Dict[str, Any]:
        """Obtiene configuración de template matching"""
        return self.get('template_matching', {})
    
    def get_navigation_config(self) -> Dict[str, int]:
        """Obtiene configuración de navegación por teclado"""
        return self.get('navigation', {})
    
    def get_retry_config(self) -> Dict[str, int]:
        """Obtiene configuración de reintentos"""
        return self.get('retries', {})
    
    def get_window_config(self) -> Dict[str, Any]:
        """Obtiene configuración de ventanas"""
        return self.get('windows', {})
    
    def get_ocr_config(self) -> Dict[str, Any]:
        """Obtiene configuración de OCR"""
        return self.get('ocr', {})
    
    def get_system_config(self) -> Dict[str, Any]:
        """Obtiene configuración del sistema"""
        return self.get('system', {})
    
    def reload_config(self):
        """Recarga la configuración desde archivo"""
        self.config = self._load_config()
        print("✅ Configuración recargada exitosamente")
    
    def validate_config(self) -> bool:
        """Valida que las configuraciones críticas estén presentes"""
        required_keys = [
            'delays.medium',
            'delays.sap_startup', 
            'template_matching.default_confidence',
            'retries.max_sap_open_attempts'
        ]
        
        for key in required_keys:
            try:
                self.get(key)
            except KeyError:
                print(f"❌ Configuración requerida faltante: {key}")
                return False
        
        print("✅ Configuración validada correctamente")
        return True


# Instancia global del gestor de configuración
config = ConfigManager()

# Funciones de conveniencia para acceso rápido
def get_delay(delay_type: str) -> float:
    """Obtiene un delay específico"""
    return config.get(f'delays.{delay_type}', 1.0)

def get_path(path_type: str) -> str:
    """Obtiene una ruta específica"""
    return config.get(f'paths.{path_type}', './')

def get_confidence(confidence_type: str = 'default') -> float:
    """Obtiene un umbral de confianza específico"""
    return config.get(f'template_matching.{confidence_type}_confidence', 0.8)

def get_navigation_tabs(tab_type: str) -> int:
    """Obtiene cantidad de tabs para navegación"""
    return config.get(f'navigation.tabs_{tab_type}', 1)

def get_retry_attempts(retry_type: str) -> int:
    """Obtiene cantidad de reintentos"""
    return config.get(f'retries.max_{retry_type}_attempts', 3)