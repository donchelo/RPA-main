# 🎯 GUÍA COMPLETA DE IMÁGENES DE REFERENCIA - SISTEMA DE VISIÓN

## 📋 **Resumen Ejecutivo**

El sistema RPA utiliza **25 imágenes de referencia** para navegar y operar dentro del módulo de pedidos de SAP Business One. Estas imágenes permiten al RPA:

1. **Ubicarse** en la pantalla correcta
2. **Encontrar** botones y elementos específicos
3. **Tomar decisiones** sobre el estado del proceso
4. **Validar** que las acciones se ejecutaron correctamente

---

## 🗂️ **CATEGORÍAS DE IMÁGENES**

### 1. **🖥️ NAVEGACIÓN PRINCIPAL** (5 imágenes)

#### **sap_icon.png** (4.8KB)
- **Propósito**: Encontrar el icono de SAP Business One en el escritorio
- **Uso**: `get_sap_icon_coordinates()`
- **Confianza**: 0.7
- **Decisión**: ¿Está SAP disponible para abrir?

#### **sap_desktop.png** (382KB)
- **Propósito**: Pantalla principal de SAP Business One
- **Uso**: Base para encontrar elementos del menú principal
- **Decisión**: ¿SAP está abierto correctamente?

#### **sap_main_interface.png** (436KB)
- **Propósito**: Interfaz principal de SAP
- **Uso**: Validación del estado general de SAP
- **Decisión**: ¿Estamos en la pantalla correcta?

#### **remote_desktop.png** (243KB)
- **Propósito**: Pantalla de escritorio remoto
- **Uso**: `get_remote_desktop()`
- **Decisión**: ¿Estamos conectados al escritorio remoto?

#### **template.png** (102KB)
- **Propósito**: Template general de referencia
- **Uso**: Base para múltiples búsquedas
- **Decisión**: ¿La pantalla tiene el formato esperado?

### 2. **📋 MENÚS Y NAVEGACIÓN** (8 imágenes)

#### **sap_modulos_menu_button.png** (864B)
- **Propósito**: Botón "Módulos" en el menú principal
- **Uso**: `get_modulos_menu_coordinates()`
- **Decisión**: ¿Dónde hacer clic para abrir módulos?

#### **sap_modulos_menu.png** (23KB)
- **Propósito**: Menú desplegado de módulos
- **Uso**: Base para encontrar submenús
- **Decisión**: ¿El menú de módulos está abierto?

#### **sap_ventas_menu_button.png** (1.1KB)
- **Propósito**: Botón "Ventas" en el menú de módulos
- **Uso**: `get_ventas_menu_coordinates()`
- **Decisión**: ¿Dónde hacer clic para abrir ventas?

#### **sap_ventas_order_menu.png** (17KB)
- **Propósito**: Menú desplegado de ventas
- **Uso**: Base para encontrar órdenes de venta
- **Decisión**: ¿El menú de ventas está abierto?

#### **sap_ventas_order_button.png** (1.0KB)
- **Propósito**: Botón "Órdenes de venta"
- **Uso**: `get_ventas_order_coordinates()`
- **Decisión**: ¿Dónde hacer clic para abrir órdenes?

#### **sap_archivo_menu_button.png** (726B)
- **Propósito**: Botón "Archivo" en el menú principal
- **Uso**: `get_archivos_menu_coordinates()`
- **Decisión**: ¿Dónde hacer clic para cerrar SAP?

#### **sap_archivo_menu.png** (14KB)
- **Propósito**: Menú desplegado de archivo
- **Uso**: Base para encontrar opciones de cierre
- **Decisión**: ¿El menú de archivo está abierto?

#### **sap_finalizar_button.png** (642B)
- **Propósito**: Botón "Finalizar" en el menú archivo
- **Uso**: `get_finalizar_button_coordinates()`
- **Decisión**: ¿Dónde hacer clic para cerrar SAP?

### 3. **📝 FORMULARIO DE PEDIDO** (7 imágenes)

#### **sap_orden_de_ventas_template.png** (102KB)
- **Propósito**: Template completo del formulario de orden de ventas
- **Uso**: Base para encontrar campos específicos
- **Decisión**: ¿Estamos en el formulario correcto?

