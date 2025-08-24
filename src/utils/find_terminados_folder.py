#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscar Carpeta "Terminados"
===========================

Este script busca la carpeta "Terminados" en Google Drive
y obtiene su ID correcto.
"""

import os
import sys
import json
import pickle

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
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

def find_terminados_folder():
    """Busca la carpeta Terminados en Google Drive"""
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
        
        # Buscar todas las carpetas
        print_section("Buscando Todas las Carpetas")
        
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            pageSize=100,
            fields="nextPageToken, files(id, name, createdTime, parents)"
        ).execute()
        
        folders = results.get('files', [])
        
        if not folders:
            print_error("No se encontraron carpetas")
            return None
        
        print_info(f"Se encontraron {len(folders)} carpetas:")
        print()
        
        terminados_folders = []
        
        for i, folder in enumerate(folders, 1):
            folder_id = folder.get('id')
            folder_name = folder.get('name', 'Sin nombre')
            created_time = folder.get('createdTime', 'N/A')
            
            print(f"{i:2d}. 📁 {folder_name}")
            print(f"    ID: {folder_id}")
            print(f"    Creado: {created_time}")
            print()
            
            # Buscar carpetas que contengan "terminados" (case insensitive)
            if "terminados" in folder_name.lower():
                terminados_folders.append(folder)
        
        # Mostrar carpetas que coinciden con "terminados"
        if terminados_folders:
            print_section("Carpetas que Coinciden con 'Terminados'")
            for i, folder in enumerate(terminados_folders, 1):
                folder_id = folder.get('id')
                folder_name = folder.get('name')
                created_time = folder.get('createdTime', 'N/A')
                
                print(f"{i}. 📁 {folder_name}")
                print(f"   ID: {folder_id}")
                print(f"   Creado: {created_time}")
                print()
        else:
            print_warning("No se encontraron carpetas con 'terminados' en el nombre")
        
        # Buscar también archivos recientes para referencia
        print_section("Archivos Recientes (últimos 5)")
        
        results = service.files().list(
            pageSize=5,
            orderBy="modifiedTime desc",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, parents)"
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            for i, file in enumerate(files, 1):
                file_id = file.get('id')
                file_name = file.get('name', 'Sin nombre')
                mime_type = file.get('mimeType', 'N/A')
                modified_time = file.get('modifiedTime', 'N/A')
                parents = file.get('parents', [])
                
                icon = "📄" if mime_type != "application/vnd.google-apps.folder" else "📁"
                print(f"{i}. {icon} {file_name}")
                print(f"   ID: {file_id}")
                print(f"   Tipo: {mime_type}")
                print(f"   Modificado: {modified_time}")
                if parents:
                    print(f"   Carpeta padre: {parents[0]}")
                print()
        
        # Información de configuración
        print_section("Configuración Recomendada")
        if terminados_folders:
            recommended_folder = terminados_folders[0]
            folder_id = recommended_folder.get('id')
            folder_name = recommended_folder.get('name')
            
            print_success(f"Carpeta recomendada: {folder_name}")
            print_info(f"ID: {folder_id}")
            print_info("Para configurar:")
            print_info("1. Actualiza config.yaml:")
            print_info(f"   google_drive:")
            print_info(f"     folder_id: \"{folder_id}\"")
            print_info("2. O actualiza el código del RPA")
            
            # Crear archivo de configuración
            config_info = {
                "google_drive": {
                    "folder_id": folder_id,
                    "folder_name": folder_name,
                    "enabled": True,
                    "upload_original_files": True
                }
            }
            
            with open("terminados_config.json", "w") as f:
                json.dump(config_info, f, indent=2)
            
            print_success("Archivo de configuración creado: terminados_config.json")
            
            return folder_id
        else:
            print_error("No se encontró una carpeta 'Terminados'")
            print_info("Crea una carpeta llamada 'Terminados' en Google Drive")
            print_info("O usa el ID de una carpeta existente")
            return None
        
    except Exception as e:
        print_error(f"Error al buscar carpetas: {e}")
        return None

def main():
    """Función principal"""
    print("🔍 Buscando carpeta 'Terminados' en Google Drive")
    print("Esto te ayudará a encontrar el ID correcto de la carpeta")
    
    try:
        folder_id = find_terminados_folder()
        
        if folder_id:
            print("\n✅ Carpeta encontrada exitosamente")
            print(f"ID de la carpeta: {folder_id}")
            print("Usa este ID para configurar el sistema RPA")
        else:
            print("\n❌ No se pudo encontrar la carpeta")
            print("Revisa los resultados y crea la carpeta si es necesario")
        
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
