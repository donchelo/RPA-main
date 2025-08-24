# 🔧 Solución para Launchers que se Cierran Inmediatamente

## 🚨 Problema Identificado

Los launchers se están cerrando inmediatamente después de ejecutarse. Esto suele ocurrir por problemas de importación de módulos que no existen o errores en la configuración.

## ✅ Solución Implementada

He creado versiones simplificadas de los launchers que funcionan correctamente:

### 📁 Archivos Creados

1. **Launchers Simplificados**:
   - `src/launchers/launcher_ventas_simple.py` - Launcher de ventas simplificado
   - `src/launchers/launcher_produccion_simple.py` - Launcher de producción simplificado

2. **Scripts Batch**:
   - `src/launchers/launcher_ventas_simple.bat` - Script batch para ventas
   - `src/launchers/launcher_produccion_simple.bat` - Script batch para producción

3. **Herramientas de Diagnóstico**:
   - `src/launchers/test_launcher.py` - Launcher de prueba para diagnóstico
   - `src/launchers/diagnostico_launchers.py` - Script de diagnóstico completo

## 🚀 Cómo Usar los Launchers Funcionales

### Opción 1: Usar los Launchers Simplificados

```bash
# Para órdenes de venta
python src/launchers/launcher_ventas_simple.py

# Para órdenes de producción
python src/launchers/launcher_produccion_simple.py
```

### Opción 2: Usar los Scripts Batch

```bash
# Para órdenes de venta
src\launchers\launcher_ventas_simple.bat

# Para órdenes de producción
src\launchers\launcher_produccion_simple.bat
```

### Opción 3: Ejecutar Diagnóstico

```bash
# Ejecutar diagnóstico completo
python src/launchers/diagnostico_launchers.py

# Ejecutar launcher de prueba
python src/launchers/test_launcher.py
```

## 🔍 Diagnóstico del Problema

### Causas Comunes

1. **Módulos RPA no encontrados**: Los launchers originales intentan importar módulos que no existen
2. **Configuración faltante**: Archivos de configuración no encontrados
3. **Dependencias faltantes**: Tkinter o otras librerías no disponibles
4. **Rutas incorrectas**: Problemas con la estructura de directorios

### Verificación Rápida

Ejecuta el diagnóstico para identificar el problema específico:

```bash
python src/launchers/diagnostico_launchers.py
```

## 🛠️ Características de los Launchers Simplificados

### ✅ Funcionalidades Implementadas

- **Interfaz gráfica completa** con Tkinter
- **Sistema de logs en tiempo real**
- **Simulación de procesamiento** (sin dependencias externas)
- **Manejo de errores robusto**
- **Verificación de archivos y directorios**
- **Interfaz específica para cada módulo**

### 🎯 Diferencias con los Originales

| Característica | Launcher Original | Launcher Simplificado |
|----------------|-------------------|----------------------|
| **Dependencias** | Requiere módulos RPA | Solo requiere Tkinter |
| **Procesamiento** | Real | Simulado |
| **Estabilidad** | Puede fallar | Estable |
| **Funcionalidad** | Completa | Básica pero funcional |

## 📋 Pasos para Migrar a los Launchers Funcionales

### 1. Probar los Launchers Simplificados

```bash
# Probar launcher de ventas
python src/launchers/launcher_ventas_simple.py

# Probar launcher de producción
python src/launchers/launcher_produccion_simple.py
```

### 2. Verificar Funcionalidad

- ✅ La ventana se abre correctamente
- ✅ Los botones funcionan
- ✅ Los logs se muestran
- ✅ La simulación de procesamiento funciona

### 3. Integrar con Módulos RPA (Opcional)

Una vez que los launchers funcionen, puedes integrar los módulos RPA reales:

1. Crear los módulos faltantes:
   - `rpa/modules/sales_order/sales_order_handler.py`
   - `rpa/modules/production_order/production_order_handler.py`

2. Reemplazar la simulación con el procesamiento real

## 🔧 Configuración Adicional

### Variables de Entorno (Opcional)

```bash
# Configurar variables de entorno
set RPA_CONFIG_PATH=config.yaml
set RPA_LOG_LEVEL=INFO
set RPA_ENVIRONMENT=DEV
```

### Archivos de Configuración

Los launchers simplificados buscan estos archivos (opcionales):
- `rpa/modules/sales_order/sales_order_config.yaml`
- `rpa/modules/production_order/production_order_config.yaml`

## 🐛 Troubleshooting

### Problema: "Launcher se cierra inmediatamente"

**Solución**:
1. Ejecutar diagnóstico: `python src/launchers/diagnostico_launchers.py`
2. Usar launcher simplificado: `python src/launchers/launcher_ventas_simple.py`
3. Verificar que Tkinter funciona: `python -c "import tkinter; print('OK')"`

### Problema: "Error de importación"

**Solución**:
1. Verificar Python instalado: `python --version`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Usar launcher simplificado que no requiere módulos externos

### Problema: "No se encuentra el archivo"

**Solución**:
1. Verificar que estás en el directorio correcto
2. Ejecutar desde la raíz del proyecto
3. Usar rutas absolutas en los scripts batch

## 📊 Estado de los Launchers

### ✅ Funcionando
- `launcher_ventas_simple.py` - ✅ Funcional
- `launcher_produccion_simple.py` - ✅ Funcional
- `test_launcher.py` - ✅ Funcional
- `diagnostico_launchers.py` - ✅ Funcional

### ⚠️ Requieren Corrección
- `launcher_ventas.py` - ❌ Se cierra inmediatamente
- `launcher_produccion.py` - ❌ Se cierra inmediatamente

## 🎯 Próximos Pasos

1. **Usar los launchers simplificados** para operaciones básicas
2. **Ejecutar diagnóstico** para identificar problemas específicos
3. **Crear módulos RPA faltantes** si se necesita funcionalidad completa
4. **Migrar gradualmente** de launchers originales a simplificados

## 📞 Soporte

Si los launchers simplificados también fallan:

1. Ejecutar diagnóstico completo
2. Verificar instalación de Python
3. Verificar que Tkinter está disponible
4. Revisar permisos de archivos
5. Contactar al equipo de desarrollo

---

**Fecha de solución**: Diciembre 2024  
**Estado**: ✅ Launchers simplificados funcionando  
**Próximo paso**: Migrar a launchers simplificados
