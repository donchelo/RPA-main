#!/usr/bin/env python3
"""
Script de análisis simplificado para RPA TAMAPRINT
Fase 0: Preparación y Análisis
"""

import os
import json
from pathlib import Path
from collections import defaultdict

def scan_python_files(project_root="."):
    """Escanea todos los archivos Python en el proyecto"""
    print("🔍 Escaneando archivos Python...")
    
    python_files = []
    file_sizes = {}
    
    for root, dirs, files in os.walk(project_root):
        # Excluir directorios comunes
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}]
        
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                python_files.append(str(file_path))
                file_sizes[str(file_path)] = file_path.stat().st_size
    
    print(f"✅ Encontrados {len(python_files)} archivos Python")
    return python_files, file_sizes

def identify_redundancies(python_files):
    """Identifica archivos redundantes"""
    print("🔍 Identificando redundancias...")
    
    redundancies = {
        'logging_systems': [],
        'rpa_implementations': [],
        'google_drive_uploaders': [],
        'test_files': [],
        'debug_files': []
    }
    
    for file_path in python_files:
        file_name = Path(file_path).name.lower()
        file_str = str(file_path).lower()
        
        # Sistemas de logging
        if 'logger' in file_name:
            redundancies['logging_systems'].append(file_path)
        
        # Implementaciones RPA
        if 'main' in file_name and 'rpa' in file_str:
            redundancies['rpa_implementations'].append(file_path)
        
        # Uploaders de Google Drive
        if 'google' in file_name and 'drive' in file_name:
            redundancies['google_drive_uploaders'].append(file_path)
        
        # Archivos de test
        if file_name.startswith('test_'):
            redundancies['test_files'].append(file_path)
        
        # Archivos de debug
        if file_name.startswith('debug_'):
            redundancies['debug_files'].append(file_path)
    
    return redundancies

def calculate_metrics(python_files, file_sizes):
    """Calcula métricas del proyecto"""
    print("📊 Calculando métricas...")
    
    total_lines = 0
    largest_files = []
    
    # Contar líneas y encontrar archivos más grandes
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
        except:
            pass
    
    # Archivos más grandes
    sorted_files = sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)
    largest_files = sorted_files[:10]
    
    metrics = {
        'total_files': len(python_files),
        'total_lines': total_lines,
        'total_size_kb': sum(file_sizes.values()) / 1024,
        'avg_file_size_kb': sum(file_sizes.values()) / len(python_files) / 1024 if python_files else 0,
        'largest_files': largest_files
    }
    
    return metrics

def generate_recommendations(redundancies):
    """Genera recomendaciones basadas en el análisis"""
    recommendations = []
    
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
    
    return recommendations

def print_summary(metrics, redundancies, recommendations):
    """Imprime resumen del análisis"""
    print("\n" + "="*60)
    print("📊 RESUMEN DEL ANÁLISIS DE DEPENDENCIAS")
    print("="*60)
    
    print(f"📁 Archivos Python: {metrics['total_files']}")
    print(f"📏 Líneas totales: {metrics['total_lines']:,}")
    print(f"💾 Tamaño total: {metrics['total_size_kb']:.1f} KB")
    print(f"📊 Tamaño promedio: {metrics['avg_file_size_kb']:.1f} KB")
    
    print(f"\n🔍 Archivos redundantes identificados:")
    total_redundancies = sum(len(files) for files in redundancies.values())
    print(f"   Total: {total_redundancies}")
    
    for category, files in redundancies.items():
        if files:
            print(f"   📁 {category}: {len(files)} archivos")
            for file in files[:3]:  # Mostrar solo los primeros 3
                print(f"      - {file}")
            if len(files) > 3:
                print(f"      ... y {len(files) - 3} más")
    
    print(f"\n💡 Recomendaciones generadas: {len(recommendations)}")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print("\n📋 Archivos más grandes:")
    for i, (file_path, size) in enumerate(metrics['largest_files'][:5], 1):
        size_kb = size / 1024
        print(f"   {i}. {file_path} ({size_kb:.1f} KB)")
    
    print("\n" + "="*60)

def save_report(report, output_file="dependency_analysis_report.json"):
    """Guarda el reporte en formato JSON"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Reporte guardado en: {output_file}")

def main():
    """Función principal del script"""
    print("🚀 INICIANDO ANÁLISIS DE DEPENDENCIAS - RPA TAMAPRINT")
    print("="*60)
    
    # Escanear archivos
    python_files, file_sizes = scan_python_files()
    
    # Identificar redundancias
    redundancies = identify_redundancies(python_files)
    
    # Calcular métricas
    metrics = calculate_metrics(python_files, file_sizes)
    
    # Generar recomendaciones
    recommendations = generate_recommendations(redundancies)
    
    # Crear reporte
    report = {
        'project_info': {
            'name': 'RPA TAMAPRINT',
            'analysis_date': str(Path().cwd()),
            'total_python_files': len(python_files)
        },
        'metrics': metrics,
        'redundancies': redundancies,
        'recommendations': recommendations
    }
    
    # Guardar y mostrar resultados
    save_report(report)
    print_summary(metrics, redundancies, recommendations)
    
    print("\n✅ Análisis completado exitosamente!")
    print("📋 Revisa el archivo 'dependency_analysis_report.json' para detalles completos")

if __name__ == "__main__":
    main()
