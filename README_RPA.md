# DOCUMENTACIÓN ESPECIALIZADA - SISTEMA RPA

## **DESCRIPCIÓN GENERAL**

El Sistema RPA (Robotic Process Automation) automatiza la inserción de órdenes de venta en SAP Business One. El sistema procesa archivos JSON que contienen información de pedidos y los inserta automáticamente en la aplicación SAP.

## **ARQUITECTURA DEL SISTEMA**

### **Componentes Principales:**

1. **RPA Main** (`rpa/main.py`): Lógica principal de automatización
2. **Vision System** (`rpa/vision/main.py`): Detección visual y template matching
3. **Logger** (`rpa/logger.py`): Sistema de logging detallado
4. **JSON Parser** (`json_parser/main.py`): Procesamiento de archivos JSON

### **Flujo de Datos:**
```
Archivos JSON → RPA → SAP Business One → Archivos Procesados
```

## **ESTRUCTURA DE ARCHIVOS**

### **Entrada de Datos:**
- **Ubicación**: `./data/outputs_json/`
- **Formato**: Archivos JSON con extensión `.json`
- **Estructura**: Ver sección "Formato de Datos"

### **Archivos Procesados:**
- **Ubicación**: `./data/outputs_json/Procesados/`
- **Movimiento**: Automático después de procesamiento exitoso

### **Imágenes de Referencia:**
- **Ubicación**: `./rpa/vision/reference_images/`
- **Propósito**: Template matching para navegación en SAP

### **Logs:**
- **Ubicación**: `./logs/rpa.log`
- **Rotación**: Máximo 5 archivos de 10MB cada uno

## **FORMATO DE DATOS JSON**

### **Estructura Requerida:**
```json
{
  "orden_compra": "4500339540",
  "fecha_documento": "29/11/2023",
  "fecha_entrega": "14/12/2023",
  "comprador": {
    "nit": "CN890924167",
    "nombre": "C.I. HERMECO S.A."
  },
  "items": [
    {
      "descripcion": "STICKER SET x 2 4.5 CENTIMETROS OFFCORSS",
      "codigo": "201889",
      "cantidad": 1500,
      "precio_unitario": 342,
      "precio_total": 513000,
      "fecha_entrega": "14/12/2023"
    }
  ],
  "valor_total": 1643866,
  "total_items_unicos": 3,
  "numero_items_totales": 5300
}
```

### **Campos Obligatorios:**
- `orden_compra`: Número de orden (string)
- `fecha_entrega`: Fecha en formato DD/MM/YYYY
- `comprador.nit`: NIT del cliente
- `items`: Array de artículos (mínimo 1)

## **PROCESO RPA DETALLADO**

### **PASO 1: INICIALIZACIÓN**
- Verificación de archivos JSON disponibles
- Filtrado de archivos (solo .json, excluye directorios)
- Logging de archivos encontrados

### **PASO 2: CONEXIÓN AL ESCRITORIO REMOTO**
- **Ventana objetivo**: "20.96.6.64 - Conexión a Escritorio remoto"
- **Máximo intentos**: 3
- **Activación**: Activar ventana si no está activa
- **Maximización**: Alt+Space, X para maximizar
- **Verificación**: Captura de pantalla para confirmar conexión

### **PASO 3: APERTURA DE SAP BUSINESS ONE**
- **Método**: Template matching + OCR de respaldo
- **Imagen de referencia**: `sap_icon.png`
- **Umbral de confianza**: 0.7
- **Tiempo de espera**: 30 segundos después de doble clic

### **PASO 4: NAVEGACIÓN A ORDEN DE VENTAS**
1. **Alt + M**: Abrir menú módulos
2. **Tecla V**: Seleccionar módulo Ventas
3. **Template matching**: Buscar botón "Orden de Ventas"
4. **Clic**: Activar orden de ventas
5. **Verificación**: Captura de pantalla de confirmación

### **PASO 5: CARGA DE DATOS DEL CLIENTE**
- **NIT**: Escribir NIT del comprador
- **Enter**: Confirmar NIT
- **3 TABs**: Navegar al campo de orden de compra

### **PASO 6: CARGA DE ORDEN DE COMPRA**
- **Orden**: Escribir número de orden
- **4 TABs**: Navegar al campo de fecha de entrega

### **PASO 7: CARGA DE FECHA DE ENTREGA**
- **Fecha**: Escribir fecha en formato DD/MM/YYYY
- **4 TABs**: Navegar al primer artículo

