#!/usr/bin/env python3
"""
Script para probar subida directa a la carpeta 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv
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


def crear_archivos_prueba():
    """Crea archivos de prueba para la subida"""
    print_section("Creando Archivos de Prueba")
    
    try:
        # Crear directorio de prueba si no existe
        test_dir = './test_subida_directa'
        os.makedirs(test_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Crear archivo PNG de prueba
        png_filename = f"test_directo_{timestamp}.png"
        png_path = os.path.join(test_dir, png_filename)
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (800, 600), color='lightgreen')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 50), f"Prueba Subida Directa", fill='black', font=font)
            draw.text((50, 100), f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font)
            draw.text((50, 150), f"Archivo: {png_filename}", fill='black', font=font)
            draw.text((50, 200), "Carpeta: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv", fill='black', font=font)
            draw.text((50, 250), "Método: Subida Directa", fill='black', font=font)
            
            img.save(png_path)
            print_success(f"Archivo PNG creado: {png_path}")
            
        except ImportError:
            with open(png_path, 'wb') as f:
                f.write(b'PNG_DIRECTO_TEST')
            print_success(f"Archivo PNG creado (simulado): {png_path}")
        
        # Crear archivo PDF de prueba
        pdf_filename = f"test_directo_{timestamp}.PDF"
        pdf_path = os.path.join(test_dir, pdf_filename)
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f"Prueba Subida Directa")
            c.drawString(100, 700, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(100, 650, f"Archivo: {pdf_filename}")
            c.drawString(100, 600, "Carpeta: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
            c.drawString(100, 550, "Método: Subida Directa")
            c.save()
            
            print_success(f"Archivo PDF creado: {pdf_path}")
            
        except ImportError:
            with open(pdf_path, 'wb') as f:
                f.write(b'PDF_DIRECTO_TEST')
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


def probar_subida_directa():
    """Prueba subir archivos directamente a la carpeta específica"""
    print_section("Probando Subida Directa")
    
    folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        # Crear archivos de prueba
        test_files = crear_archivos_prueba()
        if not test_files:
            return False
        
        uploader = GoogleDriveOAuthUploader()
        
        # Configurar la carpeta específica
        uploader.folder_id = folder_id
        
        results = []
        
        # Subir archivo PNG primero
        print_info("Subiendo archivo PNG...")
        png_result = uploader.upload_file(test_files['png_file'], test_files['png_filename'])
        
        if png_result and png_result.get('success'):
            print_success(f"PNG subido exitosamente: {test_files['png_filename']}")
            print_info(f"ID: {png_result.get('id')}")
            print_info(f"Enlace: {png_result.get('link')}")
            results.append(('PNG', png_result))
        else:
            print_error(f"Error subiendo PNG: {test_files['png_filename']}")
            print_error(f"Resultado: {png_result}")
            return False
        
        # Subir archivo PDF segundo
        print_info("Subiendo archivo PDF...")
        pdf_result = uploader.upload_file(test_files['pdf_file'], test_files['pdf_filename'])
        
        if pdf_result and pdf_result.get('success'):
            print_success(f"PDF subido exitosamente: {test_files['pdf_filename']}")
            print_info(f"ID: {pdf_result.get('id')}")
            print_info(f"Enlace: {pdf_result.get('link')}")
            results.append(('PDF', pdf_result))
        else:
            print_error(f"Error subiendo PDF: {test_files['pdf_filename']}")
            print_error(f"Resultado: {pdf_result}")
            return False
        
        return results
        
    except Exception as e:
        print_error(f"Error durante subida directa: {str(e)}")
        return False


def verificar_archivos_subidos():
    """Verifica que los archivos se subieron correctamente"""
    print_section("Verificando Archivos Subidos")
    
    folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        # Listar archivos en la carpeta
        results = uploader.service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name, webViewLink, createdTime)",
            orderBy="createdTime desc",
            pageSize=10
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            print_success(f"Se encontraron {len(files)} archivos en la carpeta:")
            
            for file in files:
                print_info(f"📄 {file.get('name')}")
                print_info(f"   ID: {file.get('id')}")
                print_info(f"   Enlace: {file.get('webViewLink')}")
                print_info(f"   Creado: {file.get('createdTime')}")
                print()
            
            return True
        else:
            print_warning("No se encontraron archivos en la carpeta")
            return False
        
    except Exception as e:
        print_error(f"Error verificando archivos: {str(e)}")
        return False


def limpiar_archivos_prueba():
    """Limpia los archivos de prueba creados"""
    print_section("Limpiando Archivos de Prueba")
    
    try:
        # Limpiar directorio de prueba
        test_dir = './test_subida_directa'
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
            print_success("Directorio de prueba eliminado")
        
        print_success("Limpieza completada")
        
    except Exception as e:
        print_error(f"Error durante limpieza: {str(e)}")


def main():
    """Función principal del script"""
    print_section("PRUEBA DE SUBIDA DIRECTA A TERMINADOS")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Probando subida directa a la carpeta Terminados...")
    print_info("Carpeta: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
    print_info("Enlace: https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
    
    try:
        # Probar subida directa
        upload_results = probar_subida_directa()
        
        if upload_results:
            print_success("🎉 SUBIDA DIRECTA EXITOSA")
            
            # Verificar archivos subidos
            verificar_archivos_subidos()
            
            # Resumen final
            print_section("RESUMEN DE SUBIDA DIRECTA")
            print_success("✅ Archivos subidos exitosamente")
            print_info("✅ Orden correcto: PNG primero, luego PDF")
            print_info("✅ Carpeta destino: 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
            
            print_section("ARCHIVOS SUBIDOS")
            for file_type, result in upload_results:
                print_info(f"{file_type}: {result.get('drive_info', {}).get('name')}")
                print_info(f"  Enlace: {result.get('drive_info', {}).get('link')}")
            
        else:
            print_error("❌ SUBIDA DIRECTA FALLÓ")
            print_info("La carpeta puede tener restricciones de permisos")
            print_info("Considera usar una de las carpetas accesibles encontradas")
        
        # Limpiar archivos de prueba
        limpiar_archivos_prueba()
        
    except KeyboardInterrupt:
        print_info("\nPrueba interrumpida por el usuario")
    except Exception as e:
        print_error(f"Error durante la prueba: {str(e)}")


if __name__ == "__main__":
    main()
