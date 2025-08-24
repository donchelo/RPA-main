# Guía del Launcher de Ventas RPA TAMAPRINT v3.0

## Descripción

El Launcher de Ventas es una aplicación mejorada que procesa automáticamente las órdenes de venta que se encuentran en la carpeta `01_Pendiente`. Esta versión incluye mejor logging, manejo de errores y una interfaz más intuitiva.

## Archivos Principales

- `launcher_ventas_mejorado.py` - Launcher principal con interfaz gráfica
- `launcher_ventas_mejorado.bat` - Archivo batch para ejecutar fácilmente
- `diagnostico_launcher_ventas.py` - Script de diagnóstico
- `test_launcher_ventas.py` - Script de prueba

## Estructura de Directorios

```
data/outputs_json/sales_order/
├── 01_Pendiente/     # Archivos JSON pendientes de procesar
├── 02_Procesando/    # Archivos en proceso
├── 03_Completado/    # Archivos procesados exitosamente
├── 04_Error/         # Archivos con errores
└── 05_Archivado/     # Archivos archivados
```

## Cómo Usar el Launcher

### 1. Ejecutar el Launcher

**Opción A: Usando el archivo batch (Recomendado)**
```bash
# Doble clic en el archivo
launcher_ventas_mejorado.bat
```

**Opción B: Usando Python directamente**
```bash
python launcher_ventas_mejorado.py
```

### 2. Interfaz del Launcher

La interfaz incluye:

- **Botón "Iniciar Procesamiento Automático"**: Inicia el procesamiento automático
- **Botón "Actualizar Estado"**: Actualiza los contadores de archivos
- **Botón "Limpiar Logs"**: Limpia la ventana de logs
- **Contadores**: Muestran el número de archivos en cada estado
- **Logs**: Muestran el progreso en tiempo real

### 3. Procesamiento Automático

1. **Iniciar**: Haz clic en "Iniciar Procesamiento Automático"
2. **Monitoreo**: El launcher monitorea continuamente la carpeta `01_Pendiente`
3. **Procesamiento**: Cuando encuentra un archivo:
   - Lo mueve a `02_Procesando`
   - Procesa los datos con el RPA
   - Lo mueve a `03_Completado` (éxito) o `04_Error` (error)
4. **Continuo**: Repite el proceso hasta que no hay más archivos pendientes
5. **Espera**: Si no hay archivos, espera 10 segundos y verifica nuevamente

### 4. Detener el Procesamiento

Haz clic en "Detener Procesamiento" para parar el procesamiento automático.

## Formato de Archivos JSON

Los archivos en `01_Pendiente` deben tener el siguiente formato:

```json
{
  "orden_compra": "4500226075",
  "fecha_documento": "22/08/2025",
  "fecha_entrega": "26/08/2025",
  "comprador": {
    "nit": "CN800069933",
    "nombre": "COMODIN S.A.S."
  },
  "items": [
    {
      "descripcion": "ETI_PAPE_CHE_11.5X6.9_HERI_F_, AZU194021",
      "codigo": "14010699001",
      "cantidad": 120,
      "precio_unitario": 304,
      "precio_total": 36480,
      "fecha_entrega": "26/08/2025"
    }
  ],
  "valor_total": 36480,
  "total_items_unicos": 1,
  "numero_items_totales": 120
}
```

## Campos Requeridos

- `orden_compra`: Número de orden de compra
- `comprador.nit`: NIT del comprador
- `comprador.nombre`: Nombre del comprador
- `fecha_entrega`: Fecha de entrega
- `items`: Array de items (al menos uno)
- `items[].codigo`: Código del producto
- `items[].cantidad`: Cantidad del producto

## Diagnóstico y Pruebas

### Ejecutar Diagnóstico
```bash
python diagnostico_launcher_ventas.py
```

### Ejecutar Prueba
```bash
python test_launcher_ventas.py
```

## Solución de Problemas

### El launcher no procesa archivos

1. **Verificar archivos pendientes**:
   ```bash
   python diagnostico_launcher_ventas.py
   ```

2. **Verificar formato JSON**:
   - Asegúrate de que los archivos JSON sean válidos
   - Verifica que tengan todos los campos requeridos

3. **Verificar permisos**:
   - Asegúrate de que el launcher tenga permisos para leer/escribir en las carpetas

### Error en el procesamiento

1. **Revisar logs**: Los errores se muestran en la ventana de logs
2. **Verificar archivos en 04_Error**: Los archivos con errores se mueven aquí
3. **Revisar formato de datos**: Verifica que los datos en el JSON sean correctos

### El launcher se cuelga

1. **Detener procesamiento**: Haz clic en "Detener Procesamiento"
2. **Reiniciar**: Cierra y vuelve a abrir el launcher
3. **Verificar archivos**: Asegúrate de que no haya archivos corruptos

## Características del Launcher Mejorado

- ✅ **Procesamiento automático continuo**
- ✅ **Logging detallado en tiempo real**
- ✅ **Manejo de errores robusto**
- ✅ **Interfaz intuitiva**
- ✅ **Estadísticas de procesamiento**
- ✅ **Monitoreo de estado de archivos**
- ✅ **Pausa automática entre archivos**
- ✅ **Detección automática de archivos nuevos**

## Archivos de Prueba

Se incluyen archivos de prueba en `01_Pendiente`:
- `4500226075.PDF.json`
- `4500226076.PDF.json`
- `4500226077.PDF.json`

Estos archivos se pueden usar para probar el funcionamiento del launcher.

## Notas Importantes

1. **No modificar archivos en proceso**: Los archivos en `02_Procesando` no deben ser modificados manualmente
2. **Backup de archivos**: Siempre haz backup de archivos importantes antes de procesarlos
3. **Monitoreo**: Revisa regularmente los logs para detectar problemas
4. **Mantenimiento**: Limpia periódicamente la carpeta `05_Archivado`

## Soporte

Si tienes problemas con el launcher:

1. Ejecuta el diagnóstico: `python diagnostico_launcher_ventas.py`
2. Revisa los logs del launcher
3. Verifica que los archivos JSON tengan el formato correcto
4. Asegúrate de que todas las carpetas existan y tengan permisos correctos
