# Integración Completa de Google Drive en RPA

## Resumen

El sistema RPA ahora incluye **integración automática con Google Drive** que se ejecuta al finalizar el procesamiento de cada documento. Cuando un archivo se procesa completamente, tanto el archivo PDF original como la imagen PNG generada se suben automáticamente a Google Drive.

## Flujo de Procesamiento Completo

### 1. Procesamiento Normal del RPA
```
Archivo JSON → Procesamiento SAP → Screenshot → Validación → Estado COMPLETED
```

### 2. Subida Automática a Google Drive (NUEVO)
```
Estado COMPLETED → Subida PDF + PNG → Confirmación → Proceso Finalizado
```

## Implementación Técnica

### Ubicación del Código

- **Manejador de Estado**: `rpa/rpa_state_handlers.py` - método `handle_completed_state()`
- **Uploader**: `rpa/google_drive_oauth_uploader.py` - clase `GoogleDriveOAuthUploader`
- **Validación**: `rpa/rpa_with_state_machine.py` - método `validate_files_for_makecom()`

### Código Clave

```python
def handle_completed_state(self, context: StateContext, **kwargs) -> Optional[RPAEvent]:
    """Maneja el estado de proceso completado"""
    # ... estadísticas y logging ...
    
    # SUBIR ARCHIVOS A GOOGLE DRIVE
    try:
        from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
        uploader = GoogleDriveOAuthUploader()
        
        # Subir archivos originales (PDF y PNG)
        upload_result = uploader.upload_original_files_for_json(context.current_file)
        
        if upload_result.get('success'):
            rpa_logger.log_action(
                "ARCHIVOS SUBIDOS EXITOSAMENTE A GOOGLE DRIVE",
                f"Archivo: {context.current_file}, Archivos subidos: {upload_result.get('files_uploaded', 0)}"
            )
        else:
            rpa_logger.log_error(
                "FALLA EN SUBIDA A GOOGLE DRIVE",
                f"Archivo: {context.current_file}, Error: {upload_result.get('message', 'Error desconocido')}"
            )
    except Exception as e:
        rpa_logger.log_error(f"Error durante subida a Google Drive: {str(e)}")
    
    return None
```

## Archivos que se Suben

### 1. Archivo PDF Original
- **Ubicación**: `./data/outputs_json/Procesados/[nombre_base].PDF`
- **Descripción**: Documento original procesado
- **Formato**: PDF (mayúscula)

### 2. Archivo PNG Generado
- **Ubicación**: `./data/outputs_json/Procesados/[nombre_base].png`
- **Descripción**: Screenshot del procesamiento en SAP
- **Formato**: PNG

## Configuración de Google Drive

### 1. Credenciales OAuth
- **Archivo**: `credentials/google_drive_credentials.json`
- **Configuración**: Seguir guía en `GOOGLE_DRIVE_INTEGRATION.md`

### 2. Carpeta de Destino
- **Configuración**: En `config.yaml` o variables de entorno
- **Carpeta por defecto**: "Terminados" en Google Drive

## Logs y Monitoreo

### Logs de Subida Exitosa
```
[INFO] Iniciando subida de archivos a Google Drive - Archivo: ejemplo.json
[INFO] ARCHIVOS SUBIDOS EXITOSAMENTE A GOOGLE DRIVE - Archivo: ejemplo.json, Archivos subidos: 2
[INFO] Archivo subido: PDF - ID: 1ABC123..., Enlace: https://drive.google.com/...
[INFO] Archivo subido: PNG - ID: 2DEF456..., Enlace: https://drive.google.com/...
```

### Logs de Error
```
[ERROR] FALLA EN SUBIDA A GOOGLE DRIVE - Archivo: ejemplo.json, Error: No se encontraron archivos originales
[ERROR] Error durante subida a Google Drive: Connection timeout - Archivo: ejemplo.json
```

## Pruebas y Validación

### Script de Prueba
```bash
python test_google_drive_upload_integration.py
```

