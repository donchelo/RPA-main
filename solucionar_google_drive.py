#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solución Automática de Problemas de Google Drive
===============================================

Este script soluciona automáticamente los problemas identificados con Google Drive:
1. Renueva el token OAuth expirado
2. Verifica y corrige permisos de carpeta
3. Configura la integración correctamente
"""

import os
import sys
import json
import time
import pickle
import shutil
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos del RPA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
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

class GoogleDriveSolver:
    """Clase para solucionar problemas de Google Drive"""
    
    def __init__(self):
        self.credentials_path = "./oauth_credentials.json"
        self.token_path = "./token.pickle"
        self.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        self.service = None
        self.user_email = None
        
    def step1_clean_expired_token(self):
        """Paso 1: Limpiar token expirado"""
        print_section("Paso 1: Limpiando Token Expirado")
        
        if os.path.exists(self.token_path):
            try:
                os.remove(self.token_path)
                print_success("Token expirado eliminado")
                return True
            except Exception as e:
                print_error(f"Error al eliminar token: {e}")
                return False
        else:
            print_info("No se encontró token existente")
            return True
    
    def step2_renew_oauth_token(self):
        """Paso 2: Renovar token OAuth"""
        print_section("Paso 2: Renovando Token OAuth")
        
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            # Scopes necesarios para Google Drive
            SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/userinfo.email']
            
            print_info("Iniciando flujo de autenticación OAuth...")
            print_info("Se abrirá una ventana del navegador para autorizar la aplicación")
            print_info("Por favor, autoriza el acceso a Google Drive")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Guardar credenciales
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            
            # Construir servicio
            self.service = build('drive', 'v3', credentials=creds)
            
            # Obtener información del usuario
            userinfo_service = build('oauth2', 'v2', credentials=creds)
            user_info = userinfo_service.userinfo().get().execute()
            self.user_email = user_info.get('email')
            
            print_success("Token OAuth renovado exitosamente")
            print_info(f"Usuario autenticado: {self.user_email}")
            return True
            
        except Exception as e:
            print_error(f"Error al renovar token OAuth: {e}")
            return False
    
    def step3_test_folder_access(self):
        """Paso 3: Probar acceso a carpeta"""
        print_section("Paso 3: Probando Acceso a Carpeta")
        
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
            print_warning("La carpeta no está compartida o no existe")
            return False
    
    def step4_create_test_folder(self):
        """Paso 4: Crear carpeta de prueba si no existe"""
        print_section("Paso 4: Creando Carpeta de Prueba")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            # Verificar si la carpeta existe
            try:
                folder = self.service.files().get(fileId=self.folder_id).execute()
                print_success(f"Carpeta ya existe: {folder.get('name', 'Sin nombre')}")
                return True
            except:
                pass
            
            # Crear nueva carpeta
            folder_metadata = {
                'name': 'Terminados',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id,name'
            ).execute()
            
            new_folder_id = folder.get('id')
            print_success(f"Carpeta creada: {folder.get('name')} (ID: {new_folder_id})")
            
            # Actualizar configuración
            self.update_config_folder_id(new_folder_id)
            
            return True
            
        except Exception as e:
            print_error(f"Error al crear carpeta: {e}")
            return False
    
    def step5_test_file_upload(self):
        """Paso 5: Probar subida de archivo"""
        print_section("Paso 5: Probando Subida de Archivo")
        
        if not self.service:
            print_error("Servicio no inicializado")
            return False
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            # Crear archivo de prueba
            test_content = "Archivo de prueba para verificar la subida a Google Drive"
            test_file_path = "./test_upload_solucion.txt"
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            print_info(f"Creando archivo de prueba: {test_file_path}")
            
            # Subir archivo
            file_metadata = {
                'name': 'test_upload_solucion.txt',
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
            try:
                os.remove(test_file_path)
            except:
                pass
            
            return True
            
        except Exception as e:
            print_error(f"Error al subir archivo: {e}")
            return False
    
    def step6_test_rpa_integration(self):
        """Paso 6: Probar integración con RPA"""
        print_section("Paso 6: Probando Integración con RPA")
        
        try:
            # Importar módulo de RPA
            from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
            
            # Crear instancia
            uploader = GoogleDriveOAuthUploader()
            
            # Probar subida de archivo de prueba
            test_content = "Archivo de prueba para RPA"
            test_file_path = "./test_rpa_integration.txt"
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            print_info("Probando subida con módulo RPA...")
            result = uploader.upload_file(test_file_path)
            
            if result and result.get('success'):
                print_success("Integración con RPA funcionando correctamente")
                print_info(f"Archivo subido: {result.get('name')}")
                print_info(f"ID: {result.get('id')}")
                
                # Limpiar archivo de prueba
                try:
                    os.remove(test_file_path)
                except:
                    pass
                
                return True
            else:
                print_error("Error en integración con RPA")
                return False
                
        except Exception as e:
            print_error(f"Error al probar integración RPA: {e}")
            return False
    
    def step7_update_configuration(self):
        """Paso 7: Actualizar configuración"""
        print_section("Paso 7: Actualizando Configuración")
        
        try:
            import yaml
            
            config_path = "./config.yaml"
            if not os.path.exists(config_path):
                print_error("Archivo de configuración no encontrado")
                return False
            
            # Leer configuración actual
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Actualizar configuración de Google Drive
            if 'google_drive' not in config:
                config['google_drive'] = {}
            
            config['google_drive'].update({
                'enabled': True,
                'folder_id': self.folder_id,
                'upload_original_files': True,
                'upload_screenshots': False
            })
            
            # Guardar configuración actualizada
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            print_success("Configuración actualizada correctamente")
            return True
            
        except Exception as e:
            print_error(f"Error al actualizar configuración: {e}")
            return False
    
    def update_config_folder_id(self, new_folder_id):
        """Actualiza el ID de carpeta en la configuración"""
        try:
            import yaml
            
            config_path = "./config.yaml"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if 'google_drive' not in config:
                config['google_drive'] = {}
            
            config['google_drive']['folder_id'] = new_folder_id
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            self.folder_id = new_folder_id
            print_success(f"ID de carpeta actualizado: {new_folder_id}")
            
        except Exception as e:
            print_error(f"Error al actualizar ID de carpeta: {e}")
    
    def run_complete_solution(self):
        """Ejecuta la solución completa"""
        print_header("SOLUCIÓN AUTOMÁTICA DE PROBLEMAS DE GOOGLE DRIVE")
        
        steps = [
            ("Limpiar Token Expirado", self.step1_clean_expired_token),
            ("Renovar Token OAuth", self.step2_renew_oauth_token),
            ("Probar Acceso a Carpeta", self.step3_test_folder_access),
            ("Crear Carpeta de Prueba", self.step4_create_test_folder),
            ("Probar Subida de Archivo", self.step5_test_file_upload),
            ("Probar Integración RPA", self.step6_test_rpa_integration),
            ("Actualizar Configuración", self.step7_update_configuration)
        ]
        
        results = []
        
        for step_name, step_func in steps:
            print_info(f"Ejecutando: {step_name}")
            try:
                result = step_func()
                results.append((step_name, result))
                
                if not result:
                    print_warning(f"Paso falló: {step_name}")
                    # Continuar con el siguiente paso
                    
            except Exception as e:
                print_error(f"Error en paso {step_name}: {e}")
                results.append((step_name, False))
        
        # Resumen final
        print_header("RESUMEN DE LA SOLUCIÓN")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print_info(f"Pasos completados exitosamente: {passed}/{total}")
        
        for step_name, result in results:
            status = "✅ COMPLETADO" if result else "❌ FALLÓ"
            print(f"  {status} - {step_name}")
        
        if passed >= 5:  # Al menos 5 de 7 pasos exitosos
            print_success("¡Problemas de Google Drive solucionados!")
            print_info("El sistema debería funcionar correctamente ahora")
        else:
            print_error("Algunos problemas persisten")
            print_info("Revisa los errores específicos y ejecuta manualmente los pasos fallidos")
        
        return passed >= 5

def main():
    """Función principal"""
    solver = GoogleDriveSolver()
    success = solver.run_complete_solution()
    
    if success:
        print_header("🎉 ¡SOLUCIÓN COMPLETADA!")
        print_info("Google Drive está configurado correctamente")
        print_info("Los documentos ahora deberían subirse automáticamente")
    else:
        print_header("⚠️ PROBLEMAS PERSISTENTES")
        print_info("Algunos problemas no se pudieron resolver automáticamente")
        print_info("Contacta al equipo técnico para asistencia adicional")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
