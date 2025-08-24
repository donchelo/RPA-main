# 🚀 GUÍA DE FUNCIONAMIENTO - RPA TAMAPRINT v3.0

## 📋 Cómo Funciona el Sistema

### 🎯 **Concepto Principal**

El sistema RPA TAMAPRINT v3.0 funciona como un **procesador automático de cola de archivos JSON**. Aquí te explico paso a paso cómo funciona:

## 🔄 **Flujo de Procesamiento**

### 1. **Estructura de Carpetas**
```
data/outputs_json/
├── 01_Pendiente/     ← Archivos que esperan ser procesados
├── 02_Procesando/    ← Archivos que están siendo procesados
├── 03_Completado/    ← Archivos procesados exitosamente
├── 04_Error/         ← Archivos que fallaron en el procesamiento
└── 05_Archivado/     ← Archivos archivados
```

### 2. **Proceso Automático**
1. **Detección**: El sistema verifica constantemente la carpeta `01_Pendiente`
2. **Selección**: Toma el primer archivo JSON que encuentre
3. **Movimiento**: Lo mueve a `02_Procesando` (para evitar duplicados)
4. **Procesamiento**: Ejecuta la lógica del módulo seleccionado
5. **Resultado**: 
   - ✅ **Éxito**: Mueve a `03_Completado`
   - ❌ **Error**: Mueve a `04_Error`

## 🎮 **Cómo Usar el Launcher Completo**

### **Paso 1: Ejecutar el Launcher**
```bash
# Opción 1: Archivo batch (Recomendado)
launcher_completo.bat

# Opción 2: Comando directo
python launcher_completo.py
```

### **Paso 2: Seleccionar Módulo**
- **Módulo de Ventas**: Para procesar órdenes de venta en SAP Business One
- **Módulo de Producción**: Para procesar órdenes de producción en SAP Business One

### **Paso 3: Iniciar Procesamiento Automático**
- Hacer clic en **"Iniciar Procesamiento Automático"**
- El sistema comenzará a procesar automáticamente todos los archivos en la cola

## 📊 **Panel de Estado**

### **Contadores en Tiempo Real**
- **Pendientes**: Archivos esperando ser procesados
- **Procesando**: Archivos actualmente en procesamiento
- **Completados**: Archivos procesados exitosamente
- **Errores**: Archivos que fallaron en el procesamiento

### **Información del Sistema**
- **Estado**: Activo/Inactivo
- **Archivo actual**: Nombre del archivo siendo procesado
- **Logs**: Información detallada de cada operación

## 🔧 **Funcionalidades Disponibles**

### **1. Procesamiento Automático**
- ✅ Procesa automáticamente todos los archivos en la cola
- ✅ Maneja errores y mueve archivos a las carpetas correspondientes
- ✅ Continúa procesando hasta que no queden archivos pendientes
- ✅ Se puede detener en cualquier momento

### **2. Procesamiento Manual**
- ✅ Seleccionar un archivo específico para procesar
- ✅ Útil para pruebas o archivos especiales

### **3. Pruebas de Módulos**
- ✅ Probar la funcionalidad del módulo seleccionado
- ✅ Verificar que el sistema esté funcionando correctamente

### **4. Sistema de Logs**
- ✅ Logs en tiempo real de todas las operaciones
- ✅ Posibilidad de guardar logs en archivo
- ✅ Limpiar logs cuando sea necesario

## 📁 **Estructura de Archivos JSON**

### **Ejemplo de Archivo de Orden de Venta**
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

## 🎯 **Casos de Uso**

### **Escenario 1: Procesamiento Automático**
1. Colocar archivos JSON en `data/outputs_json/01_Pendiente/`
2. Seleccionar módulo (Ventas o Producción)
3. Hacer clic en "Iniciar Procesamiento Automático"
4. El sistema procesará todos los archivos automáticamente

### **Escenario 2: Procesamiento Manual**
1. Seleccionar módulo
2. Hacer clic en "Procesar Archivo Manual"
3. Seleccionar archivo JSON específico
4. El sistema procesará solo ese archivo

### **Escenario 3: Monitoreo**
1. Ejecutar el launcher
2. Ver el estado de la cola en tiempo real
3. Revisar logs para información detallada
4. Usar "Actualizar Estado" para refrescar contadores

## ⚠️ **Consideraciones Importantes**

### **Antes de Iniciar**
- ✅ Asegurarse de que SAP Business One esté abierto
- ✅ Verificar que el escritorio remoto esté activo
- ✅ Tener archivos JSON válidos en la carpeta de pendientes

### **Durante el Procesamiento**
- ✅ No cerrar SAP Business One
- ✅ No mover archivos manualmente entre carpetas
- ✅ El sistema se puede detener en cualquier momento

### **Después del Procesamiento**
- ✅ Revisar logs para verificar resultados
- ✅ Verificar archivos en carpetas de completados/errores
- ✅ Guardar logs si es necesario

## 🔍 **Solución de Problemas**

### **Si el sistema no procesa archivos**
1. Verificar que hay archivos en `01_Pendiente/`
2. Revisar logs para errores específicos
3. Verificar que el módulo esté seleccionado
4. Comprobar que el procesamiento esté activo

### **Si hay errores en archivos**
1. Revisar archivos en `04_Error/`
2. Verificar formato JSON de los archivos
3. Revisar logs para detalles del error
4. Corregir archivos y moverlos de vuelta a `01_Pendiente/`

### **Si el sistema se detiene**
1. Verificar que no haya errores críticos
2. Revisar logs para información
3. Reiniciar el procesamiento automático
4. Verificar archivos en `02_Procesando/`

## 📞 **Soporte**

Para cualquier problema o duda:
- **Email**: hola@ai4u.com.co
- **Logs**: Revisar logs del sistema para detalles técnicos
- **Documentación**: Consultar esta guía y archivos de documentación

---

**🤖 AI4U | Automatización Inteligente para Ti!**
*RPA TAMAPRINT v3.0 - Sistema de Procesamiento Automático*
