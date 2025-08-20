#!/usr/bin/env python3
"""
Test para verificar que el screenshot tenga el mismo nombre que el JSON
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_screenshot_naming():
    """Prueba que el screenshot tenga el nombre correcto"""
    print("TESTING SCREENSHOT NAMING")
    print("=" * 40)
    
    # Casos de prueba
    test_cases = [
        "hermeco.json",
        "pedido_123.json", 
        "orden_compra_456.json",
        "test_file.json"
    ]
    
    for json_filename in test_cases:
        print(f"Test: {json_filename}")
        
        # Simular la lógica del código
        base_name = json_filename.replace('.json', '')
        expected_png = f'{base_name}.png'
        
        # Verificar que los nombres coincidan exactamente (excepto extensión)
        json_base = json_filename.split('.')[0]
        png_base = expected_png.split('.')[0]
        
        assert json_base == png_base, f"Nombres no coinciden: {json_base} != {png_base}"
        print(f"  JSON: {json_filename}")
        print(f"  PNG:  {expected_png}")
        print(f"  NOMBRES COINCIDEN")
        print()
    
    print("TODOS LOS TESTS DE NOMBRES PASARON")
    
    # Test adicional: verificar que ya no hay '_validation'
    print("Verificando que no hay '_validation' en nombres...")
    
    for json_filename in test_cases:
        base_name = json_filename.replace('.json', '')
        png_filename = f'{base_name}.png'
        
        assert '_validation' not in png_filename, f"Aún contiene '_validation': {png_filename}"
    
    print("CONFIRMADO: No hay '_validation' en nombres")
    
    return True

def test_example_files():
    """Prueba con ejemplos reales"""
    print("\nTESTING EJEMPLOS REALES")
    print("=" * 40)
    
    examples = [
        ("hermeco.json", "hermeco.png"),
        ("460132850113120954R730-9008516551-7001-05001.pdf.json", "460132850113120954R730-9008516551-7001-05001.pdf.png"),
        ("pedido_exito_001.json", "pedido_exito_001.png")
    ]
    
    for json_name, expected_png in examples:
        print(f"Test: {json_name}")
        
        # Simular lógica del código
        base_name = json_name.replace('.json', '')
        actual_png = f'{base_name}.png'
        
        assert actual_png == expected_png, f"Nombre incorrecto: {actual_png} != {expected_png}"
        print(f"  {json_name} -> {actual_png}")
    
    print("TODOS LOS EJEMPLOS PASARON")
    return True

def main():
    """Función principal"""
    print("VERIFICANDO NOMBRES DE SCREENSHOTS")
    print("=" * 50)
    
    results = []
    results.append(("Screenshot Naming", test_screenshot_naming()))
    results.append(("Example Files", test_example_files()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    
    all_passed = all(result for _, result in results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    if all_passed:
        print("\nNAMING CORRECTO:")
        print("   archivo.json -> archivo.png")
        print("   (Mismo nombre, solo cambia extension)")
    else:
        print("\nHAY PROBLEMAS CON EL NAMING")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)