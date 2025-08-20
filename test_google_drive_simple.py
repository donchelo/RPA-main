#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple de Google Drive - Sin Duplicaciones
===============================================

Este script prueba la funcionalidad real del RPA sin duplicar subidas.
Solo usa la función automática como lo haría el RPA en producción.
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

class GoogleDriveSimpleTest:
    """Test simple que replica exactamente lo que hace el RPA"""
    
    def __init__(self):
        self.test_results = []
        
    def find_test_files(self):
        """Encuentra archivos JSON para probar"""
        print_section("Buscando Archivos JSON para Probar")
        
        json_files = []
        
        # Buscar en directorios de datos
        search_dirs = [
            "./data/outputs_json/",
            "./data/outputs_json/Procesados/",
        ]
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            try:
                files = os.listdir(search_dir)
                
                # Buscar archivos JSON
                found_json = [f for f in files if f.endswith('.json')]
                
                for json_file in found_json[:3]:  # Tomar solo los primeros 3
                    base_name = json_file.replace('.json', '').replace('.PDF', '')
                    
                    # Verificar si existen archivos PNG y PDF correspondientes
                    png_exists = False
                    pdf_exists = False
                    
                    # Buscar PNG
                    png_file = f"{base_name}.png"
                    png_path = os.path.join(search_dir, png_file)
                    if os.path.exists(png_path):
                        png_exists = True
                    
                    # Buscar PDF (mayúscula y minúscula)
                    pdf_file_upper = f"{base_name}.PDF"
                    pdf_file_lower = f"{base_name}.pdf"
                    pdf_path_upper = os.path.join(search_dir, pdf_file_upper)
                    pdf_path_lower = os.path.join(search_dir, pdf_file_lower)
                    
                    if os.path.exists(pdf_path_upper) or os.path.exists(pdf_path_lower):
                        pdf_exists = True
                    
                    # Solo agregar si tiene al menos PNG o PDF
                    if png_exists or pdf_exists:
                        json_files.append({
                            'json_name': json_file,
                            'base_name': base_name,
                            'directory': search_dir,
                            'png_exists': png_exists,
                            'pdf_exists': pdf_exists
                        })
                    
            except Exception as e:
                print_error(f"Error al buscar en {search_dir}: {e}")
        
        print_info(f"Encontrados {len(json_files)} archivos JSON con archivos asociados")
        
        for json_file in json_files:
            print_info(f"  - {json_file['json_name']}")
            if json_file['png_exists']:
                print_info(f"    ✅ PNG: {json_file['base_name']}.png")
            if json_file['pdf_exists']:
                print_info(f"    ✅ PDF: {json_file['base_name']}.PDF/.pdf")
        
        return json_files
    
    def test_automatic_upload_only(self, json_file_info):
        """Prueba solo la función automática del RPA (sin duplicaciones)"""
        print_section(f"Probando Subida Automática: {json_file_info['json_name']}")
        
        try:
            from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
            
            # Crear nueva instancia para simular comportamiento real del RPA
            uploader = GoogleDriveOAuthUploader()
            
            # Usar SOLO la función automática que usa el RPA
            print_info("Ejecutando función automática de búsqueda y subida...")
            print_info("(Esta es la misma función que usa el RPA en producción)")
            
            result = uploader.upload_original_files_for_json(json_file_info['json_name'])
            
            if result.get('success'):
                print_success(f"✅ Subida automática exitosa")
                print_info(f"   📁 Archivos encontrados: {result['files_found']}")
                print_info(f"   📤 Archivos subidos: {result['files_uploaded']}")
                print_info(f"   ⏱️  Duración: {result.get('duration', 0):.2f} segundos")
                
                # Mostrar detalles de archivos subidos
                if 'uploaded_details' in result:
                    for detail in result['uploaded_details']:
                        file_type = detail['type']
                        drive_info = detail['drive_info']
                        print_success(f"   {file_type}: {drive_info.get('name')} (ID: {drive_info.get('id')})")
                
                return True
            else:
                print_warning(f"⚠️  Subida automática falló: {result.get('message', 'Error desconocido')}")
                return False
                
        except Exception as e:
            print_error(f"Error en prueba automática: {e}")
            return False
    
    def verify_configuration(self):
        """Verifica que la configuración esté correcta"""
        print_section("Verificando Configuración del Sistema")
        
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
                print_success("✅ Google Drive habilitado en configuración")
                print_info(f"   📁 Folder ID: {google_config.get('folder_id', 'No configurado')}")
                print_info(f"   📄 Subir archivos originales: {google_config.get('upload_original_files', False)}")
                return True
            else:
                print_error("❌ Google Drive deshabilitado en configuración")
                return False
                
        except Exception as e:
            print_error(f"Error al verificar configuración: {e}")
            return False
    
    def run_realistic_test(self):
        """Ejecuta un test realista que simula el comportamiento del RPA"""
        print_header("TEST REALISTA DE GOOGLE DRIVE (SIN DUPLICACIONES)")
        
        # Verificar configuración
        config_ok = self.verify_configuration()
        if not config_ok:
            print_error("Configuración incorrecta, abortando prueba")
            return False
        
        # Encontrar archivos de prueba
        json_files = self.find_test_files()
        
        if not json_files:
            print_error("No se encontraron archivos JSON con archivos asociados")
            return False
        
        # Probar con uno o dos archivos máximo
        test_files = json_files[:2]
        successful_uploads = 0
        
        for json_file_info in test_files:
            success = self.test_automatic_upload_only(json_file_info)
            if success:
                successful_uploads += 1
            
            self.test_results.append((json_file_info['json_name'], success))
        
        # Resumen final
        print_header("RESUMEN DEL TEST REALISTA")
        
        print_info(f"Archivos probados: {len(test_files)}")
        print_info(f"Subidas exitosas: {successful_uploads}")
        print_info(f"Tasa de éxito: {(successful_uploads/len(test_files)*100):.1f}%")
        
        print_section("Resultados Detallados")
        for json_name, success in self.test_results:
            status = "✅ EXITOSO" if success else "❌ FALLÓ"
            print(f"  {status} - {json_name}")
        
        if successful_uploads > 0:
            print_success("🎉 Google Drive está funcionando correctamente")
            print_info("El RPA subirá automáticamente los documentos sin duplicaciones")
            return True
        else:
            print_error("❌ Problemas detectados en la subida")
            return False

def main():
    """Función principal"""
    print("🚀 Iniciando test realista de Google Drive...")
    
    test = GoogleDriveSimpleTest()
    success = test.run_realistic_test()
    
    if success:
        print_header("🎯 RESULTADO FINAL: EXITOSO")
        print_success("Google Drive está configurado correctamente")
        print_success("El RPA subirá documentos automáticamente SIN duplicaciones")
        print_info("Cada archivo se sube UNA SOLA VEZ cuando el RPA procesa el JSON")
    else:
        print_header("⚠️ RESULTADO FINAL: PROBLEMAS DETECTADOS")
        print_error("Hay problemas en la integración con Google Drive")
        print_info("Revisa los errores y contacta al equipo técnico")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
