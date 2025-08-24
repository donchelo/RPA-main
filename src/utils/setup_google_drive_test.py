#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración y Verificación de Google Drive
============================================

Este script ayuda a configurar y verificar la integración con Google Drive
para el sistema RPA TAMAPRINT.

Pasos que realiza:
1. Verifica dependencias instaladas
2. Ayuda a configurar credenciales
3. Prueba la conexión con Google Drive
4. Verifica permisos de carpeta
"""

import os
import sys
import json
import time
from pathlib import Path

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def print_section(title):
    """Imprime una sección formateada"""
    print(f"\n📋 {title}")
    print("-" * 40)

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

def check_dependencies():
    """Verifica que las dependencias de Google Drive estén instaladas"""
    print_section("Verificando Dependencias")
    
    required_packages = [
        ('google-auth', 'google.auth'),
        ('google-api-python-client', 'googleapiclient'),
        ('google-auth-oauthlib', 'google_auth_oauthlib'),
        ('google-auth-httplib2', 'google_auth_httplib2')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print_success(f"{package_name} está instalado")
        except ImportError:
            print_error(f"{package_name} NO está instalado")
            missing_packages.append(package_name)
    
    if missing_packages:
        print_warning("Para instalar las dependencias faltantes, ejecuta:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_credentials():
    """Verifica si existen credenciales de Google Drive"""
    print_section("Verificando Credenciales")
    
    possible_paths = [
        "./credentials.json",
        "./google-credentials.json",
        "./service-account.json",
        "./external/validador-tamaprint/credentials.json"
    ]
    
    credentials_found = False
    
    for path in possible_paths:
        if os.path.exists(path):
            print_success(f"Credenciales encontradas en: {path}")
            credentials_found = True
            
            # Verificar que el archivo es válido
            try:
                with open(path, 'r') as f:
                    cred_data = json.load(f)
                
                # Verificar campos básicos de credenciales de servicio
                if 'type' in cred_data and cred_data['type'] == 'service_account':
                    print_success("Archivo de credenciales válido (cuenta de servicio)")
                else:
                    print_warning("El archivo parece no ser de cuenta de servicio")
                    
            except json.JSONDecodeError:
                print_error(f"El archivo {path} no es un JSON válido")
            except Exception as e:
                print_error(f"Error al leer {path}: {e}")
        else:
            print_info(f"No encontrado: {path}")
    
    if not credentials_found:
        print_error("No se encontraron credenciales de Google Drive")
        print_info("Para configurar credenciales:")
        print_info("1. Ve a Google Cloud Console: https://console.cloud.google.com/")
        print_info("2. Crea un proyecto o selecciona uno existente")
        print_info("3. Habilita la API de Google Drive")
        print_info("4. Crea credenciales de cuenta de servicio")
        print_info("5. Descarga el archivo JSON y guárdalo como 'credentials.json'")
    
    return credentials_found

def test_google_drive_connection():
    """Prueba la conexión con Google Drive"""
    print_section("Probando Conexión con Google Drive")
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Buscar credenciales
        credentials_path = None
        possible_paths = [
            "./credentials.json",
            "./google-credentials.json",
            "./service-account.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                credentials_path = path
                break
        
        if not credentials_path:
            print_error("No se encontraron credenciales para probar")
            return False
        
        # Autenticar
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        
        # Construir servicio
        service = build('drive', 'v3', credentials=credentials)
        
        # Probar conexión listando archivos
        print_info("Probando conexión...")
        results = service.files().list(pageSize=1).execute()
        
        print_success("Conexión exitosa con Google Drive API")
        return True
        
    except Exception as e:
        print_error(f"Error al conectar con Google Drive: {e}")
        return False

def test_folder_access():
    """Prueba el acceso a la carpeta configurada"""
    print_section("Verificando Acceso a Carpeta")
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Buscar credenciales
        credentials_path = None
        for path in ["./credentials.json", "./google-credentials.json", "./service-account.json"]:
            if os.path.exists(path):
                credentials_path = path
                break
        
        if not credentials_path:
            print_error("No se encontraron credenciales")
            return False
        
        # Autenticar
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        service = build('drive', 'v3', credentials=credentials)
        
        # ID de carpeta desde config.yaml
        folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        
        print_info(f"Verificando acceso a carpeta: {folder_id}")
        
        # Intentar obtener información de la carpeta
        try:
            folder = service.files().get(fileId=folder_id).execute()
            print_success(f"Acceso exitoso a carpeta: {folder.get('name', 'Sin nombre')}")
            return True
        except Exception as e:
            print_error(f"No se puede acceder a la carpeta: {e}")
            print_info("Asegúrate de que:")
            print_info("1. La carpeta existe en Google Drive")
            print_info("2. La cuenta de servicio tiene permisos de 'Editor'")
            print_info("3. El ID de carpeta es correcto")
            return False
            
    except Exception as e:
        print_error(f"Error al verificar carpeta: {e}")
        return False

def create_test_upload():
    """Crea un archivo de prueba y lo sube a Google Drive"""
    print_section("Probando Subida de Archivo")
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        # Buscar credenciales
        credentials_path = None
        for path in ["./credentials.json", "./google-credentials.json", "./service-account.json"]:
            if os.path.exists(path):
                credentials_path = path
                break
        
        if not credentials_path:
            print_error("No se encontraron credenciales")
            return False
        
        # Autenticar
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        service = build('drive', 'v3', credentials=credentials)
        
        # Crear archivo de prueba
        test_content = "Este es un archivo de prueba para verificar la integración con Google Drive.\nCreado el: " + time.strftime("%Y-%m-%d %H:%M:%S")
        test_file_path = "./test_google_drive_upload.txt"
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print_info(f"Archivo de prueba creado: {test_file_path}")
        
        # Subir archivo
        folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        
        file_metadata = {
            'name': 'test_upload.txt',
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(test_file_path, resumable=True)
        
        print_info("Subiendo archivo de prueba...")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        print_success(f"Archivo subido exitosamente")
        print_info(f"ID: {file.get('id')}")
        print_info(f"Enlace: {file.get('webViewLink')}")
        
        # Limpiar archivo local
        os.remove(test_file_path)
        print_info("Archivo local eliminado")
        
        return True
        
    except Exception as e:
        print_error(f"Error al subir archivo de prueba: {e}")
        return False

def main():
    """Función principal"""
    print_header("CONFIGURACIÓN Y VERIFICACIÓN DE GOOGLE DRIVE")
    
    print("Este script verificará y configurará la integración con Google Drive")
    print("para el sistema RPA TAMAPRINT.")
    
    # Agregar retraso inicial según la memoria del usuario
    print("\n⏳ Esperando 5 segundos para permitir cambio manual a pantalla adecuada...")
    time.sleep(5)
    
    results = []
    
    # 1. Verificar dependencias
    if check_dependencies():
        results.append(("Dependencias", True))
    else:
        results.append(("Dependencias", False))
        print_error("❌ Instala las dependencias faltantes antes de continuar")
        return False
    
    # 2. Verificar credenciales
    if check_credentials():
        results.append(("Credenciales", True))
    else:
        results.append(("Credenciales", False))
        print_error("❌ Configura las credenciales antes de continuar")
        return False
    
    # 3. Probar conexión
    if test_google_drive_connection():
        results.append(("Conexión", True))
    else:
        results.append(("Conexión", False))
        print_error("❌ Error en la conexión con Google Drive")
        return False
    
    # 4. Verificar acceso a carpeta
    if test_folder_access():
        results.append(("Acceso a carpeta", True))
    else:
        results.append(("Acceso a carpeta", False))
        print_error("❌ Error en el acceso a la carpeta")
        return False
    
    # 5. Probar subida
    if create_test_upload():
        results.append(("Subida de archivos", True))
    else:
        results.append(("Subida de archivos", False))
        print_error("❌ Error en la subida de archivos")
        return False
    
    # Mostrar resumen
    print_header("RESUMEN DE VERIFICACIÓN")
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        if success:
            print_success(f"{test_name}: PASÓ")
            passed += 1
        else:
            print_error(f"{test_name}: FALLÓ")
    
    print(f"\n📊 Resultados: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print_success("🎉 ¡TODA LA CONFIGURACIÓN ESTÁ CORRECTA!")
        print("La integración con Google Drive está lista para usar.")
        print("\nEl sistema RPA ahora puede:")
        print("- Subir archivos PNG y PDF automáticamente")
        print("- Buscar archivos originales en múltiples ubicaciones")
        print("- Registrar enlaces a archivos subidos")
        return True
    else:
        print_error(f"⚠️  {total - passed} verificación(es) fallaron")
        print("Revisa los errores y vuelve a ejecutar este script")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Configuración interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
