#!/usr/bin/env python3
"""
Script de prueba para el módulo de órdenes de producción
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
from rpa.modules.production_order import ProductionOrderHandler
from rpa.simple_logger import rpa_logger


def crear_datos_produccion_prueba():
    """Crear datos de prueba para órdenes de producción"""
    datos_prueba = {
        "numero_articulo": "101846",
        "numero_pedido_interno": "6107",
        "cantidad": 2000,
        "fecha_finalizacion": "12/09/2025",
        "unidad_medida": "PCS",
        "centro_trabajo": "CT-01",
        "observaciones": "Orden de producción de prueba para el RPA"
    }
    return datos_prueba


def mostrar_datos_prueba(datos):
    """Mostrar los datos de prueba de forma clara"""
    print("\n📋 DATOS DE PRUEBA - ÓRDENES DE PRODUCCIÓN")
    print("=" * 50)
    print(f"🏷️  Artículo: {datos['numero_articulo']}")
    print(f"📝 Pedido Interno: {datos['numero_pedido_interno']}")
    print(f"📊 Cantidad: {datos['cantidad']} {datos['unidad_medida']}")
    print(f"📅 Fecha Finalización: {datos['fecha_finalizacion']}")
    print(f"🏭 Centro Trabajo: {datos['centro_trabajo']}")
    print(f"💬 Observaciones: {datos['observaciones']}")
    print("=" * 50)


def cambiar_a_escritorio_remoto():
    """Función para cambiar al escritorio remoto usando Alt+Tab"""
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


def verificar_formulario_produccion(vision):
    """Verificar que el formulario de producción esté abierto"""
    print("🔍 Verificando que el formulario de producción esté abierto...")
    
    try:
        import pyautogui
        import cv2
        import numpy as np
        
        # Tomar screenshot y buscar elementos del formulario
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Buscar imagen del formulario de producción
        form_ref = cv2.imread('./rpa/vision/reference_images/production/sap_produccion_form.png', cv2.IMREAD_COLOR)
        
        if form_ref is not None:
            result = cv2.matchTemplate(screenshot_cv, form_ref, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > 0.7:  # Umbral de confianza
                print(f"✅ Formulario de producción detectado (confianza: {max_val:.3f})")
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
    print("🚀 INICIANDO PRUEBA DEL MÓDULO DE ÓRDENES DE PRODUCCIÓN")
    print("=" * 60)
    
    # Crear datos de prueba
    datos_prueba = crear_datos_produccion_prueba()
    mostrar_datos_prueba(datos_prueba)
    
    # Inicializar componentes
    print("\n🔧 Inicializando componentes...")
    vision = Vision()
    config = ConfigManager()
    handler = ProductionOrderHandler(vision, config)
    
    print("✅ Componentes inicializados")
    
    # Preguntar si cambiar al escritorio remoto
    print("\n🖥️  PREPARACIÓN:")
    print("1. Asegúrate de que el escritorio remoto esté abierto")
    print("2. SAP Business One debe estar disponible")
    print("3. El módulo de producción debe estar accesible")
    
    respuesta = input("\n¿Deseas cambiar automáticamente al escritorio remoto? (s/n): ").strip().lower()
    
    if respuesta == 's':
        if not cambiar_a_escritorio_remoto():
            print("⚠️  Continuando sin cambio automático de ventana")
    
    # Preguntar confirmación para continuar
    print("\n⏳ PREPARACIÓN FINAL:")
    print("• El sistema cambiará a SAP Business One")
    print("• Navegará al módulo de producción")
    print("• Creará una orden de fabricación")
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
        # Procesar orden de producción
        success = handler.process_production_order(datos_prueba)
        
        if success:
            print("\n✅ PRUEBA EXITOSA")
            print("=" * 40)
            print("• Orden de producción procesada correctamente")
            print("• Datos cargados en SAP Business One")
            print("• Formulario de producción completado")
            print("• Screenshots generados")
            print("• Logs actualizados")
            
            # Verificar formulario final
            print("\n🔍 Verificando resultado final...")
            if verificar_formulario_produccion(vision):
                print("✅ Formulario de producción confirmado")
            else:
                print("⚠️  No se pudo confirmar el formulario final")
            
        else:
            print("\n❌ PRUEBA FALLIDA")
            print("=" * 40)
            print("• Error en el procesamiento")
            print("• Revisa los logs para más detalles")
            print("• Verifica la conexión con SAP")
            print("• Asegúrate de que el módulo de producción esté disponible")
            
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {str(e)}")
        print("=" * 40)
        print("• Error inesperado durante la prueba")
        print("• Revisa la configuración del sistema")
        print("• Verifica las dependencias")
        print("• Comprueba que las imágenes de referencia existan")
    
    print("\n🏁 PRUEBA COMPLETADA")
    print("=" * 60)
    print("📁 Revisa la carpeta 'screenshots' para ver las capturas")
    print("📝 Revisa los logs para información detallada")
    print("🔄 Puedes ejecutar la prueba nuevamente si es necesario")
    print("💡 Si la prueba falló, verifica:")
    print("   - Conexión al escritorio remoto")
    print("   - Acceso al módulo de producción en SAP")
    print("   - Imágenes de referencia en la carpeta correspondiente")


if __name__ == "__main__":
    main()
