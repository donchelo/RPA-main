# FLUJO ACTUALIZADO DEL RPA

## **🎯 VISIÓN GENERAL**

El Sistema RPA automatiza la inserción de órdenes de venta en SAP Business One, procesando archivos JSON y ejecutando una secuencia de pasos automatizados para completar el proceso de forma eficiente y confiable.

## **📋 FLUJO PRINCIPAL ACTUALIZADO**

### **1. INICIALIZACIÓN DEL SISTEMA**
```
┌─────────────────────────────────────┐
│ 1. VERIFICAR ARCHIVOS JSON         │
│    • Buscar en ./data/outputs_json/│
│    • Filtrar solo archivos .json   │
│    • Excluir directorios y temp    │
└─────────────────────────────────────┘
```

### **2. CONEXIÓN AL ESCRITORIO REMOTO**
```
┌─────────────────────────────────────┐
│ 2. ESTABLECER CONEXIÓN RDP         │
│    • Buscar ventana "20.96.6.64"  │
│    • Activar ventana si inactiva   │
│    • Maximizar: Alt+Space, X       │
│    • Capturar pantalla de confirm. │
└─────────────────────────────────────┘
```

### **3. APERTURA DE SAP BUSINESS ONE**
```
┌─────────────────────────────────────┐
│ 3. ABRIR SAP BUSINESS ONE          │
│    • Template matching: sap_icon   │
│    • Doble clic en icono           │
│    • Esperar 30 segundos           │
│    • OCR de respaldo si falla      │
└─────────────────────────────────────┘
```

### **4. NAVEGACIÓN A ORDEN DE VENTAS**
```
┌─────────────────────────────────────┐
│ 4. NAVEGAR A ORDEN DE VENTAS       │
│    • Alt+M: Abrir menú módulos    │
│    • V: Seleccionar módulo Ventas  │
│    • Template matching: botón      │
│    • Clic en "Orden de Ventas"     │
└─────────────────────────────────────┘
```

### **5. CARGA DE DATOS DEL CLIENTE**
```
┌─────────────────────────────────────┐
│ 5. CARGAR DATOS BÁSICOS            │
│    • NIT del comprador             │
│    • Enter para confirmar          │
│    • 3 TABs → Orden de compra      │
│    • 4 TABs → Fecha de entrega     │
└─────────────────────────────────────┘
```

### **6. CARGA DE ARTÍCULOS**
```
┌─────────────────────────────────────┐
│ 6. PROCESAR ARTÍCULOS              │
│    • Para cada artículo:           │
│      - Código del artículo         │
│      - 2 TABs → Cantidad          │
│      - Cantidad                    │
│      - 3 TABs (siguiente) o 1 TAB │
│        (último artículo)           │
└─────────────────────────────────────┘
```

### **7. CAPTURA DE PANTALLA COMPLETA**
```
┌─────────────────────────────────────┐
│ 7. TOMAR CAPTURA DE PANTALLA       │
│    • Captura completa de pantalla  │
│    • Guardar como [filename]_totales│
│    • Log de confirmación           │
└─────────────────────────────────────┘
```

### **8. FINALIZACIÓN**
```
┌─────────────────────────────────────┐
│ 8. COMPLETAR PROCESO               │
│    • Mover archivo a Procesados/   │
│    • Logging de confirmación       │
│    • Continuar con siguiente arch. │
└─────────────────────────────────────┘
```

## **🔄 FLUJO DETALLADO POR ARCHIVO**

### **Para cada archivo JSON:**

1. **LECTURA Y VALIDACIÓN**
   - Leer archivo JSON
   - Validar estructura de datos
   - Extraer información del cliente y artículos

2. **CONEXIÓN Y PREPARACIÓN**
   - Conectar al escritorio remoto
   - Maximizar ventana
   - Abrir SAP Business One
   - Navegar a Orden de Ventas

3. **INSERCIÓN DE DATOS**
   - Cargar NIT del comprador
   - Cargar orden de compra
   - Cargar fecha de entrega
   - Procesar cada artículo

