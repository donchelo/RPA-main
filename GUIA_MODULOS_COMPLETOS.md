# 🚀 Guía Completa de Módulos RPA TAMAPRINT v3.0

## 📋 Descripción General

El sistema RPA TAMAPRINT v3.0 incluye **dos módulos independientes** que funcionan en la misma pantalla de SAP Business One:

1. **🏪 Módulo de Órdenes de Venta**
2. **🏭 Módulo de Órdenes de Producción**

Ambos módulos asumen que SAP ya está abierto y funcionan independientemente.

## 🔧 Características de Ambos Módulos

### ✅ Características Comunes
- **Navegación independiente**: Cada módulo navega a su sección específica
- **Misma pantalla base**: Ambos funcionan desde el escritorio de SAP
- **Procesamiento automático**: Procesan archivos JSON automáticamente
- **Logs detallados**: Muestran el progreso en tiempo real
- **Pruebas integradas**: Incluyen función de prueba para verificar funcionamiento

### 🏪 Módulo de Órdenes de Venta
- **Navegación**: `Alt + M` → `V` → "Orden de Ventas"
- **Campos procesados**:
  - NIT del cliente
  - Número de orden
  - Items y cantidades
- **Resultado**: Screenshot final de la orden

### 🏭 Módulo de Órdenes de Producción
- **Navegación**: `Alt + M` → `P` → "Orden de Fabricación"
- **Campos procesados**:
  - Número de artículo
  - Número de pedido interno
  - Cantidad
  - Fecha de finalización
- **Resultado**: Screenshot final de la orden

## 🚀 Cómo Usar el Sistema

### Paso 1: Preparar SAP
1. **Abrir SAP Business One**
2. **Asegurar que esté en la pantalla del escritorio**
3. **Maximizar la ventana**
4. **Tener el escritorio remoto activo**

### Paso 2: Ejecutar Launcher
```bash
launcher_funcional.bat
```

### Paso 3: Seleccionar Módulo
En el launcher, selecciona uno de los dos módulos:

#### Para Órdenes de Venta:
1. Hacer clic en **"Seleccionar Módulo de Ventas"**
2. Verificar que aparezca **"Módulo: Órdenes de Venta"**

#### Para Órdenes de Producción:
1. Hacer clic en **"Seleccionar Módulo de Producción"**
2. Verificar que aparezca **"Módulo: Órdenes de Producción"**

### Paso 4: Procesar Archivos

#### Opción A: Procesamiento Automático
1. Hacer clic en **"Iniciar Procesamiento Automático"**
2. El sistema procesará automáticamente todos los archivos en la cola
3. Los archivos se moverán entre carpetas según su estado

#### Opción B: Procesamiento Manual
1. Hacer clic en **"Procesar Archivo Manual"**
2. Seleccionar un archivo JSON específico
3. El sistema procesará solo ese archivo

#### Opción C: Probar Módulo
1. Hacer clic en **"Probar Módulo"**
2. El sistema ejecutará una prueba de navegación
3. Verificará que el módulo funcione correctamente

## 📁 Estructura de Archivos

### Directorios de Procesamiento
```
data/outputs_json/
├── 01_Pendiente/     # Archivos por procesar
├── 02_Procesando/    # Archivos en proceso
├── 03_Completado/    # Archivos procesados exitosamente
├── 04_Error/         # Archivos con errores
└── 05_Archivado/     # Archivos archivados
```

### Formato de Archivos

#### Para Órdenes de Venta:
```json
{
  "orden_compra": "OC001",
  "comprador": {
    "nombre": "Cliente Ejemplo",
    "nit": "123456789"
  },
  "items": [
    {
      "codigo": "ART001",
      "cantidad": 10,
      "descripcion": "Producto de ejemplo"
    }
  ]
}
```

#### Para Órdenes de Producción:
```json
{
  "numero_articulo": "ART001",
  "numero_pedido_interno": "PI001",
  "cantidad": 100,
  "fecha_finalizacion": "25/12/2024",
  "unidad_medida": "PCS",
  "centro_trabajo": "CT001"
}
```

## 🧪 Pruebas Disponibles

### Pruebas de Componentes
```bash
# Prueba del módulo de ventas
python test_launcher_simple.py

# Prueba del módulo de producción
python test_produccion_simple.py

# Prueba de navegación de ventas
python test_navegacion_sap.py

# Prueba de navegación de producción
python test_navegacion_produccion.py
```

### Pruebas desde el Launcher
- **"Probar Módulo"**: Ejecuta prueba de navegación del módulo seleccionado
- **Logs en tiempo real**: Muestra el progreso de las pruebas

## 📊 Monitoreo y Logs

### Logs del Sistema
- **Logs en tiempo real**: Se muestran en la interfaz del launcher
- **Archivos de log**: Se guardan en `logs/` con timestamp
- **Screenshots**: Se guardan en `screenshots/` con timestamp

### Estados de Procesamiento
- **🔄 Procesando**: Archivo en proceso
- **✅ Completado**: Procesamiento exitoso
- **❌ Error**: Error en el procesamiento
- **📁 Archivado**: Archivo procesado y archivado

## 🔍 Solución de Problemas

### Problemas Comunes

#### 1. "SAP no está abierto"
**Solución**: Asegúrate de que SAP Business One esté abierto y en la pantalla del escritorio

#### 2. "No se encuentra el botón"
**Solución**: Verifica que las imágenes de referencia existan en `rpa/vision/reference_images/`

#### 3. "Error de navegación"
**Solución**: Ejecuta la prueba del módulo para verificar la navegación

#### 4. "Archivo no válido"
**Solución**: Verifica que el archivo JSON tenga el formato correcto

### Verificación de Estado
```bash
# Verificar componentes
python diagnostico_launcher.py

# Verificar imágenes de referencia
python test_produccion_simple.py
```

## 🎯 Flujos de Trabajo

### Flujo para Órdenes de Venta
1. **Preparar SAP**: Abrir y maximizar SAP
2. **Ejecutar launcher**: `launcher_funcional.bat`
3. **Seleccionar módulo**: "Módulo de Ventas"
4. **Procesar archivos**: Automático o manual
5. **Verificar resultados**: Revisar logs y screenshots

### Flujo para Órdenes de Producción
1. **Preparar SAP**: Abrir y maximizar SAP
2. **Ejecutar launcher**: `launcher_funcional.bat`
3. **Seleccionar módulo**: "Módulo de Producción"
4. **Procesar archivos**: Automático o manual
5. **Verificar resultados**: Revisar logs y screenshots

## ✅ Estado Final

**Ambos módulos están completamente funcionales:**

- ✅ **Módulo de Ventas**: Funcionando perfectamente
- ✅ **Módulo de Producción**: Funcionando perfectamente
- ✅ **Navegación independiente**: Cada módulo va a su sección
- ✅ **Procesamiento automático**: Funciona para ambos módulos
- ✅ **Pruebas integradas**: Disponibles para ambos módulos
- ✅ **Logs detallados**: Monitoreo completo del proceso

**El sistema está listo para uso en producción con ambos módulos.** 🚀
