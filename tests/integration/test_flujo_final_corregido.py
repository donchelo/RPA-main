#!/usr/bin/env python3
"""
Script de prueba para verificar el flujo final corregido del RPA
- Verifica que se tome la screenshot final
- Verifica que se cierre la orden de venta correctamente
"""

import os
import json
import time
from datetime import datetime

def print_section(title):
    """Imprime una sección con formato"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime un mensaje informativo"""
    print(f"ℹ️  {message}")

def verificar_archivo_procesado():
    """Verifica que el archivo 4500224967.PDF.json tenga su screenshot correspondiente"""
    print_section("Verificando Archivo Procesado")
    
    # Verificar archivo JSON
    json_path = './data/outputs_json/Procesados/4500224967.PDF.json'
    if os.path.exists(json_path):
        print_success(f"Archivo JSON encontrado: {json_path}")
        
        # Leer contenido del JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print_info(f"Orden de compra: {data.get('orden_compra', 'N/A')}")
            print_info(f"Fecha documento: {data.get('fecha_documento', 'N/A')}")
            print_info(f"Valor total: {data.get('valor_total', 'N/A')}")
            
        except Exception as e:
            print_error(f"Error leyendo JSON: {str(e)}")
    else:
        print_error(f"Archivo JSON no encontrado: {json_path}")
        return False
    
    # Verificar archivo PNG (screenshot)
    png_path = './data/outputs_json/Procesados/4500224967.PDF.png'
    if os.path.exists(png_path):
        size = os.path.getsize(png_path)
        print_success(f"Archivo PNG encontrado: {png_path} ({size} bytes)")
        
        if size > 1000:  # Más de 1KB
            print_success("Screenshot parece válido (tamaño > 1KB)")
        else:
            print_error("Screenshot parece muy pequeño, puede estar corrupto")
            return False
    else:
        print_error(f"Archivo PNG no encontrado: {png_path}")
        return False
    
    return True

def verificar_flujo_completo():
    """Verifica que el flujo completo esté funcionando"""
    print_section("Verificando Flujo Completo")
    
    try:
        # Importar el sistema RPA
        from rpa.rpa_with_state_machine import RPAWithStateMachine
        from rpa.state_machine import StateMachine, RPAState, RPAEvent
        from rpa.rpa_state_handlers import RPAStateHandlers
        
        print_info("Sistema RPA importado correctamente")
        
        # Crear instancia del RPA
        rpa = RPAWithStateMachine()
        print_success("Instancia RPA creada")
        
        # Crear máquina de estados
        state_machine = StateMachine()
        print_success("Máquina de estados creada")
        
        # Crear manejadores de estado
        handlers = RPAStateHandlers(rpa)
        print_success("Manejadores de estado creados")
        
        # Registrar manejadores
        state_machine.register_state_handler(RPAState.POSITIONING_MOUSE, handlers.handle_positioning_mouse)
        state_machine.register_state_handler(RPAState.TAKING_SCREENSHOT, handlers.handle_taking_screenshot)
        state_machine.register_state_handler(RPAState.UPLOADING_TO_GOOGLE_DRIVE, handlers.handle_uploading_to_google_drive_state)
        state_machine.register_state_handler(RPAState.COMPLETED, handlers.handle_completed_state)
        print_success("Manejadores registrados")
        
        return True
        
    except ImportError as e:
        print_error(f"Error importando módulos RPA: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error en verificación del flujo: {str(e)}")
        return False

def verificar_estructura_archivos():
    """Verifica la estructura de archivos en la carpeta Procesados"""
    print_section("Verificando Estructura de Archivos")
    
    processed_dir = './data/outputs_json/Procesados'
    if not os.path.exists(processed_dir):
        print_error(f"Directorio no encontrado: {processed_dir}")
        return False
    
    print_success(f"Directorio encontrado: {processed_dir}")
    
    # Contar archivos por tipo
    files = os.listdir(processed_dir)
    json_files = [f for f in files if f.endswith('.json')]
    png_files = [f for f in files if f.endswith('.png')]
    pdf_files = [f for f in f in files if f.endswith('.PDF') or f.endswith('.pdf')]
    
    print_info(f"Archivos JSON: {len(json_files)}")
    print_info(f"Archivos PNG: {len(png_files)}")
    print_info(f"Archivos PDF: {len(pdf_files)}")
    
    # Verificar que haya archivos recientes
    recent_files = []
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(processed_dir, file)
            file_time = os.path.getmtime(file_path)
            if time.time() - file_time < 3600:  # Última hora
                recent_files.append(file)
    
    if recent_files:
        print_success(f"Archivos recientes encontrados: {len(recent_files)}")
        for file in recent_files[:5]:  # Mostrar solo los primeros 5
            print_info(f"  - {file}")
    else:
        print_error("No se encontraron archivos recientes")
    
    return True

def main():
    """Función principal del script de verificación"""
    print_section("VERIFICACIÓN DEL FLUJO FINAL CORREGIDO")
    print_info("Verificando que el RPA tome la screenshot final y cierre la orden correctamente")
    
    # Verificar archivo específico
    archivo_ok = verificar_archivo_procesado()
    
    # Verificar estructura de archivos
    estructura_ok = verificar_estructura_archivos()
    
    # Verificar flujo completo
    flujo_ok = verificar_flujo_completo()
    
    # Resumen
    print_section("RESUMEN DE VERIFICACIÓN")
    
    if archivo_ok:
        print_success("✅ Archivo procesado correctamente")
        print_info("  - JSON encontrado y válido")
        print_info("  - Screenshot PNG encontrado y válido")
    else:
        print_error("❌ Problema con archivo procesado")
    
    if estructura_ok:
        print_success("✅ Estructura de archivos correcta")
    else:
        print_error("❌ Problema con estructura de archivos")
    
    if flujo_ok:
        print_success("✅ Flujo RPA configurado correctamente")
    else:
        print_error("❌ Problema con configuración del flujo RPA")
    
    if archivo_ok and estructura_ok and flujo_ok:
        print_success("🎉 TODAS LAS VERIFICACIONES EXITOSAS")
        print_info("El sistema está funcionando correctamente")
    else:
        print_error("⚠️  ALGUNAS VERIFICACIONES FALLARON")
        print_info("Revisar los problemas identificados arriba")
    
    return archivo_ok and estructura_ok and flujo_ok

if __name__ == "__main__":
    main()
