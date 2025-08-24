# 📸 FASE 2: Captura de Imágenes de Referencia - Módulo de Producción

## 🎯 Objetivo
Capturar todas las imágenes de referencia necesarias para que el módulo de órdenes de producción funcione correctamente.

## 📋 Imágenes Requeridas

### 1. **Navegación Principal**
- `sap_produccion_menu.png` - Menú de módulos después de Alt+M
- `sap_orden_fabricacion_button.png` - Botón de orden de fabricación

### 2. **Formulario de Orden de Producción**
- `sap_produccion_form.png` - Formulario completo
- `sap_articulo_field.png` - Campo número de artículo
- `sap_pedido_interno_field.png` - Campo pedido interno
- `sap_cantidad_field.png` - Campo cantidad
- `sap_fecha_finalizacion_field.png` - Campo fecha de finalización

### 3. **Elementos de Control**
- `sap_produccion_crear_button.png` - Botón crear

## 🚀 Instrucciones de Captura

### Opción 1: Script Automatizado (Recomendado)
```bash
python capture_production_images.py
```

### Opción 2: Captura Manual
1. Abrir SAP Business One
2. Seguir el flujo de navegación
3. Capturar cada imagen según las especificaciones

## 📝 Especificaciones por Imagen

### 1. `sap_produccion_menu.png`
- **Cuándo capturar**: Después de presionar Alt+M
- **Qué debe mostrar**: Menú de módulos con "Producción" visible
- **Área de captura**: Toda la pantalla del menú

### 2. `sap_orden_fabricacion_button.png`
- **Cuándo capturar**: En el submenú de Producción
- **Qué debe mostrar**: Botón específico "Orden de Fabricación"
- **Área de captura**: Botón claramente visible

### 3. `sap_produccion_form.png`
- **Cuándo capturar**: Formulario de orden de producción abierto
- **Qué debe mostrar**: Formulario completo con todos los campos
- **Área de captura**: Toda la pantalla del formulario

### 4. `sap_articulo_field.png`
- **Cuándo capturar**: Campo de artículo activo
- **Qué debe mostrar**: Campo específico con etiqueta visible
- **Área de captura**: Campo y etiqueta cercana

### 5. `sap_pedido_interno_field.png`
- **Cuándo capturar**: Campo de pedido interno activo
- **Qué debe mostrar**: Campo específico con etiqueta visible
- **Área de captura**: Campo y etiqueta cercana

### 6. `sap_cantidad_field.png`
- **Cuándo capturar**: Campo de cantidad activo
- **Qué debe mostrar**: Campo específico con etiqueta visible
- **Área de captura**: Campo y etiqueta cercana

### 7. `sap_fecha_finalizacion_field.png`
- **Cuándo capturar**: Campo de fecha de finalización activo
- **Qué debe mostrar**: Campo específico con etiqueta visible
- **Área de captura**: Campo y etiqueta cercana

### 8. `sap_produccion_crear_button.png`
- **Cuándo capturar**: Botón crear visible
- **Qué debe mostrar**: Botón "Crear" para finalizar la orden
- **Área de captura**: Botón claramente visible

## ✅ Checklist de Verificación

- [ ] Todas las imágenes están en `rpa/vision/reference_images/production/`
- [ ] Las imágenes son claras y nítidas
- [ ] Los elementos clave son visibles en cada imagen
- [ ] Las imágenes tienen el tamaño adecuado
- [ ] Los nombres de archivo son correctos

## 🔧 Solución de Problemas

### Imagen muy grande/pequeña
- Ajustar el zoom de la pantalla antes de capturar
- Usar captura de área específica si es necesario

### Elemento no visible
- Verificar que el elemento esté en la pantalla
- Ajustar la resolución si es necesario
- Usar diferentes ángulos de captura

### Calidad de imagen pobre
- Verificar la resolución de pantalla
- Asegurar que no haya elementos superpuestos
- Capturar en condiciones de iluminación adecuadas

## 📊 Progreso de la Fase

- [x] Script de captura creado
- [x] Documentación completada
- [x] Imágenes capturadas
- [x] Verificación de calidad
- [x] Fase completada

## 🎯 Siguiente Fase

Una vez completada la captura de imágenes, procederemos a la **Fase 3: Implementación del Handler**.
