#!/usr/bin/env python3
"""
Script para crear la carpeta de destino en Google Drive
"""

import os
import json

def create_drive_folder():
    """Crea la carpeta de destino en Google Drive"""
    
    print("📁 CREANDO CARPETA EN GOOGLE DRIVE")
    print("=" * 40)
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Cargar credenciales
        credentials_path = "./credentials.json"
        if not os.path.exists(credentials_path):
            print("❌ No se encontró el archivo de credenciales")
            return None
        
        scopes = ['https://www.googleapis.com/auth/drive.file']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        
        # Crear servicio
        service = build('drive', 'v3', credentials=credentials)
        
        # Crear carpeta
        folder_metadata = {
            'name': 'RPA-TAMAPRINT-Archivos-Originales',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        print("🔄 Creando carpeta en Google Drive...")
        folder = service.files().create(
            body=folder_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        folder_id = folder.get('id')
        folder_name = folder.get('name')
        folder_link = folder.get('webViewLink')
        
        print(f"✅ Carpeta creada exitosamente!")
        print(f"📁 Nombre: {folder_name}")
        print(f"🆔 ID: {folder_id}")
        print(f"🔗 Enlace: {folder_link}")
        
        # Actualizar config.yaml con el nuevo ID
        update_config_with_folder_id(folder_id)
        
        return folder_id
        
    except Exception as e:
        print(f"❌ Error al crear carpeta: {e}")
        return None

def update_config_with_folder_id(folder_id):
    """Actualiza config.yaml con el nuevo ID de carpeta"""
    
    try:
        # Leer config.yaml
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Reemplazar el folder_id
        old_folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7"
        new_config_content = config_content.replace(old_folder_id, folder_id)
        
        # Escribir config.yaml actualizado
        with open('config.yaml', 'w', encoding='utf-8') as f:
            f.write(new_config_content)
        
        print(f"✅ Config.yaml actualizado con nuevo ID: {folder_id}")
        
    except Exception as e:
        print(f"⚠️  Error al actualizar config.yaml: {e}")

def list_my_folders():
    """Lista las carpetas disponibles en Google Drive"""
    
    print("\n📂 CARPETAS DISPONIBLES EN GOOGLE DRIVE")
    print("=" * 40)
    
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Cargar credenciales
        credentials_path = "./credentials.json"
        scopes = ['https://www.googleapis.com/auth/drive.file']
        credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        
        # Crear servicio
        service = build('drive', 'v3', credentials=credentials)
        
        # Listar carpetas
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            pageSize=10,
            fields="nextPageToken, files(id, name, webViewLink)"
        ).execute()
        
        folders = results.get('files', [])
        
        if not folders:
            print("📭 No se encontraron carpetas")
        else:
            print("📁 Carpetas encontradas:")
            for folder in folders:
                print(f"  • {folder['name']}")
                print(f"    ID: {folder['id']}")
                print(f"    Enlace: {folder['webViewLink']}")
                print()
        
        return folders
        
    except Exception as e:
        print(f"❌ Error al listar carpetas: {e}")
        return []

def main():
    """Función principal"""
    
    print("🚀 CONFIGURACIÓN DE CARPETA GOOGLE DRIVE")
    print("=" * 50)
    
    # Opción 1: Crear nueva carpeta
    print("1️⃣ Creando nueva carpeta...")
    new_folder_id = create_drive_folder()
    
    if new_folder_id:
        print(f"\n🎉 ¡CARPETA CREADA EXITOSAMENTE!")
        print(f"🆔 Nuevo ID: {new_folder_id}")
        print(f"🔗 Enlace: https://drive.google.com/drive/folders/{new_folder_id}")
        
        print(f"\n📋 PRÓXIMOS PASOS:")
        print("1. ✅ Carpeta creada en Google Drive")
        print("2. ✅ Config.yaml actualizado")
        print("3. 🚀 Ejecutar: python verificar_google_drive.py")
        print("4. 📁 Los archivos se subirán automáticamente")
    
    # Opción 2: Mostrar carpetas existentes
    print(f"\n2️⃣ Mostrando carpetas existentes...")
    list_my_folders()

if __name__ == "__main__":
    main()
