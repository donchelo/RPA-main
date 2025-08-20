#!/usr/bin/env python3
"""
Script de análisis automatizado de dependencias para RPA TAMAPRINT
Fase 0: Preparación y Análisis
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter

class DependencyAnalyzer:
    """Analizador de dependencias para el proyecto RPA"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.python_files = []
        self.dependencies = defaultdict(set)
        self.reverse_dependencies = defaultdict(set)
        self.file_sizes = {}
        self.import_patterns = []
        
    def scan_python_files(self) -> List[Path]:
        """Escanea todos los archivos Python en el proyecto"""
        print("🔍 Escaneando archivos Python...")
        
        for root, dirs, files in os.walk(self.project_root):
            # Excluir directorios comunes
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    self.python_files.append(file_path)
                    self.file_sizes[str(file_path)] = file_path.stat().st_size
        
        print(f"✅ Encontrados {len(self.python_files)} archivos Python")
        return self.python_files
    
    def extract_imports(self, file_path: Path) -> Set[str]:
        """Extrae todas las importaciones de un archivo Python"""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear el AST para extraer imports
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        if module:
                            imports.add(f"{module}.{alias.name}")
                        else:
                            imports.add(alias.name)
                            
        except Exception as e:
            print(f"⚠️ Error analizando {file_path}: {e}")
        
        return imports
    
    def analyze_dependencies(self):
        """Analiza todas las dependencias del proyecto"""
        print("🔗 Analizando dependencias...")
        
        for file_path in self.python_files:
            relative_path = file_path.relative_to(self.project_root)
            module_name = str(relative_path).replace(os.sep, '.').replace('.py', '')
            
            imports = self.extract_imports(file_path)
            
            # Filtrar imports internos del proyecto
            internal_imports = set()
            for imp in imports:
                if imp.startswith('rpa.') or imp.startswith('tests.'):
                    internal_imports.add(imp)
            
            self.dependencies[module_name] = internal_imports
            
            # Construir dependencias inversas
            for dep in internal_imports:
                self.reverse_dependencies[dep].add(module_name)
        
        print(f"✅ Analizadas dependencias de {len(self.dependencies)} módulos")
    
    def find_circular_dependencies(self) -> List[List[str]]:
        """Encuentra dependencias circulares usando DFS"""
        print("🔄 Buscando dependencias circulares...")
        
        def dfs(node, visited, rec_stack, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.dependencies.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, visited, rec_stack, path):
                        return True
                elif neighbor in rec_stack:
                    # Encontrada dependencia circular
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:]
            
            rec_stack.remove(node)
            path.pop()
            return False
        
        visited = set()
        cycles = []
        
        for node in self.dependencies:
            if node not in visited:
                path = []
                cycle = dfs(node, visited, set(), path)
                if cycle:
                    cycles.append(cycle)
        
        if cycles:
            print(f"⚠️ Encontradas {len(cycles)} dependencias circulares")
            for cycle in cycles:
                print(f"   🔄 {' -> '.join(cycle)} -> {cycle[0]}")
        else:
            print("✅ No se encontraron dependencias circulares")
        
        return cycles
    
    def identify_redundancies(self) -> Dict[str, List[str]]:
        """Identifica archivos redundantes basándose en funcionalidad similar"""
        print("🔍 Identificando redundancias...")
        
        redundancies = {
            'logging_systems': [],
            'rpa_implementations': [],
            'google_drive_uploaders': [],
            'test_files': [],
            'debug_files': []
        }
        
        # Buscar sistemas de logging
        for file_path in self.python_files:
            file_name = file_path.name
            if 'logger' in file_name.lower():
                redundancies['logging_systems'].append(str(file_path))
        
        # Buscar implementaciones RPA
        for file_path in self.python_files:
            file_name = file_path.name
            if 'main' in file_name.lower() and 'rpa' in str(file_path):
                redundancies['rpa_implementations'].append(str(file_path))
        
        # Buscar uploaders de Google Drive
        for file_path in self.python_files:
            file_name = file_path.name
            if 'google' in file_name.lower() and 'drive' in file_name.lower():
                redundancies['google_drive_uploaders'].append(str(file_path))
        
        # Buscar archivos de test
        for file_path in self.python_files:
            file_name = file_path.name
            if file_name.startswith('test_'):
                redundancies['test_files'].append(str(file_path))
        
        # Buscar archivos de debug
        for file_path in self.python_files:
            file_name = file_path.name
            if file_name.startswith('debug_'):
                redundancies['debug_files'].append(str(file_path))
        
        # Mostrar resultados
        for category, files in redundancies.items():
            if files:
                print(f"   📁 {category}: {len(files)} archivos")
                for file in files:
                    print(f"      - {file}")
        
        return redundancies
    
    def calculate_metrics(self) -> Dict:
        """Calcula métricas del proyecto"""
        print("📊 Calculando métricas...")
        
        metrics = {
            'total_files': len(self.python_files),
            'total_lines': 0,
            'total_size': sum(self.file_sizes.values()),
            'avg_file_size': 0,
            'largest_files': [],
            'most_dependent_modules': [],
            'least_dependent_modules': []
        }
        
        # Contar líneas
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    metrics['total_lines'] += lines
            except:
                pass
        
        # Calcular promedio
        if self.python_files:
            metrics['avg_file_size'] = metrics['total_size'] / len(self.python_files)
        
        # Archivos más grandes
        sorted_files = sorted(self.file_sizes.items(), key=lambda x: x[1], reverse=True)
        metrics['largest_files'] = sorted_files[:10]
        
        # Módulos con más dependencias
        sorted_deps = sorted(self.dependencies.items(), key=lambda x: len(x[1]), reverse=True)
        metrics['most_dependent_modules'] = sorted_deps[:10]
        
        # Módulos con menos dependencias
        metrics['least_dependent_modules'] = sorted_deps[-10:]
        
        return metrics
    
    def generate_report(self) -> Dict:
        """Genera reporte completo de análisis"""
        print("📋 Generando reporte...")
        
        report = {
            'project_info': {
                'name': 'RPA TAMAPRINT',
                'analysis_date': str(Path().cwd()),
                'total_python_files': len(self.python_files)
            },
            'dependencies': dict(self.dependencies),
            'reverse_dependencies': dict(self.reverse_dependencies),
            'circular_dependencies': self.find_circular_dependencies(),
            'redundancies': self.identify_redundancies(),
            'metrics': self.calculate_metrics(),
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Análisis de redundancias
        redundancies = self.identify_redundancies()
        
        if len(redundancies['logging_systems']) > 1:
            recommendations.append("CRÍTICO: Consolidar sistemas de logging - mantener solo uno")
        
        if len(redundancies['rpa_implementations']) > 1:
            recommendations.append("ALTO: Consolidar implementaciones RPA - mantener la más robusta")
        
        if len(redundancies['google_drive_uploaders']) > 1:
            recommendations.append("MEDIO: Consolidar uploaders de Google Drive")
        
        if len(redundancies['test_files']) > 20:
            recommendations.append("BAJO: Consolidar archivos de test en carpeta tests/")
        
        if len(redundancies['debug_files']) > 5:
            recommendations.append("BAJO: Mover archivos de debug a carpeta scripts/debug/")
        
        # Análisis de dependencias
        high_dependency_modules = [mod for mod, deps in self.dependencies.items() if len(deps) > 5]
        if high_dependency_modules:
            recommendations.append(f"MEDIO: Reducir acoplamiento de módulos: {', '.join(high_dependency_modules[:3])}")
        
        # Análisis de tamaño
        large_files = [f for f, s in self.file_sizes.items() if s > 50000]  # >50KB
        if large_files:
            recommendations.append(f"BAJO: Considerar dividir archivos grandes: {', '.join(large_files[:3])}")
        
        return recommendations
    
    def save_report(self, report: Dict, output_file: str = "dependency_analysis_report.json"):
        """Guarda el reporte en formato JSON"""
        output_path = self.project_root / output_file
        
        # Convertir sets a listas para serialización JSON
        serializable_report = {}
        for key, value in report.items():
            if isinstance(value, dict):
                serializable_report[key] = {}
                for k, v in value.items():
                    if isinstance(v, set):
                        serializable_report[key][k] = list(v)
                    else:
                        serializable_report[key][k] = v
            elif isinstance(value, set):
                serializable_report[key] = list(value)
            else:
                serializable_report[key] = value
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Reporte guardado en: {output_path}")
    
    def print_summary(self, report: Dict):
        """Imprime resumen del análisis"""
        print("\n" + "="*60)
        print("📊 RESUMEN DEL ANÁLISIS DE DEPENDENCIAS")
        print("="*60)
        
        metrics = report['metrics']
        print(f"📁 Archivos Python: {metrics['total_files']}")
        print(f"📏 Líneas totales: {metrics['total_lines']:,}")
        print(f"💾 Tamaño total: {metrics['total_size'] / 1024:.1f} KB")
        print(f"📊 Tamaño promedio: {metrics['avg_file_size'] / 1024:.1f} KB")
        
        print(f"\n🔄 Dependencias circulares: {len(report['circular_dependencies'])}")
        
        redundancies = report['redundancies']
        total_redundancies = sum(len(files) for files in redundancies.values())
        print(f"🔍 Archivos redundantes identificados: {total_redundancies}")
        
        print(f"\n💡 Recomendaciones generadas: {len(report['recommendations'])}")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "="*60)

def main():
    """Función principal del script"""
    print("🚀 INICIANDO ANÁLISIS DE DEPENDENCIAS - RPA TAMAPRINT")
    print("="*60)
    
    analyzer = DependencyAnalyzer()
    
    # Ejecutar análisis completo
    analyzer.scan_python_files()
    analyzer.analyze_dependencies()
    
    # Generar reporte
    report = analyzer.generate_report()
    
    # Guardar y mostrar resultados
    analyzer.save_report(report)
    analyzer.print_summary(report)
    
    print("\n✅ Análisis completado exitosamente!")
    print("📋 Revisa el archivo 'dependency_analysis_report.json' para detalles completos")

if __name__ == "__main__":
    main()
