# 🚀 Guía del Launcher Funcional RPA TAMAPRINT v3.0

## 📋 Descripción

El **Launcher Funcional** es la versión mejorada del sistema RPA que realmente ejecuta el procesamiento de órdenes de venta en SAP Business One, a diferencia del launcher anterior que solo simulaba el procesamiento.

## 🔧 Características Principales

- ✅ **Procesamiento Real**: Ejecuta realmente el RPA para procesar órdenes de venta
- ✅ **Interfaz Intuitiva**: Interfaz gráfica fácil de usar
- ✅ **Procesamiento Automático**: Procesa automáticamente la cola de archivos
- ✅ **Logs Detallados**: Muestra logs en tiempo real del procesamiento
- ✅ **Control Manual**: Permite procesar archivos individuales
- ✅ **Pruebas de Módulos**: Incluye función de prueba para verificar el funcionamiento

## 🚀 Cómo Usar el Launcher Funcional

### 1. Iniciar el Sistema

**Opción A: Usando el archivo batch (Recomendado)**
```bash
# Doble clic en el archivo
launcher_funcional.bat
```

**Opción B: Usando Python directamente**
```bash
python launcher_funcional.py
```

### 2. Seleccionar Módulo

1. En la interfaz, verás la sección "Selección de Módulos y Control"
2. Haz clic en **"Seleccionar Módulo de Ventas"**
3. Verás que el botón cambia a "Módulo de Ventas Seleccionado"
4. Los botones de control se habilitarán automáticamente

### 3. Procesar Órdenes de Venta

#### Opción A: Procesamiento Automático (Recomendado)

1. Haz clic en **"Iniciar Procesamiento Automático"**
2. El sistema comenzará a procesar automáticamente todos los archivos en la carpeta `data/outputs_json/01_Pendiente/`
3. Los archivos se moverán automáticamente a:
   - `02_Procesando/` mientras se procesan
   - `03_Completado/` si el procesamiento es exitoso
   - `04_Error/` si hay algún error

#### Opción B: Procesamiento Manual

1. Haz clic en **"Procesar Archivo Manual"**
2. Selecciona un archivo JSON específico
3. El sistema procesará solo ese archivo

#### Opción C: Probar el Módulo

1. Haz clic en **"Probar Módulo"**
2. El sistema ejecutará una prueba de navegación para verificar que todo funcione correctamente

## 📁 Estructura de Archivos

```
data/outputs_json/
├── 01_Pendiente/          # Archivos por procesar
├── 02_Procesando/         # Archivos en proceso
├── 03_Completado/         # Archivos procesados exitosamente
├── 04_Error/              # Archivos con errores
└── 05_Archivado/          # Archivos archivados
```

## 📊 Monitoreo del Sistema

### Panel de Estado
- **Pendientes**: Número de archivos por procesar
- **Procesando**: Archivos actualmente en proceso
- **Completados**: Archivos procesados exitosamente
- **Errores**: Archivos que fallaron

### Logs en Tiempo Real
- El panel derecho muestra logs detallados del procesamiento
- Incluye timestamps y mensajes descriptivos
- Puedes limpiar o guardar los logs

## 🔍 Solución de Problemas

### Problema: "No pasa nada al hacer clic en Iniciar Sistema"

**Solución:**
1. Verifica que hayas seleccionado un módulo (Ventas)
2. Asegúrate de que hay archivos JSON en `data/outputs_json/01_Pendiente/`
3. Ejecuta la prueba del módulo para verificar que funciona

### Problema: "Error al inicializar RPA"

**Solución:**
1. Ejecuta `python test_launcher_simple.py` para diagnosticar
2. Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
3. Asegúrate de estar en el directorio correcto del proyecto

### Problema: "No se encuentran archivos para procesar"

**Solución:**
1. Verifica que exista la carpeta `data/outputs_json/01_Pendiente/`
2. Asegúrate de que haya archivos JSON en esa carpeta
3. Los archivos deben tener el formato correcto (ver ejemplo abajo)

## 📄 Formato de Archivos JSON

Los archivos deben tener esta estructura:

```json
{
  "orden_compra": "4500226075",
  "comprador": {
    "nit": "900123456-7",
    "nombre": "COMODIN S.A.S."
  },
  "fecha_entrega": "25/12/2024",
  "items": [
    {
      "codigo": "ART001",
      "cantidad": 10,
      "precio_unitario": 15000
    }
  ]
}
```

## 🧪 Pruebas del Sistema

### Ejecutar Prueba Simple
```bash
python test_launcher_simple.py
```

Esta prueba verifica:
- ✅ Componentes del RPA
- ✅ Procesamiento de archivos
- ✅ Handler de ventas

### Ejecutar Diagnóstico Completo
```bash
python diagnostico_launcher.py
```

Este diagnóstico verifica:
- ✅ Directorios del sistema
- ✅ Archivos importantes
- ✅ Dependencias de Python
- ✅ Importaciones del RPA

## 📝 Logs y Debugging

### Ver Logs en Tiempo Real
- Los logs aparecen en el panel derecho del launcher
- Incluyen timestamps y mensajes descriptivos
- Puedes guardar los logs para análisis posterior

### Guardar Logs
1. Haz clic en **"Guardar Logs"**
2. Selecciona la ubicación donde guardar el archivo
3. Los logs se guardarán en formato de texto

## 🔄 Flujo de Procesamiento

1. **Detección**: El sistema detecta archivos en `01_Pendiente/`
2. **Movimiento**: Mueve el archivo a `02_Procesando/`
3. **Procesamiento**: Ejecuta el RPA para procesar la orden de venta
4. **Resultado**: 
   - ✅ Éxito: Mueve a `03_Completado/`
   - ❌ Error: Mueve a `04_Error/`
5. **Logs**: Registra todo el proceso en los logs

## ⚠️ Consideraciones Importantes

1. **Escritorio Remoto**: El RPA necesita acceso al escritorio remoto de SAP
2. **SAP Abierto**: SAP Business One debe estar abierto y accesible
3. **Permisos**: El sistema necesita permisos para controlar el mouse y teclado
4. **Resolución**: La resolución de pantalla debe ser compatible con las imágenes de referencia

## 🆘 Soporte

Si encuentras problemas:

1. **Ejecuta las pruebas**: `python test_launcher_simple.py`
2. **Revisa los logs**: En el panel de logs del launcher
3. **Verifica archivos**: Asegúrate de que los archivos JSON tengan el formato correcto
4. **Contacta soporte**: Proporciona los logs y descripción del problema

## 🎯 Próximos Pasos

1. **Configurar archivos**: Coloca archivos JSON en `data/outputs_json/01_Pendiente/`
2. **Ejecutar launcher**: Usa `launcher_funcional.bat`
3. **Seleccionar módulo**: Haz clic en "Seleccionar Módulo de Ventas"
4. **Iniciar procesamiento**: Haz clic en "Iniciar Procesamiento Automático"
5. **Monitorear**: Observa los logs y el estado de la cola

---

**¡El Launcher Funcional está listo para procesar tus órdenes de venta de manera automática!** 🚀
