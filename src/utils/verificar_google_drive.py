#!/usr/bin/env python3
"""
Script de verificación para la configuración de Google Drive
Guía paso a paso y verifica cada componente
"""

import os
import json
import sys
from pathlib import Path

def check_credentials_file():
    """Verifica si existe el archivo de credenciales"""
    print("🔐 PASO 1: Verificando archivo de credenciales...")
    
    credential_paths = [
        "./credentials.json",
        "./google-credentials.json", 
        "./service-account.json"
    ]
    
    for path in credential_paths:
        if os.path.exists(path):
            print(f"✅ Credenciales encontradas: {path}")
            
            # Verificar que el archivo es válido
            try:
                with open(path, 'r') as f:
                    creds = json.load(f)
                
                # Verificar campos requeridos
                required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
                missing_fields = [field for field in required_fields if field not in creds]
                
                if not missing_fields:
                    print(f"✅ Archivo de credenciales válido")
                    print(f"📧 Email de cuenta de servicio: {creds.get('client_email', 'No encontrado')}")
                    print(f"🏢 Proyecto: {creds.get('project_id', 'No encontrado')}")
                    return path
                else:
                    print(f"❌ Archivo de credenciales incompleto. Faltan: {missing_fields}")
                    return None
                    
            except json.JSONDecodeError:
                print(f"❌ Archivo de credenciales no es un JSON válido")
                return None
            except Exception as e:
                print(f"❌ Error al leer credenciales: {e}")
                return None
    
    print("❌ No se encontraron credenciales")
    print("\n📋 Para crear credenciales:")
    print("1. Ve a https://console.cloud.google.com/")
    print("2. Crea un proyecto o selecciona uno existente")
    print("3. Habilita Google Drive API")
    print("4. Crea credenciales de cuenta de servicio")
    print("5. Descarga el archivo JSON")
    print("6. Guárdalo como 'credentials.json' en esta carpeta")
    
    return None

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n📦 PASO 2: Verificando dependencias...")
    
    try:
        import google.auth
        import googleapiclient.discovery
        print("✅ Dependencias de Google Drive instaladas correctamente")
        return True
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("\n💡 Instala las dependencias con:")
        print("pip install google-auth google-api-python-client")
        return False

def test_google_drive_connection(credentials_path):
    """Prueba la conexión con Google Drive"""
    print("\n🔗 PASO 3: Probando conexión con Google Drive...")
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Cargar credenciales
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        
        # Crear servicio
        service = build('drive', 'v3', credentials=credentials)
        
        # Probar acceso
        about = service.about().get(fields='user').execute()
        print("✅ Conexión con Google Drive exitosa")
        print(f"👤 Usuario autenticado: {about.get('user', {}).get('emailAddress', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_folder_access():
    """Prueba acceso a la carpeta específica"""
    print("\n📁 PASO 4: Verificando acceso a la carpeta de destino...")
    
    folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
    
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
            print("❌ No se encontraron credenciales para la prueba")
            return False
        
        # Cargar credenciales
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        
        # Crear servicio
        service = build('drive', 'v3', credentials=credentials)
        
        # Probar acceso a la carpeta
        try:
            folder = service.files().get(fileId=folder_id, fields='id,name,permissions').execute()
            print(f"✅ Carpeta encontrada: {folder.get('name', 'Sin nombre')}")
            print(f"🆔 ID de carpeta: {folder.get('id')}")
            
            # Verificar permisos
            permissions = folder.get('permissions', [])
            service_account_email = credentials.service_account_email
            
            has_access = any(
                perm.get('emailAddress') == service_account_email 
                for perm in permissions
            )
            
            if has_access:
                print("✅ La cuenta de servicio tiene acceso a la carpeta")
                return True
            else:
                print("❌ La cuenta de servicio NO tiene acceso a la carpeta")
                print(f"📧 Email de la cuenta: {service_account_email}")
                print("\n💡 Para solucionarlo:")
                print("1. Abre la carpeta en Google Drive")
                print("2. Clic derecho > Compartir")
                print("3. Agrega el email de la cuenta de servicio")
                print("4. Dale permisos de 'Editor'")
                return False
                
        except Exception as e:
            print(f"❌ Error al acceder a la carpeta: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_file_upload():
    """Prueba subir un archivo de prueba"""
    print("\n📤 PASO 5: Probando subida de archivo...")
    
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        drive_uploader = GoogleDriveOAuthUploader()
        
        # Crear archivo de prueba
        test_file = "./test_upload.txt"
        with open(test_file, 'w') as f:
            f.write("Archivo de prueba para Google Drive")
        
        print(f"📄 Archivo de prueba creado: {test_file}")
        
        # Intentar subir
        result = drive_uploader.upload_file(test_file, "test_upload.txt")
        
        if result and result.get('success'):
            print("✅ Subida de archivo exitosa")
            print(f"🆔 ID del archivo: {result.get('id')}")
            print(f"🔗 Enlace: {result.get('link')}")
            
            # Limpiar archivo de prueba
            os.remove(test_file)
            return True
        else:
            print("❌ Error en la subida de archivo")
            if result:
                print(f"Error: {result.get('error', 'Desconocido')}")
            
            # Limpiar archivo de prueba
            if os.path.exists(test_file):
                os.remove(test_file)
            return False
            
    except Exception as e:
        print(f"❌ Error en la prueba de subida: {e}")
        return False

def show_next_steps():
    """Muestra los próximos pasos"""
    print("\n🎯 PRÓXIMOS PASOS:")
    print("=" * 30)
    print("1. ✅ Configurar credenciales de Google Drive")
    print("2. ✅ Compartir la carpeta con la cuenta de servicio")
    print("3. ✅ Probar la conexión")
    print("4. 🚀 Ejecutar el RPA normalmente")
    print("5. 📁 Los archivos se subirán automáticamente")
    
    print("\n📊 MONITOREO:")
    print("- Revisa los logs en ./logs/rpa.log")
    print("- Los archivos aparecerán en la carpeta de Google Drive")
    print("- Cada subida se registra con detalles completos")

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN COMPLETA DE GOOGLE DRIVE")
    print("=" * 50)
    
    # Verificar credenciales
    credentials_path = check_credentials_file()
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    
    # Verificar conexión
    connection_ok = False
    folder_ok = False
    upload_ok = False
    
    if credentials_path and deps_ok:
        connection_ok = test_google_drive_connection(credentials_path)
        
        if connection_ok:
            folder_ok = test_folder_access()
            
            if folder_ok:
                upload_ok = test_file_upload()
    
    # Resumen final
    print("\n📋 RESUMEN DE VERIFICACIÓN:")
    print("=" * 30)
    print(f"{'✅' if credentials_path else '❌'} Credenciales configuradas")
    print(f"{'✅' if deps_ok else '❌'} Dependencias instaladas")
    print(f"{'✅' if connection_ok else '❌'} Conexión con Google Drive")
    print(f"{'✅' if folder_ok else '❌'} Acceso a carpeta")
    print(f"{'✅' if upload_ok else '❌'} Subida de archivos")
    
    if all([credentials_path, deps_ok, connection_ok, folder_ok, upload_ok]):
        print("\n🎉 ¡CONFIGURACIÓN COMPLETA!")
        print("El sistema está listo para subir archivos a Google Drive")
        show_next_steps()
    else:
        print("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        print("Revisa los errores anteriores para completar la configuración")

if __name__ == "__main__":
    main()