#### **client_field.png** (574B)
- **Propósito**: Campo de cliente/NIT
- **Uso**: `get_client_coordinates()`
- **Decisión**: ¿Dónde ingresar el NIT del cliente?

#### **orden_compra.png** (631B)
- **Propósito**: Campo de orden de compra
- **Uso**: `get_orden_coordinates()`
- **Decisión**: ¿Dónde ingresar la orden de compra?

#### **fecha_entrega.png** (600B)
- **Propósito**: Campo de fecha de entrega
- **Uso**: `get_fecha_coordinates()`
- **Decisión**: ¿Dónde ingresar la fecha de entrega?

#### **primer_articulo.png** (640B)
- **Propósito**: Primera fila de artículos
- **Uso**: `get_primer_articulo_coordinates()`
- **Decisión**: ¿Dónde ingresar el primer artículo?

#### **agregar_docum_button.png** (842B)
- **Propósito**: Botón "Agregar documento"
- **Uso**: Agregar nuevos artículos al pedido
- **Decisión**: ¿Dónde hacer clic para agregar más artículos?

#### **sap_agregar_docum_button.png** (846B)
- **Propósito**: Botón alternativo "Agregar documento"
- **Uso**: Versión alternativa del botón agregar
- **Decisión**: ¿Cuál botón usar para agregar artículos?

### 4. **🔘 BOTONES DE ACCIÓN** (3 imágenes)

#### **agregar_y_button.png** (518B)
- **Propósito**: Botón principal "Agregar y"
- **Uso**: `position_mouse_on_agregar_button()`
- **Confianza**: 0.85 (primaria), 0.75 (fallback)
- **Decisión**: ¿Dónde hacer clic para finalizar el pedido?

#### **sap_popup_agregar_y.png** (2.5KB)
- **Propósito**: Botón "Agregar y" en la minipantalla
- **Uso**: Cerrar la minipantalla de confirmación
- **Decisión**: ¿Dónde hacer clic en la minipantalla?

#### **sap_popup_agregar_y_cerrar.png** (707B)
- **Propósito**: Botón "Agregar y cerrar" en la minipantalla
- **Uso**: `position_mouse_on_agregar_button()`
- **Confianza**: 0.8
- **Decisión**: ¿Dónde hacer clic para cerrar la minipantalla?

### 5. **📊 VALIDACIÓN Y CONTROL** (2 imágenes)

#### **sap_totales_section.png** (2.4KB)
- **Propósito**: Sección de totales del pedido
- **Uso**: `get_totales_section_coordinates()`
- **Confianza**: 0.5 (flexible para escritorio remoto)
- **Decisión**: ¿Dónde está la sección de totales?

#### **scroll_to_bottom.png** (360B)
- **Propósito**: Indicador de scroll hacia abajo
- **Uso**: `scroll_to_bottom()`
- **Decisión**: ¿Necesito hacer scroll para ver más contenido?

---

## 🎯 **FLUJO DE DECISIONES POR IMAGEN**

### **FASE 1: APERTURA DE SAP**
```
1. remote_desktop.png → ¿Estamos en escritorio remoto?
2. sap_icon.png → ¿Dónde está el icono de SAP?
3. sap_desktop.png → ¿SAP se abrió correctamente?
```

### **FASE 2: NAVEGACIÓN A PEDIDOS**
```
4. sap_modulos_menu_button.png → ¿Dónde hacer clic en módulos?
5. sap_modulos_menu.png → ¿El menú de módulos está abierto?
6. sap_ventas_menu_button.png → ¿Dónde hacer clic en ventas?
7. sap_ventas_order_menu.png → ¿El menú de ventas está abierto?
8. sap_ventas_order_button.png → ¿Dónde hacer clic en órdenes?
```

### **FASE 3: FORMULARIO DE PEDIDO**
```
9. sap_orden_de_ventas_template.png → ¿Estamos en el formulario correcto?
10. client_field.png → ¿Dónde ingresar el NIT?
11. orden_compra.png → ¿Dónde ingresar la orden de compra?
12. fecha_entrega.png → ¿Dónde ingresar la fecha?
13. primer_articulo.png → ¿Dónde ingresar el primer artículo?
14. agregar_docum_button.png → ¿Dónde agregar más artículos?
```

