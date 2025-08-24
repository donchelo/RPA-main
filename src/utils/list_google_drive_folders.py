#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listar Carpetas de Google Drive
===============================

Este script lista todas las carpetas disponibles en Google Drive
para encontrar el ID correcto de la carpeta de destino.
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

def list_google_drive_folders():
    """Lista todas las carpetas en Google Drive"""
    print_header("LISTANDO CARPETAS DE GOOGLE DRIVE")
    
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
        
        # Listar carpetas
        print_section("Carpetas Disponibles")
        
        # Buscar solo carpetas (mimeType = application/vnd.google-apps.folder)
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            pageSize=50,
            fields="nextPageToken, files(id, name, createdTime, parents)"
        ).execute()
        
        folders = results.get('files', [])
        
        if not folders:
            print_info("No se encontraron carpetas")
        else:
            print_info(f"Se encontraron {len(folders)} carpetas:")
            print()
            
            for i, folder in enumerate(folders, 1):
                folder_id = folder.get('id')
                folder_name = folder.get('name', 'Sin nombre')
                created_time = folder.get('createdTime', 'N/A')
                
                print(f"{i:2d}. 📁 {folder_name}")
                print(f"    ID: {folder_id}")
                print(f"    Creado: {created_time}")
                print()
        
        # También listar archivos recientes para referencia
        print_section("Archivos Recientes (últimos 10)")
        
        results = service.files().list(
            pageSize=10,
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
                
                icon = "📄" if mime_type != "application/vnd.google-apps.folder" else "📁"
                print(f"{i:2d}. {icon} {file_name}")
                print(f"    ID: {file_id}")
                print(f"    Tipo: {mime_type}")
                print(f"    Modificado: {modified_time}")
                print()
        
        # Información adicional
        print_section("Información de Configuración")
        print_info("Para usar una carpeta específica:")
        print_info("1. Copia el ID de la carpeta deseada")
        print_info("2. Actualiza el archivo config.yaml:")
        print_info("   google_drive:")
        print_info("     folder_id: \"TU_ID_DE_CARPETA\"")
        print_info("3. O actualiza el código directamente")
        
        return True
        
    except Exception as e:
        print_error(f"Error al listar carpetas: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Listando carpetas disponibles en Google Drive")
    print("Esto te ayudará a encontrar el ID correcto de la carpeta")
    
    try:
        success = list_google_drive_folders()
        
        if success:
            print("\n✅ Listado completado exitosamente")
            print("Usa uno de los IDs mostrados para configurar la carpeta de destino")
        else:
            print("\n❌ Error al listar carpetas")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Operación interrumpida por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
