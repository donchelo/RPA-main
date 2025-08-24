#!/usr/bin/env python3
"""
Script para crear una nueva carpeta en Google Drive y actualizar la configuración
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


def crear_carpeta_rpa():
    """Crea una nueva carpeta para el RPA"""
    print_section("Creando Nueva Carpeta para RPA")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return None
        
        print_success("Servicio de Google Drive inicializado correctamente")
        
        # Crear carpeta con nombre descriptivo
        nombre_carpeta = f"RPA_TAMAPRINT_{datetime.now().strftime('%Y%m%d')}"
        
        print_info(f"Creando carpeta: {nombre_carpeta}")
        
        # Crear carpeta
        file_metadata = {
            'name': nombre_carpeta,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = uploader.service.files().create(
            body=file_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        folder_id = folder.get('id')
        folder_name = folder.get('name')
        folder_link = folder.get('webViewLink')
        
        print_success(f"Carpeta creada exitosamente: {folder_name}")
        print_info(f"ID: {folder_id}")
        print_info(f"Enlace: {folder_link}")
        
        return folder_id
        
    except Exception as e:
        print_error(f"Error creando carpeta: {str(e)}")
        return None


def actualizar_configuracion(folder_id):
    """Actualiza la configuración con el nuevo ID de carpeta"""
    print_section("Actualizando Configuración")
    
    try:
        uploader_path = './rpa/google_drive_oauth_uploader.py'
        
        if not os.path.exists(uploader_path):
            print_error("No se encontró el archivo de configuración")
            return False
        
        # Leer el archivo actual
        with open(uploader_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar el folder_id
        old_folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        new_content = content.replace(old_folder_id, folder_id)
        
        # Escribir el archivo actualizado
        with open(uploader_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print_success(f"Configuración actualizada: {old_folder_id} → {folder_id}")
        print_info("El archivo de configuración ha sido actualizado")
        
        return True
        
    except Exception as e:
        print_error(f"Error actualizando configuración: {str(e)}")
        return False


def verificar_carpeta_nueva(folder_id):
    """Verifica que la nueva carpeta funciona correctamente"""
    print_section("Verificando Nueva Carpeta")
    
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


def probar_subida_archivo(folder_id):
    """Prueba subir un archivo a la nueva carpeta"""
    print_section("Probando Subida de Archivo")
    
    try:
        # Crear un archivo de prueba
        test_file_path = './test_carpeta_nueva.txt'
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(f"Archivo de prueba para carpeta {folder_id}\n")
            f.write(f"Fecha: {datetime.now().isoformat()}\n")
            f.write("Este archivo confirma que la carpeta funciona correctamente.\n")
        
        print_success(f"Archivo de prueba creado: {test_file_path}")
        
        # Crear uploader temporal con la nueva carpeta
        uploader = GoogleDriveOAuthUploader()
        uploader.folder_id = folder_id  # Usar la nueva carpeta
        
        # Subir archivo
        result = uploader.upload_file(test_file_path, "test_carpeta_nueva.txt")
        
        if result and result.get('success'):
            print_success("Archivo subido exitosamente a la nueva carpeta")
            print_info(f"ID: {result.get('id')}")
            print_info(f"Enlace: {result.get('link')}")
            
            # Limpiar archivo de prueba
            os.remove(test_file_path)
            print_info("Archivo de prueba eliminado")
            
            return True
        else:
            print_error("Error subiendo archivo de prueba")
            return False
        
    except Exception as e:
        print_error(f"Error durante prueba: {str(e)}")
        return False


def main():
    """Función principal del script"""
    print_section("CREADOR DE CARPETA GOOGLE DRIVE")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Iniciando creación de nueva carpeta para RPA...")
    
    # Crear nueva carpeta
    folder_id = crear_carpeta_rpa()
    
    if folder_id:
        print_success("Carpeta creada correctamente")
        
        # Verificar la carpeta
        if verificar_carpeta_nueva(folder_id):
            print_success("Carpeta verificada correctamente")
            
            # Probar subida de archivo
            if probar_subida_archivo(folder_id):
                print_success("Prueba de subida exitosa")
                
                # Actualizar configuración
                if actualizar_configuracion(folder_id):
                    print_success("Configuración actualizada correctamente")
                    
                    # Resumen final
                    print_section("RESUMEN FINAL")
                    print_success("✅ Carpeta creada y configurada correctamente")
                    print_info(f"ID de carpeta: {folder_id}")
                    print_info("El sistema RPA ahora usará esta carpeta para subir archivos")
                    print_info("Reinicia el sistema para aplicar los cambios")
                    
                else:
                    print_error("Error actualizando configuración")
            else:
                print_error("Error en prueba de subida")
        else:
            print_error("Error verificando carpeta")
    else:
        print_error("Error creando carpeta")


if __name__ == "__main__":
    main()