### **FASE 4: FINALIZACIÓN**
```
15. scroll_to_bottom.png → ¿Necesito hacer scroll?
16. sap_totales_section.png → ¿Dónde están los totales?
17. agregar_y_button.png → ¿Dónde hacer clic para finalizar?
18. sap_popup_agregar_y_cerrar.png → ¿Dónde cerrar la minipantalla?
```

---

## 🔧 **CONFIGURACIONES DE CONFIANZA**

### **Alta Confianza (0.8-0.85)**
- `agregar_y_button.png`: 0.85 (primaria), 0.75 (fallback)
- `sap_popup_agregar_y_cerrar.png`: 0.8
- `sap_archivo_menu_button.png`: 0.8

### **Confianza Media (0.7)**
- `sap_icon.png`: 0.7
- `sap_ventas_menu_button.png`: 0.7
- `sap_ventas_order_button.png`: 0.7

### **Confianza Flexible (0.5)**
- `sap_totales_section.png`: 0.5 (para escritorio remoto)

---

## 📈 **IMÁGENES CRÍTICAS PARA MEJORAR DECISIONES**

### **🔥 PRIORIDAD ALTA**
1. **`agregar_y_button.png`** - Botón principal de finalización
2. **`sap_popup_agregar_y_cerrar.png`** - Cierre de minipantalla
3. **`sap_totales_section.png`** - Validación de totales

### **⚡ PRIORIDAD MEDIA**
4. **`sap_orden_de_ventas_template.png`** - Template base
5. **`client_field.png`** - Campo de cliente
6. **`primer_articulo.png`** - Primera fila de artículos

### **📋 PRIORIDAD BAJA**
7. **`sap_icon.png`** - Icono de SAP
8. **`sap_modulos_menu_button.png`** - Navegación
9. **`sap_ventas_menu_button.png`** - Navegación

---

## 🎯 **RECOMENDACIONES PARA MEJORAR DECISIONES**

### **1. Actualizar Imágenes Críticas**
- **Frecuencia**: Semanal
- **Imágenes**: `agregar_y_button.png`, `sap_popup_agregar_y_cerrar.png`
- **Beneficio**: Mayor precisión en finalización de pedidos

### **2. Agregar Imágenes de Validación**
- **Nuevas imágenes sugeridas**:
  - `pedido_completado.png` - Validar que el pedido se cerró
  - `error_popup.png` - Detectar errores
  - `loading_indicator.png` - Esperar carga

### **3. Mejorar Configuraciones**
- **Ajustar confianzas** según el entorno
- **Agregar regiones de búsqueda** específicas
- **Implementar fallbacks** múltiples

### **4. Monitoreo Continuo**
- **Logs de confianza** para cada imagen
- **Alertas** cuando la confianza baje
- **Actualización automática** de templates

---

## 📊 **ESTADÍSTICAS DE USO**

### **Imágenes Más Usadas**
1. `agregar_y_button.png` - 100% de los pedidos
2. `sap_popup_agregar_y_cerrar.png` - 100% de los pedidos
3. `sap_orden_de_ventas_template.png` - 100% de los pedidos

### **Imágenes Menos Usadas**
1. `old_sap_modulos_menu_button.png` - Versión antigua
2. `old_sap_ventas_menu_button.png` - Versión antigua
3. `template.png` - Template genérico

---

## 🎯 **CONCLUSIÓN**

El sistema utiliza **25 imágenes de referencia** organizadas en **5 categorías** para navegar y operar en SAP Business One. Las **3 imágenes más críticas** son:

1. **`agregar_y_button.png`** - Finalización de pedidos
2. **`sap_popup_agregar_y_cerrar.png`** - Cierre de minipantallas
3. **`sap_totales_section.png`** - Validación de totales

**Recomendación principal**: Actualizar estas 3 imágenes críticas semanalmente para mantener la máxima precisión en las decisiones del RPA.
