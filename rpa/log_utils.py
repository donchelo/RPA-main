"""
Utilidades para el sistema de logs RPA
"""

import os
import json
import gzip
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import sqlite3
from pathlib import Path
import argparse

from rpa.logger import rpa_logger
from rpa.log_config import get_log_config, get_health_status, calculate_disk_usage

class LogUtils:
    """Utilidades para mantenimiento y análisis de logs"""
    
    def __init__(self):
        self.config = get_log_config()
        self.log_dir = self.config.get('log_dir', 'logs')
    
    def compress_old_logs(self, days_old: int = 7) -> int:
        """Comprime logs antiguos para ahorrar espacio"""
        compressed_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        try:
            for filename in os.listdir(self.log_dir):
                if not filename.endswith('.log'):
                    continue
                
                filepath = os.path.join(self.log_dir, filename)
                if not os.path.isfile(filepath):
                    continue
                
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if file_time < cutoff_date:
                    # Comprimir archivo
                    compressed_path = filepath + '.gz'
                    if not os.path.exists(compressed_path):
                        with open(filepath, 'rb') as f_in:
                            with gzip.open(compressed_path, 'wb', compresslevel=6) as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        # Verificar que la compresión fue exitosa
                        if os.path.exists(compressed_path) and os.path.getsize(compressed_path) > 0:
                            os.remove(filepath)  # Eliminar archivo original
                            compressed_count += 1
                            rpa_logger.info(f"Log comprimido: {filename}")
                        else:
                            if os.path.exists(compressed_path):
                                os.remove(compressed_path)
                            rpa_logger.error(f"Error comprimiendo: {filename}")
            
            return compressed_count
            
        except Exception as e:
            rpa_logger.error(f"Error comprimiendo logs: {e}")
            return 0
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """Limpia logs muy antiguos"""
        cleaned_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        try:
            for filename in os.listdir(self.log_dir):
                filepath = os.path.join(self.log_dir, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    if file_time < cutoff_date:
                        try:
                            os.remove(filepath)
                            cleaned_count += 1
                            rpa_logger.info(f"Log eliminado: {filename}")
                        except Exception as e:
                            rpa_logger.error(f"Error eliminando {filename}: {e}")
            
            return cleaned_count
            
        except Exception as e:
            rpa_logger.error(f"Error limpiando logs: {e}")
            return 0
    
    def analyze_log_patterns(self, hours_back: int = 24) -> Dict[str, Any]:
        """Analiza patrones en los logs"""
        analysis = {
            'error_patterns': {},
            'performance_patterns': {},
            'operation_frequency': {},
            'peak_hours': {},
            'common_issues': []
        }
        
        try:
            # Analizar archivo principal de logs
            main_log_path = os.path.join(self.log_dir, 'rpa.log')
            if os.path.exists(main_log_path):
                self._analyze_log_file(main_log_path, analysis, hours_back)
            
            # Analizar archivo de errores
            error_log_path = os.path.join(self.log_dir, 'rpa_errors.log')
            if os.path.exists(error_log_path):
                self._analyze_error_file(error_log_path, analysis, hours_back)
            
            # Analizar archivo de rendimiento
            perf_log_path = os.path.join(self.log_dir, 'rpa_performance.log')
            if os.path.exists(perf_log_path):
                self._analyze_performance_file(perf_log_path, analysis, hours_back)
            
            return analysis
            
        except Exception as e:
            rpa_logger.error(f"Error analizando patrones: {e}")
            return analysis
    
    def _analyze_log_file(self, filepath: str, analysis: Dict[str, Any], hours_back: int):
        """Analiza un archivo de log específico"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    # Extraer timestamp
                    try:
                        timestamp_str = line[:19]  # Formato: YYYY-MM-DD HH:MM:SS
                        log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        if log_time < cutoff_time:
                            continue
                        
                        # Analizar patrones
                        self._extract_patterns(line, log_time, analysis)
                        
                    except ValueError:
                        continue  # Línea sin timestamp válido
                        
        except Exception as e:
            rpa_logger.error(f"Error analizando archivo {filepath}: {e}")
    
    def _extract_patterns(self, line: str, log_time: datetime, analysis: Dict[str, Any]):
        """Extrae patrones de una línea de log"""
        hour = log_time.hour
        
        # Contar operaciones por hora
        if 'ACTION:' in line:
            operation = line.split('ACTION:')[1].split('|')[0].strip()
            analysis['operation_frequency'][operation] = analysis['operation_frequency'].get(operation, 0) + 1
            analysis['peak_hours'][hour] = analysis['peak_hours'].get(hour, 0) + 1
        
        # Detectar errores
        if 'ERROR:' in line:
            error_type = self._classify_error(line)
            analysis['error_patterns'][error_type] = analysis['error_patterns'].get(error_type, 0) + 1
        
        # Analizar rendimiento
        if 'PERFORMANCE:' in line:
            self._extract_performance_metrics(line, analysis)
    
    def _classify_error(self, line: str) -> str:
        """Clasifica un error en categorías"""
        line_lower = line.lower()
        
        if 'sap' in line_lower and 'no encontrado' in line_lower:
            return 'SAP_NOT_FOUND'
        elif 'escritorio remoto' in line_lower:
            return 'RDP_CONNECTION'
        elif 'json' in line_lower:
            return 'JSON_PARSING'
        elif 'timeout' in line_lower or 'tiempo' in line_lower:
            return 'TIMEOUT'
        elif 'permission' in line_lower or 'permiso' in line_lower:
            return 'PERMISSION'
        else:
            return 'OTHER'
    
    def _extract_performance_metrics(self, line: str, analysis: Dict[str, Any]):
        """Extrae métricas de rendimiento"""
        try:
            if 'completed in' in line:
                parts = line.split('completed in')
                if len(parts) == 2:
                    operation = parts[0].split(':')[-1].strip()
                    duration_str = parts[1].split('seconds')[0].strip()
                    duration = float(duration_str)
                    
                    if operation not in analysis['performance_patterns']:
                        analysis['performance_patterns'][operation] = []
                    
                    analysis['performance_patterns'][operation].append(duration)
                    
        except Exception as e:
            rpa_logger.error(f"Error extrayendo métricas: {e}")
    
    def _analyze_error_file(self, filepath: str, analysis: Dict[str, Any], hours_back: int):
        """Analiza archivo de errores específicamente"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        timestamp_str = line[:19]
                        log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        if log_time < cutoff_time:
                            continue
                        
                        error_type = self._classify_error(line)
                        analysis['error_patterns'][error_type] = analysis['error_patterns'].get(error_type, 0) + 1
                        
                    except ValueError:
                        continue
                        
        except Exception as e:
            rpa_logger.error(f"Error analizando archivo de errores: {e}")
    
    def _analyze_performance_file(self, filepath: str, analysis: Dict[str, Any], hours_back: int):
        """Analiza archivo de rendimiento específicamente"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        timestamp_str = line[:19]
                        log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        if log_time < cutoff_time:
                            continue
                        
                        self._extract_performance_metrics(line, analysis)
                        
                    except ValueError:
                        continue
                        
        except Exception as e:
            rpa_logger.error(f"Error analizando archivo de rendimiento: {e}")
    
    def generate_log_report(self, report_type: str = 'daily') -> Dict[str, Any]:
        """Genera un reporte completo de logs"""
        report = {
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'summary': {},
            'analysis': {},
            'recommendations': []
        }
        
        try:
            # Obtener estadísticas básicas
            report['summary'] = self._get_log_summary()
            
            # Analizar patrones
            hours_back = 24 if report_type == 'daily' else 168 if report_type == 'weekly' else 1
            report['analysis'] = self.analyze_log_patterns(hours_back)
            
            # Generar recomendaciones
            report['recommendations'] = self._generate_recommendations(report['analysis'])
            
            return report
            
        except Exception as e:
            rpa_logger.error(f"Error generando reporte: {e}")
            return report
    
    def _get_log_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen de los logs"""
        summary = {
            'total_files': 0,
            'total_size_mb': 0,
            'file_types': {},
            'oldest_log': None,
            'newest_log': None
        }
        
        try:
            for filename in os.listdir(self.log_dir):
                if filename.endswith('.log'):
                    filepath = os.path.join(self.log_dir, filename)
                    if os.path.isfile(filepath):
                        stat = os.stat(filepath)
                        size_mb = stat.st_size / (1024 * 1024)
                        
                        summary['total_files'] += 1
                        summary['total_size_mb'] += size_mb
                        
                        # Clasificar por tipo
                        file_type = filename.split('.')[0]
                        summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
                        
                        # Timestamps
                        created_time = datetime.fromtimestamp(stat.st_ctime)
                        modified_time = datetime.fromtimestamp(stat.st_mtime)
                        
                        if summary['oldest_log'] is None or created_time < summary['oldest_log']:
                            summary['oldest_log'] = created_time.isoformat()
                        
                        if summary['newest_log'] is None or modified_time > summary['newest_log']:
                            summary['newest_log'] = modified_time.isoformat()
            
            return summary
            
        except Exception as e:
            rpa_logger.error(f"Error obteniendo resumen: {e}")
            return summary
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Analizar errores frecuentes
        error_patterns = analysis.get('error_patterns', {})
        if error_patterns:
            most_common_error = max(error_patterns.items(), key=lambda x: x[1])
            if most_common_error[1] > 5:  # Más de 5 errores del mismo tipo
                recommendations.append(f"Error frecuente detectado: {most_common_error[0]} ({most_common_error[1]} veces)")
        
        # Analizar rendimiento
        performance_patterns = analysis.get('performance_patterns', {})
        for operation, durations in performance_patterns.items():
            if durations:
                avg_duration = sum(durations) / len(durations)
                if avg_duration > 30:  # Más de 30 segundos promedio
                    recommendations.append(f"Operación lenta: {operation} (promedio: {avg_duration:.1f}s)")
        
        # Analizar horas pico
        peak_hours = analysis.get('peak_hours', {})
        if peak_hours:
            busiest_hour = max(peak_hours.items(), key=lambda x: x[1])
            recommendations.append(f"Hora de mayor actividad: {busiest_hour[0]}:00 ({busiest_hour[1]} operaciones)")
        
        # Verificar salud del sistema
        health_status = get_health_status()
        if not health_status.get('config_valid', False):
            recommendations.append("Configuración de logs inválida - revisar configuración")
        
        if not health_status.get('log_directory_writable', False):
            recommendations.append("Problemas de permisos en directorio de logs")
        
        return recommendations
    
    def export_logs_to_json(self, output_file: str, hours_back: int = 24) -> bool:
        """Exporta logs a formato JSON para análisis externo"""
        try:
            exported_data = {
                'export_info': {
                    'exported_at': datetime.now().isoformat(),
                    'hours_back': hours_back,
                    'source_directory': self.log_dir
                },
                'logs': [],
                'analysis': self.analyze_log_patterns(hours_back)
            }
            
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            
            # Procesar archivos de log
            for filename in os.listdir(self.log_dir):
                if filename.endswith('.log'):
                    filepath = os.path.join(self.log_dir, filename)
                    if os.path.isfile(filepath):
                        self._export_log_file(filepath, exported_data['logs'], cutoff_time)
            
            # Guardar archivo JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(exported_data, f, indent=2, ensure_ascii=False)
            
            rpa_logger.info(f"Logs exportados a: {output_file}")
            return True
            
        except Exception as e:
            rpa_logger.error(f"Error exportando logs: {e}")
            return False
    
    def _export_log_file(self, filepath: str, logs_list: List[Dict], cutoff_time: datetime):
        """Exporta un archivo de log específico"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        # Extraer timestamp
                        timestamp_str = line[:19]
                        log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        if log_time < cutoff_time:
                            continue
                        
                        # Parsear línea de log
                        log_entry = self._parse_log_line(line, log_time)
                        if log_entry:
                            logs_list.append(log_entry)
                            
                    except ValueError:
                        continue  # Línea sin timestamp válido
                        
        except Exception as e:
            rpa_logger.error(f"Error exportando archivo {filepath}: {e}")
    
    def _parse_log_line(self, line: str, log_time: datetime) -> Optional[Dict[str, Any]]:
        """Parsea una línea de log"""
        try:
            # Extraer componentes básicos
            parts = line.split(' - ', 3)
            if len(parts) < 4:
                return None
            
            timestamp, logger_name, level, message = parts
            
            log_entry = {
                'timestamp': log_time.isoformat(),
                'logger': logger_name,
                'level': level,
                'message': message
            }
            
            # Extraer información adicional si está disponible
            if 'ACTION:' in message:
                action_parts = message.split('ACTION:')
                if len(action_parts) > 1:
                    action_info = action_parts[1].split('|')
                    log_entry['action'] = action_info[0].strip()
                    if len(action_info) > 1:
                        log_entry['details'] = action_info[1].strip()
            
            if 'ERROR:' in message:
                log_entry['error_type'] = self._classify_error(message)
            
            if 'PERFORMANCE:' in message:
                self._extract_performance_from_message(message, log_entry)
            
            return log_entry
            
        except Exception as e:
            rpa_logger.error(f"Error parseando línea de log: {e}")
            return None
    
    def _extract_performance_from_message(self, message: str, log_entry: Dict[str, Any]):
        """Extrae información de rendimiento de un mensaje"""
        try:
            if 'completed in' in message:
                parts = message.split('completed in')
                if len(parts) == 2:
                    operation = parts[0].split(':')[-1].strip()
                    duration_str = parts[1].split('seconds')[0].strip()
                    duration = float(duration_str)
                    
                    log_entry['performance'] = {
                        'operation': operation,
                        'duration': duration
                    }
                    
        except Exception as e:
            rpa_logger.error(f"Error extrayendo rendimiento: {e}")

def main():
    """Función principal para utilidades de logs"""
    parser = argparse.ArgumentParser(description='Utilidades para sistema de logs RPA')
    parser.add_argument('--action', choices=['compress', 'cleanup', 'analyze', 'report', 'export'], 
                       required=True, help='Acción a realizar')
    parser.add_argument('--days', type=int, default=7, help='Días para compresión/limpieza')
    parser.add_argument('--hours', type=int, default=24, help='Horas para análisis')
    parser.add_argument('--output', type=str, help='Archivo de salida para exportación')
    parser.add_argument('--report-type', choices=['hourly', 'daily', 'weekly'], 
                       default='daily', help='Tipo de reporte')
    
    args = parser.parse_args()
    utils = LogUtils()
    
    try:
        if args.action == 'compress':
            count = utils.compress_old_logs(args.days)
            print(f"Archivos comprimidos: {count}")
            
        elif args.action == 'cleanup':
            count = utils.cleanup_old_logs(args.days)
            print(f"Archivos eliminados: {count}")
            
        elif args.action == 'analyze':
            analysis = utils.analyze_log_patterns(args.hours)
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
            
        elif args.action == 'report':
            report = utils.generate_log_report(args.report_type)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            
        elif args.action == 'export':
            if not args.output:
                args.output = f"rpa_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            success = utils.export_logs_to_json(args.output, args.hours)
            if success:
                print(f"Logs exportados a: {args.output}")
            else:
                print("Error exportando logs")
                
    except Exception as e:
        rpa_logger.error(f"Error en utilidades de logs: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 