### **PASO 8: CARGA DE ARTÍCULOS**
Para cada artículo:
1. **Código**: Escribir código del artículo
2. **2 TABs**: Navegar al campo de cantidad
3. **Cantidad**: Escribir cantidad
4. **Navegación**:
   - **Artículos 1-N-1**: 3 TABs (siguiente artículo)
   - **Artículo N (último)**: 1 TAB (fin de artículos)

### **PASO 9: SCROLL HACIA ABAJO**
- **Función**: `scroll_to_bottom()`
- **Acción**: Buscar barra de desplazamiento vertical
- **Proceso**: 
  1. Calcular posición de scrollbar (lado derecho)
  2. Hacer clic en la barra de desplazamiento
  3. Arrastrar hacia abajo durante 2 segundos
  4. Esperar 2 segundos adicionales
- **Logging**: Métricas de rendimiento del scroll

### **PASO 9.5: CAPTURA DE TOTALES**
- **Función**: `take_totals_screenshot()`
- **Acción**: Tomar captura de pantalla de totales
- **Proceso**:
  1. Crear directorio si no existe
  2. Generar nombre con sufijo '_totales'
  3. Tomar screenshot completo
  4. Guardar en carpeta de capturas
- **Logging**: Confirmación de captura exitosa

### **PASO 10: FINALIZACIÓN**
- **Mover archivo**: JSON → carpeta Procesados
- **Logging**: Confirmación de procesamiento exitoso

## **SISTEMA DE NAVEGACIÓN**

### **Navegación por Teclado:**
- **TAB**: Navegación hacia adelante
- **Shift + TAB**: Navegación hacia atrás
- **Alt + M**: Abrir menú módulos
- **Enter**: Confirmar/activar

### **Timing Crítico:**
- **Entre caracteres**: 0.2 segundos
- **Entre campos**: 2-3 segundos
- **Después de códigos**: 3 segundos adicionales
- **Después de cantidades**: 2 segundos

## **SISTEMA DE VISIÓN**

### **Template Matching:**
- **Librería**: OpenCV
- **Método**: TM_CCOEFF_NORMED
- **Umbrales**:
  - SAP Icon: 0.7
  - Botones: 0.8
  - Secciones: 0.5

### **OCR (Reconocimiento de Texto):**
- **Librería**: Tesseract + EasyOCR
- **Configuración**: `--oem 3 --psm 6`
- **Uso**: Detección de texto cuando template matching falla

### **Imágenes de Referencia Críticas:**
- `sap_icon.png`: Icono de SAP Business One
- `sap_ventas_order_button.png`: Botón de Orden de Ventas
- `sap_modulos_menu_button.png`: Botón de menú módulos

## **SISTEMA DE LOGGING**

### **Niveles de Log:**
- **INFO**: Información general del proceso
- **ERROR**: Errores que requieren atención
- **PERFORMANCE**: Medición de tiempos de ejecución

### **Métodos Especializados:**
- `log_action()`: Acciones específicas del RPA
- `log_error()`: Errores con contexto
- `log_performance()`: Medición de rendimiento

### **Ejemplo de Log:**
```
2025-08-03 23:05:53 - RPA - INFO - ACTION: Item 3 - Último artículo completado, navegando a totales | DETAILS: Código: 201894
```

## **MANEJO DE ERRORES**

### **Errores Comunes y Soluciones:**

#### **1. Ventana de Escritorio Remoto No Encontrada**
- **Causa**: Conexión RDP perdida
- **Solución**: Reintentos automáticos (3 intentos)
- **Log**: `Ventana de escritorio remoto no encontrada`

#### **2. SAP No Se Abre**
- **Causa**: Icono no encontrado o aplicación no responde
- **Solución**: OCR de respaldo para buscar texto "SAP"
- **Log**: `Icono de SAP Business One no encontrado`

#### **3. Botón de Orden de Ventas No Encontrado**
- **Causa**: Interfaz de SAP cambió
- **Solución**: Actualizar imagen de referencia
- **Log**: `Botón de Orden de Ventas no encontrado`

#### **4. Error en Carga de Artículos**
- **Causa**: Timing incorrecto o navegación fallida
- **Solución**: Verificar tiempos de espera
- **Log**: `Error al procesar item X`

