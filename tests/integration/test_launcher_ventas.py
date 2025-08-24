#!/usr/bin/env python3
"""
Script de prueba para el Launcher de Ventas
Verifica el funcionamiento básico del procesamiento automático
"""

import os
import sys
import json
import glob
import shutil
import time
from datetime import datetime

def verificar_archivos_pendientes():
    """Verifica que haya archivos pendientes para procesar"""
    pending_dir = "data/outputs_json/sales_order/01_Pendiente"
    archivos = glob.glob(os.path.join(pending_dir, "*.json"))
    
    print(f"📄 Archivos pendientes encontrados: {len(archivos)}")
    for archivo in archivos:
        print(f"   - {os.path.basename(archivo)}")
    
    return len(archivos) > 0

def simular_procesamiento_launcher():
    """Simula el procesamiento que haría el launcher"""
    print("\n🧪 Simulando procesamiento del launcher...")
    
    pending_dir = "data/outputs_json/sales_order/01_Pendiente"
    processing_dir = "data/outputs_json/sales_order/02_Procesando"
    completed_dir = "data/outputs_json/sales_order/03_Completado"
    
    archivos = glob.glob(os.path.join(pending_dir, "*.json"))
    
    if not archivos:
        print("❌ No hay archivos para procesar")
        return False
    
    # Procesar cada archivo
    for archivo in archivos:
        filename = os.path.basename(archivo)
        print(f"\n📄 Procesando: {filename}")
        
        try:
            # Leer el archivo
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"   📊 Datos válidos cargados")
            print(f"      - Orden: {data.get('orden_compra', 'N/A')}")
            print(f"      - Comprador: {data.get('comprador', {}).get('nombre', 'N/A')}")
            
            # Mover a procesando
            processing_path = os.path.join(processing_dir, filename)
            shutil.move(archivo, processing_path)
            print(f"   📁 Movido a procesando")
            
            # Simular procesamiento
            print(f"   🔄 Simulando procesamiento RPA...")
            time.sleep(2)  # Simular tiempo de procesamiento
            
            # Mover a completado
            completed_path = os.path.join(completed_dir, filename)
            shutil.move(processing_path, completed_path)
            print(f"   ✅ Procesamiento completado")
            
        except Exception as e:
            print(f"   ❌ Error procesando {filename}: {e}")
            return False
    
    return True

def verificar_estado_final():
    """Verifica el estado final después del procesamiento"""
    print("\n📊 Estado final de directorios:")
    
    directorios = {
        "Pendientes": "data/outputs_json/sales_order/01_Pendiente",
        "Procesando": "data/outputs_json/sales_order/02_Procesando", 
        "Completados": "data/outputs_json/sales_order/03_Completado",
        "Errores": "data/outputs_json/sales_order/04_Error"
    }
    
    for nombre, directorio in directorios.items():
        archivos = glob.glob(os.path.join(directorio, "*.json"))
        print(f"   {nombre}: {len(archivos)} archivos")

def main():
    """Función principal de prueba"""
    print("🚀 PRUEBA DEL LAUNCHER DE VENTAS")
    print("=" * 40)
    
    # Verificar archivos pendientes
    if not verificar_archivos_pendientes():
        print("❌ No hay archivos pendientes para procesar")
        print("💡 Agrega archivos JSON a la carpeta 01_Pendiente")
        return
    
    # Simular procesamiento
    if simular_procesamiento_launcher():
        print("\n✅ Procesamiento simulado exitosamente")
    else:
        print("\n❌ Error en el procesamiento simulado")
        return
    
    # Verificar estado final
    verificar_estado_final()
    
    print("\n" + "=" * 40)
    print("✅ Prueba completada")
    print("\n💡 Para usar el launcher real:")
    print("   1. Ejecuta: launcher_ventas_mejorado.bat")
    print("   2. Haz clic en 'Iniciar Procesamiento Automático'")
    print("   3. El launcher procesará automáticamente los archivos pendientes")

if __name__ == "__main__":
    main()
