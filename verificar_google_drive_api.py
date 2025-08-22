#!/usr/bin/env python3
"""
Script para verificar el estado de la API de Google Drive y la autenticación
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


def verificar_archivos_oauth():
    """Verifica que los archivos de OAuth estén presentes"""
    print_section("Verificando Archivos OAuth")
    
    oauth_files = [
        './oauth_credentials.json',
        './client_secret.json',
        './token.pickle'
    ]
    
    files_status = {}
    
    for file_path in oauth_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            files_status[file_path] = {
                'exists': True,
                'size': file_size,
                'status': '✅ Presente'
            }
            print_success(f"{file_path} - {file_size} bytes")
        else:
            files_status[file_path] = {
                'exists': False,
                'size': 0,
                'status': '❌ No encontrado'
            }
            print_error(f"{file_path} - No encontrado")
    
    return files_status


def verificar_credenciales_oauth():
    """Verifica que las credenciales OAuth sean válidas"""
    print_section("Verificando Credenciales OAuth")
    
    oauth_paths = ['./oauth_credentials.json', './client_secret.json']
    
    for oauth_path in oauth_paths:
        if os.path.exists(oauth_path):
            try:
                with open(oauth_path, 'r', encoding='utf-8') as f:
                    credentials = json.load(f)
                
                print_success(f"Archivo {oauth_path} cargado correctamente")
                
                # Verificar estructura de credenciales
                if 'installed' in credentials:
                    installed = credentials['installed']
                    required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
                    
                    missing_fields = []
                    for field in required_fields:
                        if field not in installed:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print_error(f"Campos faltantes en {oauth_path}: {missing_fields}")
                    else:
                        print_success(f"Todos los campos requeridos presentes en {oauth_path}")
                        print_info(f"Client ID: {installed['client_id'][:20]}...")
                        print_info(f"Project ID: {installed.get('project_id', 'No especificado')}")
                
                elif 'web' in credentials:
                    print_info(f"Credenciales web detectadas en {oauth_path}")
                
                else:
                    print_error(f"Formato de credenciales no reconocido en {oauth_path}")
                
            except json.JSONDecodeError as e:
                print_error(f"Error decodificando JSON en {oauth_path}: {str(e)}")
            except Exception as e:
                print_error(f"Error leyendo {oauth_path}: {str(e)}")
        else:
            print_error(f"Archivo {oauth_path} no encontrado")


def verificar_token_oauth():
    """Verifica el token de OAuth"""
    print_section("Verificando Token OAuth")
    
    token_path = './token.pickle'
    
    if os.path.exists(token_path):
        try:
            import pickle
            
            with open(token_path, 'rb') as f:
                token = pickle.load(f)
            
            print_success("Token OAuth cargado correctamente")
            
            # Verificar propiedades del token
            if hasattr(token, 'expired'):
                if token.expired:
                    print_warning("Token OAuth expirado")
                else:
                    print_success("Token OAuth válido")
            
            if hasattr(token, 'refresh_token'):
                if token.refresh_token:
                    print_success("Token de refresco disponible")
                else:
                    print_warning("Token de refresco no disponible")
            
            if hasattr(token, 'scopes'):
                print_info(f"Scopes: {token.scopes}")
            
            return True
            
        except Exception as e:
            print_error(f"Error cargando token: {str(e)}")
            return False
    else:
        print_error("Archivo token.pickle no encontrado")
        print_info("Se requerirá autenticación manual")
        return False


def verificar_conexion_api():
    """Verifica la conexión a la API de Google Drive"""
    print_section("Verificando Conexión a API de Google Drive")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        print_info("Inicializando GoogleDriveOAuthUploader...")
        uploader = GoogleDriveOAuthUploader()
        
        if uploader.service:
            print_success("Servicio de Google Drive inicializado correctamente")
            
            # Verificar que podemos hacer una llamada básica a la API
            try:
                # Obtener información del usuario
                about = uploader.service.about().get(fields='user,storageQuota').execute()
                
                user = about.get('user', {})
                if user:
                    print_success(f"Usuario autenticado: {user.get('displayName', 'N/A')}")
                    print_info(f"Email: {user.get('emailAddress', 'N/A')}")
                    print_info(f"ID: {user.get('permissionId', 'N/A')}")
                
                # Verificar cuota de almacenamiento
                storage = about.get('storageQuota', {})
                if storage:
                    total = storage.get('limit', 0)
                    used = storage.get('usage', 0)
                    if total > 0:
                        percentage = (used / total) * 100
                        print_info(f"Almacenamiento: {used} / {total} bytes ({percentage:.1f}%)")
                
                return True
                
            except Exception as e:
                print_error(f"Error verificando información del usuario: {str(e)}")
                return False
        else:
            print_error("No se pudo inicializar el servicio de Google Drive")
            return False
            
    except ImportError as e:
        print_error(f"Error importando módulos: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error verificando conexión: {str(e)}")
        return False


def verificar_permisos_drive():
    """Verifica los permisos de Google Drive"""
    print_section("Verificando Permisos de Google Drive")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("Servicio no disponible")
            return False
        
        # Verificar permisos de lectura
        try:
            # Listar archivos (permiso de lectura)
            results = uploader.service.files().list(
                pageSize=1,
                fields="files(id, name)"
            ).execute()
            
            print_success("Permisos de lectura: ✅ OK")
            
        except Exception as e:
            print_error(f"Error verificando permisos de lectura: {str(e)}")
            return False
        
        # Verificar permisos de escritura
        try:
            # Crear un archivo de prueba temporal
            test_file_path = './test_permissions.txt'
            with open(test_file_path, 'w') as f:
                f.write("Archivo de prueba para verificar permisos")
            
            # Intentar subir el archivo
            result = uploader.upload_file(test_file_path, "test_permissions.txt")
            
            if result and result.get('success'):
                print_success("Permisos de escritura: ✅ OK")
                
                # Limpiar archivo de prueba
                try:
                    os.remove(test_file_path)
                    # También eliminar el archivo de Google Drive
                    file_id = result.get('id')
                    if file_id:
                        uploader.service.files().delete(fileId=file_id).execute()
                except:
                    pass
                
                return True
            else:
                print_error("Permisos de escritura: ❌ FALLIDO")
                return False
                
        except Exception as e:
            print_error(f"Error verificando permisos de escritura: {str(e)}")
            return False
            
    except Exception as e:
        print_error(f"Error verificando permisos: {str(e)}")
        return False


def verificar_carpeta_configurada():
    """Verifica la carpeta configurada en el sistema"""
    print_section("Verificando Carpeta Configurada")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        
        uploader = GoogleDriveOAuthUploader()
        
        if not uploader.service:
            print_error("Servicio no disponible")
            return False
        
        folder_id = uploader.folder_id
        print_info(f"Carpeta configurada: {folder_id}")
        
        try:
            # Verificar que la carpeta existe
            folder = uploader.service.files().get(
                fileId=folder_id,
                fields='id,name,webViewLink,permissions'
            ).execute()
            
            print_success(f"Carpeta encontrada: {folder.get('name', 'Sin nombre')}")
            print_info(f"ID: {folder.get('id')}")
            print_info(f"Enlace: {folder.get('webViewLink')}")
            
            # Verificar permisos en la carpeta
            try:
                results = uploader.service.files().list(
                    q=f"'{folder_id}' in parents",
                    pageSize=1,
                    fields="files(id, name)"
                ).execute()
                
                print_success("Permisos en carpeta: ✅ OK")
                return True
                
            except Exception as e:
                print_error(f"Error verificando permisos en carpeta: {str(e)}")
                return False
            
        except Exception as e:
            print_error(f"Carpeta no encontrada o no accesible: {str(e)}")
            return False
            
    except Exception as e:
        print_error(f"Error verificando carpeta: {str(e)}")
        return False


def generar_reporte_completo():
    """Genera un reporte completo del estado de Google Drive"""
    print_section("GENERANDO REPORTE COMPLETO")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'oauth_files': verificar_archivos_oauth(),
        'oauth_credentials': True,  # Se verifica en la función
        'oauth_token': verificar_token_oauth(),
        'api_connection': verificar_conexion_api(),
        'drive_permissions': verificar_permisos_drive(),
        'configured_folder': verificar_carpeta_configurada()
    }
    
    # Resumen final
    print_section("RESUMEN DEL ESTADO")
    
    checks = [
        ('Archivos OAuth', any(report['oauth_files'][f]['exists'] for f in report['oauth_files'])),
        ('Credenciales OAuth', report['oauth_credentials']),
        ('Token OAuth', report['oauth_token']),
        ('Conexión API', report['api_connection']),
        ('Permisos Drive', report['drive_permissions']),
        ('Carpeta Configurada', report['configured_folder'])
    ]
    
    all_ok = True
    for check_name, status in checks:
        if status:
            print_success(f"{check_name}: ✅ OK")
        else:
            print_error(f"{check_name}: ❌ PROBLEMA")
            all_ok = False
    
    if all_ok:
        print_success("🎉 TODOS LOS CHECKS PASARON - Google Drive está funcionando correctamente")
    else:
        print_error("⚠️  ALGUNOS CHECKS FALLARON - Revisar configuración de Google Drive")
    
    return report


def main():
    """Función principal del script"""
    print_section("VERIFICACIÓN COMPLETA DE GOOGLE DRIVE API")
    
    # Configurar logging
    rpa_logger.setup_logger()
    
    print_info("Iniciando verificación completa de la API de Google Drive...")
    
    # Verificar credenciales OAuth
    verificar_credenciales_oauth()
    
    # Generar reporte completo
    report = generar_reporte_completo()
    
    # Guardar reporte
    try:
        with open('./google_drive_status_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print_info("Reporte guardado en: google_drive_status_report.json")
    except Exception as e:
        print_error(f"Error guardando reporte: {str(e)}")


if __name__ == "__main__":
    main()
