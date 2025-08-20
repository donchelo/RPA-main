#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Subida Automática a Google Drive
========================================

Este script prueba la funcionalidad de subida automática de documentos
a Google Drive del sistema RPA TAMAPRINT.

Funcionalidades que prueba:
- Autenticación con Google Drive API
- Búsqueda de archivos originales (PNG y PDF)
- Subida de archivos a la carpeta configurada
- Verificación de permisos y configuración
"""

import os
import sys
import time
import json
import shutil
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos del RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rpa.google_drive_uploader import GoogleDriveUploader
    from rpa.config_manager import ConfigManager
    from rpa.simple_logger import rpa_logger
except ImportError as e:
    print(f"❌ Error al importar módulos del RPA: {e}")
    print("Asegúrate de estar ejecutando desde el directorio raíz del proyecto")
    sys.exit(1)

class GoogleDriveTest:
    """Clase para realizar pruebas completas de Google Drive"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.uploader = GoogleDriveUploader()
        self.test_files_created = []
        
    def print_header(self, title):
        """Imprime un encabezado formateado"""
        print("\n" + "="*60)
        print(f"🔍 {title}")
        print("="*60)
    
    def print_section(self, title):
        """Imprime una sección formateada"""
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def print_success(self, message):
        """Imprime un mensaje de éxito"""
        print(f"✅ {message}")
    
    def print_error(self, message):
        """Imprime un mensaje de error"""
        print(f"❌ {message}")
    
    def print_info(self, message):
        """Imprime un mensaje informativo"""
        print(f"ℹ️  {message}")
    
    def test_configuration(self):
        """Prueba la configuración de Google Drive"""
        self.print_section("Verificando Configuración")
        
        # Verificar configuración en config.yaml
        google_config = self.config.get('google_drive', {})
        
        if not google_config.get('enabled', False):
            self.print_error("Google Drive está deshabilitado en config.yaml")
            return False
        
        self.print_success("Google Drive está habilitado en config.yaml")
        
        folder_id = google_config.get('folder_id')
        if folder_id:
            self.print_success(f"ID de carpeta configurado: {folder_id}")
        else:
            self.print_error("No se encontró ID de carpeta en config.yaml")
            return False
        
        return True
    
    def test_credentials(self):
        """Prueba la disponibilidad de credenciales"""
        self.print_section("Verificando Credenciales")
        
        if not self.uploader.credentials_path:
            self.print_error("No se encontraron credenciales de Google Drive")
            self.print_info("Ubicaciones buscadas:")
            possible_paths = [
                "./credentials.json",
                "./google-credentials.json", 
                "./service-account.json",
                "./external/validador-tamaprint/credentials.json"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    self.print_success(f"✅ {path}")
                else:
                    self.print_info(f"❌ {path}")
            return False
        
        self.print_success(f"Credenciales encontradas en: {self.uploader.credentials_path}")
        return True
    
    def test_authentication(self):
        """Prueba la autenticación con Google Drive"""
        self.print_section("Probando Autenticación")
        
        if self.uploader._authenticate():
            self.print_success("Autenticación exitosa con Google Drive API")
            return True
        else:
            self.print_error("Falló la autenticación con Google Drive API")
            return False
    
    def create_test_files(self):
        """Crea archivos de prueba para simular documentos originales"""
        self.print_section("Creando Archivos de Prueba")
        
        test_base_name = "TEST_GOOGLE_DRIVE_001"
        
        # Crear archivo PNG de prueba
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        png_path = f"./data/outputs_json/{test_base_name}.png"
        
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        with open(png_path, 'wb') as f:
            f.write(png_content)
        
        self.test_files_created.append(png_path)
        self.print_success(f"Archivo PNG creado: {png_path}")
        
        # Crear archivo PDF de prueba (simulado)
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
        pdf_path = f"./data/outputs_json/{test_base_name}.pdf"
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)
        
        self.test_files_created.append(pdf_path)
        self.print_success(f"Archivo PDF creado: {pdf_path}")
        
        return test_base_name
    
    def test_file_upload(self, base_name):
        """Prueba la subida de archivos específicos"""
        self.print_section("Probando Subida de Archivos")
        
        # Probar subida de archivo PNG
        png_path = f"./data/outputs_json/{base_name}.png"
        if os.path.exists(png_path):
            self.print_info(f"Subiendo archivo PNG: {png_path}")
            result = self.uploader.upload_file(png_path)
            
            if result and result.get('success'):
                self.print_success(f"PNG subido exitosamente - ID: {result.get('id')}")
                self.print_info(f"Enlace: {result.get('link')}")
            else:
                self.print_error(f"Error al subir PNG: {result.get('error', 'Error desconocido')}")
        
        # Probar subida de archivo PDF
        pdf_path = f"./data/outputs_json/{base_name}.pdf"
        if os.path.exists(pdf_path):
            self.print_info(f"Subiendo archivo PDF: {pdf_path}")
            result = self.uploader.upload_file(pdf_path)
            
            if result and result.get('success'):
                self.print_success(f"PDF subido exitosamente - ID: {result.get('id')}")
                self.print_info(f"Enlace: {result.get('link')}")
            else:
                self.print_error(f"Error al subir PDF: {result.get('error', 'Error desconocido')}")
    
    def test_automatic_upload(self, base_name):
        """Prueba la funcionalidad de subida automática"""
        self.print_section("Probando Subida Automática")
        
        # Crear un archivo JSON simulado para probar la búsqueda automática
        json_filename = f"{base_name}.PDF.json"
        json_path = f"./data/outputs_json/{json_filename}"
        
        # Crear contenido JSON de prueba
        test_json = {
            "test": True,
            "filename": json_filename,
            "timestamp": time.time()
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_json, f, indent=2)
        
        self.test_files_created.append(json_path)
        self.print_info(f"Archivo JSON creado: {json_path}")
        
        # Probar la función de subida automática
        self.print_info("Ejecutando subida automática...")
        result = self.uploader.upload_original_files_for_json(json_filename)
        
        if result.get('success'):
            self.print_success(f"Subida automática exitosa")
            self.print_info(f"Archivos encontrados: {result.get('files_found')}")
            self.print_info(f"Archivos subidos: {result.get('files_uploaded')}")
            self.print_info(f"Duración: {result.get('duration', 0):.2f} segundos")
            
            # Mostrar detalles de archivos subidos
            for uploaded in result.get('uploaded_details', []):
                drive_info = uploaded.get('drive_info', {})
                self.print_success(f"  - {uploaded.get('type')}: {drive_info.get('name')} (ID: {drive_info.get('id')})")
        else:
            self.print_error(f"Error en subida automática: {result.get('message', 'Error desconocido')}")
    
    def cleanup_test_files(self):
        """Limpia los archivos de prueba creados"""
        self.print_section("Limpiando Archivos de Prueba")
        
        for file_path in self.test_files_created:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.print_success(f"Archivo eliminado: {file_path}")
            except Exception as e:
                self.print_error(f"Error al eliminar {file_path}: {e}")
    
    def run_complete_test(self):
        """Ejecuta todas las pruebas en secuencia"""
        self.print_header("INICIANDO TEST DE GOOGLE DRIVE")
        
        # Agregar retraso inicial según la memoria del usuario
        print("⏳ Esperando 5 segundos para permitir cambio manual a pantalla adecuada...")
        time.sleep(5)
        
        test_results = []
        
        # 1. Verificar configuración
        if self.test_configuration():
            test_results.append(("Configuración", True))
        else:
            test_results.append(("Configuración", False))
            self.print_error("❌ Test falló en configuración. Deteniendo pruebas.")
            return False
        
        # 2. Verificar credenciales
        if self.test_credentials():
            test_results.append(("Credenciales", True))
        else:
            test_results.append(("Credenciales", False))
            self.print_error("❌ Test falló en credenciales. Deteniendo pruebas.")
            return False
        
        # 3. Probar autenticación
        if self.test_authentication():
            test_results.append(("Autenticación", True))
        else:
            test_results.append(("Autenticación", False))
            self.print_error("❌ Test falló en autenticación. Deteniendo pruebas.")
            return False
        
        # 4. Crear archivos de prueba
        try:
            base_name = self.create_test_files()
            test_results.append(("Creación de archivos de prueba", True))
        except Exception as e:
            self.print_error(f"Error al crear archivos de prueba: {e}")
            test_results.append(("Creación de archivos de prueba", False))
            return False
        
        # 5. Probar subida de archivos
        try:
            self.test_file_upload(base_name)
            test_results.append(("Subida de archivos", True))
        except Exception as e:
            self.print_error(f"Error en subida de archivos: {e}")
            test_results.append(("Subida de archivos", False))
        
        # 6. Probar subida automática
        try:
            self.test_automatic_upload(base_name)
            test_results.append(("Subida automática", True))
        except Exception as e:
            self.print_error(f"Error en subida automática: {e}")
            test_results.append(("Subida automática", False))
        
        # 7. Limpiar archivos de prueba
        self.cleanup_test_files()
        
        # Mostrar resumen final
        self.print_header("RESUMEN DE PRUEBAS")
        
        passed = 0
        total = len(test_results)
        
        for test_name, success in test_results:
            if success:
                self.print_success(f"{test_name}: PASÓ")
                passed += 1
            else:
                self.print_error(f"{test_name}: FALLÓ")
        
        print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")
        
        if passed == total:
            self.print_success("🎉 ¡TODAS LAS PRUEBAS PASARON! La integración con Google Drive funciona correctamente.")
            return True
        else:
            self.print_error(f"⚠️  {total - passed} prueba(s) fallaron. Revisa los errores arriba.")
            return False

def main():
    """Función principal del script de prueba"""
    print("🚀 Iniciando Test de Integración con Google Drive")
    print("Este test verificará la funcionalidad completa de subida automática")
    
    try:
        tester = GoogleDriveTest()
        success = tester.run_complete_test()
        
        if success:
            print("\n✅ Test completado exitosamente")
            print("La integración con Google Drive está funcionando correctamente")
        else:
            print("\n❌ Test falló")
            print("Revisa los errores y asegúrate de que:")
            print("1. Las credenciales de Google Drive estén configuradas")
            print("2. La carpeta de Google Drive esté compartida correctamente")
            print("3. La configuración en config.yaml sea correcta")
        
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
