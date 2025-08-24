# Sistema RPA - Automatización de Procesos

## 📋 Descripción
Sistema de Automatización Robótica de Procesos (RPA) para la gestión automatizada de órdenes de venta y producción en SAP.

## 🏗️ Estructura del Proyecto

```
RPA-main/
├── src/                          # Código fuente principal
│   ├── launchers/               # Launchers principales
│   │   ├── launcher_ventas_mejorado.py
│   │   ├── launcher_ventas_funcional.bat
│   │   ├── launcher_ventas_mejorado.bat
│   │   ├── rpa_launcher_v3_final.py
│   │   ├── rpa_launcher_v3_final.bat
│   │   └── legacy/              # Versiones anteriores
│   └── utils/                   # Utilidades y scripts
├── rpa/                         # Módulo RPA principal
│   ├── modules/                 # Módulos específicos
│   │   ├── sales_order/         # Gestión de órdenes de venta
│   │   └── production_order/    # Gestión de órdenes de producción
│   ├── vision/                  # Sistema de visión computacional
│   └── core/                    # Componentes principales
├── tests/                       # Tests organizados
│   ├── unit/                    # Tests unitarios
│   ├── integration/             # Tests de integración
│   ├── legacy/                  # Tests legacy
│   └── fixtures/                # Datos de prueba
├── docs/                        # Documentación
│   ├── guides/                  # Guías de usuario
│   ├── technical/               # Documentación técnica
│   ├── solutions/               # Soluciones a problemas
│   └── progress/                # Progreso del desarrollo
├── scripts/                     # Scripts de utilidad
│   ├── setup/                   # Scripts de configuración
│   ├── maintenance/             # Scripts de mantenimiento
│   └── diagnostics/             # Scripts de diagnóstico
├── debug/                       # Archivos de debug
├── logs/                        # Archivos de log
├── temp/                        # Archivos temporales
├── data/                        # Datos del sistema
├── assets/                      # Recursos estáticos
└── credentials/                 # Credenciales (no versionado)
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- SAP GUI instalado y configurado
- Acceso a escritorio remoto

### Instalación
1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar credenciales en `credentials/`
4. Ejecutar el launcher principal:
   ```bash
   python src/launchers/rpa_launcher_v3_final.py
   ```

## 📁 Componentes Principales

### Launchers
- **`rpa_launcher_v3_final.py`**: Launcher principal del sistema
- **`launcher_ventas_mejorado.py`**: Launcher específico para ventas

### Módulos RPA
- **Sales Order**: Gestión automatizada de órdenes de venta
- **Production Order**: Gestión automatizada de órdenes de producción

### Sistema de Visión
- Detección automática de elementos en pantalla
- Navegación inteligente en SAP
- Captura de imágenes de referencia

## 🧪 Testing

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/unit/

# Tests de integración
python -m pytest tests/integration/

# Tests específicos
python scripts/run_tests.py
```

## 📚 Documentación

- **Guías**: `docs/guides/` - Guías de usuario y uso
- **Técnica**: `docs/technical/` - Documentación técnica
- **Soluciones**: `docs/solutions/` - Soluciones a problemas comunes
- **Progreso**: `docs/progress/` - Historial de desarrollo

## 🔧 Configuración

### Archivos de Configuración
- `config.yaml`: Configuración principal del sistema
- `rpa/modules/*/config.yaml`: Configuraciones específicas por módulo

### Variables de Entorno
- Crear archivo `.env` con credenciales necesarias
- Configurar rutas de archivos y directorios

## 🐛 Debugging

### Archivos de Debug
- `debug/`: Contiene archivos de diagnóstico y debug
- `logs/`: Archivos de log del sistema
- `temp/`: Archivos temporales

### Scripts de Diagnóstico
```bash
# Verificar dependencias
python src/utils/check_dependencies.py

# Diagnosticar problemas
python debug/diagnostico_problema.py
```

## 📈 Estado del Proyecto

- ✅ **Fase 1**: Estructura base completada
- ✅ **Fase 2**: Sistema de visión implementado
- ✅ **Fase 3**: Módulos de ventas y producción
- ✅ **Fase 4**: Integración con Google Drive
- ✅ **Fase 5**: Documentación y optimización

## 🤝 Contribución

1. Crear una rama para tu feature
2. Implementar cambios
3. Ejecutar tests
4. Crear pull request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 📞 Soporte

Para soporte técnico, contactar al equipo de desarrollo.