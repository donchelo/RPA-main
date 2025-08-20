#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Subida a Carpeta "Terminados"
=====================================

Este script verifica que los archivos se suben correctamente
a la carpeta "Terminados" en Google Drive.

Carpeta destino: https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv
"""

import os
import sys
import json
import time
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

def print_warning(message):
    """Imprime un mensaje de advertencia"""
    print(f"⚠️  {message}")

class TestUploadToTerminados:
    """Test de subida a carpeta Terminados"""
    
    def __init__(self):
        self.credentials_path = "./oauth_credentials.json"
        self.token_path = "./token.pickle"
        self.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"  # Carpeta "Terminados"
        self.service = None
        self.test_files_created = []
        
    def authenticate(self):
        """Autentica con Google Drive"""
        print_section("Autenticando con Google Drive")
        
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/drive']
            
            creds = None
            
            if os.path.exists(self.token_path):
                print_info("Cargando token existente...")
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print_info("Refrescando token...")
                    creds.refresh(Request())
                else:
                    print_info("Iniciando autenticación OAuth...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                with open(self.token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('drive', 'v3', credentials=creds)
            print_success("Autenticación exitosa")
            return True
            
        except Exception as e:
            print_error(f"Error en autenticación: {e}")
            return False
    
    def verify_folder_access(self):
        """Verifica acceso a la carpeta Terminados"""
        print_section("Verificando Acceso a Carpeta 'Terminados'")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            print_info(f"Verificando acceso a carpeta: {self.folder_id}")
            folder = self.service.files().get(fileId=self.folder_id).execute()
            
            folder_name = folder.get('name', 'Sin nombre')
            print_success(f"Acceso exitoso a carpeta: {folder_name}")
            
            if folder_name == "Terminados":
                print_success("✅ Carpeta correcta identificada")
            else:
                print_warning(f"⚠️  Nombre de carpeta: {folder_name} (esperado: Terminados)")
            
            return True
            
        except Exception as e:
            print_error(f"No se puede acceder a la carpeta: {e}")
            return False
    
    def create_test_files(self):
        """Crea archivos de prueba"""
        print_section("Creando Archivos de Prueba")
        
        test_base_name = f"TEST_TERMINADOS_{int(time.time())}"
        
        # Crear archivo PNG
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        png_path = f"./data/outputs_json/{test_base_name}.png"
        
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        with open(png_path, 'wb') as f:
            f.write(png_content)
        
        self.test_files_created.append(png_path)
        print_success(f"Archivo PNG creado: {png_path}")
        
        # Crear archivo PDF
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Terminados Test) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
        pdf_path = f"./data/outputs_json/{test_base_name}.pdf"
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)
        
        self.test_files_created.append(pdf_path)
        print_success(f"Archivo PDF creado: {pdf_path}")
        
        return test_base_name
    
    def upload_to_terminados(self, base_name):
        """Sube archivos a la carpeta Terminados"""
        print_section("Subiendo Archivos a Carpeta 'Terminados'")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return []
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            uploaded_files = []
            
            # Subir PNG
            png_path = f"./data/outputs_json/{base_name}.png"
            if os.path.exists(png_path):
                print_info(f"Subiendo PNG: {os.path.basename(png_path)}")
                
                file_metadata = {
                    'name': f'{base_name}.png',
                    'parents': [self.folder_id],
                    'description': 'Archivo de prueba - Subido a carpeta Terminados'
                }
                
                media = MediaFileUpload(png_path, resumable=True)
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink,parents'
                ).execute()
                
                uploaded_files.append({
                    'type': 'PNG',
                    'id': file.get('id'),
                    'name': file.get('name'),
                    'link': file.get('webViewLink'),
                    'parents': file.get('parents', [])
                })
                
                print_success(f"PNG subido - ID: {file.get('id')}")
            
            # Subir PDF
            pdf_path = f"./data/outputs_json/{base_name}.pdf"
            if os.path.exists(pdf_path):
                print_info(f"Subiendo PDF: {os.path.basename(pdf_path)}")
                
                file_metadata = {
                    'name': f'{base_name}.pdf',
                    'parents': [self.folder_id],
                    'description': 'Archivo de prueba - Subido a carpeta Terminados'
                }
                
                media = MediaFileUpload(pdf_path, resumable=True)
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink,parents'
                ).execute()
                
                uploaded_files.append({
                    'type': 'PDF',
                    'id': file.get('id'),
                    'name': file.get('name'),
                    'link': file.get('webViewLink'),
                    'parents': file.get('parents', [])
                })
                
                print_success(f"PDF subido - ID: {file.get('id')}")
            
            return uploaded_files
            
        except Exception as e:
            print_error(f"Error al subir archivos: {e}")
            return []
    
    def verify_upload_location(self, uploaded_files):
        """Verifica que los archivos están en la carpeta correcta"""
        print_section("Verificando Ubicación de Archivos")
        
        if not uploaded_files:
            print_error("No hay archivos para verificar")
            return False
        
        try:
            all_correct = True
            
            for file_info in uploaded_files:
                file_id = file_info['id']
                file_name = file_info['name']
                file_type = file_info['type']
                parents = file_info.get('parents', [])
                
                # Verificar que el archivo está en la carpeta correcta
                if self.folder_id in parents:
                    print_success(f"✅ {file_type}: {file_name} está en carpeta 'Terminados'")
                    print_info(f"   Enlace: {file_info['link']}")
                else:
                    print_error(f"❌ {file_type}: {file_name} NO está en carpeta 'Terminados'")
                    print_info(f"   Carpeta actual: {parents}")
                    all_correct = False
            
            return all_correct
            
        except Exception as e:
            print_error(f"Error al verificar ubicación: {e}")
            return False
    
    def cleanup_test_files(self):
        """Limpia archivos de prueba locales"""
        print_section("Limpiando Archivos Locales")
        
        for file_path in self.test_files_created:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print_success(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print_error(f"Error al eliminar {file_path}: {e}")
    
    def run_test(self):
        """Ejecuta el test completo"""
        print_header("TEST DE SUBIDA A CARPETA 'TERMINADOS'")
        
        # Agregar retraso inicial según la memoria del usuario
        print("⏳ Esperando 5 segundos para permitir cambio manual a pantalla adecuada...")
        time.sleep(5)
        
        test_results = []
        
        # 1. Autenticar
        if self.authenticate():
            test_results.append(("Autenticación", True))
        else:
            test_results.append(("Autenticación", False))
            print_error("❌ Test falló en autenticación")
            return False
        
        # 2. Verificar acceso a carpeta
        if self.verify_folder_access():
            test_results.append(("Acceso a carpeta", True))
        else:
            test_results.append(("Acceso a carpeta", False))
            print_error("❌ Test falló en acceso a carpeta")
            return False
        
        # 3. Crear archivos de prueba
        try:
            base_name = self.create_test_files()
            test_results.append(("Creación de archivos", True))
        except Exception as e:
            print_error(f"Error al crear archivos: {e}")
            test_results.append(("Creación de archivos", False))
            return False
        
        # 4. Subir archivos
        uploaded_files = self.upload_to_terminados(base_name)
        if uploaded_files:
            test_results.append(("Subida de archivos", True))
        else:
            test_results.append(("Subida de archivos", False))
            print_error("❌ Test falló en subida de archivos")
            return False
        
        # 5. Verificar ubicación
        if self.verify_upload_location(uploaded_files):
            test_results.append(("Verificación de ubicación", True))
        else:
            test_results.append(("Verificación de ubicación", False))
        
        # 6. Limpiar archivos locales
        self.cleanup_test_files()
        
        # Mostrar resumen
        print_header("RESUMEN DEL TEST")
        
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
            print_success("🎉 ¡TEST EXITOSO!")
            print("Los archivos se suben correctamente a la carpeta 'Terminados'")
            print("\n✅ El sistema RPA está configurado para:")
            print("   - Subir archivos a la carpeta 'Terminados'")
            print("   - Verificar que los archivos están en la ubicación correcta")
            print("   - Proporcionar enlaces directos a los archivos")
            print("\n🔗 Carpeta de destino:")
            print("   https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv")
            return True
        else:
            print_error(f"⚠️  {total - passed} prueba(s) fallaron")
            return False

def main():
    """Función principal"""
    print("📁 Ejecutando Test de Subida a Carpeta 'Terminados'")
    print("Este test verifica que los archivos se suben a la carpeta correcta")
    
    try:
        tester = TestUploadToTerminados()
        success = tester.run_test()
        
        if success:
            print("\n✅ TEST COMPLETADO EXITOSAMENTE")
            print("Los archivos se suben correctamente a la carpeta 'Terminados'")
            print("El sistema RPA está listo para uso en producción")
        else:
            print("\n❌ TEST FALLÓ")
            print("Revisa los errores para identificar el problema")
        
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
