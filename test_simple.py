#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple de validación
Verifica que ambos handlers funcionen correctamente
"""

import os
import sys

# Agregar el directorio del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_sales_handler():
    """Prueba el handler de ventas"""
    print("PROBANDO HANDLER DE VENTAS")
    print("-" * 30)
    
    try:
        from rpa.modules.sales_order.sales_order_handler import SalesOrderHandler
        
        handler = SalesOrderHandler()
        print("OK - Handler de ventas inicializado")
        
        pending_count = handler.get_pending_count()
        print(f"Archivos pendientes: {pending_count}")
        
        status = handler.get_status_summary()
        print(f"Estado: {status}")
        
        return True
        
    except Exception as e:
        print(f"ERROR - Handler de ventas: {str(e)}")
        return False

def test_production_handler():
    """Prueba el handler de producción"""
    print("\nPROBANDO HANDLER DE PRODUCCION")
    print("-" * 30)
    
    try:
        from rpa.modules.production_order.production_order_handler import ProductionOrderHandler
        
        handler = ProductionOrderHandler()
        print("OK - Handler de produccion inicializado")
        
        pending_count = handler.get_pending_count()
        print(f"Archivos pendientes: {pending_count}")
        
        status = handler.get_status_summary()
        print(f"Estado: {status}")
        
        return True
        
    except Exception as e:
        print(f"ERROR - Handler de produccion: {str(e)}")
        return False

def main():
    print("VALIDACION SISTEMA RPA")
    print("=" * 30)
    
    sales_ok = test_sales_handler()
    production_ok = test_production_handler()
    
    print("\nRESUMEN:")
    print("-" * 10)
    print(f"Ventas: {'OK' if sales_ok else 'ERROR'}")
    print(f"Produccion: {'OK' if production_ok else 'ERROR'}")
    
    if sales_ok and production_ok:
        print("\nVALIDACION EXITOSA!")
        return True
    else:
        print("\nVALIDACION FALLO!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)