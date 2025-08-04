import schedule
import time
import os
from rpa.main import RPA
import logging

# Configurar logging
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

def run_rpa_task():
    """Ejecuta el proceso RPA para automatizar SAP"""
    logging.info('Iniciando proceso RPA')
    print('Iniciando proceso RPA...')

    rpa = RPA()
    max_retries = 3
    
    for i in range(max_retries):
        if rpa.open_sap():
            rpa.run()
            break
        else:
            print(f"Error al abrir SAP. Reintentando... ({i+1}/{max_retries})")
            logging.warning(f"Error al abrir SAP. Intento {i+1}/{max_retries}")
            time.sleep(10)
    
    logging.info('Proceso RPA completado, esperando próxima ejecución en 10 minutos')
    print('Proceso RPA completado, esperando próxima ejecución en 10 minutos')
    print('Sistema RPA en espera - monitoreando nuevos archivos JSON...')

print("=== SISTEMA RPA TAMAPRINT ===")
print("Iniciando sistema de automatización RPA para SAP...")

# Ejecutar una vez al inicio
run_rpa_task()

# Programar ejecución cada 10 minutos
schedule.every(10).minutes.do(run_rpa_task)

print("Sistema RPA activo. Presiona Ctrl+C para detener.")

# Loop principal del sistema
while True:
    try:
        schedule.run_pending()
        time.sleep(10)  # Verificar cada 10 segundos
        print('.', end='', flush=True)  # Indicador de actividad
    except KeyboardInterrupt:
        print("\nSistema RPA detenido por el usuario.")
        logging.info("Sistema RPA detenido por el usuario")
        break
    except Exception as e:
        print(f"\nError en el sistema RPA: {e}")
        logging.error(f"Error en el sistema RPA: {e}")
        time.sleep(30)  # Esperar 30 segundos antes de continuar en caso de error