### Funcionalidades de Prueba
1. **Subida Directa**: Prueba la funcionalidad de Google Drive independientemente
2. **Integración con Máquina de Estados**: Prueba el flujo completo
3. **Creación de Archivos de Prueba**: Genera archivos simulados para testing

## Manejo de Errores

### Tipos de Errores
1. **Archivos no encontrados**: Los archivos PDF/PNG no existen
2. **Error de conexión**: Problemas de red o autenticación
3. **Error de permisos**: Falta de permisos en Google Drive
4. **Error de configuración**: Credenciales incorrectas

### Comportamiento en Caso de Error
- **No bloquea el proceso**: El RPA continúa funcionando
- **Logging detallado**: Todos los errores se registran
- **Reintentos**: Configurables en el uploader
- **Notificación**: Errores visibles en logs

## Ventajas de la Integración

### 1. Automatización Completa
- No requiere intervención manual
- Se ejecuta automáticamente al completar procesamiento

### 2. Trazabilidad
- Enlaces directos a archivos en Google Drive
- IDs únicos para cada archivo subido
- Logs detallados de cada subida

### 3. Integración con Make.com
- Archivos disponibles inmediatamente para Make.com
- Estructura consistente de archivos
- Metadatos preservados

### 4. Respaldo Automático
- Copia de seguridad en la nube
- Acceso desde cualquier dispositivo
- Historial completo de procesamiento

## Configuración Avanzada

### Personalización de Carpetas
```python
# En google_drive_oauth_uploader.py
class GoogleDriveOAuthUploader:
    def __init__(self, folder_id=None):
        self.folder_id = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')
```

### Configuración de Reintentos
```python
# Configurar reintentos en caso de falla
uploader = GoogleDriveOAuthUploader()
uploader.max_retries = 3
uploader.retry_delay = 5  # segundos
```

### Filtros de Archivos
```python
# Personalizar qué archivos se suben
def upload_original_files_for_json(self, json_filename, file_types=['PDF', 'PNG']):
    # Lógica de subida con filtros personalizados
```

## Troubleshooting

### Problemas Comunes

#### 1. "No se encontraron archivos originales"
**Causa**: Los archivos PDF/PNG no están en las ubicaciones esperadas
**Solución**: Verificar rutas y nombres de archivos

#### 2. "Error de autenticación"
**Causa**: Credenciales OAuth expiradas o incorrectas
**Solución**: Regenerar credenciales siguiendo la guía de configuración

#### 3. "Error de conexión"
**Causa**: Problemas de red o firewall
**Solución**: Verificar conectividad a internet y configuración de proxy

#### 4. "Error de permisos"
**Causa**: Falta de permisos en la carpeta de Google Drive
**Solución**: Verificar permisos de la carpeta de destino

### Comandos de Diagnóstico

```bash
# Verificar configuración de Google Drive
python verificar_google_drive.py

# Probar subida directa
python test_google_drive_upload_integration.py

# Revisar logs
tail -f logs/rpa.log | grep "GOOGLE_DRIVE"
```

## Estado del Proyecto

### ✅ Completado
- [x] Integración automática en estado COMPLETED
- [x] Subida de archivos PDF y PNG
- [x] Logging detallado
- [x] Manejo de errores
- [x] Scripts de prueba
- [x] Documentación completa

### 🔄 En Desarrollo
- [ ] Configuración de carpetas personalizadas
- [ ] Filtros avanzados de archivos
- [ ] Notificaciones por email en caso de error
- [ ] Dashboard de monitoreo

### 📋 Pendiente
- [ ] Integración con Make.com webhooks
- [ ] Compresión automática de archivos grandes
- [ ] Backup automático de logs
- [ ] Métricas de rendimiento

## Conclusión

La integración de Google Drive está **completamente funcional** y se ejecuta automáticamente al finalizar el procesamiento de cada documento. Esto asegura que:

1. **Todos los archivos procesados** se suban a Google Drive
2. **El proceso sea completamente automático** sin intervención manual
3. **Se mantenga trazabilidad completa** con logs detallados
4. **Los archivos estén disponibles** para Make.com y otros sistemas

La implementación es robusta, maneja errores apropiadamente y no interfiere con el flujo principal del RPA.
