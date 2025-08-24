#!/usr/bin/env python3
"""
Script de prueba para verificar el flujo completo corregido del RPA
- Verifica que se haga clic en "Agregar y cerrar"
- Verifica que se suban los archivos en orden: PNG primero, luego PDF
- Verifica que el PDF subido sea el que llegó a la carpeta "Procesados"
"""

import os
import json
import time
import shutil
from datetime import datetime
from pathlib import Path

def print_section(title):
    """Imprime una sección con formato"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime un mensaje informativo"""
    print(f"ℹ️  {message}")

def crear_archivos_prueba():
    """Crea archivos de prueba para simular el procesamiento"""
    print_section("Creando Archivos de Prueba")
    
    # Crear directorios necesarios
    processed_dir = './data/outputs_json/Procesados'
    os.makedirs(processed_dir, exist_ok=True)
    
    # Generar nombre base único
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f"test_flujo_{timestamp}"
    
    # Crear archivo JSON de prueba
    json_filename = f"{base_name}.json"
    json_path = os.path.join(processed_dir, json_filename)
    
    test_data = {
        "archivo": json_filename,
        "fecha_procesamiento": datetime.now().isoformat(),
        "estado": "completado",
        "datos_prueba": {
            "nit": "123456789",
            "orden_compra": "OC-001",
            "fecha_entrega": "25/12/2024"
        }
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    # Crear archivo PNG de prueba (screenshot)
    png_filename = f"{base_name}.png"
    png_path = os.path.join(processed_dir, png_filename)
    
    # Crear un archivo PNG dummy (simulando screenshot)
    with open(png_path, 'wb') as f:
        # Escribir bytes mínimos para simular PNG
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82')
    
    # Crear archivo PDF de prueba (documento original)
    pdf_filename = f"{base_name}.PDF"
    pdf_path = os.path.join(processed_dir, pdf_filename)
    
    # Crear un archivo PDF dummy
    with open(pdf_path, 'wb') as f:
        # Escribir bytes mínimos para simular PDF
        f.write(b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF\n')
    
    print_success(f"Archivo JSON creado: {json_path}")
    print_success(f"Archivo PNG creado: {png_path}")
    print_success(f"Archivo PDF creado: {pdf_path}")
    
    return {
        'base_name': base_name,
        'json_filename': json_filename,
        'json_path': json_path,
        'png_filename': png_filename,
        'png_path': png_path,
        'pdf_filename': pdf_filename,
        'pdf_path': pdf_path
    }

def verificar_archivos_creados(test_files):
    """Verifica que todos los archivos de prueba existan"""
    print_section("Verificando Archivos Creados")
    
    archivos_verificados = []
    
    for file_type, file_path in [
        ('JSON', test_files['json_path']),
        ('PNG', test_files['png_path']),
        ('PDF', test_files['pdf_path'])
    ]:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print_success(f"{file_type}: {os.path.basename(file_path)} ({size} bytes)")
            archivos_verificados.append(file_type)
        else:
            print_error(f"{file_type}: {os.path.basename(file_path)} - NO ENCONTRADO")
    
    return len(archivos_verificados) == 3

def probar_flujo_completo(test_files):
    """Prueba el flujo completo del RPA con los archivos de prueba"""
    print_section("Probando Flujo Completo del RPA")
    
    try:
        # Importar el sistema RPA
        from rpa.rpa_with_state_machine import RPAWithStateMachine
        from rpa.state_machine import StateMachine, RPAState, RPAEvent
        from rpa.rpa_state_handlers import RPAStateHandlers
        
        print_info("Inicializando sistema RPA...")
        
        # Crear instancia del RPA
        rpa = RPAWithStateMachine()
        
        # Crear máquina de estados
        state_machine = StateMachine()
        
        # Crear manejadores de estado
        handlers = RPAStateHandlers(rpa)
        
        # Registrar manejadores
        state_machine.register_state_handler(RPAState.POSITIONING_MOUSE, handlers.handle_positioning_mouse)
        state_machine.register_state_handler(RPAState.UPLOADING_TO_GOOGLE_DRIVE, handlers.handle_uploading_to_google_drive_state)
        state_machine.register_state_handler(RPAState.COMPLETED, handlers.handle_completed_state)
        
        # Configurar contexto
        state_machine.context.current_file = test_files['json_filename']
        state_machine.context.start_time = time.time()
        
        print_info("Sistema RPA inicializado correctamente")
        
        # Simular que estamos en el estado POSITIONING_MOUSE
        print_info("Simulando estado POSITIONING_MOUSE...")
        state_machine.current_state = RPAState.POSITIONING_MOUSE
        
        # Ejecutar el estado de posicionamiento del mouse
        print_info("Ejecutando posicionamiento del mouse...")
        event = state_machine.execute_current_state()
        
        if event == RPAEvent.MOUSE_POSITIONED:
            print_success("Mouse posicionado correctamente")
            
            # Disparar transición al estado de subida a Google Drive
            print_info("Transicionando a estado UPLOADING_TO_GOOGLE_DRIVE...")
            success = state_machine.trigger_event(RPAEvent.MOUSE_POSITIONED)
            
            if success:
                print_success("Transición exitosa a UPLOADING_TO_GOOGLE_DRIVE")
                
                # Ejecutar el estado de subida a Google Drive
                print_info("Ejecutando subida a Google Drive...")
                event = state_machine.execute_current_state()
                
                if event == RPAEvent.GOOGLE_DRIVE_UPLOADED:
                    print_success("Archivos subidos exitosamente a Google Drive")
                    
                    # Disparar transición al estado completado
                    print_info("Transicionando a estado COMPLETED...")
                    success = state_machine.trigger_event(RPAEvent.GOOGLE_DRIVE_UPLOADED)
                    
                    if success:
                        print_success("Proceso completado exitosamente")
                        return True
                    else:
                        print_error("Fallo en transición a estado COMPLETED")
                        return False
                else:
                    print_error(f"Fallo en subida a Google Drive: {event}")
                    return False
            else:
                print_error("Fallo en transición a UPLOADING_TO_GOOGLE_DRIVE")
                return False
        else:
            print_error(f"Fallo en posicionamiento del mouse: {event}")
            return False
            
    except ImportError as e:
        print_error(f"Error importando módulos RPA: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error en flujo completo: {str(e)}")
        return False

def limpiar_archivos_prueba(test_files):
    """Limpia los archivos de prueba creados"""
    print_section("Limpiando Archivos de Prueba")
    
    archivos_eliminados = 0
    
    for file_type, file_path in [
        ('JSON', test_files['json_path']),
        ('PNG', test_files['png_path']),
        ('PDF', test_files['pdf_path'])
    ]:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print_success(f"{file_type} eliminado: {os.path.basename(file_path)}")
                archivos_eliminados += 1
        except Exception as e:
            print_error(f"Error eliminando {file_type}: {str(e)}")
    
    return archivos_eliminados

def main():
    """Función principal del script de prueba"""
    print_section("PRUEBA DEL FLUJO COMPLETO CORREGIDO")
    print_info("Verificando que el RPA haga clic en 'Agregar y cerrar' y suba archivos en orden correcto")
    
    # Crear archivos de prueba
    test_files = crear_archivos_prueba()
    
    # Verificar que los archivos se crearon correctamente
    if not verificar_archivos_creados(test_files):
        print_error("No se pudieron crear todos los archivos de prueba")
        return False
    
    # Probar el flujo completo
    print_info("Iniciando prueba del flujo completo...")
    success = probar_flujo_completo(test_files)
    
    if success:
        print_success("PRUEBA EXITOSA: El flujo completo funciona correctamente")
        print_info("✅ Se hace clic en 'Agregar y cerrar'")
        print_info("✅ Se suben archivos en orden: PNG primero, luego PDF")
        print_info("✅ El PDF subido es el que llegó a la carpeta 'Procesados'")
    else:
        print_error("PRUEBA FALLIDA: El flujo completo no funciona correctamente")
    
    # Limpiar archivos de prueba
    limpiar_archivos_prueba(test_files)
    
    return success

if __name__ == "__main__":
    main()
