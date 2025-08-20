# Guía para Configurar la Detección de la Interfaz Principal de SAP

## 📋 Resumen

Esta guía te ayudará a configurar el sistema RPA para que detecte automáticamente cuando está en la interfaz principal de SAP, basándose en la imagen que has proporcionado.

## 🎯 Objetivo

El sistema debe reconocer cuando está en la pantalla principal de SAP que muestra:
- Barra de menú superior con: "Archivo", "Editar", "Visualizar", "Datos", "Pasar a", "Módulos", "Herramientas"
- Barra de herramientas con iconos de Excel, Word, PDF, etc.
- Icono de menú hamburguesa en la esquina inferior izquierda

## 📁 Ubicación de la Imagen

La imagen de referencia debe guardarse en:
```
./rpa/vision/reference_images/sap_main_interface.png
```

## 🚀 Pasos para Configurar

### Paso 1: Capturar la Imagen de Referencia

**Opción A: Usar el script automático (Recomendado)**
```bash
python capture_sap_main_interface.py
```

**Opción B: Captura manual**
1. Abre SAP y navega a la pantalla principal
2. Toma un screenshot de la pantalla completa
3. Guarda la imagen como `sap_main_interface.png` en la carpeta `./rpa/vision/reference_images/`

### Paso 2: Verificar la Detección

Ejecuta el script de prueba:
```bash
python test_sap_main_interface_detection.py
```

### Paso 3: Ajustar Configuración (si es necesario)

Si la detección no funciona correctamente, puedes ajustar el umbral de confianza en:
```python
# En rpa/screen_detector.py, línea ~40
self.confidence_thresholds = {
    ScreenState.REMOTE_DESKTOP: 0.85,
    ScreenState.SAP_DESKTOP: 0.80,  # Ajustar este valor si es necesario
    ScreenState.SALES_ORDER_FORM: 0.85,
}
```

## 🔧 Cómo Funciona

### Detección Actualizada

El sistema ahora busca múltiples elementos para detectar SAP:

1. **Icono de SAP** (`sap_icon.png`)
2. **Botón de módulos** (`sap_modulos_menu_button.png`)
3. **Interfaz principal** (`sap_main_interface.png`) - **NUEVO**
4. **Layout de SAP Desktop** (`sap_desktop.png`)

### Algoritmo de Detección

```python
def _detect_sap_desktop(self, screenshot):
    matches = []
    
    # Buscar icono de SAP
    if self.sap_icon_image is not None:
        result = cv2.matchTemplate(screenshot, self.sap_icon_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        matches.append(max_val)
    
    # Buscar botón de módulos
    if self.sap_modulos_menu_button is not None:
        result = cv2.matchTemplate(screenshot, self.sap_modulos_menu_button, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        matches.append(max_val)
    
    # Buscar interfaz principal de SAP (NUEVO)
    if self.sap_main_interface_image is not None:
        result = cv2.matchTemplate(screenshot, self.sap_main_interface_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        matches.append(max_val)
    
    # Calcular confianza promedio
    return sum(matches) / len(matches) if matches else 0.0
```

## 📊 Umbrales de Confianza

- **SAP Desktop**: 0.80 (80%)
- **Remote Desktop**: 0.85 (85%)
- **Sales Order Form**: 0.85 (85%)

## 🐛 Solución de Problemas

### Problema: No detecta SAP
**Solución:**
1. Verifica que la imagen esté guardada correctamente
2. Asegúrate de que SAP esté visible en pantalla
3. Reduce el umbral de confianza temporalmente para debug

### Problema: Detecta SAP incorrectamente
**Solución:**
1. Aumenta el umbral de confianza
2. Captura una nueva imagen de referencia más específica
3. Verifica que no haya elementos similares en otras pantallas

### Problema: Detección lenta
**Solución:**
1. Usa imágenes de referencia más pequeñas
2. Especifica regiones de búsqueda más pequeñas
3. Optimiza la resolución de las imágenes

## 📝 Logs y Debug

El sistema guarda logs detallados en:
- **Logs generales**: `./logs/`
- **Screenshots de debug**: `./debug_screenshots/`

Para ver logs específicos de detección:
```python
import logging
logging.getLogger('rpa.screen_detector').setLevel(logging.DEBUG)
```

## ✅ Verificación Final

Para verificar que todo funciona correctamente:

1. **Ejecuta la prueba completa:**
   ```bash
   python test_sap_main_interface_detection.py
   ```

2. **Verifica los resultados:**
   - Estado detectado: `sap_desktop`
   - Confianza: > 0.80
   - Screenshot guardado correctamente

3. **Prueba en diferentes condiciones:**
   - Con diferentes resoluciones
   - Con diferentes temas de SAP
   - Con diferentes ventanas abiertas

## 🔄 Mantenimiento

### Actualizar la Imagen de Referencia

Si la interfaz de SAP cambia:
1. Ejecuta `python capture_sap_main_interface.py`
2. Prueba con `python test_sap_main_interface_detection.py`
3. Ajusta umbrales si es necesario

### Backup de Imágenes

Mantén un backup de las imágenes de referencia en:
```
./rpa/vision/reference_images/backup/
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en `./logs/`
2. Verifica los screenshots en `./debug_screenshots/`
3. Ejecuta las pruebas de diagnóstico
4. Consulta la documentación técnica

---

**Nota**: Esta configuración mejora significativamente la precisión de detección de SAP al incluir múltiples elementos de referencia, haciendo el sistema más robusto ante cambios menores en la interfaz.