4. **CAPTURA Y FINALIZACIÓN**
   - Tomar captura de pantalla completa
   - Mover archivo procesado
   - Continuar con siguiente archivo

## **⚡ SECUENCIA DE COMANDOS**

### **Navegación por Teclado:**
```
TAB → Navegación hacia adelante
Shift + TAB → Navegación hacia atrás
Alt + M → Abrir menú módulos
Enter → Confirmar/activar
Alt + Space → Menú de ventana
X → Maximizar ventana
```

### **Timing Crítico:**
```
Entre caracteres: 0.2 segundos
Entre campos: 2-3 segundos
Después de códigos: 3 segundos adicionales
Después de cantidades: 2 segundos
Captura de pantalla: Inmediata
```

## **🎯 PUNTOS DE CONTROL**

### **Verificaciones Automáticas:**
1. **Existencia de archivos JSON** en directorio
2. **Conexión al escritorio remoto** activa
3. **SAP Business One** abierto correctamente
4. **Navegación a Orden de Ventas** exitosa
5. **Carga de datos** sin errores
6. **Procesamiento de artículos** completo
7. **Captura de pantalla** exitosa
8. **Movimiento de archivo** a procesados

### **Logging en Cada Paso:**
```
ACTION: [Descripción de la acción]
DETAILS: [Detalles específicos]
PERFORMANCE: [Tiempo de ejecución]
ERROR: [Errores si los hay]
```

## **🛡️ MANEJO DE ERRORES**

### **Estrategias de Recuperación:**
1. **Reintentos automáticos** para operaciones críticas
2. **Múltiples métodos de detección** (template + OCR)
3. **Logging detallado** para diagnóstico
4. **Continuación del proceso** aunque falle un archivo

### **Errores Comunes:**
- Ventana de escritorio remoto no encontrada
- SAP no se abre correctamente
- Botón de Orden de Ventas no encontrado
- Error en carga de artículos
- Problemas de timing o navegación

## **📊 MÉTRICAS DE RENDIMIENTO**

### **Tiempos Estimados:**
- **Por artículo**: ~18 segundos
- **Por archivo**: ~90 segundos
- **Captura de pantalla**: ~1 segundo
- **Maximización de ventana**: ~2 segundos

### **Tasa de Éxito:**
- **Conexión RDP**: >95%
- **Apertura de SAP**: >90%
- **Navegación**: >85%
- **Procesamiento completo**: >80%

## **🔧 CONFIGURACIÓN DEL SISTEMA**

### **Archivos de Configuración:**
- **Imágenes de referencia**: `./rpa/vision/reference_images/`
- **Logs**: `./logs/rpa.log`
- **Archivos de entrada**: `./data/outputs_json/`
- **Archivos procesados**: `./data/outputs_json/Procesados/`

### **Dependencias Críticas:**
- Python 3.8+
- PyAutoGUI
- OpenCV
- Tesseract OCR
- EasyOCR

## **🎯 OBJETIVOS DEL SISTEMA**

### **Automatización Completa:**
1. **Procesamiento automático** de archivos JSON
2. **Navegación inteligente** en SAP Business One
3. **Detección visual** de elementos de interfaz
4. **Captura automática** de pantalla completa
5. **Gestión de archivos** procesados

### **Confiabilidad:**
1. **Logging detallado** de todas las operaciones
2. **Manejo robusto** de errores
3. **Reintentos automáticos** para operaciones críticas
4. **Continuación del proceso** aunque fallen archivos individuales

### **Eficiencia:**
1. **Procesamiento en lote** de múltiples archivos
2. **Optimización de timing** para escritorio remoto
3. **Métricas de rendimiento** para monitoreo
4. **Configuración flexible** para diferentes entornos

---

**NOTA**: Este flujo actualizado simplifica el proceso eliminando el scroll automático y enfocándose en la captura directa de pantalla completa después de procesar todos los artículos. 