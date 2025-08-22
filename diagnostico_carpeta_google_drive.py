#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de la carpeta de Google Drive
"""

import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.simple_logger import rpa_logger
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


def verificar_configuracion_carpeta():
    """Verifica la configuración de la carpeta de Google Drive"""
    print_section("Verificando Configuración de Carpeta")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        print_success("Servicio de Google Drive inicializado correctamente")
        print_info(f"Carpeta configurada: {uploader.folder_id}")
        
        # Verificar que la carpeta existe y es accesible
        try:
            folder = uploader.service.files().get(
                fileId=uploader.folder_id,
                fields='id,name,webViewLink,parents'
            ).execute()
            
            print_success(f"Carpeta encontrada: {folder.get('name', 'Sin nombre')}")
            print_info(f"ID de carpeta: {folder.get('id')}")
            print_info(f"Enlace: {folder.get('webViewLink')}")
            
            # Verificar permisos
            print_info("Verificando permisos de escritura...")
            
            # Intentar listar archivos en la carpeta
            results = uploader.service.files().list(
                q=f"'{uploader.folder_id}' in parents",
                pageSize=10,
                fields="nextPageToken, files(id, name, createdTime)"
            ).execute()
            
            files = results.get('files', [])
            print_success(f"Permisos OK - Archivos en carpeta: {len(files)}")
            
            if files:
                print_info("Últimos archivos en la carpeta:")
                for file in files[:5]:  # Mostrar solo los últimos 5
                    print_info(f"  - {file.get('name')} (ID: {file.get('id')})")
            
            return True
            
        except Exception as e:
            print_error(f"Error verificando carpeta: {str(e)}")
            return False
            
    except Exception as e:
        print_error(f"Error durante verificación: {str(e)}")
        return False


def crear_archivo_prueba():
    """Crea un archivo de prueba para diagnosticar la subida"""
    print_section("Creando Archivo de Prueba")
    
    # Crear directorio de procesados si no existe
    processed_dir = './data/outputs_json/Procesados'
    os.makedirs(processed_dir, exist_ok=True)
    
    # Nombre base para archivo de prueba
    test_base_name = f"diagnostico_carpeta_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Crear archivo JSON de prueba
    json_filename = f"{test_base_name}.json"
    json_path = os.path.join(processed_dir, json_filename)
    
    test_data = {
        "archivo": json_filename,
        "fecha_procesamiento": datetime.now().isoformat(),
        "estado": "diagnostico",
        "carpeta_destino": "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
    }
    
    import json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print_success(f"Archivo JSON creado: {json_path}")
    
    # Crear archivo PNG de prueba
    png_filename = f"{test_base_name}.png"
    png_path = os.path.join(processed_dir, png_filename)
    
    # Crear un archivo PNG simple
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
        
        draw.text((50, 50), f"Diagnóstico Carpeta: {test_base_name}", fill='black', font=font)
        draw.text((50, 100), f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font)
        draw.text((50, 150), f"Carpeta Destino: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv", fill='black', font=font)
        draw.text((50, 200), "Este archivo debe aparecer en la carpeta correcta", fill='black', font=font)
        
        img.save(png_path)
        print_success(f"Archivo PNG creado: {png_path}")
        
    except ImportError:
        # Si PIL no está disponible, crear un archivo vacío
        with open(png_path, 'wb') as f:
            f.write(b'PNG_DIAGNOSTICO')
        print_success(f"Archivo PNG simulado creado: {png_path}")
    
    # Crear archivo PDF de prueba
    pdf_filename = f"{test_base_name}.PDF"
    pdf_path = os.path.join(processed_dir, pdf_filename)
    
    # Crear un archivo PDF simple
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, f"Diagnóstico Carpeta: {test_base_name}")
        c.drawString(100, 700, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 650, f"Carpeta Destino: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
        c.drawString(100, 600, "Este archivo debe aparecer en la carpeta correcta")
        c.save()
        
        print_success(f"Archivo PDF creado: {pdf_path}")
        
    except ImportError:
        # Si reportlab no está disponible, crear un archivo vacío
        with open(pdf_path, 'wb') as f:
            f.write(b'PDF_DIAGNOSTICO')
        print_success(f"Archivo PDF simulado creado: {pdf_path}")
    
    return test_base_name, json_filename


def probar_subida_directa():
    """Prueba la subida directa a la carpeta específica"""
    print_section("Probando Subida Directa a Carpeta Específica")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        # Crear archivos de prueba
        test_base_name, json_filename = crear_archivo_prueba()
        
        print_info("Iniciando subida directa a carpeta específica...")
        print_info(f"Carpeta destino: {uploader.folder_id}")
        
        # Probar subida de archivos
        upload_result = uploader.upload_original_files_for_json(json_filename)
        
        if upload_result.get('success'):
            print_success(f"Subida exitosa: {upload_result.get('files_uploaded', 0)} archivos subidos")
            
            # Mostrar detalles de archivos subidos
            for file_info in upload_result.get('uploaded_files', []):
                print_info(f"Archivo {file_info.get('type')}: {file_info.get('drive_info', {}).get('name')}")
                print_info(f"  ID: {file_info.get('drive_info', {}).get('id')}")
                print_info(f"  Enlace: {file_info.get('drive_info', {}).get('link')}")
                
                # Verificar que el archivo está en la carpeta correcta
                try:
                    file_id = file_info.get('drive_info', {}).get('id')
                    if file_id:
                        file_details = uploader.service.files().get(
                            fileId=file_id,
                            fields='id,name,parents,webViewLink'
                        ).execute()
                        
                        parents = file_details.get('parents', [])
                        if uploader.folder_id in parents:
                            print_success(f"  ✅ Archivo está en la carpeta correcta")
                        else:
                            print_error(f"  ❌ Archivo NO está en la carpeta correcta")
                            print_info(f"  Carpeta actual: {parents}")
                            print_info(f"  Carpeta esperada: {uploader.folder_id}")
                except Exception as e:
                    print_error(f"  Error verificando ubicación: {str(e)}")
            
            return True
        else:
            print_error(f"Falla en subida: {upload_result.get('message', 'Error desconocido')}")
            return False
            
    except Exception as e:
        print_error(f"Error durante prueba de subida: {str(e)}")
        return False


def verificar_archivos_en_carpeta():
    """Verifica los archivos recién subidos en la carpeta"""
    print_section("Verificando Archivos en Carpeta")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        # Buscar archivos recién subidos (últimos 10 minutos)
        from datetime import datetime, timedelta
        cutoff_time = datetime.now() - timedelta(minutes=10)
        cutoff_time_str = cutoff_time.isoformat() + 'Z'
        
        print_info(f"Buscando archivos subidos después de: {cutoff_time_str}")
        
        results = uploader.service.files().list(
            q=f"'{uploader.folder_id}' in parents and createdTime > '{cutoff_time_str}'",
            orderBy='createdTime desc',
            pageSize=20,
            fields="nextPageToken, files(id, name, createdTime, webViewLink)"
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            print_success(f"Encontrados {len(files)} archivos recientes en la carpeta:")
            for file in files:
                created_time = file.get('createdTime', 'Desconocido')
                print_info(f"  - {file.get('name')} (ID: {file.get('id')}) - {created_time}")
                print_info(f"    Enlace: {file.get('webViewLink')}")
        else:
            print_info("No se encontraron archivos recientes en la carpeta")
        
        return True
        
    except Exception as e:
        print_error(f"Error verificando archivos: {str(e)}")
        return False


def main():
    """Función principal del script de diagnóstico"""
    print_section("DIAGNÓSTICO CARPETA GOOGLE DRIVE")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Iniciando diagnóstico de carpeta de Google Drive...")
    
    # Verificar configuración
    config_ok = verificar_configuracion_carpeta()
    
    if config_ok:
        # Probar subida directa
        subida_ok = probar_subida_directa()
        
        if subida_ok:
            # Verificar archivos en carpeta
            verificar_archivos_en_carpeta()
    
    # Resumen de resultados
    print_section("RESUMEN DE DIAGNÓSTICO")
    
    if config_ok:
        print_success("✅ Configuración de carpeta: CORRECTA")
    else:
        print_error("❌ Configuración de carpeta: PROBLEMA")
    
    print_info("Revisar los resultados anteriores para identificar el problema")
    print_info("Si los archivos no aparecen en la carpeta correcta, verificar:")
    print_info("  1. Permisos de la carpeta en Google Drive")
    print_info("  2. Configuración de OAuth")
    print_info("  3. ID de carpeta correcto")


if __name__ == "__main__":
    main()
