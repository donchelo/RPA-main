# 📦 Guía de Dependencias - RPA TAMAPRINT

Este documento explica las diferentes opciones de instalación de dependencias para el sistema RPA TAMAPRINT.

## 🎯 Opciones de Instalación

### 1. **Instalación Completa** (Recomendada)
```bash
pip install -r requirements.txt
```
**Incluye:** Todas las dependencias principales + dependencias adicionales para funcionalidad completa.

### 2. **Instalación Mínima** (Funcionalidad Básica)
```bash
pip install -r requirements-minimal.txt
```
**Incluye:** Solo las dependencias esenciales para funcionamiento básico.
**Nota:** Algunas funcionalidades avanzadas (EasyOCR, procesamiento avanzado de imágenes) no estarán disponibles.

### 3. **Instalación de Desarrollo** (Para Desarrolladores)
```bash
# Primero instalar dependencias principales
pip install -r requirements.txt

# Luego instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```
**Incluye:** Todas las dependencias + herramientas de testing, linting, y desarrollo.

## 📋 Descripción de Dependencias

### 🔧 **Dependencias Principales**

#### Automatización y Control de Interfaz
- **PyAutoGUI**: Automatización de mouse y teclado
- **PyGetWindow**: Manejo de ventanas de Windows
- **PyMsgBox**: Cuadros de diálogo
- **pyperclip**: Manejo del portapapeles
- **PyRect/PyScreeze**: Captura de pantalla y coordenadas
- **pytweening**: Animaciones suaves
- **pywin32-ctypes**: Integración con Windows API
- **MouseInfo**: Información del mouse

#### Visión Computacional
- **opencv-python**: Procesamiento de imágenes y template matching
- **pillow**: Manipulación de imágenes
- **numpy**: Operaciones numéricas
- **scikit-image**: Procesamiento avanzado de imágenes
- **matplotlib**: Visualización de imágenes

#### OCR y Reconocimiento de Texto
- **pytesseract**: OCR básico con Tesseract
- **easyocr**: OCR avanzado con deep learning
- **torch/torchvision/torchaudio**: Backend para EasyOCR

#### Utilidades del Sistema
- **schedule**: Programación de tareas
- **psutil**: Información del sistema
- **colorama**: Colores en terminal
- **requests**: Peticiones HTTP
- **PyYAML**: Configuración YAML
- **loguru**: Logging avanzado
- **pathlib2**: Manejo de rutas
- **jsonschema**: Validación de JSON

### 🛠️ **Dependencias de Desarrollo**

#### Testing
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **pytest-mock**: Mocking para tests
- **pytest-asyncio**: Testing asíncrono
- **pytest-html**: Reportes HTML

#### Formateo y Linting
- **black**: Formateador de código
- **flake8**: Linter de código
- **mypy**: Verificación de tipos
- **isort**: Ordenamiento de imports
- **autopep8**: Formateo automático

#### Documentación
- **sphinx**: Generador de documentación
- **sphinx-rtd-theme**: Tema ReadTheDocs
- **myst-parser**: Parser Markdown

#### Profiling y Debugging
- **memory-profiler**: Análisis de memoria
- **line-profiler**: Profiling línea por línea
- **py-spy**: Profiler de rendimiento

## ⚠️ **Requisitos del Sistema**

### Windows
- Python 3.8 o superior
- Tesseract OCR instalado en `C:\Program Files\Tesseract-OCR\`
- Permisos de administrador para algunas operaciones

### Dependencias del Sistema
```bash
# Instalar Tesseract OCR (Windows)
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki

# Verificar instalación
tesseract --version
```

## 🔄 **Actualización de Dependencias**

### Verificar Versiones Actuales
```bash
pip list --outdated
```

### Actualizar Dependencias Específicas
```bash
pip install --upgrade nombre-paquete
```

### Actualizar Todas las Dependencias
```bash
pip install --upgrade -r requirements.txt
```

## 🚨 **Solución de Problemas**

### Error de Tesseract
```
pytesseract.pytesseract.TesseractNotFoundError
```
**Solución:** Verificar que Tesseract esté instalado y la ruta sea correcta.

### Error de EasyOCR
```
ModuleNotFoundError: No module named 'torch'
```
**Solución:** Instalar PyTorch manualmente si hay problemas de compatibilidad.

### Error de OpenCV
```
ImportError: DLL load failed
```
**Solución:** Reinstalar opencv-python con `pip uninstall opencv-python && pip install opencv-python`.

### Conflictos de Versiones
```bash
# Crear entorno virtual
python -m venv rpa_env
rpa_env\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 📊 **Información de Versiones**

Las versiones especificadas en los archivos de requirements son las versiones estables más recientes al momento de la actualización. Para ver las versiones exactas instaladas:

```bash
pip freeze
```

## 🔗 **Enlaces Útiles**

- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PyTorch Installation](https://pytorch.org/get-started/locally/)
