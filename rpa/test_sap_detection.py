#!/usr/bin/env python3
"""
Script de prueba para la detección de SAP Business One usando OCR
"""

import time
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpa.vision.main import Vision
from rpa.logger import rpa_logger

def test_sap_text_detection():
    """Prueba la detección de SAP Business One por texto"""
    print("🧪 Iniciando prueba de detección de SAP Business One por texto")
    print("=" * 60)
    
    try:
        vision = Vision()
        
        # Probar método de texto
        print("📝 Probando detección por texto OCR...")
        text_coordinates = vision.get_sap_text_coordinates()
        
        if text_coordinates:
            print(f"✅ SAP Business One encontrado por texto en: {text_coordinates}")
            return True
        else:
            print("❌ No se encontró SAP Business One por texto")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de texto: {str(e)}")
        return False

def test_sap_robust_detection():
    """Prueba la detección robusta de SAP Business One"""
    print("\n🔄 Iniciando prueba de detección robusta de SAP Business One")
    print("=" * 60)
    
    try:
        vision = Vision()
        
        # Probar método robusto
        print("🔍 Probando detección robusta (OCR + Template Matching)...")
        robust_coordinates = vision.get_sap_coordinates_robust()
        
        if robust_coordinates:
            print(f"✅ SAP Business One encontrado por método robusto en: {robust_coordinates}")
            return True
        else:
            print("❌ No se encontró SAP Business One con ningún método")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba robusta: {str(e)}")
        return False

def test_sap_image_detection():
    """Prueba la detección de SAP Business One por imagen (método original)"""
    print("\n🖼️ Iniciando prueba de detección de SAP Business One por imagen")
    print("=" * 60)
    
    try:
        vision = Vision()
        
        # Probar método de imagen
        print("🖼️ Probando detección por template matching...")
        image_coordinates = vision.get_sap_coordinates()
        
        if image_coordinates:
            print(f"✅ SAP Business One encontrado por imagen en: {image_coordinates}")
            return True
        else:
            print("❌ No se encontró SAP Business One por imagen")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de imagen: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de detección de SAP Business One")
    print("=" * 60)
    
    results = {
        "text_detection": False,
        "image_detection": False,
        "robust_detection": False
    }
    
    try:
        # Prueba de detección por texto
        results["text_detection"] = test_sap_text_detection()
        
        # Prueba de detección por imagen
        results["image_detection"] = test_sap_image_detection()
        
        # Prueba de detección robusta
        results["robust_detection"] = test_sap_robust_detection()
        
        # Resumen de resultados
        print("\n📊 RESUMEN DE PRUEBAS")
        print("=" * 60)
        print(f"✅ Detección por texto: {'EXITOSA' if results['text_detection'] else 'FALLIDA'}")
        print(f"✅ Detección por imagen: {'EXITOSA' if results['image_detection'] else 'FALLIDA'}")
        print(f"✅ Detección robusta: {'EXITOSA' if results['robust_detection'] else 'FALLIDA'}")
        
        # Recomendación
        if results["robust_detection"]:
            print("\n🎉 El sistema robusto funciona correctamente")
            print("💡 Se recomienda usar get_sap_coordinates_robust() en producción")
        elif results["text_detection"]:
            print("\n⚠️ Solo funciona la detección por texto")
            print("💡 Se recomienda usar get_sap_text_coordinates() en producción")
        elif results["image_detection"]:
            print("\n⚠️ Solo funciona la detección por imagen")
            print("💡 Se recomienda usar get_sap_coordinates() en producción")
        else:
            print("\n❌ Ningún método funciona")
            print("💡 Revisar configuración y dependencias")
        
    except Exception as e:
        print(f"❌ Error general en pruebas: {str(e)}")
        rpa_logger.log_error(f"Error en pruebas de detección SAP: {str(e)}", "Función main")

if __name__ == "__main__":
    main() 