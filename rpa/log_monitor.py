"""
Sistema de monitoreo y dashboard para logs RPA
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import psutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict, deque
import sqlite3
from pathlib import Path

from rpa.logger import rpa_logger
from rpa.log_config import get_log_config, get_health_status, calculate_disk_usage

class LogMonitor:
    """Monitor de logs en tiempo real"""
    
    def __init__(self):
        self.config = get_log_config()
        self.log_dir = self.config.get('log_dir', 'logs')
        self.monitoring_active = False
        self.metrics_history = deque(maxlen=1000)
        self.alert_history = deque(maxlen=100)
        self.db_path = os.path.join(self.log_dir, 'log_metrics.db')
        self.setup_database()
    
    def setup_database(self):
        """Configura la base de datos para métricas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla para métricas de operaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operation_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    duration REAL NOT NULL,
                    success BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    context TEXT
                )
            ''')
            
            # Tabla para alertas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    operation TEXT
                )
            ''')
            
            # Tabla para estadísticas del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpu_percent REAL,
                    memory_percent REAL,
                    disk_usage REAL,
                    log_file_count INTEGER,
                    total_log_size REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            rpa_logger.error(f"Error setting up database: {e}")
    
    def start_monitoring(self):
        """Inicia el monitoreo en tiempo real"""
        self.monitoring_active = True
        rpa_logger.info("Iniciando monitoreo de logs")
        
        # Thread para monitoreo de sistema
        system_thread = threading.Thread(target=self._monitor_system, daemon=True)
        system_thread.start()
        
        # Thread para análisis de logs
        log_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        log_thread.start()
    
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.monitoring_active = False
        rpa_logger.info("Deteniendo monitoreo de logs")
    
    def _monitor_system(self):
        """Monitorea métricas del sistema"""
        while self.monitoring_active:
            try:
                # Obtener métricas del sistema
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                disk_usage = calculate_disk_usage(self.log_dir)
                
                # Contar archivos de log
                log_files = [f for f in os.listdir(self.log_dir) if f.endswith('.log')]
                total_log_size = sum(
                    os.path.getsize(os.path.join(self.log_dir, f)) 
                    for f in log_files
                ) / (1024 * 1024)  # MB
                
                # Guardar en base de datos
                self._save_system_stats(cpu_percent, memory_percent, disk_usage, 
                                      len(log_files), total_log_size)
                
                # Verificar umbrales de alerta
                self._check_system_alerts(cpu_percent, memory_percent, disk_usage, total_log_size)
                
                time.sleep(60)  # Monitoreo cada minuto
                
            except Exception as e:
                rpa_logger.error(f"Error en monitoreo de sistema: {e}")
                time.sleep(60)
    
    def _monitor_logs(self):
        """Monitorea cambios en archivos de log"""
        log_files = {
            'main': os.path.join(self.log_dir, 'rpa.log'),
            'error': os.path.join(self.log_dir, 'rpa_errors.log'),
            'performance': os.path.join(self.log_dir, 'rpa_performance.log'),
            'structured': os.path.join(self.log_dir, 'rpa_structured.log')
        }
        
        file_sizes = {}
        for name, path in log_files.items():
            if os.path.exists(path):
                file_sizes[name] = os.path.getsize(path)
        
        while self.monitoring_active:
            try:
                for name, path in log_files.items():
                    if os.path.exists(path):
                        current_size = os.path.getsize(path)
                        if name in file_sizes and current_size > file_sizes[name]:
                            # Archivo creció, analizar nuevas líneas
                            self._analyze_log_changes(name, path, file_sizes[name], current_size)
                        file_sizes[name] = current_size
                
                time.sleep(10)  # Verificar cada 10 segundos
                
            except Exception as e:
                rpa_logger.error(f"Error en monitoreo de logs: {e}")
                time.sleep(10)
    
    def _analyze_log_changes(self, log_type: str, file_path: str, old_size: int, new_size: int):
        """Analiza cambios en archivos de log"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(old_size)
                new_lines = f.readlines()
            
            for line in new_lines:
                self._process_log_line(log_type, line.strip())
                
        except Exception as e:
            rpa_logger.error(f"Error analizando cambios en {log_type}: {e}")
    
    def _process_log_line(self, log_type: str, line: str):
        """Procesa una línea de log"""
        try:
            # Detectar patrones importantes
            if 'ERROR' in line:
                self._record_error_alert(line)
            elif 'PERFORMANCE' in line:
                self._extract_performance_metrics(line)
            elif 'ALERTA' in line:
                self._record_alert(line)
                
        except Exception as e:
            rpa_logger.error(f"Error procesando línea de log: {e}")
    
    def _record_error_alert(self, line: str):
        """Registra una alerta de error"""
        alert = {
            'type': 'ERROR_DETECTED',
            'message': line,
            'severity': 'HIGH',
            'timestamp': datetime.now().isoformat()
        }
        self.alert_history.append(alert)
        self._save_alert(alert)
    
    def _extract_performance_metrics(self, line: str):
        """Extrae métricas de rendimiento de una línea de log"""
        try:
            # Buscar patrón de duración
            if 'completed in' in line:
                parts = line.split('completed in')
                if len(parts) == 2:
                    operation = parts[0].split(':')[-1].strip()
                    duration_str = parts[1].split('seconds')[0].strip()
                    duration = float(duration_str)
                    
                    # Guardar métrica
                    self._save_operation_metric(operation, duration, True)
                    
        except Exception as e:
            rpa_logger.error(f"Error extrayendo métricas: {e}")
    
    def _record_alert(self, line: str):
        """Registra una alerta del sistema"""
        alert = {
            'type': 'SYSTEM_ALERT',
            'message': line,
            'severity': 'MEDIUM' if 'MEDIUM' in line else 'HIGH' if 'HIGH' in line else 'LOW',
            'timestamp': datetime.now().isoformat()
        }
        self.alert_history.append(alert)
        self._save_alert(alert)
    
    def _save_operation_metric(self, operation: str, duration: float, success: bool, context: str = None):
        """Guarda una métrica de operación en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO operation_metrics (operation, duration, success, context)
                VALUES (?, ?, ?, ?)
            ''', (operation, duration, success, context))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            rpa_logger.error(f"Error guardando métrica: {e}")
    
    def _save_alert(self, alert: Dict[str, Any]):
        """Guarda una alerta en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts (alert_type, message, severity, operation)
                VALUES (?, ?, ?, ?)
            ''', (alert['type'], alert['message'], alert['severity'], alert.get('operation')))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            rpa_logger.error(f"Error guardando alerta: {e}")
    
    def _save_system_stats(self, cpu_percent: float, memory_percent: float, 
                          disk_usage: float, log_file_count: int, total_log_size: float):
        """Guarda estadísticas del sistema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_stats (cpu_percent, memory_percent, disk_usage, log_file_count, total_log_size)
                VALUES (?, ?, ?, ?, ?)
            ''', (cpu_percent, memory_percent, disk_usage, log_file_count, total_log_size))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            rpa_logger.error(f"Error guardando estadísticas: {e}")
    
    def _check_system_alerts(self, cpu_percent: float, memory_percent: float, 
                           disk_usage: float, total_log_size: float):
        """Verifica condiciones de alerta del sistema"""
        alerts = []
        
        # Verificar uso de CPU
        if cpu_percent > 80:
            alerts.append({
                'type': 'HIGH_CPU_USAGE',
                'message': f'Uso de CPU alto: {cpu_percent:.1f}%',
                'severity': 'MEDIUM'
            })
        
        # Verificar uso de memoria
        if memory_percent > 80:
            alerts.append({
                'type': 'HIGH_MEMORY_USAGE',
                'message': f'Uso de memoria alto: {memory_percent:.1f}%',
                'severity': 'MEDIUM'
            })
        
        # Verificar tamaño de logs
        if total_log_size > 100:  # 100MB
            alerts.append({
                'type': 'LARGE_LOG_FILES',
                'message': f'Tamaño total de logs: {total_log_size:.1f}MB',
                'severity': 'LOW'
            })
        
        # Registrar alertas
        for alert in alerts:
            self._record_alert(alert['message'])
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Obtiene datos para el dashboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Estadísticas de operaciones
            cursor.execute('''
                SELECT operation, 
                       COUNT(*) as count,
                       AVG(duration) as avg_duration,
                       SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count
                FROM operation_metrics 
                WHERE timestamp > datetime('now', '-24 hours')
                GROUP BY operation
            ''')
            operation_stats = cursor.fetchall()
            
            # Alertas recientes
            cursor.execute('''
                SELECT alert_type, severity, COUNT(*) as count
                FROM alerts 
                WHERE timestamp > datetime('now', '-24 hours')
                GROUP BY alert_type, severity
            ''')
            alert_stats = cursor.fetchall()
            
            # Estadísticas del sistema
            cursor.execute('''
                SELECT AVG(cpu_percent), AVG(memory_percent), AVG(disk_usage)
                FROM system_stats 
                WHERE timestamp > datetime('now', '-1 hour')
            ''')
            system_stats = cursor.fetchone()
            
            conn.close()
            
            return {
                'operation_stats': operation_stats,
                'alert_stats': alert_stats,
                'system_stats': system_stats,
                'health_status': get_health_status(),
                'current_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            rpa_logger.error(f"Error obteniendo datos del dashboard: {e}")
            return {}
    
    def generate_report(self, report_type: str = 'daily') -> Dict[str, Any]:
        """Genera un reporte de métricas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if report_type == 'daily':
                time_filter = "datetime('now', '-24 hours')"
            elif report_type == 'weekly':
                time_filter = "datetime('now', '-7 days')"
            else:
                time_filter = "datetime('now', '-1 hour')"
            
            # Métricas de operaciones
            cursor.execute(f'''
                SELECT operation, 
                       COUNT(*) as total_operations,
                       AVG(duration) as avg_duration,
                       MIN(duration) as min_duration,
                       MAX(duration) as max_duration,
                       SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count,
                       COUNT(*) - SUM(CASE WHEN success THEN 1 ELSE 0 END) as error_count
                FROM operation_metrics 
                WHERE timestamp > {time_filter}
                GROUP BY operation
            ''')
            operations = cursor.fetchall()
            
            # Alertas
            cursor.execute(f'''
                SELECT alert_type, severity, COUNT(*) as count
                FROM alerts 
                WHERE timestamp > {time_filter}
                GROUP BY alert_type, severity
            ''')
            alerts = cursor.fetchall()
            
            # Estadísticas del sistema
            cursor.execute(f'''
                SELECT AVG(cpu_percent), AVG(memory_percent), AVG(disk_usage),
                       MAX(cpu_percent), MAX(memory_percent), MAX(disk_usage)
                FROM system_stats 
                WHERE timestamp > {time_filter}
            ''')
            system = cursor.fetchone()
            
            conn.close()
            
            return {
                'report_type': report_type,
                'period': time_filter,
                'operations': operations,
                'alerts': alerts,
                'system_stats': system,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            rpa_logger.error(f"Error generando reporte: {e}")
            return {}

class LogDashboard:
    """Dashboard visual para logs RPA"""
    
    def __init__(self, monitor: LogMonitor):
        self.monitor = monitor
        self.fig, self.axes = None, None
    
    def create_dashboard(self):
        """Crea un dashboard visual"""
        try:
            data = self.monitor.get_dashboard_data()
            
            # Crear figura con subplots
            self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 10))
            self.fig.suptitle('Dashboard RPA - Sistema de Logs', fontsize=16)
            
            # Gráfico 1: Operaciones por duración
            self._plot_operations_duration(data.get('operation_stats', []))
            
            # Gráfico 2: Alertas por tipo
            self._plot_alerts_by_type(data.get('alert_stats', []))
            
            # Gráfico 3: Uso del sistema
            self._plot_system_usage(data.get('system_stats', []))
            
            # Gráfico 4: Estado de salud
            self._plot_health_status(data.get('health_status', {}))
            
            plt.tight_layout()
            return self.fig
            
        except Exception as e:
            rpa_logger.error(f"Error creando dashboard: {e}")
            return None
    
    def _plot_operations_duration(self, operation_stats):
        """Gráfico de duración de operaciones"""
        if not operation_stats:
            return
        
        ax = self.axes[0, 0]
        operations = [op[0] for op in operation_stats]
        avg_durations = [op[2] for op in operation_stats]
        
        bars = ax.bar(operations, avg_durations, color='skyblue')
        ax.set_title('Duración Promedio de Operaciones')
        ax.set_ylabel('Duración (segundos)')
        ax.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, duration in zip(bars, avg_durations):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'{duration:.1f}s', ha='center', va='bottom')
    
    def _plot_alerts_by_type(self, alert_stats):
        """Gráfico de alertas por tipo"""
        if not alert_stats:
            return
        
        ax = self.axes[0, 1]
        alert_types = [alert[0] for alert in alert_stats]
        counts = [alert[2] for alert in alert_stats]
        colors = ['red' if alert[1] == 'HIGH' else 'orange' if alert[1] == 'MEDIUM' else 'yellow' 
                 for alert in alert_stats]
        
        bars = ax.bar(alert_types, counts, color=colors)
        ax.set_title('Alertas por Tipo')
        ax.set_ylabel('Cantidad')
        ax.tick_params(axis='x', rotation=45)
    
    def _plot_system_usage(self, system_stats):
        """Gráfico de uso del sistema"""
        if not system_stats or not system_stats[0]:
            return
        
        ax = self.axes[1, 0]
        metrics = ['CPU', 'Memoria', 'Disco']
        values = [system_stats[0] or 0, system_stats[1] or 0, system_stats[2] or 0]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        bars = ax.bar(metrics, values, color=colors)
        ax.set_title('Uso del Sistema (%)')
        ax.set_ylabel('Porcentaje')
        ax.set_ylim(0, 100)
        
        # Agregar valores en las barras
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   f'{value:.1f}%', ha='center', va='bottom')
    
    def _plot_health_status(self, health_status):
        """Gráfico de estado de salud"""
        ax = self.axes[1, 1]
        
        if not health_status:
            ax.text(0.5, 0.5, 'Sin datos de salud', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Estado de Salud del Sistema')
            return
        
        # Crear gráfico de estado
        status_items = ['Configuración', 'Directorio', 'Archivos']
        status_values = [
            1 if health_status.get('config_valid', False) else 0,
            1 if health_status.get('log_directory_exists', False) else 0,
            1 if all(health_status.get('files_status', {}).values()) else 0
        ]
        colors = ['green' if v else 'red' for v in status_values]
        
        bars = ax.bar(status_items, status_values, color=colors)
        ax.set_title('Estado de Salud del Sistema')
        ax.set_ylabel('Estado (1=OK, 0=Error)')
        ax.set_ylim(0, 1)
    
    def save_dashboard(self, filename: str = None):
        """Guarda el dashboard como imagen"""
        if self.fig is None:
            self.create_dashboard()
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'dashboard_rpa_{timestamp}.png'
        
        try:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            rpa_logger.info(f"Dashboard guardado: {filename}")
            return filename
        except Exception as e:
            rpa_logger.error(f"Error guardando dashboard: {e}")
            return None

def main():
    """Función principal para ejecutar el monitor"""
    monitor = LogMonitor()
    dashboard = LogDashboard(monitor)
    
    try:
        # Iniciar monitoreo
        monitor.start_monitoring()
        
        # Crear y guardar dashboard
        dashboard.create_dashboard()
        dashboard.save_dashboard()
        
        # Mantener ejecutando
        while True:
            time.sleep(300)  # Actualizar cada 5 minutos
            dashboard.create_dashboard()
            dashboard.save_dashboard()
            
    except KeyboardInterrupt:
        print("\nDeteniendo monitor...")
        monitor.stop_monitoring()
    except Exception as e:
        rpa_logger.error(f"Error en monitor principal: {e}")

if __name__ == "__main__":
    main() 