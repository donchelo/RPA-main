# 🤖 Guía de Usuario - Launcher RPA TAMAPRINT

## 📖 ¿Qué es este sistema?

El **Sistema RPA TAMAPRINT** automatiza la inserción de órdenes de venta en SAP Business One. Solo necesita colocar archivos JSON con los datos de las órdenes y el sistema se encarga del resto.

## 🚀 Inicio Rápido (Para Usuarios No Técnicos)

### Opción 1: Usar la Aplicación Gráfica (RECOMENDADO)

1. **Hacer doble clic en: `rpa_launcher.bat`**
2. Se abrirá una ventana con interfaz gráfica
3. Hacer clic en el botón verde **"🚀 INICIAR RPA"**
4. El sistema comenzará a procesar automáticamente

### Opción 2: Solo la Ventana Gráfica

1. **Hacer doble clic en: `rpa_launcher.py`**
   - (Si no funciona, usar la Opción 1)

## 🔧 Primera Vez - Instalación de Dependencias

**Solo la primera vez:**

1. **Hacer doble clic en: `install_requirements.bat`**
2. Escribir `s` y presionar Enter para confirmar
3. Esperar que termine la instalación
4. Una vez completado, ya puede usar el sistema

## 📱 Cómo Usar la Interfaz Gráfica

### Pantalla Principal

```
┌─────────────────────────────────────┐
│  🤖 Sistema RPA TAMAPRINT           │
│                                     │
│  [Control del Sistema]    [Logs]    │
│  Estado: Detenido         [Logs...] │
│  [🚀 INICIAR RPA]         [Logs...] │
│                          [Logs...] │
│  Archivos JSON:          [Logs...] │
│  Pendientes: 5                     │
│  Procesados hoy: 3                 │
│                                    │
│  Requisitos:                       │
│  Python: ✅                       │
│  Dependencias: ✅                  │
│  Tesseract: ✅                     │
└─────────────────────────────────────┘
```

### Botones Principales

- **🚀 INICIAR RPA**: Comienza el procesamiento automático
- **⏹️ DETENER RPA**: Detiene el sistema (solo aparece cuando está ejecutándose)
- **🔄 Actualizar**: Actualiza el conteo de archivos JSON
- **📦 Instalar Dependencias**: Instala componentes necesarios
- **🗑️ Limpiar Logs**: Borra los mensajes mostrados
- **📁 Abrir Carpeta Logs**: Abre la carpeta con logs detallados

### Estados del Sistema

- **🔴 Estado: Detenido** - El sistema no está procesando
- **🟢 Estado: Ejecutándose** - El sistema está trabajando automáticamente

## 📄 Preparar Archivos JSON

### Dónde Colocar los Archivos

Los archivos JSON deben colocarse en:
```
RPA-main/data/outputs_json/
```

### Formato del Archivo JSON

```json
{
  "comprador": {
    "nit": "900123456"
  },
  "orden_compra": "OC-2024-001",
  "fecha_entrega": "31/12/2024",
  "items": [
    {
      "codigo": "PROD001",
      "cantidad": "10"
    },
    {
      "codigo": "PROD002",
      "cantidad": "5"
    }
  ]
}
```

### Archivos Procesados

Una vez procesados exitosamente, los archivos se mueven automáticamente a:
```
RPA-main/data/outputs_json/Procesados/
```

## ⚠️ Requisitos Previos

### Lo que debe estar listo ANTES de usar el sistema:

1. **✅ Conexión de Escritorio Remoto activa** a la dirección `20.96.6.64`
2. **✅ SAP Business One** debe estar disponible en el escritorio remoto
3. **✅ Python** instalado en el computador
4. **✅ Tesseract OCR** instalado (se detecta automáticamente)

### Verificar Requisitos

La aplicación verifica automáticamente estos requisitos y muestra:
- ✅ **Verde**: Requisito cumplido
- ❌ **Rojo**: Requisito faltante
- ⏳ **Amarillo**: Verificando...

## 🕒 Funcionamiento Automático

Una vez iniciado, el sistema:

1. **Busca archivos JSON** cada 10 minutos
2. **Se conecta al escritorio remoto** automáticamente
3. **Abre SAP Business One** si es necesario
4. **Procesa cada orden** paso a paso
5. **Mueve archivos completados** a la carpeta "Procesados"
6. **Repite el proceso** continuamente

## 📊 Monitoreo y Logs

### En la Interfaz Gráfica

- **Logs en tiempo real**: Se muestran en el panel derecho
- **Contadores**: Archivos pendientes y procesados
- **Estado**: Visual del sistema (Detenido/Ejecutándose)

### Logs Detallados

Los logs completos se guardan en la carpeta `logs/`:
- `rpa.log`: Log principal del sistema
- `rpa_errors.log`: Solo errores
- `rpa_performance.log`: Métricas de rendimiento

## 🆘 Solución de Problemas Comunes

### "No se encontró main.py"
- **Solución**: Asegúrese de ejecutar los archivos .bat desde la carpeta RPA-main

### "Python no está instalado"
- **Solución**: Instale Python desde https://python.org y marque "Add Python to PATH"

### "Dependencias faltantes"
- **Solución**: Ejecute `install_requirements.bat` o use el botón "📦 Instalar Dependencias"

### "Tesseract no encontrado"
- **Solución**: Descargue e instale desde https://github.com/UB-Mannheim/tesseract/wiki

### "Ventana de escritorio remoto no encontrada"
- **Solución**: 
  1. Reconecte al escritorio remoto (20.96.6.64)
  2. Asegúrese de que la ventana esté visible
  3. Reinicie el sistema RPA

### "Error al procesar archivo JSON"
- **Solución**:
  1. Verifique el formato del archivo JSON
  2. Asegúrese de que SAP esté disponible
  3. Revise los logs detallados

## 📞 ¿Necesita Ayuda?

### Información de Soporte
- **Logs detallados**: Carpeta `logs/` (hacer clic en "📁 Abrir Carpeta Logs")
- **Estado del sistema**: Visible en la interfaz principal
- **Archivos de configuración**: `config.yaml` (para usuarios técnicos)

### Antes de Contactar Soporte

1. **Revisar los logs** en la interfaz gráfica
2. **Verificar requisitos** (todos deben estar en ✅)
3. **Probar reiniciar** el sistema RPA
4. **Tomar captura de pantalla** del error

---

## 🎯 Resumen para Usuarios No Técnicos

### Para usar el sistema:
1. **Doble clic** en `rpa_launcher.bat`
2. **Clic** en "🚀 INICIAR RPA"
3. **Colocar archivos JSON** en `data/outputs_json/`
4. **El sistema trabaja solo** ✨

### Si hay problemas:
1. **Ejecutar** `install_requirements.bat` (primera vez)
2. **Verificar** que los requisitos estén en ✅
3. **Revisar logs** para más información
4. **Contactar soporte técnico** con capturas de pantalla

**¡El sistema está diseñado para ser simple y automático!** 🤖✨