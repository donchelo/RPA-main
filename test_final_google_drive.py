#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Final de Google Drive
==========================

Este script realiza una prueba final completa de la integración con Google Drive
usando archivos reales del sistema RPA.
"""

import os
import sys
import json
import time
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos del RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
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

class GoogleDriveFinalTest:
    """Clase para realizar prueba final de Google Drive"""
    
    def __init__(self):
        self.test_results = []
        
    def find_test_files(self):
        """Encuentra archivos de prueba reales"""
        print_section("Buscando Archivos de Prueba")
        
        test_files = []
        
        # Buscar en directorios de datos
        search_dirs = [
            "./data/outputs_json/",
            "./data/outputs_json/Procesados/",
            "./data/original_files/"
        ]
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            try:
                files = os.listdir(search_dir)
                
                # Buscar archivos JSON
                json_files = [f for f in files if f.endswith('.json')]
                
                for json_file in json_files[:3]:  # Tomar solo los primeros 3
                    base_name = json_file.replace('.json', '').replace('.PDF', '')
                    
                    # Buscar archivos PNG y PDF correspondientes
                    png_file = f"{base_name}.png"
                    pdf_file = f"{base_name}.pdf"
                    pdf_file_upper = f"{base_name}.PDF"
                    
                    png_path = os.path.join(search_dir, png_file)
                    pdf_path = os.path.join(search_dir, pdf_file)
                    pdf_path_upper = os.path.join(search_dir, pdf_file_upper)
                    
                    test_file = {
                        'json_name': json_file,
                        'base_name': base_name,
                        'json_path': os.path.join(search_dir, json_file),
                        'png_path': png_path if os.path.exists(png_path) else None,
                        'pdf_path': pdf_path_upper if os.path.exists(pdf_path_upper) else (pdf_path if os.path.exists(pdf_path) else None)
                    }
                    
                    test_files.append(test_file)
                    
            except Exception as e:
                print_error(f"Error al buscar en {search_dir}: {e}")
        
        print_info(f"Encontrados {len(test_files)} archivos de prueba")
        
        for test_file in test_files:
            print_info(f"  - {test_file['json_name']}")
            if test_file['png_path']:
                print_info(f"    PNG: {os.path.basename(test_file['png_path'])}")
            if test_file['pdf_path']:
                print_info(f"    PDF: {os.path.basename(test_file['pdf_path'])}")
        
        return test_files
    
    def test_upload_with_rpa_module(self, test_file):
        """Prueba la subida usando el módulo RPA"""
        print_section(f"Probando Subida: {test_file['json_name']}")
        
        try:
            from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
            
            uploader = GoogleDriveOAuthUploader()
            
            files_uploaded = []
            files_failed = []
            
            # Probar subida de PNG
            if test_file['png_path']:
                print_info(f"Subiendo PNG: {os.path.basename(test_file['png_path'])}")
                result = uploader.upload_file(test_file['png_path'])
                
                if result and result.get('success'):
                    print_success(f"PNG subido: {result.get('name')} (ID: {result.get('id')})")
                    files_uploaded.append(('PNG', result))
                else:
                    print_error(f"Error al subir PNG: {result.get('error', 'Error desconocido')}")
                    files_failed.append(('PNG', result))
            
            # Probar subida de PDF
            if test_file['pdf_path']:
                print_info(f"Subiendo PDF: {os.path.basename(test_file['pdf_path'])}")
                result = uploader.upload_file(test_file['pdf_path'])
                
                if result and result.get('success'):
                    print_success(f"PDF subido: {result.get('name')} (ID: {result.get('id')})")
                    files_uploaded.append(('PDF', result))
                else:
                    print_error(f"Error al subir PDF: {result.get('error', 'Error desconocido')}")
                    files_failed.append(('PDF', result))
            
            # Probar función automática
            print_info("Probando función automática de búsqueda y subida...")
            auto_result = uploader.upload_original_files_for_json(test_file['json_name'])
            
            if auto_result.get('success'):
                print_success(f"Subida automática exitosa: {auto_result['files_uploaded']}/{auto_result['files_found']} archivos")
            else:
                print_warning(f"Subida automática falló: {auto_result.get('message', 'Error desconocido')}")
            
            return {
                'success': len(files_uploaded) > 0,
                'files_uploaded': files_uploaded,
                'files_failed': files_failed,
                'auto_result': auto_result
            }
            
        except Exception as e:
            print_error(f"Error en prueba: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_configuration(self):
        """Verifica la configuración actual"""
        print_section("Verificando Configuración")
        
        try:
            import yaml
            
            config_path = "./config.yaml"
            if not os.path.exists(config_path):
                print_error("Archivo de configuración no encontrado")
                return False
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            google_config = config.get('google_drive', {})
            
            if google_config.get('enabled', False):
                print_success("Google Drive está habilitado")
                print_info(f"Folder ID: {google_config.get('folder_id', 'No configurado')}")
                print_info(f"Subir archivos originales: {google_config.get('upload_original_files', False)}")
                print_info(f"Subir screenshots: {google_config.get('upload_screenshots', False)}")
                return True
            else:
                print_warning("Google Drive está deshabilitado en la configuración")
                return False
                
        except Exception as e:
            print_error(f"Error al verificar configuración: {e}")
            return False
    
    def test_token_status(self):
        """Verifica el estado del token OAuth"""
        print_section("Verificando Estado del Token")
        
        token_path = "./token.pickle"
        
        if os.path.exists(token_path):
            try:
                import pickle
                with open(token_path, 'rb') as f:
                    token = pickle.load(f)
                
                if hasattr(token, 'valid') and token.valid:
                    print_success("Token OAuth válido")
                    return True
                elif hasattr(token, 'expired') and token.expired:
                    print_warning("Token OAuth expirado")
                    return False
                else:
                    print_info("Token OAuth encontrado (estado desconocido)")
                    return True
            except Exception as e:
                print_error(f"Error al verificar token: {e}")
                return False
        else:
            print_warning("No se encontró token OAuth")
            return False
    
    def run_complete_test(self):
        """Ejecuta la prueba completa"""
        print_header("PRUEBA FINAL DE GOOGLE DRIVE")
        
        # Verificar configuración
        config_ok = self.test_configuration()
        self.test_results.append(("Configuración", config_ok))
        
        # Verificar token
        token_ok = self.test_token_status()
        self.test_results.append(("Token OAuth", token_ok))
        
        # Encontrar archivos de prueba
        test_files = self.find_test_files()
        
        if not test_files:
            print_error("No se encontraron archivos de prueba")
            return False
        
        # Probar subida con cada archivo
        upload_tests = []
        for test_file in test_files[:2]:  # Probar solo los primeros 2
            result = self.test_upload_with_rpa_module(test_file)
            upload_tests.append((test_file['json_name'], result))
            self.test_results.append((f"Subida {test_file['json_name']}", result['success']))
        
        # Resumen final
        print_header("RESUMEN DE LA PRUEBA FINAL")
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        print_info(f"Pruebas pasadas: {passed}/{total}")
        
        for test_name, result in self.test_results:
            status = "✅ PASÓ" if result else "❌ FALLÓ"
            print(f"  {status} - {test_name}")
        
        # Detalles de subidas
        print_section("Detalles de Subidas")
        for json_name, result in upload_tests:
            if result['success']:
                print_success(f"{json_name}: Subida exitosa")
                for file_type, upload_info in result['files_uploaded']:
                    print_info(f"  - {file_type}: {upload_info.get('name')} (ID: {upload_info.get('id')})")
            else:
                print_error(f"{json_name}: Subida falló")
                if 'error' in result:
                    print_info(f"  Error: {result['error']}")
        
        if passed >= total * 0.8:  # Al menos 80% de éxito
            print_success("¡Google Drive está funcionando correctamente!")
            print_info("Los documentos se subirán automáticamente cuando el RPA los procese")
            return True
        else:
            print_error("Hay problemas que necesitan atención")
            return False

def main():
    """Función principal"""
    test = GoogleDriveFinalTest()
    success = test.run_complete_test()
    
    if success:
        print_header("🎉 ¡PRUEBA EXITOSA!")
        print_info("Google Drive está configurado y funcionando correctamente")
        print_info("El sistema RPA subirá automáticamente los documentos a Drive")
    else:
        print_header("⚠️ PROBLEMAS DETECTADOS")
        print_info("Algunos problemas persisten en la integración con Google Drive")
        print_info("Revisa los errores específicos y contacta al equipo técnico")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
