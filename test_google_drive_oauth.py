#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Google Drive con OAuth
==============================

Este script prueba la funcionalidad de Google Drive usando credenciales OAuth
para el sistema RPA TAMAPRINT.

Funcionalidades que prueba:
- Autenticación OAuth con Google Drive API
- Subida de archivos de prueba
- Verificación de permisos y configuración
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

class GoogleDriveOAuthTest:
    """Clase para realizar pruebas de Google Drive con OAuth"""
    
    def __init__(self):
        self.credentials_path = "./oauth_credentials.json"
        self.token_path = "./token.pickle"
        self.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        self.service = None
        self.test_files_created = []
        
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
                return True
            else:
                print_error("El archivo no contiene credenciales OAuth válidas")
                return False
                
        except Exception as e:
            print_error(f"Error al leer credenciales: {e}")
            return False
    
    def authenticate_oauth(self):
        """Autentica usando OAuth"""
        print_section("Autenticando con OAuth")
        
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            # Scopes necesarios para Google Drive
            SCOPES = ['https://www.googleapis.com/auth/drive']
            
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
            print_success("Autenticación OAuth exitosa")
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
            return True
        except Exception as e:
            print_error(f"No se puede acceder a la carpeta: {e}")
            print_info("Asegúrate de que:")
            print_info("1. La carpeta existe en Google Drive")
            print_info("2. Tu cuenta tiene permisos de 'Editor'")
            print_info("3. El ID de carpeta es correcto")
            return False
    
    def create_test_files(self):
        """Crea archivos de prueba"""
        print_section("Creando Archivos de Prueba")
        
        test_base_name = "TEST_OAUTH_001"
        
        # Crear archivo PNG de prueba
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        png_path = f"./data/outputs_json/{test_base_name}.png"
        
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        with open(png_path, 'wb') as f:
            f.write(png_content)
        
        self.test_files_created.append(png_path)
        print_success(f"Archivo PNG creado: {png_path}")
        
        # Crear archivo PDF de prueba
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
        pdf_path = f"./data/outputs_json/{test_base_name}.pdf"
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)
        
        self.test_files_created.append(pdf_path)
        print_success(f"Archivo PDF creado: {pdf_path}")
        
        return test_base_name
    
    def test_file_upload(self, base_name):
        """Prueba la subida de archivos"""
        print_section("Probando Subida de Archivos")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            # Probar subida de PNG
            png_path = f"./data/outputs_json/{base_name}.png"
            if os.path.exists(png_path):
                print_info(f"Subiendo archivo PNG: {png_path}")
                
                file_metadata = {
                    'name': f'{base_name}.png',
                    'parents': [self.folder_id]
                }
                
                media = MediaFileUpload(png_path, resumable=True)
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink'
                ).execute()
                
                print_success(f"PNG subido exitosamente - ID: {file.get('id')}")
                print_info(f"Enlace: {file.get('webViewLink')}")
            
            # Probar subida de PDF
            pdf_path = f"./data/outputs_json/{base_name}.pdf"
            if os.path.exists(pdf_path):
                print_info(f"Subiendo archivo PDF: {pdf_path}")
                
                file_metadata = {
                    'name': f'{base_name}.pdf',
                    'parents': [self.folder_id]
                }
                
                media = MediaFileUpload(pdf_path, resumable=True)
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink'
                ).execute()
                
                print_success(f"PDF subido exitosamente - ID: {file.get('id')}")
                print_info(f"Enlace: {file.get('webViewLink')}")
            
            return True
            
        except Exception as e:
            print_error(f"Error al subir archivos: {e}")
            return False
    
    def test_automatic_upload_simulation(self, base_name):
        """Simula la funcionalidad de subida automática"""
        print_section("Simulando Subida Automática")
        
        # Crear archivo JSON simulado
        json_filename = f"{base_name}.PDF.json"
        json_path = f"./data/outputs_json/{json_filename}"
        
        test_json = {
            "test": True,
            "filename": json_filename,
            "timestamp": time.time(),
            "upload_simulation": True
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_json, f, indent=2)
        
        self.test_files_created.append(json_path)
        print_info(f"Archivo JSON creado: {json_path}")
        
        # Simular búsqueda y subida automática
        files_found = []
        files_uploaded = []
        
        # Buscar archivos originales
        search_locations = [
            './data/outputs_json/',
            './data/',
            './'
        ]
        
        for location in search_locations:
            png_path = os.path.join(location, f"{base_name}.png")
            pdf_path = os.path.join(location, f"{base_name}.pdf")
            
            if os.path.exists(png_path):
                files_found.append(('PNG', png_path))
            if os.path.exists(pdf_path):
                files_found.append(('PDF', pdf_path))
        
        print_info(f"Archivos encontrados: {len(files_found)}")
        
        # Simular subida
        if files_found:
            print_success("Simulación de subida automática exitosa")
            for file_type, file_path in files_found:
                print_info(f"  - {file_type}: {os.path.basename(file_path)}")
        else:
            print_warning("No se encontraron archivos para subir")
        
        return len(files_found) > 0
    
    def cleanup_test_files(self):
        """Limpia los archivos de prueba"""
        print_section("Limpiando Archivos de Prueba")
        
        for file_path in self.test_files_created:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print_success(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print_error(f"Error al eliminar {file_path}: {e}")
    
    def run_complete_test(self):
        """Ejecuta todas las pruebas"""
        print_header("INICIANDO TEST DE GOOGLE DRIVE CON OAUTH")
        
        # Agregar retraso inicial según la memoria del usuario
        print("⏳ Esperando 5 segundos para permitir cambio manual a pantalla adecuada...")
        time.sleep(5)
        
        test_results = []
        
        # 1. Verificar dependencias
        if self.check_dependencies():
            test_results.append(("Dependencias", True))
        else:
            test_results.append(("Dependencias", False))
            print_error("❌ Test falló en dependencias")
            return False
        
        # 2. Verificar credenciales OAuth
        if self.check_oauth_credentials():
            test_results.append(("Credenciales OAuth", True))
        else:
            test_results.append(("Credenciales OAuth", False))
            print_error("❌ Test falló en credenciales")
            return False
        
        # 3. Autenticar con OAuth
        if self.authenticate_oauth():
            test_results.append(("Autenticación OAuth", True))
        else:
            test_results.append(("Autenticación OAuth", False))
            print_error("❌ Test falló en autenticación")
            return False
        
        # 4. Verificar acceso a carpeta
        if self.test_folder_access():
            test_results.append(("Acceso a carpeta", True))
        else:
            test_results.append(("Acceso a carpeta", False))
            print_error("❌ Test falló en acceso a carpeta")
            return False
        
        # 5. Crear archivos de prueba
        try:
            base_name = self.create_test_files()
            test_results.append(("Creación de archivos", True))
        except Exception as e:
            print_error(f"Error al crear archivos: {e}")
            test_results.append(("Creación de archivos", False))
            return False
        
        # 6. Probar subida de archivos
        if self.test_file_upload(base_name):
            test_results.append(("Subida de archivos", True))
        else:
            test_results.append(("Subida de archivos", False))
        
        # 7. Simular subida automática
        if self.test_automatic_upload_simulation(base_name):
            test_results.append(("Simulación automática", True))
        else:
            test_results.append(("Simulación automática", False))
        
        # 8. Limpiar archivos
        self.cleanup_test_files()
        
        # Mostrar resumen
        print_header("RESUMEN DE PRUEBAS OAUTH")
        
        passed = 0
        total = len(test_results)
        
        for test_name, success in test_results:
            if success:
                print_success(f"{test_name}: PASÓ")
                passed += 1
            else:
                print_error(f"{test_name}: FALLÓ")
        
        print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")
        
        if passed == total:
            print_success("🎉 ¡TODAS LAS PRUEBAS PASARON! La integración OAuth funciona correctamente.")
            return True
        else:
            print_error(f"⚠️  {total - passed} prueba(s) fallaron")
            return False

def main():
    """Función principal"""
    print("🚀 Iniciando Test de Google Drive con OAuth")
    print("Este test verificará la funcionalidad usando credenciales OAuth")
    
    try:
        tester = GoogleDriveOAuthTest()
        success = tester.run_complete_test()
        
        if success:
            print("\n✅ Test completado exitosamente")
            print("La integración OAuth con Google Drive está funcionando")
        else:
            print("\n❌ Test falló")
            print("Revisa los errores y asegúrate de que:")
            print("1. Las credenciales OAuth estén configuradas correctamente")
            print("2. La carpeta de Google Drive esté compartida")
            print("3. Tengas permisos de escritura en la carpeta")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrumpido por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
