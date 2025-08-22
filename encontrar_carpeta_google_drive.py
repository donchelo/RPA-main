#!/usr/bin/env python3
"""
Script para encontrar y listar carpetas disponibles en Google Drive
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


def listar_carpetas_disponibles():
    """Lista todas las carpetas disponibles en Google Drive"""
    print_section("Listando Carpetas Disponibles")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        print_success("Servicio de Google Drive inicializado correctamente")
        
        # Buscar todas las carpetas
        print_info("Buscando carpetas en Google Drive...")
        
        results = uploader.service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            pageSize=50,
            fields="nextPageToken, files(id, name, createdTime, webViewLink, parents)"
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            print_success(f"Encontradas {len(folders)} carpetas:")
            print_info("Carpetas disponibles:")
            
            for i, folder in enumerate(folders, 1):
                print_info(f"{i:2d}. {folder.get('name', 'Sin nombre')}")
                print_info(f"     ID: {folder.get('id')}")
                print_info(f"     Enlace: {folder.get('webViewLink')}")
                print_info(f"     Creada: {folder.get('createdTime', 'Desconocido')}")
                print()
        else:
            print_info("No se encontraron carpetas")
        
        return True
        
    except Exception as e:
        print_error(f"Error listando carpetas: {str(e)}")
        return False


def buscar_carpeta_por_nombre(nombre_busqueda):
    """Busca una carpeta específica por nombre"""
    print_section(f"Buscando Carpeta: '{nombre_busqueda}'")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        # Buscar carpeta por nombre
        query = f"mimeType='application/vnd.google-apps.folder' and name contains '{nombre_busqueda}'"
        
        results = uploader.service.files().list(
            q=query,
            pageSize=20,
            fields="nextPageToken, files(id, name, createdTime, webViewLink, parents)"
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            print_success(f"Encontradas {len(folders)} carpetas que coinciden con '{nombre_busqueda}':")
            
            for i, folder in enumerate(folders, 1):
                print_info(f"{i}. {folder.get('name', 'Sin nombre')}")
                print_info(f"   ID: {folder.get('id')}")
                print_info(f"   Enlace: {folder.get('webViewLink')}")
                print_info(f"   Creada: {folder.get('createdTime', 'Desconocido')}")
                print()
        else:
            print_info(f"No se encontraron carpetas que coincidan con '{nombre_busqueda}'")
        
        return True
        
    except Exception as e:
        print_error(f"Error buscando carpeta: {str(e)}")
        return False


def verificar_carpeta_especifica(folder_id):
    """Verifica si una carpeta específica existe y es accesible"""
    print_section(f"Verificando Carpeta: {folder_id}")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        # Intentar obtener información de la carpeta
        try:
            folder = uploader.service.files().get(
                fileId=folder_id,
                fields='id,name,webViewLink,parents,createdTime'
            ).execute()
            
            print_success(f"Carpeta encontrada: {folder.get('name', 'Sin nombre')}")
            print_info(f"ID: {folder.get('id')}")
            print_info(f"Enlace: {folder.get('webViewLink')}")
            print_info(f"Creada: {folder.get('createdTime', 'Desconocido')}")
            
            # Verificar permisos intentando listar archivos
            try:
                results = uploader.service.files().list(
                    q=f"'{folder_id}' in parents",
                    pageSize=5,
                    fields="files(id, name)"
                ).execute()
                
                files = results.get('files', [])
                print_success(f"Permisos OK - Archivos en carpeta: {len(files)}")
                
                return True
                
            except Exception as e:
                print_error(f"Error verificando permisos: {str(e)}")
                return False
            
        except Exception as e:
            print_error(f"Carpeta no encontrada o no accesible: {str(e)}")
            return False
        
    except Exception as e:
        print_error(f"Error verificando carpeta: {str(e)}")
        return False


def crear_carpeta_nueva(nombre_carpeta):
    """Crea una nueva carpeta en Google Drive"""
    print_section(f"Creando Nueva Carpeta: '{nombre_carpeta}'")
    
    try:
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
        
        # Crear carpeta
        file_metadata = {
            'name': nombre_carpeta,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = uploader.service.files().create(
            body=file_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        print_success(f"Carpeta creada exitosamente: {folder.get('name')}")
        print_info(f"ID: {folder.get('id')}")
        print_info(f"Enlace: {folder.get('webViewLink')}")
        
        return folder.get('id')
        
    except Exception as e:
        print_error(f"Error creando carpeta: {str(e)}")
        return None


def actualizar_configuracion_carpeta(nuevo_folder_id):
    """Actualiza la configuración con el nuevo ID de carpeta"""
    print_section("Actualizando Configuración")
    
    try:
        # Verificar que la carpeta existe
        if verificar_carpeta_especifica(nuevo_folder_id):
            print_success("Carpeta verificada correctamente")
            
            # Actualizar el archivo de configuración
            uploader_path = './rpa/google_drive_oauth_uploader.py'
            
            if os.path.exists(uploader_path):
                with open(uploader_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Reemplazar el folder_id
                old_folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
                new_content = content.replace(old_folder_id, nuevo_folder_id)
                
                with open(uploader_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print_success(f"Configuración actualizada: {old_folder_id} → {nuevo_folder_id}")
                print_info("Reinicia el sistema para aplicar los cambios")
                
                return True
            else:
                print_error("No se encontró el archivo de configuración")
                return False
        else:
            print_error("No se puede actualizar con una carpeta inválida")
            return False
            
    except Exception as e:
        print_error(f"Error actualizando configuración: {str(e)}")
        return False


def main():
    """Función principal del script"""
    print_section("BUSCADOR DE CARPETAS GOOGLE DRIVE")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Iniciando búsqueda de carpetas en Google Drive...")
    
    # Verificar carpeta actual
    print_info("Verificando carpeta actual...")
    carpeta_actual_ok = verificar_carpeta_especifica("17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
    
    if not carpeta_actual_ok:
        print_info("La carpeta actual no es accesible. Buscando alternativas...")
        
        # Listar carpetas disponibles
        listar_carpetas_disponibles()
        
        # Buscar carpetas con nombres comunes
        nombres_comunes = ["Terminados", "Procesados", "RPA", "Archivos", "Documentos"]
        for nombre in nombres_comunes:
            buscar_carpeta_por_nombre(nombre)
        
        print_info("\nOpciones disponibles:")
        print_info("1. Usar una carpeta existente de la lista anterior")
        print_info("2. Crear una nueva carpeta")
        print_info("3. Verificar permisos de la carpeta actual")
        
    else:
        print_success("La carpeta actual es accesible")
    
    # Resumen
    print_section("RESUMEN")
    if carpeta_actual_ok:
        print_success("✅ Carpeta actual: ACCESIBLE")
    else:
        print_error("❌ Carpeta actual: NO ACCESIBLE")
        print_info("Revisa la lista de carpetas disponibles arriba")


if __name__ == "__main__":
    main()
