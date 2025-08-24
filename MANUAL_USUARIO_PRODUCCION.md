# 📖 MANUAL DE USUARIO - MÓDULO DE ÓRDENES DE PRODUCCIÓN

## 🎯 **INTRODUCCIÓN**

Este manual te guiará paso a paso para usar el módulo de automatización de órdenes de producción en SAP Business One.

### **¿Qué hace este módulo?**

- 🤖 **Automatiza** la creación de órdenes de producción
- 📝 **Llena automáticamente** todos los campos requeridos
- 📸 **Documenta** el proceso con screenshots
- ⏸️ **Pausa** para tu decisión final (crear o borrar)

---

## 🚀 **INICIO RÁPIDO**

### **Paso 1: Preparación**

1. **Asegúrate de tener:**
   - ✅ SAP Business One abierto
   - ✅ Escritorio remoto disponible
   - ✅ Imágenes de referencia capturadas

2. **Ejecuta el script:**
   ```bash
   python test_produccion_real.py
   ```

3. **Sigue las instrucciones en pantalla**

### **Paso 2: Confirmación**

- El script te pedirá confirmación para empezar
- Presiona **ENTER** cuando estés listo
- El proceso será completamente automático

### **Paso 3: Resultado**

- El formulario se llenará automáticamente
- Se tomará un screenshot
- Tú decides: **Crear** o **Borrar**

---

## 📋 **REQUISITOS PREVIOS**

### **Software Requerido**

- ✅ **Python 3.8+**
- ✅ **SAP Business One**
- ✅ **Escritorio Remoto** (si aplica)
- ✅ **Dependencias Python** (instaladas automáticamente)

### **Configuración SAP**

- ✅ **SAP abierto** en pantalla principal
- ✅ **Usuario con permisos** para órdenes de producción
- ✅ **Módulo de producción** habilitado

### **Imágenes de Referencia**

- ✅ **Capturadas** usando `capture_production_images.py`
- ✅ **Ubicadas** en `rpa/vision/reference_images/production/`
- ✅ **Actualizadas** si cambia la interfaz de SAP

---

## 🔧 **CONFIGURACIÓN INICIAL**

### **1. Instalar Dependencias**

```bash
# Ejecutar en la terminal
pip install pyautogui opencv-python numpy PyYAML Pillow
```

### **2. Capturar Imágenes de Referencia**

```bash
# Ejecutar el script de captura
python capture_production_images.py

# Seguir las instrucciones para capturar:
# - Botón "Orden de Fabricación"
# - Formulario de producción
# - Campo artículo
# - Campo cantidad
# - Campo pedido interno
# - Campo fecha de finalización
# - Botón crear
```

### **3. Verificar Configuración**

```bash
# Ejecutar prueba rápida
python test_rapido_produccion.py
```

---

## 📊 **FORMATO DE DATOS**

### **Estructura JSON Requerida**

```json
{
  "numero_articulo": "101846",
  "numero_pedido_interno": "6107",
  "cantidad": 2000,
  "fecha_finalizacion": "12/09/2025",
  "unidad_medida": "PCS",
  "centro_trabajo": "CT-01",
  "observaciones": "Orden de producción automatizada"
}
```

### **Campos Obligatorios**

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `numero_articulo` | String | "101846" | Código del artículo |
| `numero_pedido_interno` | String | "6107" | Número de pedido |
| `cantidad` | Integer | 2000 | Cantidad a producir |
| `fecha_finalizacion` | String | "12/09/2025" | Fecha DD/MM/YYYY |

### **Campos Opcionales**

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `unidad_medida` | String | "PCS" | Unidad de medida |
| `centro_trabajo` | String | "CT-01" | Centro de trabajo |
| `observaciones` | String | "Texto" | Observaciones |

---

## 🎮 **SCRIPTS DISPONIBLES**

### **1. Script Principal: `test_produccion_real.py`**

**Propósito:** Prueba completa con datos reales
**Uso:** Para uso diario y pruebas finales

```bash
python test_produccion_real.py
```

**Características:**
- ✅ Datos reales predefinidos
- ✅ Navegación completa automática
- ✅ Screenshot automático
- ✅ Pausa para decisión manual

### **2. Script de Verificación: `test_rapido_produccion.py`**

**Propósito:** Verificar configuración sin SAP
**Uso:** Para verificar que todo esté configurado

```bash
python test_rapido_produccion.py
```

**Características:**
- ✅ No requiere SAP abierto
- ✅ Verifica imágenes de referencia
- ✅ Valida configuración
- ✅ Prueba rápida

### **3. Script de Prueba: `test_produccion_ficticia.py`**

**Propósito:** Prueba con datos ficticios
**Uso:** Para pruebas y desarrollo

```bash
python test_produccion_ficticia.py
```

**Características:**
- ✅ Datos ficticios seguros
- ✅ Navegación completa
- ✅ Ideal para pruebas

---

## 🔄 **FLUJO DE TRABAJO**

### **Proceso Automatizado**

1. **🔄 Cambio de Ventana**
   - Alt+Tab automático al escritorio remoto
   - Verificación de ventana activa

2. **📂 Navegación SAP**
   - Alt+M (abrir módulos)
   - P (ir a producción)
   - Clic en "Orden de Fabricación"

3. **📝 Llenado Automático**
   - **Artículo**: Busca campo + clic + escribe
   - **Cantidad**: TAB+TAB + escribe
   - **Fecha**: 7 TABs + escribe
   - **Pedido**: TAB+TAB + escribe

4. **📸 Documentación**
   - Screenshot automático
   - Guardado con timestamp

5. **⏸️ Decisión Manual**
   - Formulario listo
   - Tú decides: Crear o Borrar

