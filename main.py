import schedule
import time
import os
from rpa.rpa_with_state_machine import RPAWithStateMachine
from rpa.simple_logger import rpa_logger
import logging

# Configurar logging
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

def run_rpa_task():
    """Ejecuta el proceso RPA con máquina de estados para automatizar SAP"""
    logging.info('Iniciando proceso RPA con máquina de estados')
    print('Iniciando proceso RPA con máquina de estados...')
    
    rpa_logger.log_action("=== INICIO DE CICLO RPA ===", "Sistema iniciando procesamiento")

    try:
        rpa = RPAWithStateMachine()
        
        # El método run() maneja internamente toda la lógica de reintentos
        # usando la máquina de estados
        rpa.run()
        
        # Obtener información final del estado
        state_info = rpa.get_state_info()
        rpa_logger.log_action(
            "Ciclo RPA completado", 
            f"Estado final: {state_info['current_state']}"
        )
        
    except Exception as e:
        error_msg = f"Error crítico en el sistema RPA: {str(e)}"
        logging.error(error_msg)
        rpa_logger.log_error(error_msg, "Error en ciclo principal")
        print(f"Error crítico: {e}")
    
    logging.info('Proceso RPA completado, esperando próxima ejecución en 10 minutos')
    print('Proceso RPA completado, esperando próxima ejecución en 10 minutos')
    print('Sistema RPA en espera - monitoreando nuevos archivos JSON...')
    rpa_logger.log_action("=== FIN DE CICLO RPA ===", "Sistema en espera para próximo ciclo")

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
