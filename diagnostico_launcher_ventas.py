#!/usr/bin/env python3
"""
Diagnóstico del Launcher para Órdenes de Venta
Verifica el funcionamiento del procesamiento automático
"""

import os
import sys
import json
import glob
import shutil
import time
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_estructura_directorios():
    """Verifica que existan todos los directorios necesarios"""
    print("🔍 Verificando estructura de directorios...")
    
    base_dir = "data/outputs_json"
    sales_base = os.path.join(base_dir, "sales_order")
    
    directorios = [
        sales_base,
        os.path.join(sales_base, "01_Pendiente"),
        os.path.join(sales_base, "02_Procesando"),
        os.path.join(sales_base, "03_Completado"),
        os.path.join(sales_base, "04_Error"),
        os.path.join(sales_base, "05_Archivado")
    ]
    
    for directorio in directorios:
        if os.path.exists(directorio):
            print(f"✅ {directorio}")
        else:
            print(f"❌ {directorio} - NO EXISTE")
            try:
                os.makedirs(directorio, exist_ok=True)
                print(f"   📁 Creado: {directorio}")
            except Exception as e:
                print(f"   ❌ Error creando: {e}")

def verificar_archivos_pendientes():
    """Verifica los archivos en la carpeta de pendientes"""
    print("\n📄 Verificando archivos pendientes...")
    
    pending_dir = "data/outputs_json/sales_order/01_Pendiente"
    archivos = glob.glob(os.path.join(pending_dir, "*.json"))
    
    if not archivos:
        print("❌ No hay archivos pendientes")
        return False
    
    print(f"✅ Encontrados {len(archivos)} archivos pendientes:")
    
    for archivo in archivos:
        filename = os.path.basename(archivo)
        print(f"   📄 {filename}")
        
        # Verificar que el JSON sea válido
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar campos requeridos
            campos_requeridos = ['orden_compra', 'comprador', 'fecha_entrega', 'items']
            campos_faltantes = []
            
            for campo in campos_requeridos:
                if campo not in data:
                    campos_faltantes.append(campo)
            
            if campos_faltantes:
                print(f"      ⚠️ Campos faltantes: {campos_faltantes}")
            else:
                print(f"      ✅ JSON válido")
                
        except json.JSONDecodeError as e:
            print(f"      ❌ JSON inválido: {e}")
        except Exception as e:
            print(f"      ❌ Error leyendo archivo: {e}")
    
    return True

def simular_procesamiento_manual():
    """Simula el procesamiento manual de un archivo"""
    print("\n🧪 Simulando procesamiento manual...")
    
    pending_dir = "data/outputs_json/sales_order/01_Pendiente"
    processing_dir = "data/outputs_json/sales_order/02_Procesando"
    completed_dir = "data/outputs_json/sales_order/03_Completado"
    
    archivos = glob.glob(os.path.join(pending_dir, "*.json"))
    
    if not archivos:
        print("❌ No hay archivos para procesar")
        return
    
    # Tomar el primer archivo
    archivo_origen = archivos[0]
    filename = os.path.basename(archivo_origen)
    
    print(f"📄 Procesando: {filename}")
    
    try:
        # Leer el archivo
        with open(archivo_origen, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"   📊 Datos cargados:")
        print(f"      - Orden: {data.get('orden_compra', 'N/A')}")
        print(f"      - Comprador: {data.get('comprador', {}).get('nombre', 'N/A')}")
        print(f"      - NIT: {data.get('comprador', {}).get('nit', 'N/A')}")
        print(f"      - Items: {len(data.get('items', []))}")
        
        # Simular procesamiento (solo mover el archivo)
        archivo_procesando = os.path.join(processing_dir, filename)
        archivo_completado = os.path.join(completed_dir, filename)
        
        # Mover a procesando
        shutil.move(archivo_origen, archivo_procesando)
        print(f"   📁 Movido a procesando: {filename}")
        
        # Simular tiempo de procesamiento
        print("   ⏳ Simulando procesamiento RPA...")
        time.sleep(3)
        
        # Mover a completado
        shutil.move(archivo_procesando, archivo_completado)
        print(f"   ✅ Procesamiento completado: {filename}")
        
    except Exception as e:
        print(f"   ❌ Error en procesamiento: {e}")

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
    """Función principal del diagnóstico"""
    print("🚀 DIAGNÓSTICO DEL LAUNCHER - ÓRDENES DE VENTA")
    print("=" * 50)
    
    # Verificar estructura
    verificar_estructura_directorios()
    
    # Verificar archivos pendientes
    if verificar_archivos_pendientes():
        # Simular procesamiento
        simular_procesamiento_manual()
    
    # Verificar estado final
    verificar_estado_final()
    
    print("\n" + "=" * 50)
    print("✅ Diagnóstico completado")
    print("\n💡 Recomendaciones:")
    print("   1. Verifica que el launcher esté ejecutándose")
    print("   2. Selecciona 'Módulo de Ventas' en el launcher")
    print("   3. Haz clic en 'Iniciar Procesamiento Automático'")
    print("   4. Revisa los logs del launcher para ver el progreso")

if __name__ == "__main__":
    main()
