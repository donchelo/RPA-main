#!/usr/bin/env python3
"""
Script de prueba para verificar la integración de subida a Google Drive
en el flujo completo del RPA con máquina de estados.
"""

import os
import sys
import time
import json
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.simple_logger import rpa_logger
from rpa.rpa_with_state_machine import RPAWithStateMachine
from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader


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


def create_test_files():
    """Crea archivos de prueba para simular el procesamiento completo"""
    print_section("Creando Archivos de Prueba")
    
    # Crear directorio de procesados si no existe
    processed_dir = './data/outputs_json/Procesados'
    os.makedirs(processed_dir, exist_ok=True)
    
    # Nombre base para archivos de prueba
    test_base_name = f"test_google_drive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Crear archivo JSON de prueba
    json_filename = f"{test_base_name}.json"
    json_path = os.path.join(processed_dir, json_filename)
    
    test_data = {
        "archivo": json_filename,
        "fecha_procesamiento": datetime.now().isoformat(),
        "estado": "completado",
        "datos_extraidos": {
            "cliente": "Cliente de Prueba",
            "orden": "12345",
            "fecha": "2024-01-15"
        }
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print_success(f"Archivo JSON creado: {json_path}")
    
    # Crear archivo PNG de prueba (simular screenshot)
    png_filename = f"{test_base_name}.png"
    png_path = os.path.join(processed_dir, png_filename)
    
    # Crear un archivo PNG simple (simulado)
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Crear imagen de prueba
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        # Agregar texto de prueba
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 50), f"Archivo de Prueba: {test_base_name}", fill='black', font=font)
        draw.text((50, 100), f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font)
        draw.text((50, 150), "Este es un archivo PNG de prueba para Google Drive", fill='black', font=font)
        
        img.save(png_path)
        print_success(f"Archivo PNG creado: {png_path}")
        
    except ImportError:
        # Si PIL no está disponible, crear un archivo vacío
        with open(png_path, 'wb') as f:
            f.write(b'PNG_TEST_FILE')
        print_success(f"Archivo PNG simulado creado: {png_path}")
    
    # Crear archivo PDF de prueba
    pdf_filename = f"{test_base_name}.PDF"
    pdf_path = os.path.join(processed_dir, pdf_filename)
    
    # Crear un archivo PDF simple (simulado)
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, f"Archivo PDF de Prueba: {test_base_name}")
        c.drawString(100, 700, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 650, "Este es un archivo PDF de prueba para Google Drive")
        c.save()
        
        print_success(f"Archivo PDF creado: {pdf_path}")
        
    except ImportError:
        # Si reportlab no está disponible, crear un archivo vacío
        with open(pdf_path, 'wb') as f:
            f.write(b'PDF_TEST_FILE')
        print_success(f"Archivo PDF simulado creado: {pdf_path}")
    
    return test_base_name, json_filename


def test_google_drive_upload():
    """Prueba la subida directa a Google Drive"""
    print_section("Probando Subida Directa a Google Drive")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        print_success("Servicio de Google Drive inicializado correctamente")
        
        # Crear archivos de prueba
        test_base_name, json_filename = create_test_files()
        
        # Probar subida de archivos
        print_info("Iniciando subida de archivos a Google Drive...")
        upload_result = uploader.upload_original_files_for_json(json_filename)
        
        if upload_result.get('success'):
            print_success(f"Subida exitosa: {upload_result.get('files_uploaded', 0)} archivos subidos")
            
            # Mostrar detalles de archivos subidos
            for file_info in upload_result.get('uploaded_files', []):
                print_info(f"Archivo {file_info.get('type')}: {file_info.get('drive_info', {}).get('name')}")
                print_info(f"  ID: {file_info.get('drive_info', {}).get('id')}")
                print_info(f"  Enlace: {file_info.get('drive_info', {}).get('link')}")
            
            return True
        else:
            print_error(f"Falla en subida: {upload_result.get('message', 'Error desconocido')}")
            return False
            
    except Exception as e:
        print_error(f"Error durante prueba de Google Drive: {str(e)}")
        return False


def test_state_machine_integration():
    """Prueba la integración con la máquina de estados"""
    print_section("Probando Integración con Máquina de Estados")
    
    try:
        # Crear archivos de prueba
        test_base_name, json_filename = create_test_files()
        
        # Crear instancia del RPA
        rpa = RPAWithStateMachine()
        
        # Simular datos del archivo
        test_data = {
            "archivo": json_filename,
            "fecha_procesamiento": datetime.now().isoformat(),
            "estado": "completado"
        }
        
        print_info("Simulando procesamiento completo con máquina de estados...")
        
        # Simular el estado UPLOADING_TO_GOOGLE_DRIVE directamente
        from rpa.state_machine import StateContext, RPAState, RPAEvent
        
        context = StateContext()
        context.current_file = json_filename
        context.start_time = time.time() - 60  # Simular 1 minuto de procesamiento
        context.processing_stats = {
            'remote_desktop_time': 5.2,
            'sap_navigation_time': 12.8,
            'screenshot_time': 3.1
        }
        
        # Ejecutar el manejador del estado UPLOADING_TO_GOOGLE_DRIVE
        result = rpa.state_handlers.handle_uploading_to_google_drive_state(context)
        
        if result == RPAEvent.GOOGLE_DRIVE_UPLOADED:
            print_success("Estado UPLOADING_TO_GOOGLE_DRIVE ejecutado correctamente")
            print_info("Archivos subidos en orden: PNG primero, luego PDF")
        else:
            print_error(f"Estado UPLOADING_TO_GOOGLE_DRIVE falló: {result}")
            return False
        
        print_info("Verificar logs para detalles de subida a Google Drive")
        
        return True
        
    except Exception as e:
        print_error(f"Error durante prueba de integración: {str(e)}")
        return False


def main():
    """Función principal del script de prueba"""
    print_section("PRUEBA DE INTEGRACIÓN GOOGLE DRIVE")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Iniciando pruebas de integración de Google Drive...")
    
    # Prueba 1: Subida directa a Google Drive
    test1_success = test_google_drive_upload()
    
    # Prueba 2: Integración con máquina de estados
    test2_success = test_state_machine_integration()
    
    # Resumen de resultados
    print_section("RESUMEN DE PRUEBAS")
    
    if test1_success:
        print_success("✅ Prueba de subida directa a Google Drive: EXITOSA")
    else:
        print_error("❌ Prueba de subida directa a Google Drive: FALLIDA")
    
    if test2_success:
        print_success("✅ Prueba de integración con máquina de estados: EXITOSA")
    else:
        print_error("❌ Prueba de integración con máquina de estados: FALLIDA")
    
    if test1_success and test2_success:
        print_success("🎉 TODAS LAS PRUEBAS EXITOSAS - Integración de Google Drive funcionando correctamente")
    else:
        print_error("⚠️  ALGUNAS PRUEBAS FALLARON - Revisar configuración de Google Drive")
    
    print_info("Revisar logs para detalles completos del proceso")


if __name__ == "__main__":
    main()
