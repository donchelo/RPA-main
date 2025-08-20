# 🗺️ DIAGRAMA DE DEPENDENCIAS - RPA TAMAPRINT

## 📊 DIAGRAMA PRINCIPAL DE DEPENDENCIAS

```mermaid
graph TD
    %% Punto de entrada
    MAIN[main.py] --> RPA_SM[rpa_with_state_machine.py]
    MAIN --> LOGGER[simple_logger.py]
    
    %% Implementaciones RPA
    RPA_SM --> VISION[vision/main.py]
    RPA_SM --> CONFIG[config_manager.py]
    RPA_SM --> ERROR[error_handler.py]
    RPA_SM --> STATE[state_machine.py]
    RPA_SM --> HANDLERS[rpa_state_handlers.py]
    RPA_SM --> SMART[smart_waits.py]
    
    %% Implementación original (OBSOLETA)
    RPA_OLD[rpa/main.py] --> VISION
    RPA_OLD --> CONFIG
    RPA_OLD --> ERROR
    RPA_OLD --> SMART
    
    %% Sistema de visión
    VISION --> TEMPLATE[vision/template_matcher.py]
    VISION --> CONFIG
    VISION --> LOGGER
    
    %% Máquina de estados
    STATE --> LOGGER
    HANDLERS --> STATE
    HANDLERS --> VISION
    HANDLERS --> CONFIG
    HANDLERS --> SMART
    
    %% Utilidades
    SMART --> CONFIG
    SMART --> LOGGER
    ERROR --> CONFIG
    ERROR --> LOGGER
    
    %% Google Drive
    GDRIVE_OAUTH[google_drive_oauth_uploader.py] --> LOGGER
    GDRIVE_OLD[google_drive_uploader.py] --> LOGGER
    
    %% Logger obsoleto
    LOGGER_OLD[logger.py] --> NONE[none]
    
    %% Estilo para archivos obsoletos
    classDef obsolete fill:#ffcccc,stroke:#ff0000,stroke-width:2px
    classDef active fill:#ccffcc,stroke:#00ff00,stroke-width:2px
    classDef core fill:#ccccff,stroke:#0000ff,stroke-width:2px
    
    class RPA_OLD,LOGGER_OLD,GDRIVE_OLD obsolete
    class RPA_SM,VISION,CONFIG,ERROR,STATE,HANDLERS,SMART,TEMPLATE,GDRIVE_OAUTH active
    class MAIN,LOGGER core
```

## 🔄 FLUJO DE DEPENDENCIAS CRÍTICAS

```mermaid
graph LR
    %% Flujo principal
    A[main.py] --> B[rpa_with_state_machine.py]
    B --> C[state_machine.py]
    B --> D[rpa_state_handlers.py]
    D --> E[vision/main.py]
    D --> F[config_manager.py]
    D --> G[smart_waits.py]
    
    %% Dependencias de logging
    B --> H[simple_logger.py]
    C --> H
    D --> H
    E --> H
    F --> H
    G --> H
    
    %% Dependencias de configuración
    B --> F
    D --> F
    E --> F
    G --> F
    
    %% Estilo
    classDef entry fill:#ffcc99
    classDef core fill:#99ccff
    classDef utility fill:#cc99ff
    
    class A entry
    class B,C,D,E core
    class F,G,H utility
```

## 🚨 DEPENDENCIAS PROBLEMÁTICAS

```mermaid
graph TD
    %% Acoplamiento alto de simple_logger
    LOGGER[simple_logger.py] --> A[rpa_with_state_machine.py]
    LOGGER --> B[vision/main.py]
    LOGGER --> C[error_handler.py]
    LOGGER --> D[state_machine.py]
    LOGGER --> E[smart_waits.py]
    LOGGER --> F[google_drive_oauth_uploader.py]
    
    %% Acoplamiento alto de config_manager
    CONFIG[config_manager.py] --> A
    CONFIG --> B
    CONFIG --> C
    CONFIG --> E
    CONFIG --> G[template_matcher.py]
    
    %% Redundancias
    RPA1[rpa/main.py] --> B
    RPA1 --> CONFIG
    RPA1 --> C
    RPA1 --> E
    
    RPA2[rpa_with_state_machine.py] --> B
    RPA2 --> CONFIG
    RPA2 --> C
    RPA2 --> E
    
    %% Estilo para problemas
    classDef problem fill:#ffcccc,stroke:#ff0000,stroke-width:3px
    classDef redundancy fill:#ffffcc,stroke:#ffaa00,stroke-width:2px
    
    class LOGGER,CONFIG problem
    class RPA1,RPA2 redundancy
```

