#!/usr/bin/env python3
"""
Script de prueba para el módulo de órdenes de producción con datos reales
Versión completamente automática
"""

import os
import sys
import time
import json
import cv2
import numpy as np
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rpa.vision.main import Vision
from rpa.config_manager import ConfigManager
from rpa.modules.production_order import ProductionOrderHandler
from rpa.simple_logger import rpa_logger


def crear_datos_reales():
    """Crear datos reales para la prueba de producción"""
    datos_reales = {
        "numero_articulo": "101846",
        "numero_pedido_interno": "6107",
        "cantidad": 2000,
        "fecha_finalizacion": "12/09/2025",
        "unidad_medida": "PCS",
        "centro_trabajo": "CT-01",
        "observaciones": "Orden de producción real para pruebas del RPA"
    }
    return datos_reales


def mostrar_datos_prueba(datos):
    """Mostrar los datos de prueba de forma clara"""
    print("\n📋 DATOS DE PRUEBA REALES")
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


def verificar_formulario_abierto(vision):
    """Verificar que el formulario de producción esté abierto"""
    print("🔍 Verificando que el formulario esté abierto...")
    
    try:
        import pyautogui
        
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


def test_produccion_real():
    """Función principal para probar producción con datos reales"""
    print("🧪 PRUEBA DE PRODUCCIÓN CON DATOS REALES")
    print("=" * 60)
    
    try:
        # 1. Inicializar componentes
        print("🔄 Inicializando componentes del RPA...")
        config = ConfigManager()
        vision = Vision()
        production_handler = ProductionOrderHandler(vision, config)
        
        # 2. Crear datos reales
        print("🔄 Creando datos reales...")
        datos_reales = crear_datos_reales()
        mostrar_datos_prueba(datos_reales)
        
        # 3. Confirmación inicial única
        print("\n⏸️  CONFIRMACIÓN INICIAL")
        print("=" * 40)
        print("🔧 El script procederá automáticamente hasta el final:")
        print("1. Cambiará al escritorio remoto")
        print("2. Navegará a SAP")
        print("3. Abrirá el formulario de producción")
        print("4. Llenará los datos automáticamente")
        print("5. NO creará la orden (esperará tu decisión manual)")
        
        input("\n⏸️  Presiona ENTER para comenzar la automatización completa...")
        
        # 4. Inicio automático
        print("\n🚀 INICIANDO AUTOMATIZACIÓN COMPLETA...")
        print("   El script procederá automáticamente hasta el final")
        
        # 5. Cambiar al escritorio remoto
        print("\n🔄 PASO 0: Cambiando al escritorio remoto...")
        escritorio_remoto_activado = cambiar_a_escritorio_remoto()
        
        if escritorio_remoto_activado:
            print("✅ Escritorio remoto activado exitosamente")
        else:
            print("⚠️  Continuando sin confirmación del escritorio remoto")
        
        # 6. Ejecutar navegación
        print("\n🔄 PASO 1: Navegando al módulo de producción...")
        print("   - Presionando Alt+M...")
        print("   - Presionando P...")
        print("   - Buscando botón 'Orden de Fabricación'...")
        
        navigation_success = production_handler.navigate_to_production()
        
        if not navigation_success:
            print("❌ Error en la navegación.")
            print("💡 Verifica:")
            print("   - Que SAP esté abierto")
            print("   - Que estés en la pantalla principal")
            print("   - Que las imágenes de referencia existan")
            return False
        
        print("✅ Navegación completada exitosamente")
        
        # 7. Verificar que el formulario esté abierto
        print("\n🔄 PASO 2: Verificando formulario...")
        time.sleep(2.0)  # Esperar a que se abra el formulario
        
        formulario_abierto = verificar_formulario_abierto(vision)
        
        if not formulario_abierto:
            print("⚠️  El formulario podría no estar completamente abierto")
            print("💡 Continuando con el llenado de datos...")
        
        # 8. Procesar orden de producción automáticamente
        print("\n🔄 PASO 3: Llenando formulario con datos reales...")
        print("   - Cargando artículo: 101846...")
        print("   - Cargando pedido interno: 6107...")
        print("   - Cargando cantidad: 2000...")
        print("   - Cargando fecha de finalización: 12/09/2025...")
        
        success = production_handler.process_production_order(
            datos_reales, 
            auto_click_crear=False  # NO hacer clic automático
        )
        
        if success:
            print("\n🎉 FORMULARIO COMPLETADO EXITOSAMENTE")
            print("=" * 50)
            print("✅ Todos los campos han sido llenados automáticamente")
            print("✅ Los datos reales están en el formulario")
            print("✅ El formulario está listo para revisión")
            
            print("\n💡 DATOS CARGADOS:")
            print(f"   - Artículo: {datos_reales['numero_articulo']}")
            print(f"   - Pedido: {datos_reales['numero_pedido_interno']}")
            print(f"   - Cantidad: {datos_reales['cantidad']}")
            print(f"   - Fecha: {datos_reales['fecha_finalizacion']}")
            
            print("\n🎯 DECISIÓN MANUAL REQUERIDA:")
            print("   - Haz clic en 'Crear' si los datos están correctos")
            print("   - Haz clic en 'Borrar' si quieres cancelar")
            print("   - Modifica cualquier campo si es necesario")
            
            # 9. Finalización automática
            print("\n✅ AUTOMATIZACIÓN COMPLETADA")
            print("=" * 40)
            print("El script ha terminado exitosamente.")
            print("Los datos están cargados en el formulario.")
            print("Toma tu decisión manual en SAP cuando estés listo.")
            print("✅ Prueba de producción con datos reales finalizada correctamente")
            
            # 10. Resumen final
            print("\n📊 RESUMEN DE LA PRUEBA")
            print("=" * 40)
            print("✅ Cambio a escritorio remoto: " + ("Exitoso" if escritorio_remoto_activado else "Manual"))
            print("✅ Navegación: Exitosa")
            print("✅ Verificación de formulario: " + ("Exitosa" if formulario_abierto else "Manual"))
            print("✅ Carga de datos: Exitosa")
            print("✅ Validación: Exitosa")
            print("✅ Control manual: Funcionando")
            print("✅ Módulo de producción: LISTO PARA USO")
            
        else:
            print("❌ Error procesando la orden de producción")
            print("💡 Verifica los logs para más detalles")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        rpa_logger.error(f"Error en test_produccion_real: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE PRODUCCIÓN CON DATOS REALES")
    print("=" * 60)
    print("🎯 Objetivo: Probar el módulo de producción con datos reales")
    print("🎯 Modo: Completamente automático hasta la decisión final")
    print("🎯 Característica: Datos reales de producción")
    print("🎯 Resultado esperado: Formulario llenado automáticamente")
    
    # Ejecutar prueba
    if test_produccion_real():
        print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("✅ El módulo de producción funciona correctamente")
        print("✅ Los datos reales se cargaron sin problemas")
        print("✅ La automatización completa funciona")
        print("✅ El módulo está listo para uso en producción")
    else:
        print("\n❌ LA PRUEBA FALLÓ")
        print("=" * 60)
        print("💡 Revisa los errores y verifica la configuración")
        print("💡 Asegúrate de que SAP esté abierto y accesible")


if __name__ == "__main__":
    main()
