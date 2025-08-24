#!/usr/bin/env python3
"""
Verificación de Estructura de Directorios Separados
Verifica que la nueva estructura de carpetas separadas esté correcta
"""

import os
import glob
from datetime import datetime

def verificar_estructura_directorios():
    """Verifica la estructura de directorios separados"""
    print("🔍 Verificando estructura de directorios separados...")
    
    # Estructura esperada
    estructura_esperada = {
        "sales_order": [
            "01_Pendiente",
            "02_Procesando", 
            "03_Completado",
            "04_Error",
            "05_Archivado"
        ],
        "production_order": [
            "01_Pendiente",
            "02_Procesando",
            "03_Completado", 
            "04_Error",
            "05_Archivado"
        ]
    }
    
    base_dir = "data/outputs_json"
    
    # Verificar cada módulo
    for modulo, subcarpetas in estructura_esperada.items():
        print(f"\n📁 Verificando módulo: {modulo}")
        modulo_dir = os.path.join(base_dir, modulo)
        
        if not os.path.exists(modulo_dir):
            print(f"❌ No existe el directorio: {modulo_dir}")
            continue
        
        print(f"✅ Directorio base existe: {modulo_dir}")
        
        # Verificar subcarpetas
        for subcarpeta in subcarpetas:
            subcarpeta_path = os.path.join(modulo_dir, subcarpeta)
            if os.path.exists(subcarpeta_path):
                print(f"  ✅ {subcarpeta}")
            else:
                print(f"  ❌ {subcarpeta} - NO EXISTE")

def contar_archivos_por_modulo():
    """Cuenta los archivos en cada módulo"""
    print("\n📊 Contando archivos por módulo...")
    
    base_dir = "data/outputs_json"
    
    for modulo in ["sales_order", "production_order"]:
        print(f"\n🏷️  Módulo: {modulo}")
        modulo_dir = os.path.join(base_dir, modulo)
        
        if not os.path.exists(modulo_dir):
            print("  ❌ Directorio no existe")
            continue
        
        # Contar archivos en cada subcarpeta
        subcarpetas = ["01_Pendiente", "02_Procesando", "03_Completado", "04_Error", "05_Archivado"]
        
        for subcarpeta in subcarpetas:
            subcarpeta_path = os.path.join(modulo_dir, subcarpeta)
            if os.path.exists(subcarpeta_path):
                archivos = glob.glob(os.path.join(subcarpeta_path, "*.json"))
                print(f"  📁 {subcarpeta}: {len(archivos)} archivos")
                
                # Mostrar nombres de archivos si hay alguno
                if archivos:
                    for archivo in archivos:
                        print(f"    📄 {os.path.basename(archivo)}")
            else:
                print(f"  ❌ {subcarpeta}: No existe")

def mostrar_archivos_ejemplo():
    """Muestra el contenido de los archivos de ejemplo"""
    print("\n📋 Mostrando archivos de ejemplo...")
    
    archivos_ejemplo = [
        ("sales_order/01_Pendiente/orden_venta_ejemplo_001.json", "Ventas"),
        ("production_order/01_Pendiente/orden_produccion_ejemplo_001.json", "Producción")
    ]
    
    for archivo_relativo, tipo in archivos_ejemplo:
        archivo_path = os.path.join("data/outputs_json", archivo_relativo)
        
        if os.path.exists(archivo_path):
            print(f"\n📄 Archivo de ejemplo ({tipo}): {archivo_relativo}")
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    print("   Contenido:")
                    print("   " + contenido.replace('\n', '\n   '))
            except Exception as e:
                print(f"   ❌ Error leyendo archivo: {e}")
        else:
            print(f"❌ Archivo no existe: {archivo_relativo}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE ESTRUCTURA SEPARADA")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar estructura
    verificar_estructura_directorios()
    
    # Contar archivos
    contar_archivos_por_modulo()
    
    # Mostrar ejemplos
    mostrar_archivos_ejemplo()
    
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 Resumen de la nueva estructura:")
    print("   🏪 Ventas: data/outputs_json/sales_order/")
    print("   🏭 Producción: data/outputs_json/production_order/")
    print("\n🚀 Ahora puedes:")
    print("   1. Colocar archivos de ventas en: sales_order/01_Pendiente/")
    print("   2. Colocar archivos de producción en: production_order/01_Pendiente/")
    print("   3. Seleccionar el módulo correspondiente en el launcher")
    print("   4. El sistema procesará solo los archivos del módulo seleccionado")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para continuar...")
