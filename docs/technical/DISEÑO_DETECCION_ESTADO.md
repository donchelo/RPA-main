# 🎯 Diseño del Sistema de Detección de Estado - RPA TAMAPRINT

## 📋 Análisis del Problema

### Situación Actual
El RPA actual no tiene un sistema robusto para identificar en qué pantalla se encuentra antes de proceder. Esto causa:
- Errores cuando el sistema está en un estado inesperado
- Falta de adaptabilidad a diferentes situaciones
- Dificultad para recuperarse de errores

### Estados Principales Identificados
1. **Escritorio Remoto** - Pantalla de conexión remota
2. **SAP Desktop** - SAP abierto pero no en formulario de órdenes
3. **Formulario de Órdenes de Venta** - Pantalla donde se ingresan pedidos

## 🏗️ Arquitectura Propuesta

### 1. **Sistema de Detección de Estado (State Detector)**

```python
class ScreenState(Enum):
    UNKNOWN = "unknown"
    REMOTE_DESKTOP = "remote_desktop"
    SAP_DESKTOP = "sap_desktop"
    SALES_ORDER_FORM = "sales_order_form"
    ERROR = "error"
```

### 2. **Detectores Específicos por Pantalla**

#### A. Remote Desktop Detector
- **Indicadores**: Barra de título "Conexión a Escritorio remoto"
- **Elementos clave**: Botones de control de ventana remota
- **Confianza**: Alta (0.9+)

#### B. SAP Desktop Detector
- **Indicadores**: Icono de SAP, menú de módulos
- **Elementos clave**: Botón "Módulos", menú principal
- **Confianza**: Media-Alta (0.8+)

#### C. Sales Order Form Detector
- **Indicadores**: Campos específicos del formulario
- **Elementos clave**: Campo cliente, orden de compra, fecha
- **Confianza**: Alta (0.85+)

### 3. **Estrategia de Detección**

#### Fase 1: Detección Rápida
```python
def detect_current_screen() -> ScreenState:
    # 1. Tomar screenshot
    # 2. Detectar elementos clave de cada pantalla
    # 3. Calcular confianza por pantalla
    # 4. Retornar estado con mayor confianza
```

#### Fase 2: Verificación de Confianza
```python
def verify_screen_state(state: ScreenState) -> bool:
    # Verificar múltiples elementos para confirmar estado
    # Retornar True si la confianza es suficiente
```

## 🔧 Implementación por Fases

### **Fase 1: Sistema Base de Detección**
1. Crear `ScreenDetector` class
2. Implementar detección básica de las 3 pantallas principales
3. Integrar con máquina de estados existente

### **Fase 2: Navegación Inteligente**
1. Crear `NavigationPlanner` que determine ruta óptima
2. Implementar lógica de maximización automática
3. Añadir detección de errores y recuperación

### **Fase 3: Optimización y Robustez**
1. Mejorar confianza de detección
2. Añadir timeout y reintentos
3. Implementar logging detallado

## 📊 Flujo de Trabajo Propuesto

```
1. INICIO
   ↓
2. DETECTAR ESTADO ACTUAL
   ├── Remote Desktop → Ir a paso 3
   ├── SAP Desktop → Ir a paso 4
   ├── Sales Order Form → Ir a paso 5
   └── Unknown → Ir a paso 2 (reintentar)
   ↓
3. MAXIMIZAR Y CONECTAR REMOTE DESKTOP
   ↓
4. ABRIR/NAVEGAR A SAP
   ↓
5. NAVEGAR A FORMULARIO DE ÓRDENES
   ↓
6. INICIAR PROCESAMIENTO DE DATOS
```

## 🎯 Beneficios Esperados

### Robustez
- ✅ Siempre sabe dónde está
- ✅ Se adapta a cualquier estado inicial
- ✅ Recuperación automática de errores

### Eficiencia
- ✅ No repite pasos innecesarios
- ✅ Navegación optimizada
- ✅ Menor tiempo de procesamiento

### Mantenibilidad
- ✅ Código más limpio y organizado
- ✅ Fácil debugging
- ✅ Escalable para nuevos estados

## 🔄 Plan de Refactorización

### **Semana 1: Fase 1**
- [ ] Crear `ScreenDetector` class
- [ ] Implementar detección básica
- [ ] Integrar con estado actual

### **Semana 2: Fase 2**
- [ ] Crear `NavigationPlanner`
- [ ] Implementar lógica de navegación
- [ ] Añadir maximización automática

### **Semana 3: Fase 3**
- [ ] Optimizar detección
- [ ] Añadir robustez
- [ ] Testing y validación

## 📝 Próximos Pasos

1. **Revisar y aprobar diseño**
2. **Crear prototipo de `ScreenDetector`**
3. **Implementar detección básica**
4. **Integrar con sistema existente**
5. **Testing y validación**

¿Te parece bien este enfoque? ¿Quieres que empecemos con la Fase 1?
