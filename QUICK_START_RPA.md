# GUÍA DE INICIO RÁPIDO - SISTEMA RPA

## **🚀 INICIO RÁPIDO**

### **1. Verificar Estado del Sistema**
```bash
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Verificar archivos JSON disponibles
ls ./data/outputs_json/*.json

# Verificar logs recientes
tail -n 50 ./logs/rpa.log
```

### **2. Ejecutar Sistema RPA**
```bash
python main.py
```

### **3. Monitorear Ejecución**
- **Logs en tiempo real**: `./logs/rpa.log`
- **Archivos procesados**: `./data/outputs_json/Procesados/`
- **Screenshots**: `./rpa/vision/reference_images/inserted_orders/`

## **🔧 CONFIGURACIÓN RÁPIDA**

### **Requisitos Previos:**
- ✅ Python 3.8+ instalado
- ✅ Tesseract OCR instalado en `C:\Program Files\Tesseract-OCR\`
- ✅ Conexión RDP activa a `20.96.6.64`
- ✅ SAP Business One disponible en escritorio remoto

### **Instalación de Dependencias:**
```bash
pip install -r requirements.txt
```

## **📋 CHECKLIST DE VERIFICACIÓN**

### **Antes de Ejecutar:**
- [ ] Conexión RDP estable y activa
- [ ] SAP Business One cerrado (el RPA lo abrirá)
- [ ] Archivos JSON en `./data/outputs_json/`
- [ ] Entorno virtual activado
- [ ] No interferir durante la ejecución

### **Durante la Ejecución:**
- [ ] Sistema ejecutándose sin errores
- [ ] Logs mostrando progreso normal
- [ ] Archivos moviéndose a carpeta Procesados
- [ ] SAP abriéndose y navegando correctamente

### **Después de la Ejecución:**
- [ ] Archivos JSON movidos a Procesados
- [ ] Logs sin errores críticos
- [ ] Sistema esperando próxima ejecución (10 min)

## **🚨 PROBLEMAS COMUNES Y SOLUCIONES RÁPIDAS**

### **Error: "Ventana de escritorio remoto no encontrada"**
```bash
# Solución: Verificar conexión RDP
# 1. Reconectar a escritorio remoto
# 2. Verificar que la ventana esté activa
# 3. Reiniciar el sistema RPA
```

### **Error: "Icono de SAP Business One no encontrado"**
```bash
# Solución: Actualizar imagen de referencia
# 1. Tomar nueva captura del icono de SAP
# 2. Reemplazar ./rpa/vision/reference_images/sap_icon.png
# 3. Reiniciar el sistema
```

### **Error: "No hay archivos JSON disponibles"**
```bash
# Solución: Verificar archivos de entrada
# 1. Colocar archivos JSON en ./data/outputs_json/
# 2. Verificar formato correcto del JSON
# 3. Esperar próxima ejecución automática
```

### **Error: "Error al procesar item X"**
```bash
# Solución: Ajustar timing
# 1. Revisar logs para identificar el problema específico
# 2. Aumentar tiempos de espera si es necesario
# 3. Verificar navegación en SAP
```

## **📊 MONITOREO RÁPIDO**

### **Comandos Útiles:**
```bash
# Ver logs en tiempo real
Get-Content ./logs/rpa.log -Wait

# Ver archivos procesados
ls ./data/outputs_json/Procesados/

# Ver archivos pendientes
ls ./data/outputs_json/*.json

# Verificar estado del proceso
Get-Process python
```

### **Métricas de Rendimiento:**
- **Tiempo por artículo**: ~18 segundos
- **Tiempo por archivo**: ~90 segundos
- **Archivos por hora**: ~40 archivos
- **Uptime esperado**: 24/7

## **🔍 DIAGNÓSTICO RÁPIDO**

### **Síntomas y Soluciones:**

#### **Síntoma: Sistema no inicia**
- **Causa**: Entorno virtual no activado
- **Solución**: `.\venv\Scripts\Activate.ps1`

#### **Síntoma: Error de dependencias**
- **Causa**: Librerías no instaladas
- **Solución**: `pip install -r requirements.txt`

#### **Síntoma: SAP no se abre**
- **Causa**: Imagen de referencia desactualizada
- **Solución**: Actualizar `sap_icon.png`

#### **Síntoma: Navegación fallida**
- **Causa**: Interfaz de SAP cambió
- **Solución**: Actualizar imágenes de referencia

#### **Síntoma: Archivos no se procesan**
- **Causa**: Formato JSON incorrecto
- **Solución**: Verificar estructura del JSON

## **📝 NOTAS IMPORTANTES**

### **Para Futuros Agentes:**

1. **NO MODIFICAR** el código sin consultar la documentación completa
2. **SIEMPRE PROBAR** cambios en ambiente de desarrollo
3. **MANTENER LOGS** detallados de cualquier modificación
4. **DOCUMENTAR** cualquier cambio en la interfaz de SAP

### **Archivos Críticos (NO TOCAR):**
- `rpa/main.py` - Lógica principal del RPA
- `rpa/vision/main.py` - Sistema de visión
- `rpa/logger.py` - Sistema de logging
- `requirements.txt` - Dependencias del sistema

### **Archivos de Configuración:**
- `main.py` - Configuración de ejecución
- `rpa/vision/reference_images/` - Imágenes de referencia
- `./data/outputs_json/` - Archivos de entrada

## **📞 CONTACTO DE EMERGENCIA**

### **En Caso de Problemas Críticos:**
1. **Revisar logs** en `./logs/rpa.log`
2. **Consultar documentación** en `README_RPA.md`
3. **Verificar conectividad** RDP
4. **Reiniciar sistema** si es necesario

### **Información del Sistema:**
- **Versión**: RPA v1.0
- **Última actualización**: Agosto 2025
- **Responsable**: Equipo de Automatización

---

**⚠️ IMPORTANTE**: Esta guía es para uso rápido. Para modificaciones o problemas complejos, consultar la documentación completa en `README_RPA.md`. 