## 🎯 ARQUITECTURA OBJETIVO

```mermaid
graph TD
    %% Nueva estructura propuesta
    MAIN[main.py] --> CORE[core/]
    CORE --> RPA[rpa_engine.py]
    CORE --> VISION[vision_engine.py]
    CORE --> CONFIG[config_manager.py]
    CORE --> LOGGER[logger.py]
    
    %% Interfaces
    RPA --> INTERFACE[rpa_interface.py]
    VISION --> VISION_INTERFACE[vision_interface.py]
    
    %% Implementaciones
    RPA --> STATE_IMPL[state_machine_impl.py]
    VISION --> TEMPLATE_IMPL[template_matcher_impl.py]
    VISION --> OCR_IMPL[ocr_engine_impl.py]
    
    %% Utilidades
    CORE --> UTILS[utils/]
    UTILS --> ERROR[error_handler.py]
    UTILS --> WAITS[smart_waits.py]
    UTILS --> DRIVE[google_drive.py]
    
    %% Estilo para nueva arquitectura
    classDef new fill:#ccffcc,stroke:#00ff00,stroke-width:2px
    classDef interface fill:#ffffcc,stroke:#ffaa00,stroke-width:2px
    
    class CORE,RPA,VISION,CONFIG,LOGGER,UTILS new
    class INTERFACE,VISION_INTERFACE interface
```

## 📊 MÉTRICAS DE COMPLEJIDAD

### Acoplamiento por Módulo:

| Módulo | Dependencias Salientes | Dependencias Entrantes | Complejidad |
|--------|----------------------|----------------------|-------------|
| `simple_logger` | 0 | 15+ | **ALTA** |
| `config_manager` | 0 | 10+ | **ALTA** |
| `vision/main` | 3 | 8+ | **MEDIA** |
| `rpa_with_state_machine` | 8 | 3 | **MEDIA** |
| `error_handler` | 2 | 4 | **BAJA** |
| `state_machine` | 1 | 3 | **BAJA** |

### Redundancias Identificadas:

1. **Sistemas de Logging**: 2 implementaciones
2. **Implementaciones RPA**: 2 versiones
3. **Google Drive**: 2 uploaders
4. **Tests**: Dispersos en múltiples ubicaciones

## 🔧 PLAN DE REFACTORIZACIÓN VISUAL

### Fase 1: Eliminación de Redundancias
```mermaid
graph LR
    A[Estado Actual] --> B[Eliminar logger.py]
    B --> C[Eliminar google_drive_uploader.py]
    C --> D[Evaluar rpa/main.py]
    D --> E[Estado Limpio]
    
    classDef current fill:#ffcccc
    classDef clean fill:#ccffcc
    
    class A current
    class E clean
```

### Fase 2: Reestructuración
```mermaid
graph LR
    A[Estado Limpio] --> B[Crear src/]
    B --> C[Mover módulos]
    C --> D[Actualizar imports]
    D --> E[Estructura Nueva]
    
    classDef clean fill:#ccffcc
    classDef new fill:#99ccff
    
    class A clean
    class E new
```

### Fase 3: Optimización
```mermaid
graph LR
    A[Estructura Nueva] --> B[Inyección Dependencias]
    B --> C[Factories]
    C --> D[Interfaces]
    D --> E[Arquitectura Final]
    
    classDef new fill:#99ccff
    classDef final fill:#cc99ff
    
    class A new
    class E final
```

## 📝 NOTAS DE IMPLEMENTACIÓN

### Prioridades de Refactorización:

1. **CRÍTICO**: Eliminar `logger.py` y `google_drive_uploader.py`
2. **ALTO**: Decidir entre `rpa/main.py` y `rpa_with_state_machine.py`
3. **MEDIO**: Reducir acoplamiento de `simple_logger` y `config_manager`
4. **BAJO**: Implementar interfaces y factories

### Riesgos Identificados:

- **Alto**: Cambios en `simple_logger` afectan a 15+ módulos
- **Medio**: Eliminación de `rpa/main.py` puede romper tests
- **Bajo**: Reestructuración de directorios es mecánica

---

**Última actualización**: Diciembre 2024
