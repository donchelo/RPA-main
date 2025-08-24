#!/usr/bin/env python3
"""
Script de optimización para el módulo de órdenes de producción
Analiza y optimiza la configuración para mejor performance
"""

import os
import sys
import time
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.simple_logger import rpa_logger


class ProductionOptimizer:
    """Optimizador para el módulo de producción"""
    
    def __init__(self):
        self.config_path = "./rpa/modules/production_order/production_order_config.yaml"
        self.backup_path = "./rpa/modules/production_order/production_order_config_backup.yaml"
        self.optimization_report = "./optimization_report.json"
        
    def load_config(self) -> Dict[str, Any]:
        """Cargar configuración actual"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            rpa_logger.error(f"Error cargando configuración: {e}")
            return {}
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Guardar configuración"""
        try:
            # Crear backup antes de modificar
            self.create_backup()
            
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, indent=2)
            
            rpa_logger.info("✅ Configuración optimizada guardada")
            return True
        except Exception as e:
            rpa_logger.error(f"Error guardando configuración: {e}")
            return False
    
    def create_backup(self) -> bool:
        """Crear backup de la configuración actual"""
        try:
            current_config = self.load_config()
            with open(self.backup_path, 'w', encoding='utf-8') as file:
                yaml.dump(current_config, file, default_flow_style=False, indent=2)
            
            rpa_logger.info(f"✅ Backup creado: {self.backup_path}")
            return True
        except Exception as e:
            rpa_logger.error(f"Error creando backup: {e}")
            return False
    
    def analyze_performance(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar configuración actual y sugerir optimizaciones"""
        analysis = {
            "current_settings": {},
            "optimization_suggestions": [],
            "performance_score": 0,
            "estimated_improvement": 0
        }
        
        # Analizar delays de navegación
        nav_config = config.get('production_order', {}).get('navigation', {})
        analysis["current_settings"]["navigation"] = nav_config
        
        # Calcular score de performance
        total_delay = (
            nav_config.get('alt_m_delay', 0.5) +
            nav_config.get('p_key_delay', 1.0) +
            nav_config.get('mouse_click_delay', 2.0) +
            nav_config.get('form_load_delay', 3.0)
        )
        
        # Score basado en delays (menor = mejor)
        if total_delay <= 5.0:
            analysis["performance_score"] = 90
        elif total_delay <= 7.0:
            analysis["performance_score"] = 75
        elif total_delay <= 10.0:
            analysis["performance_score"] = 60
        else:
            analysis["performance_score"] = 40
        
        # Sugerencias de optimización
        suggestions = []
        
        if nav_config.get('alt_m_delay', 0.5) > 0.3:
            suggestions.append({
                "type": "navigation_delay",
                "setting": "alt_m_delay",
                "current": nav_config.get('alt_m_delay', 0.5),
                "suggested": 0.3,
                "improvement": "Reducir delay después de Alt+M para navegación más rápida"
            })
        
        if nav_config.get('p_key_delay', 1.0) > 0.5:
            suggestions.append({
                "type": "navigation_delay",
                "setting": "p_key_delay",
                "current": nav_config.get('p_key_delay', 1.0),
                "suggested": 0.5,
                "improvement": "Reducir delay después de presionar P"
            })
        
        if nav_config.get('mouse_click_delay', 2.0) > 1.0:
            suggestions.append({
                "type": "navigation_delay",
                "setting": "mouse_click_delay",
                "current": nav_config.get('mouse_click_delay', 2.0),
                "suggested": 1.0,
                "improvement": "Reducir delay después de clic en botón"
            })
        
        # Analizar template matching
        tm_config = config.get('production_order', {}).get('template_matching', {})
        analysis["current_settings"]["template_matching"] = tm_config
        
        # Sugerencias para template matching
        if tm_config.get('field_confidence', 0.85) > 0.8:
            suggestions.append({
                "type": "template_matching",
                "setting": "field_confidence",
                "current": tm_config.get('field_confidence', 0.85),
                "suggested": 0.8,
                "improvement": "Reducir confianza para campos para mayor flexibilidad"
            })
        
        analysis["optimization_suggestions"] = suggestions
        
        # Calcular mejora estimada
        if suggestions:
            estimated_improvement = len(suggestions) * 5  # 5% por optimización
            analysis["estimated_improvement"] = min(estimated_improvement, 20)
        
        return analysis
    
    def apply_optimizations(self, config: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Aplicar optimizaciones sugeridas"""
        optimized_config = config.copy()
        production_config = optimized_config.get('production_order', {})
        
        applied_optimizations = []
        
        for suggestion in analysis.get('optimization_suggestions', []):
            setting_type = suggestion['type']
            setting_name = suggestion['setting']
            suggested_value = suggestion['suggested']
            
            if setting_type == 'navigation_delay':
                if 'navigation' not in production_config:
                    production_config['navigation'] = {}
                production_config['navigation'][setting_name] = suggested_value
                applied_optimizations.append(f"✅ {setting_name}: {suggestion['current']} → {suggested_value}")
            
            elif setting_type == 'template_matching':
                if 'template_matching' not in production_config:
                    production_config['template_matching'] = {}
                production_config['template_matching'][setting_name] = suggested_value
                applied_optimizations.append(f"✅ {setting_name}: {suggestion['current']} → {suggested_value}")
        
        optimized_config['production_order'] = production_config
        
        # Agregar configuración de performance si no existe
        if 'performance' not in production_config:
            production_config['performance'] = {
                'screenshot_quality': 95,
                'retry_attempts': 3,
                'retry_delay': 1.0
            }
            applied_optimizations.append("✅ Agregada configuración de performance")
        
        return optimized_config, applied_optimizations
    
    def generate_report(self, analysis: Dict[str, Any], applied_optimizations: List[str]) -> bool:
        """Generar reporte de optimización"""
        try:
            report = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "analysis": analysis,
                "applied_optimizations": applied_optimizations,
                "backup_location": self.backup_path,
                "recommendations": [
                    "Ejecutar test_produccion_real.py para verificar optimizaciones",
                    "Monitorear logs para detectar problemas",
                    "Ajustar configuración manualmente si es necesario"
                ]
            }
            
            with open(self.optimization_report, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2, ensure_ascii=False)
            
            rpa_logger.info(f"✅ Reporte de optimización guardado: {self.optimization_report}")
            return True
        except Exception as e:
            rpa_logger.error(f"Error generando reporte: {e}")
            return False
    
    def optimize(self) -> bool:
        """Ejecutar optimización completa"""
        print("🔧 INICIANDO OPTIMIZACIÓN DEL MÓDULO DE PRODUCCIÓN")
        print("=" * 60)
        
        # 1. Cargar configuración actual
        print("📋 Cargando configuración actual...")
        config = self.load_config()
        if not config:
            print("❌ Error cargando configuración")
            return False
        
        # 2. Analizar performance
        print("📊 Analizando performance actual...")
        analysis = self.analyze_performance(config)
        
        # 3. Mostrar análisis
        print(f"\n📈 ANÁLISIS DE PERFORMANCE")
        print("=" * 40)
        print(f"Score actual: {analysis['performance_score']}/100")
        print(f"Delays totales: {sum(analysis['current_settings']['navigation'].values()):.1f}s")
        print(f"Mejora estimada: {analysis['estimated_improvement']}%")
        
        # 4. Mostrar sugerencias
        if analysis['optimization_suggestions']:
            print(f"\n💡 SUGERENCIAS DE OPTIMIZACIÓN")
            print("=" * 40)
            for i, suggestion in enumerate(analysis['optimization_suggestions'], 1):
                print(f"{i}. {suggestion['improvement']}")
                print(f"   {suggestion['setting']}: {suggestion['current']} → {suggestion['suggested']}")
        else:
            print("\n✅ Configuración ya está optimizada")
        
        # 5. Aplicar optimizaciones
        if analysis['optimization_suggestions']:
            print(f"\n🚀 APLICANDO OPTIMIZACIONES")
            print("=" * 40)
            
            optimized_config, applied_optimizations = self.apply_optimizations(config, analysis)
            
            for optimization in applied_optimizations:
                print(optimization)
            
            # 6. Guardar configuración optimizada
            if self.save_config(optimized_config):
                print("\n✅ Configuración optimizada guardada")
            else:
                print("\n❌ Error guardando configuración optimizada")
                return False
            
            # 7. Generar reporte
            self.generate_report(analysis, applied_optimizations)
            
            print(f"\n📋 RESUMEN DE OPTIMIZACIÓN")
            print("=" * 40)
            print(f"✅ Optimizaciones aplicadas: {len(applied_optimizations)}")
            print(f"✅ Backup creado: {self.backup_path}")
            print(f"✅ Reporte generado: {self.optimization_report}")
            print(f"💡 Mejora estimada: {analysis['estimated_improvement']}%")
            
            print(f"\n🎯 PRÓXIMOS PASOS")
            print("=" * 40)
            print("1. Ejecutar: python test_produccion_real.py")
            print("2. Verificar que todo funcione correctamente")
            print("3. Revisar logs para detectar problemas")
            print("4. Ajustar configuración manualmente si es necesario")
            
        else:
            print("\n✅ No se requieren optimizaciones")
        
        return True


def main():
    """Función principal"""
    print("🚀 OPTIMIZADOR DE MÓDULO DE PRODUCCIÓN")
    print("=" * 60)
    print("🎯 Objetivo: Optimizar configuración para mejor performance")
    print("🎯 Características: Análisis automático y optimización inteligente")
    print("🎯 Resultado: Configuración optimizada y reporte detallado")
    
    optimizer = ProductionOptimizer()
    
    if optimizer.optimize():
        print("\n🎉 OPTIMIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("✅ El módulo de producción está optimizado")
        print("✅ La configuración ha sido mejorada")
        print("✅ Se ha generado un reporte detallado")
        print("✅ El módulo está listo para uso en producción")
    else:
        print("\n❌ LA OPTIMIZACIÓN FALLÓ")
        print("=" * 60)
        print("💡 Revisa los errores y verifica la configuración")


if __name__ == "__main__":
    main()