### **Tiempo Estimado**

- **Total**: 30-45 segundos
- **Navegación**: 10-15 segundos
- **Llenado**: 15-20 segundos
- **Documentación**: 5 segundos

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### **Problema: "Campo artículo no encontrado"**

**Síntomas:**
- Error en logs: "Campo artículo no encontrado"
- Script continúa con fallback por TAB

**Soluciones:**
1. **Actualizar imagen de referencia:**
   ```bash
   python capture_production_images.py
   ```

2. **Ajustar confianza en config.yaml:**
   ```yaml
   template_matching:
     field_confidence: 0.7  # Reducir de 0.8 a 0.7
   ```

3. **Verificar que SAP esté en el estado correcto**

### **Problema: "Botón no encontrado"**

**Síntomas:**
- Error: "Botón de orden de fabricación no encontrado"
- Script se detiene

**Soluciones:**
1. **Verificar navegación:**
   - SAP debe estar en pantalla principal
   - Alt+M debe funcionar

2. **Actualizar imagen del botón:**
   ```bash
   python capture_production_images.py
   ```

3. **Verificar permisos de usuario**

### **Problema: "Datos no válidos"**

**Síntomas:**
- Error: "Campo requerido faltante"
- Script se detiene antes de empezar

**Soluciones:**
1. **Verificar formato de fecha:**
   - Usar DD/MM/YYYY
   - Ejemplo: "12/09/2025"

2. **Verificar cantidad:**
   - Debe ser número entero
   - Mayor que 0

3. **Verificar campos obligatorios:**
   - numero_articulo
   - numero_pedido_interno
   - cantidad
   - fecha_finalizacion

---

## 📈 **MONITOREO Y LOGS**

### **Ubicación de Logs**

```bash
# Logs principales
./logs/rpa_production.log

# Screenshots
./screenshots/produccion_antes_crear_YYYYMMDD_HHMMSS.png
```

### **Información en Logs**

```python
# Ejemplo de logs
2025-08-24 10:08:40 - INFO - 🚀 Iniciando procesamiento
2025-08-24 10:08:40 - INFO - ✅ Validación completada
2025-08-24 10:08:40 - INFO - 🔄 Cargando artículo: 101846
2025-08-24 10:08:40 - INFO - ✅ Campo encontrado (confianza: 1.000)
```

### **Interpretación de Logs**

- **INFO**: Operación exitosa
- **WARNING**: Problema menor, script continúa
- **ERROR**: Problema crítico, script se detiene

---

## ⚙️ **CONFIGURACIÓN AVANZADA**

### **Archivo de Configuración**

```yaml
# production_order_config.yaml
production_order:
  navigation:
    alt_m_delay: 0.5          # Delay después de Alt+M
    p_key_delay: 1.0          # Delay después de P
    mouse_click_delay: 2.0    # Delay después de clic
    
  template_matching:
    orden_fabricacion_button_confidence: 0.8
    field_confidence: 0.8
    crear_button_confidence: 0.85
```

### **Ajustes de Performance**

**Para sistemas lentos:**
```yaml
navigation:
  alt_m_delay: 1.0      # Aumentar de 0.5 a 1.0
  p_key_delay: 2.0      # Aumentar de 1.0 a 2.0
  mouse_click_delay: 3.0 # Aumentar de 2.0 a 3.0
```

**Para sistemas rápidos:**
```yaml
navigation:
  alt_m_delay: 0.3      # Reducir de 0.5 a 0.3
  p_key_delay: 0.5      # Reducir de 1.0 a 0.5
  mouse_click_delay: 1.0 # Reducir de 2.0 a 1.0
```

---

## 🔒 **SEGURIDAD Y BUENAS PRÁCTICAS**

### **Seguridad**

- ✅ **No compartir** imágenes de referencia
- ✅ **Usar datos de prueba** para desarrollo
- ✅ **Verificar permisos** de usuario SAP
- ✅ **Hacer backup** de configuraciones

### **Buenas Prácticas**

- ✅ **Probar primero** con datos ficticios
- ✅ **Revisar logs** después de cada ejecución
- ✅ **Actualizar imágenes** si cambia SAP
- ✅ **Documentar cambios** en configuración

### **Mantenimiento**

- ✅ **Revisar logs** semanalmente
- ✅ **Actualizar imágenes** mensualmente
- ✅ **Verificar configuración** trimestralmente
- ✅ **Hacer backup** de todo el módulo

---

## 📞 **SOPORTE**

### **Antes de Contactar Soporte**

1. ✅ **Revisar este manual**
2. ✅ **Verificar logs** de error
3. ✅ **Probar con datos simples**
4. ✅ **Verificar configuración**

### **Información para Soporte**

Cuando contactes soporte, incluye:

- **Error específico** del log
- **Datos utilizados** (sin información sensible)
- **Configuración actual** (archivo YAML)
- **Versión de SAP** y Python
- **Screenshot** del error (si aplica)

### **Recursos Adicionales**

- 📚 **Documentación técnica**: `FASE_5_DOCUMENTACION_PRODUCCION.md`
- 🔧 **Guía de configuración**: `GUIA_CONFIGURACION.md`
- 🛠️ **Troubleshooting**: `TROUBLESHOOTING.md`

---

## ✅ **CONCLUSIÓN**

Este módulo está diseñado para ser **fácil de usar** y **confiable**. Con la configuración correcta y siguiendo este manual, podrás automatizar la creación de órdenes de producción de manera eficiente y segura.

**¡El módulo está listo para uso en producción!** 🚀

---

*Manual de usuario - Versión 1.0.0*
*Fecha: 24 de Agosto, 2025*
*Estado: LISTO PARA PRODUCCIÓN*
