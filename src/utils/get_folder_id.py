#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obtener ID de Carpeta "Terminados"
==================================

Este script busca específicamente la carpeta "Terminados" en Google Drive
y obtiene su ID para configurar la subida de archivos.
"""

import os
import sys
import json
import pickle

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"📁 {title}")
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

def get_terminados_folder_id():
    """Obtiene el ID de la carpeta 'Terminados'"""
    print_header("BUSCANDO CARPETA 'TERMINADOS'")
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        # Scopes necesarios
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        creds = None
        credentials_path = "./oauth_credentials.json"
        token_path = "./token.pickle"
        
        # Verificar si existe un token guardado
        if os.path.exists(token_path):
            print_info("Cargando token existente...")
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Si no hay credenciales válidas, autenticar
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print_info("Refrescando token...")
                creds.refresh(Request())
            else:
                print_info("Iniciando flujo de autenticación OAuth...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Guardar credenciales para la próxima vez
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # Construir servicio
        service = build('drive', 'v3', credentials=creds)
        print_success("Conexión exitosa con Google Drive")
        
        # Buscar específicamente la carpeta "Terminados"
        print_section("Buscando Carpeta 'Terminados'")
        
        query = "name='Terminados' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(
            q=query,
            fields="files(id, name, createdTime, parents)"
        ).execute()
        
        folders = results.get('files', [])
        
        if not folders:
            print_error("No se encontró la carpeta 'Terminados'")
            print_info("Creando la carpeta 'Terminados'...")
            
            # Crear la carpeta si no existe
            folder_metadata = {
                'name': 'Terminados',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = service.files().create(
                body=folder_metadata,
                fields='id,name'
            ).execute()
            
            folder_id = folder.get('id')
            folder_name = folder.get('name')
            
            print_success(f"Carpeta '{folder_name}' creada exitosamente")
            print_info(f"ID de la carpeta: {folder_id}")
            
        else:
            folder = folders[0]  # Tomar la primera carpeta encontrada
            folder_id = folder.get('id')
            folder_name = folder.get('name')
            created_time = folder.get('createdTime', 'N/A')
            
            print_success(f"Carpeta '{folder_name}' encontrada")
            print_info(f"ID de la carpeta: {folder_id}")
            print_info(f"Creada: {created_time}")
        
        # Mostrar información de configuración
        print_section("Configuración Requerida")
        print_info("Para configurar la subida a esta carpeta:")
        print_info("1. Actualiza el archivo config.yaml:")
        print_info("   google_drive:")
        print_info(f"     folder_id: \"{folder_id}\"")
        print_info("2. O actualiza directamente el código del RPA")
        
        # Crear archivo de configuración temporal
        config_info = {
            "google_drive": {
                "folder_id": folder_id,
                "folder_name": folder_name,
                "enabled": True,
                "upload_original_files": True
            }
        }
        
        with open("folder_config.json", "w") as f:
            json.dump(config_info, f, indent=2)
        
        print_success("Archivo de configuración temporal creado: folder_config.json")
        
        return folder_id
        
    except Exception as e:
        print_error(f"Error al buscar la carpeta: {e}")
        return None

def main():
    """Función principal"""
    print("🔍 Buscando carpeta 'Terminados' en Google Drive")
    print("Esto configurará la carpeta correcta para la subida de archivos")
    
    try:
        folder_id = get_terminados_folder_id()
        
        if folder_id:
            print("\n✅ Configuración completada exitosamente")
            print(f"Los archivos se subirán a la carpeta con ID: {folder_id}")
            print("Actualiza la configuración del RPA con este ID")
        else:
            print("\n❌ Error al obtener el ID de la carpeta")
        
        return 0 if folder_id else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Operación interrumpida por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
