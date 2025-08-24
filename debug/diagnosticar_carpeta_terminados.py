#!/usr/bin/env python3
"""
Script para diagnosticar por qué la carpeta 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv no es accesible via API
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


def print_warning(message):
    """Imprime un mensaje de advertencia"""
    print(f"⚠️  {message}")


def verificar_usuario_autenticado():
    """Verifica qué usuario está autenticado"""
    print_section("Verificando Usuario Autenticado")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio")
            return None
        
        # Obtener información del usuario
        about = uploader.service.about().get(fields='user').execute()
        user = about.get('user', {})
        
        if user:
            print_success(f"Usuario autenticado: {user.get('displayName', 'N/A')}")
            print_info(f"Email: {user.get('emailAddress', 'N/A')}")
            print_info(f"ID: {user.get('permissionId', 'N/A')}")
            return user
        else:
            print_error("No se pudo obtener información del usuario")
            return None
            
    except Exception as e:
        print_error(f"Error verificando usuario: {str(e)}")
        return None


def listar_carpetas_accesibles():
    """Lista todas las carpetas accesibles"""
    print_section("Listando Carpetas Accesibles")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio")
            return []
        
        # Listar todas las carpetas
        results = uploader.service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name, webViewLink, owners, permissions)",
            pageSize=50
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            print_success(f"Se encontraron {len(folders)} carpetas accesibles:")
            
            for folder in folders:
                print_info(f"📁 {folder.get('name', 'Sin nombre')}")
                print_info(f"   ID: {folder.get('id')}")
                print_info(f"   Enlace: {folder.get('webViewLink')}")
                
                # Verificar propietario
                owners = folder.get('owners', [])
                if owners:
                    owner = owners[0]
                    print_info(f"   Propietario: {owner.get('displayName', 'N/A')} ({owner.get('emailAddress', 'N/A')})")
                
                print()
        else:
            print_warning("No se encontraron carpetas accesibles")
        
        return folders
        
    except Exception as e:
        print_error(f"Error listando carpetas: {str(e)}")
        return []


def buscar_carpeta_por_nombre():
    """Busca carpetas por nombre similar a 'Terminados'"""
    print_section("Buscando Carpetas por Nombre")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio")
            return []
        
        # Buscar carpetas con nombres similares
        search_terms = ['terminados', 'terminado', 'finalizado', 'completado', 'rpa']
        
        found_folders = []
        
        for term in search_terms:
            results = uploader.service.files().list(
                q=f"mimeType='application/vnd.google-apps.folder' and name contains '{term}'",
                fields="files(id, name, webViewLink, owners)",
                pageSize=10
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                print_info(f"Carpetas encontradas con '{term}':")
                for folder in folders:
                    print_info(f"  📁 {folder.get('name')} (ID: {folder.get('id')})")
                    found_folders.extend(folders)
        
        if not found_folders:
            print_warning("No se encontraron carpetas con nombres similares")
        
        return found_folders
        
    except Exception as e:
        print_error(f"Error buscando carpetas: {str(e)}")
        return []


def intentar_acceder_carpeta_especifica():
    """Intenta acceder a la carpeta específica con diferentes métodos"""
    print_section("Intentando Acceder a Carpeta Específica")
    
    folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio")
            return False
        
        # Método 1: Intentar obtener información básica
        print_info("Método 1: Obtener información básica...")
        try:
            folder = uploader.service.files().get(
                fileId=folder_id,
                fields='id,name,webViewLink'
            ).execute()
            
            print_success(f"Carpeta encontrada: {folder.get('name')}")
            print_info(f"ID: {folder.get('id')}")
            print_info(f"Enlace: {folder.get('webViewLink')}")
            return True
            
        except Exception as e:
            print_error(f"Error método 1: {str(e)}")
        
        # Método 2: Intentar listar contenido
        print_info("Método 2: Listar contenido...")
        try:
            results = uploader.service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name)",
                pageSize=1
            ).execute()
            
            print_success("Se puede acceder al contenido de la carpeta")
            return True
            
        except Exception as e:
            print_error(f"Error método 2: {str(e)}")
        
        # Método 3: Intentar crear un archivo de prueba
        print_info("Método 3: Crear archivo de prueba...")
        try:
            test_file_path = './test_access.txt'
            with open(test_file_path, 'w') as f:
                f.write("Prueba de acceso a carpeta")
            
            result = uploader.upload_file(test_file_path, "test_access.txt")
            
            if result and result.get('success'):
                print_success("Se puede escribir en la carpeta")
                # Limpiar archivo de prueba
                try:
                    os.remove(test_file_path)
                    file_id = result.get('id')
                    if file_id:
                        uploader.service.files().delete(fileId=file_id).execute()
                except:
                    pass
                return True
            else:
                print_error("No se puede escribir en la carpeta")
                
        except Exception as e:
            print_error(f"Error método 3: {str(e)}")
        
        return False
        
    except Exception as e:
        print_error(f"Error general: {str(e)}")
        return False


def verificar_permisos_especiales():
    """Verifica permisos especiales y configuraciones"""
    print_section("Verificando Permisos Especiales")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("No se pudo inicializar el servicio")
            return
        
        # Verificar scopes del token
        print_info("Verificando scopes del token...")
        try:
            import pickle
            with open('./token.pickle', 'rb') as f:
                token = pickle.load(f)
            
            if hasattr(token, 'scopes'):
                print_info(f"Scopes actuales: {token.scopes}")
                
                required_scopes = [
                    'https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/drive',
                    'https://www.googleapis.com/auth/drive.readonly'
                ]
                
                for scope in required_scopes:
                    if scope in token.scopes:
                        print_success(f"Scope presente: {scope}")
                    else:
                        print_warning(f"Scope faltante: {scope}")
            else:
                print_warning("No se pueden verificar los scopes")
                
        except Exception as e:
            print_error(f"Error verificando scopes: {str(e)}")
        
        # Verificar configuración de la API
        print_info("Verificando configuración de la API...")
        try:
            about = uploader.service.about().get(fields='importFormats,exportFormats').execute()
            print_success("API configurada correctamente")
        except Exception as e:
            print_error(f"Error en configuración de API: {str(e)}")
        
    except Exception as e:
        print_error(f"Error verificando permisos: {str(e)}")


def generar_recomendaciones():
    """Genera recomendaciones basadas en los resultados"""
    print_section("Recomendaciones")
    
    print_info("Basado en el diagnóstico, aquí están las posibles soluciones:")
    print()
    
    print_info("1. 📁 VERIFICAR PROPIEDAD DE LA CARPETA")
    print_info("   - La carpeta puede pertenecer a otra cuenta de Google")
    print_info("   - Verificar que esté compartida con mgarciap333@gmail.com")
    print_info("   - Comprobar permisos de acceso (lectura/escritura)")
    print()
    
    print_info("2. 🔗 COMPARTIR LA CARPETA")
    print_info("   - Ir a https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
    print_info("   - Hacer clic en 'Compartir'")
    print_info("   - Agregar mgarciap333@gmail.com con permisos de 'Editor'")
    print()
    
    print_info("3. 🔄 USAR CARPETA ALTERNATIVA")
    print_info("   - Crear una nueva carpeta en tu Google Drive")
    print_info("   - Usar una de las carpetas accesibles encontradas")
    print_info("   - Actualizar la configuración del RPA")
    print()
    
    print_info("4. 🔑 VERIFICAR AUTENTICACIÓN")
    print_info("   - Eliminar token.pickle y reautenticarse")
    print_info("   - Verificar que la cuenta correcta esté autenticada")
    print_info("   - Comprobar que los scopes incluyan drive.file")
    print()


def main():
    """Función principal del script"""
    print_section("DIAGNÓSTICO CARPETA TERMINADOS")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Diagnosticando por qué la carpeta 17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv no es accesible...")
    
    # Verificar usuario autenticado
    user = verificar_usuario_autenticado()
    
    # Listar carpetas accesibles
    accessible_folders = listar_carpetas_accesibles()
    
    # Buscar carpetas por nombre
    similar_folders = buscar_carpeta_por_nombre()
    
    # Intentar acceder a la carpeta específica
    can_access = intentar_acceder_carpeta_especifica()
    
    # Verificar permisos especiales
    verificar_permisos_especiales()
    
    # Generar recomendaciones
    generar_recomendaciones()
    
    # Resumen final
    print_section("RESUMEN DEL DIAGNÓSTICO")
    
    if can_access:
        print_success("✅ La carpeta es accesible")
    else:
        print_error("❌ La carpeta no es accesible")
        print_info(f"📁 Carpetas accesibles encontradas: {len(accessible_folders)}")
        print_info(f"🔍 Carpetas similares encontradas: {len(similar_folders)}")
    
    if user:
        print_info(f"👤 Usuario autenticado: {user.get('emailAddress', 'N/A')}")


if __name__ == "__main__":
    main()
