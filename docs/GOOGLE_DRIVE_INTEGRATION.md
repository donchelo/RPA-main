# 📁 Integración con Google Drive - RPA TAMAPRINT

## 🎯 Objetivo

El sistema RPA ahora sube automáticamente los archivos PNG y PDF originales a una carpeta específica de Google Drive cuando procesa las órdenes de venta.

## 🔧 Configuración Inicial

### 1. Instalar Dependencias

```bash
pip install google-auth google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### 2. Configurar Credenciales de Google Drive

1. **Ve a Google Cloud Console**: https://console.cloud.google.com/
2. **Crea o selecciona un proyecto**
3. **Habilita la API de Google Drive**:
   - Ve a "APIs & Services" > "Library"
   - Busca "Google Drive API" y habilítala
4. **Crea credenciales de cuenta de servicio**:
   - Ve a "APIs & Services" > "Credentials"
   - Clic en "Create Credentials" > "Service Account"
   - Completa los datos y descarga el archivo JSON
5. **Guarda el archivo de credenciales** como uno de estos nombres:
   - `./credentials.json`
   - `./google-credentials.json`
   - `./service-account.json`

### 3. Configurar Permisos de la Carpeta

1. **Abre la carpeta de Google Drive**: https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7
2. **Comparte la carpeta** con el email de la cuenta de servicio
3. **Dale permisos de "Editor"** para que pueda subir archivos

### 4. Ejecutar Configuración

```bash
python setup_google_drive_integration.py
```

## 📂 Estructura de Archivos

```
RPA-main/
├── data/
│   ├── outputs_json/           # Archivos JSON a procesar
│   │   └── Procesados/         # Archivos JSON procesados
│   └── original_files/         # Archivos originales (opcional)
│       ├── png/
│       └── pdf/
├── credentials.json            # Credenciales de Google Drive
└── rpa/
    └── google_drive_uploader.py  # Módulo de Google Drive
```

## 🚀 Funcionamiento Automático

### Flujo de Procesamiento

1. **El RPA procesa un archivo JSON** (ej: `4500224743.PDF.json`)
2. **Busca archivos originales** con el mismo nombre base:
   - PNG: `4500224743.png`
   - PDF: `4500224743.PDF` o `4500224743.pdf`
3. **Busca en múltiples ubicaciones**:
   - `./data/outputs_json/Procesados/`
   - `./data/outputs_json/`
   - `./data/original_files/`
   - `./data/`
4. **Sube los archivos encontrados** a Google Drive
5. **Registra el resultado** en los logs

### Ubicaciones de Búsqueda

El sistema busca archivos originales en este orden:
1. Carpeta de procesados
2. Carpeta de archivos JSON
3. Carpeta de archivos originales
4. Directorio raíz

## 📊 Monitoreo y Logs

### Logs de Google Drive

Los logs incluyen información detallada sobre:
- ✅ Archivos encontrados para subir
- ✅ Estado de autenticación con Google Drive
- ✅ Progreso de subida de archivos
- ✅ Enlaces a archivos subidos
- ❌ Errores de conexión o permisos

### Ejemplo de Log

```
[2024-01-15 10:30:15] Iniciando subida de archivos originales a Google Drive | Archivo: 4500224743.PDF.json
[2024-01-15 10:30:15] Buscando archivos originales para subir | Base: 4500224743
[2024-01-15 10:30:16] Subiendo archivo a Google Drive | Archivo: 4500224743.png
[2024-01-15 10:30:18] Archivo subido exitosamente | Nombre: 4500224743.png, ID: 1abc123def456
[2024-01-15 10:30:18] Archivos originales subidos a Google Drive exitosamente | Subidos: 2/2
```

## 🔧 Configuración Avanzada

### config.yaml

```yaml
google_drive:
  enabled: true                    # Habilitar/deshabilitar Google Drive
  folder_id: "17zOU8KlONbkfzvEyHRcXx9IvhUA7"  # ID de carpeta destino
  upload_original_files: true      # Subir archivos originales
  upload_screenshots: false        # No subir screenshots del RPA
```

### Variables de Entorno (Opcional)

```bash
export GOOGLE_APPLICATION_CREDENTIALS="./credentials.json"
```

## 🛠️ Resolución de Problemas

### Error: "Credenciales no encontradas"

**Solución**: 
- Verifica que el archivo de credenciales existe
- Verifica el nombre del archivo (debe ser exacto)
- Usa la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS`

### Error: "Acceso denegado"

**Solución**:
- Verifica que la carpeta de Google Drive está compartida con la cuenta de servicio
- Verifica que la cuenta de servicio tiene permisos de "Editor"
- Verifica que el folder_id es correcto

### Error: "Archivos no encontrados"

**Solución**:
- Verifica que los archivos PNG/PDF están en las ubicaciones correctas
- Verifica que los nombres de archivo coinciden con el JSON
- Revisa los logs para ver dónde está buscando el sistema

### Error: "Módulo no disponible"

**Solución**:
```bash
pip install google-auth google-api-python-client
```

## 📋 Lista de Verificación

Antes de usar el sistema, verifica:

- [ ] ✅ Dependencias instaladas
- [ ] ✅ Credenciales de Google Drive configuradas
- [ ] ✅ Carpeta de Google Drive compartida
- [ ] ✅ Archivos originales en ubicaciones correctas
- [ ] ✅ Script de configuración ejecutado sin errores

## 🎯 Carpeta de Destino

**ID de Carpeta**: `17zOU8KlONbkfzvEyHRcXx9IvhUA7`

**Enlace**: https://drive.google.com/drive/folders/17zOU8KlONbkfzvEyHRcXx9IvhUA7

Los archivos se subirán automáticamente a esta carpeta con sus nombres originales.

## 📞 Soporte

Si tienes problemas con la integración:

1. **Revisa los logs** en `./logs/rpa.log`
2. **Ejecuta el script de configuración** `python setup_google_drive_integration.py`
3. **Verifica las credenciales** y permisos de la carpeta
4. **Contacta al equipo técnico** con los logs de error
