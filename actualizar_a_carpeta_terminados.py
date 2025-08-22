#!/usr/bin/env python3
"""
Script para actualizar la configuración a la carpeta RPA_TAMAPRINT_TERMINADOS
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


def actualizar_configuracion_terminados():
    """Actualiza la configuración para usar la carpeta RPA_TAMAPRINT_TERMINADOS"""
    print_section("Actualizando Configuración a Carpeta Terminados")
    
    try:
        uploader_path = './rpa/google_drive_oauth_uploader.py'
        
        if not os.path.exists(uploader_path):
            print_error("No se encontró el archivo de configuración")
            return False
        
        # Leer el archivo actual
        with open(uploader_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar el folder_id con la carpeta de terminados
        current_folder_id = "1LYNxk7iZWspTGOEGeJY7RW1YHUKpISue"
        terminados_folder_id = "1XzrdVoXKUxlAXkPm70jPlXaYuLG_ZoAj"
        
        new_content = content.replace(current_folder_id, terminados_folder_id)
        
        # Escribir el archivo actualizado
        with open(uploader_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print_success(f"Configuración actualizada: {current_folder_id} → {terminados_folder_id}")
        print_info("El archivo de configuración ha sido actualizado para usar RPA_TAMAPRINT_TERMINADOS")
        
        return True
        
    except Exception as e:
        print_error(f"Error actualizando configuración: {str(e)}")
        return False


def verificar_carpeta_terminados():
    """Verifica que la carpeta de terminados funciona correctamente"""
    print_section("Verificando Carpeta Terminados")
    
    folder_id = "1XzrdVoXKUxlAXkPm70jPlXaYuLG_ZoAj"
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        # Verificar que la carpeta existe
        try:
            folder = uploader.service.files().get(
                fileId=folder_id,
                fields='id,name,webViewLink'
            ).execute()
            
            print_success(f"Carpeta verificada: {folder.get('name')}")
            print_info(f"ID: {folder.get('id')}")
            print_info(f"Enlace: {folder.get('webViewLink')}")
            
            return True
            
        except Exception as e:
            print_error(f"Error verificando carpeta: {str(e)}")
            return False
        
    except Exception as e:
        print_error(f"Error durante verificación: {str(e)}")
        return False


def probar_subida_terminados():
    """Prueba subir un archivo a la carpeta de terminados"""
    print_section("Probando Subida a Carpeta Terminados")
    
    try:
        # Crear un archivo de prueba
        test_file_path = './test_carpeta_terminados.txt'
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(f"Archivo de prueba para carpeta RPA_TAMAPRINT_TERMINADOS\n")
            f.write(f"Fecha: {datetime.now().isoformat()}\n")
            f.write("Este archivo confirma que la carpeta de terminados funciona.\n")
        
        print_success(f"Archivo de prueba creado: {test_file_path}")
        
        # Crear uploader con la carpeta de terminados
        uploader = GoogleDriveOAuthUploader()
        uploader.folder_id = "1XzrdVoXKUxlAXkPm70jPlXaYuLG_ZoAj"
        
        # Subir archivo
        result = uploader.upload_file(test_file_path, "test_carpeta_terminados.txt")
        
        if result and result.get('success'):
            print_success("Archivo subido exitosamente a la carpeta de terminados")
            print_info(f"ID: {result.get('id')}")
            print_info(f"Enlace: {result.get('link')}")
            
            # Limpiar archivo de prueba
            os.remove(test_file_path)
            print_info("Archivo de prueba eliminado")
            
            return True
        else:
            print_error("Error subiendo archivo a la carpeta de terminados")
            return False
        
    except Exception as e:
        print_error(f"Error durante prueba: {str(e)}")
        return False


def probar_sistema_completo():
    """Prueba el sistema completo con la nueva configuración"""
    print_section("Probando Sistema Completo")
    
    try:
        # Actualizar configuración
        if not actualizar_configuracion_terminados():
            return False
        
        # Verificar carpeta
        if not verificar_carpeta_terminados():
            return False
        
        # Probar subida
        if not probar_subida_terminados():
            return False
        
        # Probar el sistema RPA completo
        print_info("Probando integración con máquina de estados...")
        
        # Crear archivos de prueba para el RPA
        processed_dir = './data/outputs_json/Procesados'
        os.makedirs(processed_dir, exist_ok=True)
        
        test_base_name = f"test_terminados_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Crear archivo JSON de prueba
        json_filename = f"{test_base_name}.json"
        json_path = os.path.join(processed_dir, json_filename)
        
        import json
        test_data = {
            "archivo": json_filename,
            "fecha_procesamiento": datetime.now().isoformat(),
            "estado": "completado",
            "carpeta_destino": "RPA_TAMAPRINT_TERMINADOS"
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        # Crear archivo PNG de prueba
        png_filename = f"{test_base_name}.png"
        png_path = os.path.join(processed_dir, png_filename)
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (800, 600), color='white')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 50), f"Prueba Terminados: {test_base_name}", fill='black', font=font)
            draw.text((50, 100), f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font)
            draw.text((50, 150), "Carpeta: RPA_TAMAPRINT_TERMINADOS", fill='black', font=font)
            
            img.save(png_path)
            
        except ImportError:
            with open(png_path, 'wb') as f:
                f.write(b'PNG_TERMINADOS_TEST')
        
        # Crear archivo PDF de prueba
        pdf_filename = f"{test_base_name}.PDF"
        pdf_path = os.path.join(processed_dir, pdf_filename)
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f"Prueba Terminados: {test_base_name}")
            c.drawString(100, 700, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(100, 650, "Carpeta: RPA_TAMAPRINT_TERMINADOS")
            c.save()
            
        except ImportError:
            with open(pdf_path, 'wb') as f:
                f.write(b'PDF_TERMINADOS_TEST')
        
        print_success("Archivos de prueba creados para sistema completo")
        
        # Probar subida con el método del RPA
        uploader = GoogleDriveOAuthUploader()
        upload_result = uploader.upload_original_files_for_json(json_filename)
        
        if upload_result.get('success'):
            print_success("Sistema completo funcionando correctamente")
            print_info(f"Archivos subidos: {upload_result.get('files_uploaded', 0)}")
            
            # Mostrar detalles
            for file_info in upload_result.get('uploaded_files', []):
                print_info(f"Archivo {file_info.get('type')}: {file_info.get('drive_info', {}).get('name')}")
                print_info(f"  ID: {file_info.get('drive_info', {}).get('id')}")
                print_info(f"  Enlace: {file_info.get('drive_info', {}).get('link')}")
            
            return True
        else:
            print_error("Error en sistema completo")
            return False
        
    except Exception as e:
        print_error(f"Error durante prueba del sistema: {str(e)}")
        return False


def main():
    """Función principal del script"""
    print_section("ACTUALIZACIÓN A CARPETA TERMINADOS")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Actualizando sistema para usar la carpeta RPA_TAMAPRINT_TERMINADOS")
    
    # Probar sistema completo
    if probar_sistema_completo():
        print_success("Sistema actualizado y funcionando correctamente")
        
        # Resumen final
        print_section("RESUMEN FINAL")
        print_success("✅ Configuración actualizada a RPA_TAMAPRINT_TERMINADOS")
        print_info("ID de carpeta: 1XzrdVoXKUxlAXkPm70jPlXaYuLG_ZoAj")
        print_info("Enlace: https://drive.google.com/drive/folders/1XzrdVoXKUxlAXkPm70jPlXaYuLG_ZoAj")
        print_info("El sistema RPA ahora subirá archivos a esta carpeta")
        print_info("Orden: PNG primero, luego PDF")
        
    else:
        print_error("Error actualizando el sistema")


if __name__ == "__main__":
    main()
