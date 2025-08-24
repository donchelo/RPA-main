#!/usr/bin/env python3
"""
Script de prueba para el módulo de órdenes de venta
"""

import os
import sys
import json
import time
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.config_manager import ConfigManager
from rpa.modules.sales_order import SalesOrderHandler
from rpa.simple_logger import rpa_logger


def crear_datos_venta_prueba():
    """Crear datos de prueba para órdenes de venta"""
    datos_prueba = {
        "orden_compra": "TEST-001",
        "fecha_documento": "22/08/2025",
        "fecha_entrega": "26/08/2025",
        "comprador": {
            "nit": "900123456",
            "nombre": "EMPRESA DE PRUEBA S.A.S."
        },
        "items": [
            {
                "descripcion": "Producto de prueba 1",
                "codigo": "001",
                "cantidad": 10,
                "precio_unitario": 1000,
                "precio_total": 10000,
                "fecha_entrega": "26/08/2025"
            },
            {
                "descripcion": "Producto de prueba 2", 
                "codigo": "002",
                "cantidad": 5,
                "precio_unitario": 2000,
                "precio_total": 10000,
                "fecha_entrega": "26/08/2025"
            }
        ],
        "valor_total": 20000,
        "total_items_unicos": 2,
        "numero_items_totales": 15
    }
    return datos_prueba


def mostrar_datos_prueba(datos):
    """Mostrar los datos de prueba de forma clara"""
    print("\n📋 DATOS DE PRUEBA - ÓRDENES DE VENTA")
    print("=" * 50)
    print(f"📝 Orden de Compra: {datos['orden_compra']}")
    print(f"📅 Fecha Documento: {datos['fecha_documento']}")
    print(f"📅 Fecha Entrega: {datos['fecha_entrega']}")
    print(f"🏢 Comprador: {datos['comprador']['nombre']}")
    print(f"🆔 NIT: {datos['comprador']['nit']}")
    print(f"💰 Valor Total: ${datos['valor_total']:,}")
    print(f"📦 Items: {datos['total_items_unicos']} productos únicos")
    print(f"📊 Cantidad Total: {datos['numero_items_totales']} unidades")
    print("=" * 50)
    
    print("\n📦 ITEMS:")
    for i, item in enumerate(datos['items'], 1):
        print(f"  {i}. {item['descripcion']}")
        print(f"     Código: {item['codigo']}")
        print(f"     Cantidad: {item['cantidad']}")
        print(f"     Precio: ${item['precio_unitario']:,}")
        print(f"     Total: ${item['precio_total']:,}")


def cambiar_a_escritorio_remoto():
    """Función para cambiar al escritorio remoto"""
    print("🔄 Cambiando al escritorio remoto...")
    
    try:
        import pyautogui
        
        # Método simple: usar Alt+Tab para cambiar a la ventana anterior
        print("   - Usando Alt+Tab para cambiar ventana...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(2.0)  # Esperar a que se active la ventana
        
        print("✅ Cambio de ventana completado")
        return True
        
    except Exception as e:
        print(f"⚠️  Error cambiando ventana: {e}")
        print("💡 El script continuará, pero asegúrate de que el escritorio remoto esté activo")
        time.sleep(3.0)
        return False


def verificar_formulario_ventas(vision):
    """Verificar que el formulario de ventas esté abierto"""
    print("🔍 Verificando que el formulario de ventas esté abierto...")
    
    try:
        import pyautogui
        import cv2
        import numpy as np
        
        # Tomar screenshot y buscar elementos del formulario
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Buscar imagen del formulario de ventas
        form_ref = cv2.imread('./rpa/vision/reference_images/sap_orden_de_ventas_template.png', cv2.IMREAD_COLOR)
        
        if form_ref is not None:
            result = cv2.matchTemplate(screenshot_cv, form_ref, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > 0.7:  # Umbral de confianza
                print(f"✅ Formulario de ventas detectado (confianza: {max_val:.3f})")
                return True
            else:
                print(f"⚠️  Formulario no detectado claramente (confianza: {max_val:.3f})")
                return False
        else:
            print("⚠️  Imagen de referencia del formulario no encontrada")
            return False
            
    except Exception as e:
        print(f"⚠️  Error verificando formulario: {e}")
        return False


def main():
    """Función principal de prueba"""
    print("🚀 INICIANDO PRUEBA DEL MÓDULO DE ÓRDENES DE VENTA")
    print("=" * 60)
    
    # Crear datos de prueba
    datos_prueba = crear_datos_venta_prueba()
    mostrar_datos_prueba(datos_prueba)
    
    # Inicializar componentes
    print("\n🔧 Inicializando componentes...")
    vision = Vision()
    config = ConfigManager()
    handler = SalesOrderHandler(vision, config)
    
    print("✅ Componentes inicializados")
    
    # Preguntar si cambiar al escritorio remoto
    print("\n🖥️  PREPARACIÓN:")
    print("1. Asegúrate de que el escritorio remoto esté abierto")
    print("2. SAP Business One debe estar disponible")
    print("3. El sistema debe estar listo para recibir órdenes")
    
    respuesta = input("\n¿Deseas cambiar automáticamente al escritorio remoto? (s/n): ").strip().lower()
    
    if respuesta == 's':
        if not cambiar_a_escritorio_remoto():
            print("⚠️  Continuando sin cambio automático de ventana")
    
    # Preguntar confirmación para continuar
    print("\n⏳ PREPARACIÓN FINAL:")
    print("• El sistema cambiará a SAP Business One")
    print("• Navegará al módulo de ventas")
    print("• Procesará los datos de prueba")
    print("• Tomará screenshots de confirmación")
    
    confirmacion = input("\n¿Estás listo para continuar? (s/n): ").strip().lower()
    
    if confirmacion != 's':
        print("❌ Prueba cancelada por el usuario")
        return
    
    # Ejecutar prueba
    print("\n🚀 EJECUTANDO PRUEBA...")
    print("-" * 40)
    
    try:
        # Procesar orden de venta
        success = handler.process_sales_order(datos_prueba)
        
        if success:
            print("\n✅ PRUEBA EXITOSA")
            print("=" * 40)
            print("• Orden de venta procesada correctamente")
            print("• Datos cargados en SAP Business One")
            print("• Screenshots generados")
            print("• Logs actualizados")
            
            # Verificar formulario final
            print("\n🔍 Verificando resultado final...")
            if verificar_formulario_ventas(vision):
                print("✅ Formulario de ventas confirmado")
            else:
                print("⚠️  No se pudo confirmar el formulario final")
            
        else:
            print("\n❌ PRUEBA FALLIDA")
            print("=" * 40)
            print("• Error en el procesamiento")
            print("• Revisa los logs para más detalles")
            print("• Verifica la conexión con SAP")
            
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {str(e)}")
        print("=" * 40)
        print("• Error inesperado durante la prueba")
        print("• Revisa la configuración del sistema")
        print("• Verifica las dependencias")
    
    print("\n🏁 PRUEBA COMPLETADA")
    print("=" * 60)
    print("📁 Revisa la carpeta 'screenshots' para ver las capturas")
    print("📝 Revisa los logs para información detallada")
    print("🔄 Puedes ejecutar la prueba nuevamente si es necesario")


if __name__ == "__main__":
    main()