### **Estrategias de Recuperación:**
1. **Reintentos automáticos** para operaciones críticas
2. **Múltiples métodos de detección** (template + OCR)
3. **Logging detallado** para diagnóstico
4. **Continuación del proceso** aunque falle un archivo

## **CONFIGURACIÓN Y DEPENDENCIAS**

### **Requisitos del Sistema:**
- **Python**: 3.8+
- **Sistema Operativo**: Windows 10/11
- **Resolución**: Mínimo 1920x1080
- **Tesseract**: Instalado en `C:\Program Files\Tesseract-OCR\`

### **Dependencias Principales:**
```txt
pyautogui==0.9.54
opencv-python==4.10.0.84
pytesseract==0.3.10
easyocr==1.7.0
pillow==11.0.0
numpy==2.1.3
```

### **Configuración de PyAutoGUI:**
- **Fail-safe**: Habilitado (mover mouse a esquina para parar)
- **Timing**: Configurado para escritorio remoto
- **Duración**: Movimientos suaves para mejor detección

## **MONITOREO Y MANTENIMIENTO**

### **Archivos de Monitoreo:**
- **Logs**: `./logs/rpa.log`
- **Screenshots**: `./rpa/vision/reference_images/inserted_orders/`
- **Archivos procesados**: `./data/outputs_json/Procesados/`

### **Métricas de Rendimiento:**
- **Tiempo por artículo**: ~18 segundos
- **Tiempo por archivo**: ~90 segundos
- **Tiempo total del proceso**: Variable según cantidad de archivos

### **Mantenimiento Preventivo:**
1. **Actualizar imágenes de referencia** si cambia la interfaz de SAP
2. **Revisar logs** diariamente para errores
3. **Verificar conexión RDP** antes de ejecutar
4. **Limpiar archivos temporales** semanalmente

## **TROUBLESHOOTING AVANZADO**

### **Problemas de Timing:**
```python
# Aumentar tiempos si hay problemas de estabilidad
time.sleep(3)  # En lugar de 2
pyautogui.typewrite(text, interval=0.3)  # En lugar de 0.2
```

### **Problemas de Detección Visual:**
```python
# Reducir umbral de confianza
if max_val > 0.5:  # En lugar de 0.7
```

### **Problemas de Navegación:**
```python
# Agregar TABs adicionales si es necesario
pyautogui.hotkey('tab')
pyautogui.hotkey('tab')
pyautogui.hotkey('tab')
pyautogui.hotkey('tab')  # TAB adicional
```

## **CASOS DE USO ESPECÍFICOS**

### **Caso 1: Un Solo Artículo**
- **Navegación**: 1 TAB después de cantidad
- **Log**: `Item 1 - Último artículo completado`

### **Caso 2: Múltiples Artículos**
- **Artículos 1-N-1**: 3 TABs después de cantidad
- **Artículo N**: 1 TAB después de cantidad

### **Caso 3: Sin Archivos para Procesar**
- **Log**: `No hay archivos JSON disponibles para procesar`
- **Acción**: Esperar 10 minutos y verificar de nuevo

## **BEST PRACTICES**

### **Para Desarrolladores:**
1. **Siempre agregar logging** antes de cambios críticos
2. **Probar con diferentes cantidades de artículos**
3. **Verificar timing en escritorio remoto**
4. **Mantener imágenes de referencia actualizadas**

### **Para Operadores:**
1. **Verificar conexión RDP** antes de iniciar
2. **No interferir** durante la ejecución
3. **Revisar logs** después de errores
4. **Mantener archivos JSON** en formato correcto

### **Para Mantenimiento:**
1. **Backup de imágenes de referencia** antes de cambios
2. **Documentar cambios** en la interfaz de SAP
3. **Monitorear rendimiento** regularmente
4. **Actualizar documentación** cuando sea necesario

## **CONTACTO Y SOPORTE**

### **Información del Sistema:**
- **Versión**: RPA v1.0
- **Última actualización**: Agosto 2025
- **Responsable**: Equipo de Automatización

### **Archivos Críticos:**
- **Configuración principal**: `rpa/main.py`
- **Sistema de visión**: `rpa/vision/main.py`
- **Logging**: `rpa/logger.py`
- **Entrada de datos**: `./data/outputs_json/`

---

**NOTA**: Esta documentación debe mantenerse actualizada con cualquier cambio en el sistema RPA. Los futuros agentes deben consultar esta documentación antes de realizar modificaciones al código. 