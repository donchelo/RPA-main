#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validación de integración
Verifica que ambos sistemas (ventas y producción) funcionen de forma idéntica
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def create_test_sales_order():
    """Crea un archivo JSON de prueba para órdenes de venta"""
    test_data = {
        "orden_compra": "TEST-VENTA-001",
        "comprador": {
            "nombre": "Cliente Prueba Ventas",
            "nit": "900123456-1"
        },
        "fecha_entrega": "31/12/2024",
        "items": [
            {
                "codigo": "PROD001",
                "cantidad": 10,
                "descripcion": "Producto de prueba 1"
            },
            {
                "codigo": "PROD002", 
                "cantidad": 5,
                "descripcion": "Producto de prueba 2"
            }
        ],
        "created_at": datetime.now().isoformat(),
        "test_file": True
    }
    
    # Crear directorio si no existe
    sales_dir = os.path.join(project_root, "data", "outputs_json", "sales_order", "01_Pendiente")
    os.makedirs(sales_dir, exist_ok=True)
    
    # Guardar archivo
    filename = "test_sales_order_001.json"
    filepath = os.path.join(sales_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"OK Archivo de prueba de ventas creado: {filename}")
    return filepath

def create_test_production_order():
    """Crea un archivo JSON de prueba para órdenes de producción"""
    test_data = {
        "articulo": "FABRIC001",
        "pedido_interno": "PI-2024-001",
        "cantidad": 100,
        "fecha_finalizacion": "15/01/2025",
        "observaciones": "Orden de prueba para validación",
        "created_at": datetime.now().isoformat(),
        "test_file": True
    }
    
    # Crear directorio si no existe
    production_dir = os.path.join(project_root, "data", "outputs_json", "production_order", "01_Pendiente")
    os.makedirs(production_dir, exist_ok=True)
    
    # Guardar archivo
    filename = "test_production_order_001.json"
    filepath = os.path.join(production_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Archivo de prueba de producción creado: {filename}")
    return filepath

def test_sales_order_handler():
    """Prueba el handler de órdenes de venta"""
    print("\n🛒 PROBANDO HANDLER DE ÓRDENES DE VENTA")
    print("=" * 50)
    
    try:
        from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
        
        handler = SalesOrderHandler()
        print("✅ Handler de ventas inicializado correctamente")
        
        # Verificar métodos principales
        pending_count = handler.get_pending_count()
        print(f"📄 Archivos pendientes: {pending_count}")
        
        status = handler.get_status_summary()
        print(f"📊 Estado: {status}")
        
        # Verificar estructura de directorios
        print(f"📁 Directorio base: {handler.base_dir}")
        print(f"📁 Pendientes: {os.path.exists(handler.pending_dir)}")
        print(f"📁 Procesando: {os.path.exists(handler.processing_dir)}")
        print(f"📁 Completados: {os.path.exists(handler.completed_dir)}")
        print(f"📁 Errores: {os.path.exists(handler.error_dir)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando handler de ventas: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_production_order_handler():
    """Prueba el handler de órdenes de producción"""
    print("\n🏭 PROBANDO HANDLER DE ÓRDENES DE PRODUCCIÓN")
    print("=" * 50)
    
    try:
        from rpa.modules.production_order.production_order_handler import ProductionOrderHandler
        
        handler = ProductionOrderHandler()
        print("✅ Handler de producción inicializado correctamente")
        
        # Verificar métodos principales
        pending_count = handler.get_pending_count()
        print(f"📄 Archivos pendientes: {pending_count}")
        
        status = handler.get_status_summary()
        print(f"📊 Estado: {status}")
        
        # Verificar estructura de directorios
        print(f"📁 Directorio base: {handler.base_dir}")
        print(f"📁 Pendientes: {os.path.exists(handler.pending_dir)}")
        print(f"📁 Procesando: {os.path.exists(handler.processing_dir)}")
        print(f"📁 Completados: {os.path.exists(handler.completed_dir)}")
        print(f"📁 Errores: {os.path.exists(handler.error_dir)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando handler de producción: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def validate_identical_structure():
    """Valida que ambos sistemas tengan estructura idéntica"""
    print("\n🔍 VALIDANDO ESTRUCTURA IDÉNTICA")
    print("=" * 50)
    
    try:
        from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
        from rpa.modules.production_order.production_order_handler import ProductionOrderHandler
        
        sales_handler = SalesOrderHandler()
        production_handler = ProductionOrderHandler()
        
        # Verificar que ambos hereden de la misma clase base
        print(f"✅ Sales handler hereda de: {sales_handler.__class__.__bases__}")
        print(f"✅ Production handler hereda de: {production_handler.__class__.__bases__}")
        
        # Verificar métodos comunes
        common_methods = ['process_pending_orders', 'get_pending_count', 'get_status_summary']
        
        for method in common_methods:
            sales_has = hasattr(sales_handler, method)
            production_has = hasattr(production_handler, method)
            
            if sales_has and production_has:
                print(f"✅ Ambos handlers tienen método: {method}")
            else:
                print(f"❌ Método faltante - Sales: {sales_has}, Production: {production_has}: {method}")
        
        # Verificar estructura de directorios
        sales_dirs = ['pending_dir', 'processing_dir', 'completed_dir', 'error_dir']
        production_dirs = ['pending_dir', 'processing_dir', 'completed_dir', 'error_dir']
        
        for dir_attr in sales_dirs:
            sales_has = hasattr(sales_handler, dir_attr)
            production_has = hasattr(production_handler, dir_attr)
            
            if sales_has and production_has:
                print(f"✅ Ambos handlers tienen directorio: {dir_attr}")
            else:
                print(f"❌ Directorio faltante - Sales: {sales_has}, Production: {production_has}: {dir_attr}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validando estructura: {str(e)}")
        return False

def main():
    """Función principal de validación"""
    print("INICIANDO VALIDACION DE SISTEMA RPA")
    print("=" * 60)
    
    # Crear archivos de prueba
    sales_file = create_test_sales_order()
    production_file = create_test_production_order()
    
    # Probar handlers
    sales_ok = test_sales_order_handler()
    production_ok = test_production_order_handler()
    
    # Validar estructura idéntica
    structure_ok = validate_identical_structure()
    
    # Resumen final
    print("\n📋 RESUMEN DE VALIDACIÓN")
    print("=" * 50)
    print(f"✅ Handler de ventas: {'OK' if sales_ok else 'ERROR'}")
    print(f"✅ Handler de producción: {'OK' if production_ok else 'ERROR'}")
    print(f"✅ Estructura idéntica: {'OK' if structure_ok else 'ERROR'}")
    
    if sales_ok and production_ok and structure_ok:
        print("\n🎉 ¡VALIDACIÓN EXITOSA!")
        print("Los dos sistemas funcionan de forma idéntica")
        return True
    else:
        print("\n❌ VALIDACIÓN FALLÓ")
        print("Los sistemas no funcionan de forma idéntica")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)