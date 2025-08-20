#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico Completo de Google Drive
====================================

Este script realiza un diagnóstico completo de la integración con Google Drive
para identificar todos los problemas que impiden la subida de documentos.
"""

import os
import sys
import json
import time
import pickle
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos del RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def print_warning(message):
    """Imprime un mensaje de advertencia"""
    print(f"⚠️  {message}")

class GoogleDriveDiagnostico:
    """Clase para realizar diagnóstico completo de Google Drive"""
    
    def __init__(self):
        self.credentials_path = "./oauth_credentials.json"
        self.token_path = "./token.pickle"
        self.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        self.service = None
        self.user_email = None
        
    def check_dependencies(self):
        """Verifica que las dependencias estén instaladas"""
        print_section("Verificando Dependencias")
        
        try:
            import google.auth
            import googleapiclient
            import google_auth_oauthlib
            import google_auth_httplib2
            print_success("Todas las dependencias de Google Drive están instaladas")
            return True
        except ImportError as e:
            print_error(f"Falta dependencia: {e}")
            print_warning("Instala con: pip install google-auth google-api-python-client google-auth-oauthlib google-auth-httplib2")
            return False
    
    def check_oauth_credentials(self):
        """Verifica las credenciales OAuth"""
        print_section("Verificando Credenciales OAuth")
        
        if not os.path.exists(self.credentials_path):
            print_error(f"No se encontró el archivo de credenciales: {self.credentials_path}")
            return False
        
        try:
            with open(self.credentials_path, 'r') as f:
                cred_data = json.load(f)
            
            if 'installed' in cred_data:
                print_success("Credenciales OAuth encontradas y válidas")
                print_info(f"Project ID: {cred_data['installed'].get('project_id', 'N/A')}")
                print_info(f"Client ID: {cred_data['installed'].get('client_id', 'N/A')}")
                return True
            else:
                print_error("El archivo no contiene credenciales OAuth válidas")
                return False
                
        except Exception as e:
            print_error(f"Error al leer credenciales: {e}")
            return False
    
    def authenticate_oauth(self):
        """Autentica usando OAuth y obtiene información del usuario"""
        print_section("Autenticando con OAuth")
        
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            # Scopes necesarios para Google Drive
            SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/userinfo.email']
            
            creds = None
            
            # Verificar si existe un token guardado
            if os.path.exists(self.token_path):
                print_info("Cargando token existente...")
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            # Si no hay credenciales válidas, autenticar
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print_info("Refrescando token...")
                    creds.refresh(Request())
                else:
                    print_info("Iniciando flujo de autenticación OAuth...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Guardar credenciales para la próxima vez
                with open(self.token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            # Construir servicio
            self.service = build('drive', 'v3', credentials=creds)
            
            # Obtener información del usuario
            userinfo_service = build('oauth2', 'v2', credentials=creds)
            user_info = userinfo_service.userinfo().get().execute()
            self.user_email = user_info.get('email')
            
            print_success("Autenticación OAuth exitosa")
            print_info(f"Usuario autenticado: {self.user_email}")
            return True
            
        except Exception as e:
            print_error(f"Error en autenticación OAuth: {e}")
            return False
    
    def test_folder_access(self):
        """Prueba el acceso a la carpeta configurada"""
        print_section("Verificando Acceso a Carpeta")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            print_info(f"Verificando acceso a carpeta: {self.folder_id}")
            folder = self.service.files().get(fileId=self.folder_id).execute()
            print_success(f"Acceso exitoso a carpeta: {folder.get('name', 'Sin nombre')}")
            print_info(f"Tipo de archivo: {folder.get('mimeType', 'N/A')}")
            print_info(f"Propietario: {folder.get('owners', [{}])[0].get('emailAddress', 'N/A')}")
            return True
        except Exception as e:
            print_error(f"No se puede acceder a la carpeta: {e}")
            print_info("Posibles causas:")
            print_info("1. La carpeta no existe")
            print_info("2. La carpeta no está compartida con tu cuenta")
            print_info("3. No tienes permisos suficientes")
            print_info("4. El ID de carpeta es incorrecto")
            return False
    
    def list_user_folders(self):
        """Lista las carpetas accesibles del usuario"""
        print_section("Listando Carpetas Accesibles")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            # Buscar carpetas del usuario
            results = self.service.files().list(
                q="mimeType='application/vnd.google-apps.folder' and trashed=false",
                pageSize=10,
                fields="nextPageToken, files(id, name, owners)"
            ).execute()
            
            folders = results.get('files', [])
            
            if not folders:
                print_warning("No se encontraron carpetas")
                return False
            
            print_info(f"Encontradas {len(folders)} carpetas:")
            for folder in folders:
                owner_email = folder.get('owners', [{}])[0].get('emailAddress', 'N/A')
                print_info(f"  - {folder['name']} (ID: {folder['id']}, Propietario: {owner_email})")
                
                # Verificar si es la carpeta que buscamos
                if folder['id'] == self.folder_id:
                    print_success(f"¡Encontrada la carpeta objetivo: {folder['name']}!")
                    return True
            
            print_warning("La carpeta objetivo no está en la lista de carpetas accesibles")
            return False
            
        except Exception as e:
            print_error(f"Error al listar carpetas: {e}")
            return False
    
    def test_file_upload(self):
        """Prueba la subida de un archivo de prueba"""
        print_section("Probando Subida de Archivo")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            # Crear archivo de prueba
            test_content = "Este es un archivo de prueba para verificar la subida a Google Drive"
            test_file_path = "./test_upload_diagnostico.txt"
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            print_info(f"Creando archivo de prueba: {test_file_path}")
            
            # Subir archivo
            file_metadata = {
                'name': 'test_upload_diagnostico.txt',
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(test_file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            print_success(f"Archivo subido exitosamente - ID: {file.get('id')}")
            print_info(f"Enlace: {file.get('webViewLink')}")
            
            # Limpiar archivo de prueba
            os.remove(test_file_path)
            
            return True
            
        except Exception as e:
            print_error(f"Error al subir archivo: {e}")
            return False
    
    def check_rpa_integration(self):
        """Verifica la integración con el RPA"""
        print_section("Verificando Integración con RPA")
        
        # Verificar archivos del RPA
        rpa_files = [
            "./rpa/google_drive_uploader.py",
            "./rpa/google_drive_oauth_uploader.py"
        ]
        
        for file_path in rpa_files:
            if os.path.exists(file_path):
                print_success(f"Archivo RPA encontrado: {file_path}")
            else:
                print_error(f"Archivo RPA faltante: {file_path}")
        
        # Verificar configuración
        config_path = "./config.yaml"
        if os.path.exists(config_path):
            print_success("Archivo de configuración encontrado")
            
            # Leer configuración
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                google_config = config.get('google_drive', {})
                if google_config.get('enabled', False):
                    print_success("Google Drive está habilitado en la configuración")
                    print_info(f"Folder ID configurado: {google_config.get('folder_id', 'No configurado')}")
                else:
                    print_warning("Google Drive está deshabilitado en la configuración")
                    
            except Exception as e:
                print_error(f"Error al leer configuración: {e}")
        else:
            print_error("Archivo de configuración no encontrado")
    
    def check_data_structure(self):
        """Verifica la estructura de datos para archivos a subir"""
        print_section("Verificando Estructura de Datos")
        
        data_dirs = [
            "./data/outputs_json/",
            "./data/outputs_json/Procesados/",
            "./data/original_files/",
            "./data/"
        ]
        
        for dir_path in data_dirs:
            if os.path.exists(dir_path):
                print_success(f"Directorio encontrado: {dir_path}")
                
                # Contar archivos
                try:
                    files = os.listdir(dir_path)
                    json_files = [f for f in files if f.endswith('.json')]
                    png_files = [f for f in files if f.endswith('.png')]
                    pdf_files = [f for f in files if f.endswith('.pdf') or f.endswith('.PDF')]
                    
                    print_info(f"  - JSON: {len(json_files)} archivos")
                    print_info(f"  - PNG: {len(png_files)} archivos")
                    print_info(f"  - PDF: {len(pdf_files)} archivos")
                    
                except Exception as e:
                    print_error(f"Error al listar archivos en {dir_path}: {e}")
            else:
                print_warning(f"Directorio no encontrado: {dir_path}")
    
    def run_complete_diagnosis(self):
        """Ejecuta el diagnóstico completo"""
        print_header("DIAGNÓSTICO COMPLETO DE GOOGLE DRIVE")
        
        results = []
        
        # Verificar dependencias
        results.append(("Dependencias", self.check_dependencies()))
        
        # Verificar credenciales
        results.append(("Credenciales OAuth", self.check_oauth_credentials()))
        
        # Autenticar
        results.append(("Autenticación", self.authenticate_oauth()))
        
        # Verificar acceso a carpeta
        results.append(("Acceso a Carpeta", self.test_folder_access()))
        
        # Listar carpetas si falla el acceso
        if not results[-1][1]:
            results.append(("Listado de Carpetas", self.list_user_folders()))
        
        # Probar subida de archivo
        results.append(("Subida de Archivo", self.test_file_upload()))
        
        # Verificar integración RPA
        self.check_rpa_integration()
        
        # Verificar estructura de datos
        self.check_data_structure()
        
        # Resumen
        print_header("RESUMEN DEL DIAGNÓSTICO")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print_info(f"Pruebas pasadas: {passed}/{total}")
        
        if passed == total:
            print_success("¡Todos los componentes están funcionando correctamente!")
        else:
            print_error("Se encontraron problemas que necesitan atención:")
            for test_name, result in results:
                status = "✅ PASÓ" if result else "❌ FALLÓ"
                print(f"  {status} - {test_name}")
        
        return passed == total

def main():
    """Función principal"""
    diagnostico = GoogleDriveDiagnostico()
    success = diagnostico.run_complete_diagnosis()
    
    if not success:
        print_header("RECOMENDACIONES")
        print_info("1. Verifica que la carpeta esté compartida con tu cuenta de Google")
        print_info("2. Asegúrate de tener permisos de 'Editor' en la carpeta")
        print_info("3. Verifica que el ID de carpeta sea correcto")
        print_info("4. Revisa que las credenciales OAuth tengan los scopes correctos")
        print_info("5. Ejecuta el script de configuración: python setup_google_drive_test.py")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
