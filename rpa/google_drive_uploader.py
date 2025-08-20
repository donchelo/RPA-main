import os
import shutil
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rpa.simple_logger import rpa_logger
import time

class GoogleDriveUploader:
    """
    Gestor simplificado para subir archivos a Google Drive
    Específicamente diseñado para archivos PNG y PDF originales
    """
    
    def __init__(self):
        self.folder_id = "17zOU8KlONbkfzvEyHRcXx9IvhUA7-dKv"
        self.credentials_path = None
        self.service = None
        self._find_credentials()
        
    def _find_credentials(self):
        """Busca el archivo de credenciales en ubicaciones comunes"""
        possible_paths = [
            "./credentials.json",
            "./google-credentials.json",
            "./service-account.json",
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
            "./external/validador-tamaprint/credentials.json"
        ]
        
        for path in possible_paths:
            if path and os.path.exists(path):
                self.credentials_path = path
                rpa_logger.log_action("Credenciales de Google encontradas", f"Ruta: {path}")
                return True
        
        rpa_logger.log_action("No se encontraron credenciales de Google Drive", 
                             "Subida a Drive deshabilitada")
        return False
    
    def _authenticate(self):
        """Autentica con Google Drive API"""
        if not self.credentials_path:
            return False
            
        try:
            scopes = ['https://www.googleapis.com/auth/drive']
            credentials = Credentials.from_service_account_file(
                self.credentials_path, 
                scopes=scopes
            )
            
            self.service = build('drive', 'v3', credentials=credentials)
            rpa_logger.log_action("Autenticación con Google Drive exitosa", 
                                f"Carpeta destino: {self.folder_id}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error en autenticación Google Drive: {str(e)}")
            return False
    
    def upload_file(self, file_path, custom_name=None):
        """
        Sube un archivo a Google Drive
        
        Args:
            file_path: Ruta local del archivo
            custom_name: Nombre personalizado (opcional)
        
        Returns:
            dict: Información del archivo subido o None si falla
        """
        if not self.service and not self._authenticate():
            return None
            
        if not os.path.exists(file_path):
            rpa_logger.log_error(f"Archivo no encontrado para subir: {file_path}")
            return None
        
        try:
            filename = custom_name or os.path.basename(file_path)
            
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(file_path, resumable=True)
            
            rpa_logger.log_action("Subiendo archivo a Google Drive", 
                                f"Archivo: {filename}")
            
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
        """
        Busca y sube archivos PNG y PDF originales basados en el nombre del JSON
        
        Args:
            json_filename: Nombre del archivo JSON (ej: "4500224743.PDF.json")
        
        Returns:
            dict: Resultado de la operación
        """
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
        
        # Buscar archivos originales en múltiples ubicaciones
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
        
        # Buscar PDF original  
        pdf_name = f"{base_name}.pdf"
        for location in search_locations:
            pdf_path = os.path.join(location, pdf_name)
            if os.path.exists(pdf_path):
                files_found.append(('PDF', pdf_path))
                break
        
        # También buscar con extensión .PDF (mayúscula)
        pdf_name_upper = f"{base_name}.PDF"
        for location in search_locations:
            pdf_path = os.path.join(location, pdf_name_upper)
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
            rpa_logger.log_action("No se pudieron subir archivos originales", "Revisar logs para más detalles")
        
        return result

# Instancia global para usar en el RPA
drive_uploader = GoogleDriveUploader()
