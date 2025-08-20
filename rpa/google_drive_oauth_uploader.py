#!/usr/bin/env python3
"""
Gestor de Google Drive con OAuth delegation
"""

import os
import pickle
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rpa.simple_logger import rpa_logger

class GoogleDriveOAuthUploader:
    """
    Gestor para subir archivos a Google Drive usando OAuth delegation
    """
    
    def __init__(self):
        self.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        self.creds = None
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self._authenticate()
        
    def _authenticate(self):
        """Autentica usando OAuth delegation"""
        try:
            # Cargar credenciales guardadas
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            
            # Si no hay credenciales válidas, solicitar autorización
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    # Buscar archivo de credenciales OAuth
                    oauth_credentials_path = None
                    for path in ["./oauth_credentials.json", "./client_secret.json"]:
                        if os.path.exists(path):
                            oauth_credentials_path = path
                            break
                    
                    if not oauth_credentials_path:
                        rpa_logger.log_error("No se encontraron credenciales OAuth")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        oauth_credentials_path, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Guardar credenciales
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)
            
            # Crear servicio
            self.service = build('drive', 'v3', credentials=self.creds)
            rpa_logger.log_action("OAuth delegation configurado", f"Carpeta: {self.folder_id}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error en autenticación OAuth: {str(e)}")
            return False
    
    def upload_file(self, file_path, custom_name=None):
        """Sube un archivo a Google Drive"""
        if not self.service:
            return None
            
        if not os.path.exists(file_path):
            rpa_logger.log_error(f"Archivo no encontrado: {file_path}")
            return None
        
        try:
            filename = custom_name or os.path.basename(file_path)
            
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(file_path, resumable=True)
            
            rpa_logger.log_action("Subiendo archivo con OAuth", f"Archivo: {filename}")
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            rpa_logger.log_action("Archivo subido exitosamente", 
                                f"Nombre: {filename}, ID: {file.get('id')}")
            
            return {
                'id': file.get('id'),
                'name': filename,
                'link': file.get('webViewLink'),
                'success': True
            }
            
        except Exception as e:
            rpa_logger.log_error(f"Error al subir archivo: {str(e)}", 
                               f"Archivo: {file_path}")
            return {'success': False, 'error': str(e)}
    
    def upload_original_files_for_json(self, json_filename):
        """Busca y sube archivos PNG y PDF originales"""
        start_time = time.time()
        
        # Extraer nombre base del JSON
        if json_filename.endswith('.PDF.json'):
            base_name = json_filename.replace('.PDF.json', '')
        elif json_filename.endswith('.json'):
            base_name = json_filename.replace('.json', '')
        else:
            base_name = json_filename
        
        rpa_logger.log_action("Buscando archivos originales para subir", 
                            f"Base: {base_name}")
        
        # Buscar archivos originales
        search_locations = [
            './data/outputs_json/Procesados/',
            './data/outputs_json/',
            './data/',
            './'
        ]
        
        files_found = []
        files_uploaded = []
        
        # Buscar PNG original
        png_name = f"{base_name}.png"
        for location in search_locations:
            png_path = os.path.join(location, png_name)
            if os.path.exists(png_path):
                files_found.append(('PNG', png_path))
                break
        
        # Buscar PDF original (priorizar .PDF mayúscula, luego .pdf minúscula)
        pdf_name_upper = f"{base_name}.PDF"
        pdf_found = False
        for location in search_locations:
            pdf_path = os.path.join(location, pdf_name_upper)
            if os.path.exists(pdf_path):
                files_found.append(('PDF', pdf_path))
                pdf_found = True
                break
        
        # Si no se encontró .PDF mayúscula, buscar .pdf minúscula
        if not pdf_found:
            pdf_name = f"{base_name}.pdf"
            for location in search_locations:
                pdf_path = os.path.join(location, pdf_name)
                if os.path.exists(pdf_path):
                    files_found.append(('PDF', pdf_path))
                    break
        
        if not files_found:
            rpa_logger.log_action("No se encontraron archivos originales", 
                                f"Búsqueda para: {base_name}")
            return {
                'success': False,
                'message': 'No se encontraron archivos originales',
                'files_found': 0,
                'files_uploaded': 0
            }
        
        # Subir archivos encontrados
        for file_type, file_path in files_found:
            result = self.upload_file(file_path)
            if result and result.get('success'):
                files_uploaded.append({
                    'type': file_type,
                    'original_path': file_path,
                    'drive_info': result
                })
        
        duration = time.time() - start_time
        success = len(files_uploaded) > 0
        
        result = {
            'success': success,
            'files_found': len(files_found),
            'files_uploaded': len(files_uploaded),
            'uploaded_details': files_uploaded,
            'duration': duration
        }
        
        if success:
            rpa_logger.log_action("Archivos originales subidos exitosamente", 
                                f"Subidos: {len(files_uploaded)}/{len(files_found)}")
        else:
            rpa_logger.log_action("No se pudieron subir archivos originales", "Revisar logs")
        
        return result

# Instancia global para usar en el RPA
drive_uploader = GoogleDriveOAuthUploader()
