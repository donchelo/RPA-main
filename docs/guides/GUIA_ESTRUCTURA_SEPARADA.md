# 📁 Guía de Estructura de Directorios Separados RPA TAMAPRINT v3.0

## 🎯 Objetivo

Separar completamente los archivos de órdenes de venta y órdenes de producción para una mejor organización y control del procesamiento.

## 📂 Nueva Estructura de Directorios

```
data/outputs_json/
├── sales_order/                    # 🏪 Módulo de Órdenes de Venta
│   ├── 01_Pendiente/              # Archivos por procesar
│   ├── 02_Procesando/             # Archivos en proceso
│   ├── 03_Completado/             # Archivos procesados exitosamente
│   ├── 04_Error/                  # Archivos con errores
│   └── 05_Archivado/              # Archivos archivados
│
└── production_order/               # 🏭 Módulo de Órdenes de Producción
    ├── 01_Pendiente/              # Archivos por procesar
    ├── 02_Procesando/             # Archivos en proceso
    ├── 03_Completado/             # Archivos procesados exitosamente
    ├── 04_Error/                  # Archivos con errores
    └── 05_Archivado/              # Archivos archivados
```

## 🚀 Cómo Usar la Nueva Estructura

### Para Órdenes de Venta

1. **Colocar archivos**: Copia tus archivos JSON de ventas en:
   ```
   data/outputs_json/sales_order/01_Pendiente/
   ```

2. **Formato requerido**:
   ```json
   {
     "orden_compra": "OC001",
     "comprador": {
       "nombre": "Cliente Ejemplo S.A.",
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

3. **Seleccionar módulo**: En el launcher, selecciona "Módulo de Ventas"

4. **Procesar**: El sistema procesará solo los archivos de la carpeta de ventas

### Para Órdenes de Producción

1. **Colocar archivos**: Copia tus archivos JSON de producción en:
   ```
   data/outputs_json/production_order/01_Pendiente/
   ```

2. **Formato requerido**:
   ```json
   {
     "numero_articulo": "101846",
     "numero_pedido_interno": "6107",
     "cantidad": 100,
     "fecha_finalizacion": "25/12/2025",
     "unidad_medida": "PCS",
     "centro_trabajo": "CT001"
   }
   ```

3. **Seleccionar módulo**: En el launcher, selecciona "Módulo de Producción"

4. **Procesar**: El sistema procesará solo los archivos de la carpeta de producción

## 🔄 Flujo de Procesamiento

### Flujo Automático

1. **Colocar archivos** en la carpeta `01_Pendiente` del módulo correspondiente
2. **Ejecutar launcher**: `launcher_funcional.bat`
3. **Seleccionar módulo** (Ventas o Producción)
4. **Iniciar procesamiento automático**
5. **Monitorear**: Los archivos se mueven automáticamente entre carpetas

### Estados de los Archivos

- **01_Pendiente**: Archivos por procesar
- **02_Procesando**: Archivos en proceso actual
- **03_Completado**: Archivos procesados exitosamente
- **04_Error**: Archivos con errores durante el procesamiento
- **05_Archivado**: Archivos archivados después del procesamiento

## 📊 Ventajas de la Separación

### ✅ Beneficios

1. **Organización clara**: Cada módulo tiene su propia estructura
2. **Procesamiento independiente**: No hay mezcla de archivos entre módulos
3. **Control granular**: Puedes procesar solo ventas o solo producción
4. **Trazabilidad**: Fácil seguimiento de archivos por módulo
5. **Mantenimiento**: Más fácil de mantener y debuggear

### 🎯 Casos de Uso

#### Escenario 1: Solo Ventas
- Colocar archivos en `sales_order/01_Pendiente/`
- Seleccionar "Módulo de Ventas" en el launcher
- Procesar automáticamente

#### Escenario 2: Solo Producción
- Colocar archivos en `production_order/01_Pendiente/`
- Seleccionar "Módulo de Producción" en el launcher
- Procesar automáticamente

#### Escenario 3: Ambos Módulos
- Colocar archivos de ventas en `sales_order/01_Pendiente/`
- Colocar archivos de producción en `production_order/01_Pendiente/`
- Procesar cada módulo por separado

## 🧪 Verificación

### Script de Verificación

Ejecuta el script para verificar que la estructura esté correcta:

```bash
python verificar_estructura_separada.py
```

Este script verifica:
- ✅ Existencia de todas las carpetas
- ✅ Contenido de archivos por módulo
- ✅ Formato de archivos de ejemplo

### Verificación Manual

1. **Verificar estructura**:
   ```
   data/outputs_json/sales_order/01_Pendiente/     # Debe existir
   data/outputs_json/production_order/01_Pendiente/ # Debe existir
   ```

2. **Verificar archivos de ejemplo**:
   - `sales_order/01_Pendiente/orden_venta_ejemplo_001.json`
   - `production_order/01_Pendiente/orden_produccion_ejemplo_001.json`

## 🔧 Configuración del Launcher

El launcher funcional ha sido actualizado para:

- **Detectar automáticamente** el módulo seleccionado
- **Cambiar directorios** según el módulo
- **Procesar solo** los archivos del módulo correspondiente
- **Mostrar logs** específicos del módulo

### Logs del Sistema

Cuando seleccionas un módulo, verás logs como:
```
[15:00:00] Módulo seleccionado: sales_order
[15:00:01] 📁 Directorios actualizados para módulo de ventas
[15:00:02] 📄 Procesando archivo: orden_venta_001.json
```

## 📝 Ejemplos de Archivos

### Archivo de Venta de Ejemplo

```json
{
  "orden_compra": "OC001",
  "comprador": {
    "nombre": "Cliente Ejemplo S.A.",
    "nit": "123456789"
  },
  "items": [
    {
      "codigo": "ART001",
      "cantidad": 10,
      "descripcion": "Producto de ejemplo 1"
    },
    {
      "codigo": "ART002",
      "cantidad": 5,
      "descripcion": "Producto de ejemplo 2"
    }
  ]
}
```

### Archivo de Producción de Ejemplo

```json
{
  "numero_articulo": "101846",
  "numero_pedido_interno": "6107",
  "cantidad": 100,
  "fecha_finalizacion": "25/12/2025",
  "unidad_medida": "PCS",
  "centro_trabajo": "CT001",
  "observaciones": "Orden de producción de ejemplo para el RPA"
}
```

## ✅ Estado Final

**La nueva estructura está completamente implementada:**

- ✅ **Carpetas separadas** para cada módulo
- ✅ **Archivos de ejemplo** creados
- ✅ **Launcher actualizado** para usar la nueva estructura
- ✅ **Script de verificación** disponible
- ✅ **Documentación completa** actualizada

**El sistema está listo para usar con la nueva estructura separada.** 🚀
