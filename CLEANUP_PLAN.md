# Plan de Limpieza y Reorganización del Proyecto RPA

## Problemas Identificados

### 1. Archivos Launcher Duplicados
- `launcher_funcional.py` (25KB) - Versión funcional
- `launcher_completo.py` (20KB) - Versión completa
- `launcher_definitivo.py` (12KB) - Versión definitiva
- `launcher_ultra_simple.py` (2.3KB) - Versión simple
- `launcher_ventas_mejorado.py` (13KB) - Versión para ventas
- `rpa_launcher.py` (19KB) - Launcher principal
- `rpa_launcher_v2.py` (29KB) - Versión 2
- `rpa_launcher_v3.py` (30KB) - Versión 3
- `rpa_launcher_v3_simple.py` (19KB) - Versión 3 simple
- `rpa_launcher_v3_robust.py` (24KB) - Versión 3 robusta
- `rpa_launcher_v3_final.py` (24KB) - Versión 3 final

### 2. Archivos de Test Dispersos
- Archivos de test en raíz: `test_*.py`
- Archivos de test en `/tests/legacy/`
- Archivos de test en `/tests/`

### 3. Archivos de Documentación Redundantes
- Múltiples archivos `.md` con información similar
- Archivos de diagnóstico que pueden consolidarse

### 4. Archivos Temporales y Debug
- Archivos de log en raíz
- Archivos de debug dispersos
- Archivos temporales

## Plan de Reorganización

### 1. Estructura de Carpetas Propuesta
```
RPA-main/
├── src/                          # Código fuente principal
│   ├── rpa/                      # Módulo RPA principal
│   ├── launchers/                # Todos los launchers
│   └── utils/                    # Utilidades
├── tests/                        # Todos los tests organizados
│   ├── unit/                     # Tests unitarios
│   ├── integration/              # Tests de integración
│   ├── legacy/                   # Tests legacy (para depuración)
│   └── fixtures/                 # Datos de prueba
├── docs/                         # Documentación consolidada
├── scripts/                      # Scripts de utilidad
├── logs/                         # Todos los logs
├── debug/                        # Archivos de debug
├── temp/                         # Archivos temporales
├── assets/                       # Recursos estáticos
└── data/                         # Datos del sistema
```

### 2. Consolidación de Launchers
- **Mantener**: `launcher_funcional.py` (versión principal)
- **Mantener**: `launcher_ventas_mejorado.py` (para ventas)
- **Mover a legacy**: Resto de launchers

### 3. Consolidación de Tests
- Mover todos los `test_*.py` de la raíz a `/tests/`
- Organizar por tipo: unit, integration, legacy

### 4. Limpieza de Documentación
- Consolidar archivos `.md` similares
- Crear documentación principal en `/docs/`

### 5. Archivos a Eliminar
- Archivos de log en raíz
- Archivos temporales
- Archivos de debug obsoletos
- Archivos duplicados

## Archivos Críticos a Preservar
- `main.py` - Punto de entrada principal
- `requirements.txt` - Dependencias
- `config.yaml` - Configuración
- `rpa/` - Módulo principal
- `data/` - Datos del sistema
- `assets/` - Recursos

## Archivos a Mover
- Todos los launchers → `/src/launchers/`
- Todos los tests → `/tests/`
- Documentación → `/docs/`
- Scripts → `/scripts/`
- Logs → `/logs/`
