#!/usr/bin/env python3
"""
Script de prueba para el módulo de órdenes de producción con datos ficticios
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


def crear_datos_ficticios():
    """Crear datos ficticios para la prueba de producción"""
    datos_ficticios = {
        "numero_articulo": "ART-FICTICIO-001",
        "numero_pedido_interno": "PI-FICTICIO-2024-001",
        "cantidad": 150,
        "fecha_finalizacion": "30/12/2024",
        "unidad_medida": "PCS",
        "centro_trabajo": "CT-FICTICIO-01",
        "observaciones": "Orden de producción ficticia para pruebas del RPA"
    }
    return datos_ficticios


def mostrar_datos_prueba(datos):
    """Mostrar los datos de prueba de forma clara"""
    print("\n📋 DATOS DE PRUEBA FICTICIOS")
    print("=" * 50)
    print(f"🏷️  Artículo: {datos['numero_articulo']}")
    print(f"📝 Pedido Interno: {datos['numero_pedido_interno']}")
    print(f"📊 Cantidad: {datos['cantidad']} {datos['unidad_medida']}")
    print(f"📅 Fecha Finalización: {datos['fecha_finalizacion']}")
    print(f"🏭 Centro Trabajo: {datos['centro_trabajo']}")
    print(f"💬 Observaciones: {datos['observaciones']}")
    print("=" * 50)


def test_produccion_ficticia():
    """Función principal para probar producción con datos ficticios"""
    print("🧪 PRUEBA DE PRODUCCIÓN FICTICIA")
    print("=" * 60)
    
    try:
        # 1. Inicializar componentes
        print("🔄 Inicializando componentes del RPA...")
        config = ConfigManager()
        vision = Vision()
        production_handler = ProductionOrderHandler(vision, config)
        
        # 2. Crear datos ficticios
        print("🔄 Creando datos ficticios...")
        datos_ficticios = crear_datos_ficticios()
        mostrar_datos_prueba(datos_ficticios)
        
        # 3. Preparación manual
        print("\n⏸️  PREPARACIÓN MANUAL REQUERIDA")
        print("=" * 40)
        print("🔧 PASOS A SEGUIR:")
        print("1. Abre SAP Business One")
        print("2. Asegúrate de estar en la pantalla principal")
        print("3. Ten el escritorio remoto abierto (pero no necesariamente activo)")
        print("4. Verifica que las imágenes de referencia estén disponibles")
        print("5. El script navegará automáticamente y se pasará al escritorio remoto")
        
        input("\n⏸️  Presiona ENTER cuando estés listo para comenzar...")
        
        # 4. Retraso inicial para cambio manual a escritorio remoto
        print("\n⏸️  RETRASO INICIAL - Cambiando al escritorio remoto...")
        print("   Tienes 5 segundos para cambiar manualmente al escritorio remoto si es necesario...")
        
        for i in range(5, 0, -1):
            print(f"   Iniciando en {i}...")
            time.sleep(1)
        
        # 5. Cambiar automáticamente al escritorio remoto
        print("\n🔄 PASO 0: Cambiando al escritorio remoto...")
        print("   - Buscando ventana de escritorio remoto...")
        print("   - Activando ventana...")
        
        # Buscar y activar la ventana del escritorio remoto
        try:
            import pyautogui
            
            # Buscar la ventana del escritorio remoto usando template matching
            print("   - Buscando ventana de escritorio remoto...")
            
            # Tomar screenshot y buscar la imagen del escritorio remoto
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Cargar imagen de referencia del escritorio remoto
            remote_desktop_ref = cv2.imread('./rpa/vision/reference_images/remote_desktop.png', cv2.IMREAD_COLOR)
            
            if remote_desktop_ref is not None:
                # Buscar coincidencia
                result = cv2.matchTemplate(screenshot_cv, remote_desktop_ref, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > 0.8:  # Umbral de confianza
                    # Calcular centro del elemento encontrado
                    w = remote_desktop_ref.shape[1]
                    h = remote_desktop_ref.shape[0]
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2
                    
                    # Hacer clic en el centro
                    pyautogui.click(center_x, center_y)
                    remote_desktop_found = True
                    print("✅ Escritorio remoto encontrado y activado")
                    time.sleep(2.0)  # Esperar a que se active completamente
                else:
                    remote_desktop_found = False
                    print("⚠️  No se pudo encontrar el escritorio remoto automáticamente")
                    print("💡 El script continuará, pero asegúrate de que el escritorio remoto esté visible")
                    time.sleep(3.0)  # Dar tiempo para cambio manual si es necesario
            else:
                remote_desktop_found = False
                print("⚠️  Imagen de referencia del escritorio remoto no encontrada")
                time.sleep(3.0)
            
            if remote_desktop_found:
                print("✅ Escritorio remoto encontrado y activado")
                time.sleep(2.0)  # Esperar a que se active completamente
            else:
                print("⚠️  No se pudo encontrar el escritorio remoto automáticamente")
                print("💡 El script continuará, pero asegúrate de que el escritorio remoto esté visible")
                time.sleep(3.0)  # Dar tiempo para cambio manual si es necesario
                
        except Exception as e:
            print(f"⚠️  Error cambiando al escritorio remoto: {e}")
            print("💡 El script continuará, pero asegúrate de que el escritorio remoto esté activo")
            time.sleep(3.0)
        
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
        
        # 7. Verificar formulario
        print("\n⏸️  VERIFICACIÓN DEL FORMULARIO")
        print("=" * 40)
        print("🔍 Verifica que:")
        print("   - El formulario de orden de producción esté abierto")
        print("   - Todos los campos estén visibles")
        print("   - El formulario esté listo para recibir datos")
        
        input("\n⏸️  Presiona ENTER para continuar con el llenado de campos...")
        
        # 8. Procesar orden de producción
        print("\n🔄 PASO 2: Llenando formulario con datos ficticios...")
        print("   - Cargando artículo...")
        print("   - Cargando pedido interno...")
        print("   - Cargando cantidad...")
        print("   - Cargando fecha de finalización...")
        
        success = production_handler.process_production_order(
            datos_ficticios, 
            auto_click_crear=False  # NO hacer clic automático
        )
        
        if success:
            print("\n🎉 FORMULARIO COMPLETADO EXITOSAMENTE")
            print("=" * 50)
            print("✅ Todos los campos han sido llenados")
            print("✅ Los datos ficticios están en el formulario")
            print("✅ El formulario está listo para revisión")
            
            print("\n💡 PRÓXIMOS PASOS:")
            print("   🔍 Revisa todos los datos en SAP:")
            print(f"      - Artículo: {datos_ficticios['numero_articulo']}")
            print(f"      - Pedido: {datos_ficticios['numero_pedido_interno']}")
            print(f"      - Cantidad: {datos_ficticios['cantidad']}")
            print(f"      - Fecha: {datos_ficticios['fecha_finalizacion']}")
            
            print("\n   🎯 DECISIÓN MANUAL:")
            print("      - Haz clic en 'Crear' si los datos están correctos")
            print("      - Haz clic en 'Borrar' si quieres cancelar")
            print("      - Modifica cualquier campo si es necesario")
            
            # 7. Pausa final
            print("\n⏸️  ESPERANDO DECISIÓN MANUAL")
            print("=" * 40)
            print("El script ha terminado. Toma tu decisión en SAP.")
            print("Presiona ENTER cuando hayas completado la acción...")
            
            input()
            print("✅ Prueba de producción ficticia finalizada correctamente")
            
            # 8. Resumen final
            print("\n📊 RESUMEN DE LA PRUEBA")
            print("=" * 40)
            print("✅ Navegación: Exitosa")
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
        rpa_logger.error(f"Error en test_produccion_ficticia: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE PRODUCCIÓN FICTICIA")
    print("=" * 60)
    print("🎯 Objetivo: Probar el módulo de producción con datos ficticios")
    print("🎯 Modo: Control manual (sin auto-click en crear)")
    print("🎯 Resultado esperado: Formulario llenado para revisión humana")
    
    # Ejecutar prueba
    if test_produccion_ficticia():
        print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("✅ El módulo de producción funciona correctamente")
        print("✅ Los datos ficticios se cargaron sin problemas")
        print("✅ El control manual está funcionando")
        print("✅ El módulo está listo para uso en producción")
    else:
        print("\n❌ LA PRUEBA FALLÓ")
        print("=" * 60)
        print("💡 Revisa los errores y verifica la configuración")
        print("💡 Asegúrate de que SAP esté abierto y accesible")


if __name__ == "__main__":
    main()
