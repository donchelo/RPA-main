#!/usr/bin/env python3
"""
Script de prueba para subir archivos a la carpeta específica 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.simple_logger import rpa_logger


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


def actualizar_configuracion_carpeta_original():
    """Actualiza la configuración para usar la carpeta original del usuario"""
    print_section("Actualizando Configuración a Carpeta Original")
    
    try:
        uploader_path = './rpa/google_drive_oauth_uploader.py'
        
        if not os.path.exists(uploader_path):
            print_error("No se encontró el archivo de configuración")
            return False
        
        # Leer el archivo actual
        with open(uploader_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar el folder_id con la carpeta original del usuario
        current_folder_id = "1LYNxk7iZWspTGOEGeJY7RW1YHUKpISue"  # RPA_TAMAPRINT_20250821
        original_folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"  # Terminados
        
        new_content = content.replace(current_folder_id, original_folder_id)
        
        # Escribir el archivo actualizado
        with open(uploader_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print_success(f"Configuración actualizada: {current_folder_id} → {original_folder_id}")
        print_info("El archivo de configuración ha sido actualizado para usar la carpeta Terminados")
        
        return True
        
    except Exception as e:
        print_error(f"Error actualizando configuración: {str(e)}")
        return False


def verificar_carpeta_terminados():
    """Verifica que la carpeta Terminados funciona correctamente"""
    print_section("Verificando Carpeta Terminados")
    
    folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
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


def crear_archivos_prueba():
    """Crea archivos de prueba para la subida"""
    print_section("Creando Archivos de Prueba")
    
    try:
        # Crear directorio de prueba si no existe
        test_dir = './test_files_terminados'
        os.makedirs(test_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Crear archivo PNG de prueba
        png_filename = f"test_terminados_{timestamp}.png"
        png_path = os.path.join(test_dir, png_filename)
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (800, 600), color='lightblue')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 50), f"Prueba Carpeta Terminados", fill='black', font=font)
            draw.text((50, 100), f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font)
            draw.text((50, 150), f"Archivo: {png_filename}", fill='black', font=font)
            draw.text((50, 200), "Carpeta: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv", fill='black', font=font)
            
            img.save(png_path)
            print_success(f"Archivo PNG creado: {png_path}")
            
        except ImportError:
            with open(png_path, 'wb') as f:
                f.write(b'PNG_TERMINADOS_TEST')
            print_success(f"Archivo PNG creado (simulado): {png_path}")
        
        # Crear archivo PDF de prueba
        pdf_filename = f"test_terminados_{timestamp}.PDF"
        pdf_path = os.path.join(test_dir, pdf_filename)
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f"Prueba Carpeta Terminados")
            c.drawString(100, 700, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(100, 650, f"Archivo: {pdf_filename}")
            c.drawString(100, 600, "Carpeta: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
            c.save()
            
            print_success(f"Archivo PDF creado: {pdf_path}")
            
        except ImportError:
            with open(pdf_path, 'wb') as f:
                f.write(b'PDF_TERMINADOS_TEST')
            print_success(f"Archivo PDF creado (simulado): {pdf_path}")
        
        return {
            'png_file': png_path,
            'pdf_file': pdf_path,
            'png_filename': png_filename,
            'pdf_filename': pdf_filename
        }
        
    except Exception as e:
        print_error(f"Error creando archivos de prueba: {str(e)}")
        return None


def probar_subida_individual():
    """Prueba subir archivos individualmente"""
    print_section("Probando Subida Individual")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        # Crear archivos de prueba
        test_files = crear_archivos_prueba()
        if not test_files:
            return False
        
        uploader = GoogleDriveOAuthUploader()
        
        # Configurar la carpeta específica
        uploader.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        
        results = []
        
        # Subir archivo PNG
        print_info("Subiendo archivo PNG...")
        png_result = uploader.upload_file(test_files['png_file'], test_files['png_filename'])
        
        if png_result and png_result.get('success'):
            print_success(f"PNG subido exitosamente: {test_files['png_filename']}")
            print_info(f"ID: {png_result.get('id')}")
            print_info(f"Enlace: {png_result.get('link')}")
            results.append(('PNG', png_result))
        else:
            print_error(f"Error subiendo PNG: {test_files['png_filename']}")
            return False
        
        # Subir archivo PDF
        print_info("Subiendo archivo PDF...")
        pdf_result = uploader.upload_file(test_files['pdf_file'], test_files['pdf_filename'])
        
        if pdf_result and pdf_result.get('success'):
            print_success(f"PDF subido exitosamente: {test_files['pdf_filename']}")
            print_info(f"ID: {pdf_result.get('id')}")
            print_info(f"Enlace: {pdf_result.get('link')}")
            results.append(('PDF', pdf_result))
        else:
            print_error(f"Error subiendo PDF: {test_files['pdf_filename']}")
            return False
        
        return results
        
    except Exception as e:
        print_error(f"Error durante subida individual: {str(e)}")
        return False


def probar_subida_sistema_rpa():
    """Prueba la subida usando el sistema RPA completo"""
    print_section("Probando Sistema RPA Completo")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        # Crear archivos de prueba
        test_files = crear_archivos_prueba()
        if not test_files:
            return False
        
        # Crear archivo JSON de prueba (como lo haría el RPA)
        processed_dir = './data/outputs_json/Procesados'
        os.makedirs(processed_dir, exist_ok=True)
        
        json_filename = f"test_terminados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        json_path = os.path.join(processed_dir, json_filename)
        
        test_data = {
            "archivo": json_filename,
            "fecha_procesamiento": datetime.now().isoformat(),
            "estado": "completado",
            "carpeta_destino": "Terminados",
            "archivos_originales": {
                "png": test_files['png_filename'],
                "pdf": test_files['pdf_filename']
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print_success(f"Archivo JSON creado: {json_path}")
        
        # Copiar archivos de prueba al directorio de procesados
        import shutil
        
        png_dest = os.path.join(processed_dir, test_files['png_filename'])
        pdf_dest = os.path.join(processed_dir, test_files['pdf_filename'])
        
        shutil.copy2(test_files['png_file'], png_dest)
        shutil.copy2(test_files['pdf_file'], pdf_dest)
        
        print_success("Archivos copiados al directorio de procesados")
        
        # Probar subida con el método del RPA
        uploader = GoogleDriveOAuthUploader()
        uploader.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        
        upload_result = uploader.upload_original_files_for_json(json_filename)
        
        if upload_result.get('success'):
            print_success("Sistema RPA funcionando correctamente")
            print_info(f"Archivos subidos: {upload_result.get('files_uploaded', 0)}")
            
            # Mostrar detalles
            for file_info in upload_result.get('uploaded_files', []):
                print_info(f"Archivo {file_info.get('type')}: {file_info.get('drive_info', {}).get('name')}")
                print_info(f"  ID: {file_info.get('drive_info', {}).get('id')}")
                print_info(f"  Enlace: {file_info.get('drive_info', {}).get('link')}")
            
            return True
        else:
            print_error("Error en sistema RPA")
            return False
        
    except Exception as e:
        print_error(f"Error durante prueba del sistema RPA: {str(e)}")
        return False


def limpiar_archivos_prueba():
    """Limpia los archivos de prueba creados"""
    print_section("Limpiando Archivos de Prueba")
    
    try:
        # Limpiar directorio de prueba
        test_dir = './test_files_terminados'
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
            print_success("Directorio de prueba eliminado")
        
        # Limpiar archivos de procesados
        processed_dir = './data/outputs_json/Procesados'
        if os.path.exists(processed_dir):
            for file in os.listdir(processed_dir):
                if file.startswith('test_terminados_'):
                    file_path = os.path.join(processed_dir, file)
                    os.remove(file_path)
                    print_info(f"Archivo eliminado: {file}")
        
        print_success("Limpieza completada")
        
    except Exception as e:
        print_error(f"Error durante limpieza: {str(e)}")


def main():
    """Función principal del script"""
    print_section("PRUEBA DE SUBIDA A CARPETA TERMINADOS")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Iniciando pruebas de subida a la carpeta Terminados...")
    print_info("Carpeta: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
    print_info("Enlace: https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
    
    try:
        # Actualizar configuración
        if not actualizar_configuracion_carpeta_original():
            return
        
        # Verificar carpeta
        if not verificar_carpeta_terminados():
            return
        
        # Probar subida individual
        individual_results = probar_subida_individual()
        if not individual_results:
            print_error("Prueba individual falló")
            return
        
        # Probar sistema RPA completo
        rpa_success = probar_subida_sistema_rpa()
        
        # Resumen final
        print_section("RESUMEN DE PRUEBAS")
        
        if individual_results and rpa_success:
            print_success("🎉 TODAS LAS PRUEBAS EXITOSAS")
            print_info("✅ Subida individual: OK")
            print_info("✅ Sistema RPA completo: OK")
            print_info("✅ Carpeta configurada: Terminados")
            print_info("✅ Archivos subidos en orden: PNG primero, luego PDF")
            
            print_section("ARCHIVOS SUBIDOS")
            for file_type, result in individual_results:
                print_info(f"{file_type}: {result.get('drive_info', {}).get('name')}")
                print_info(f"  Enlace: {result.get('drive_info', {}).get('link')}")
            
        else:
            print_error("⚠️  ALGUNAS PRUEBAS FALLARON")
        
        # Preguntar si limpiar archivos
        print_info("\n¿Deseas limpiar los archivos de prueba? (s/n): ", end='')
        # En un entorno automático, asumimos que sí
        limpiar_archivos_prueba()
        
    except KeyboardInterrupt:
        print_info("\nPruebas interrumpidas por el usuario")
    except Exception as e:
        print_error(f"Error durante las pruebas: {str(e)}")


if __name__ == "__main__":
    main()
