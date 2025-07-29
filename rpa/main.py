import pyautogui
import time
import os
import json
from rpa.vision.main import Vision
from json_parser.main import JsonParser
from rpa.logger import rpa_logger

vision = Vision()
json_parser = JsonParser()

class RPA:
    def __init__(self):
        self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"

    def print_position(self):
        while True:
            print(pyautogui.position())

    def load_nit(self, nit):
        start_time = time.time()
        rpa_logger.log_action("Iniciando carga de NIT", f"NIT: {nit}")
        
        try:
            time.sleep(1)
            self.get_remote_desktop()
            time.sleep(1)
            pyautogui.screenshot("./rpa/vision/reference_images/template.png")
            vision.save_template()
            coordinates = vision.get_client_coordinates()
            time.sleep(1)
            pyautogui.moveTo(coordinates, duration=0.5)
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.typewrite(nit, interval=0.2)
            time.sleep(1)
            pyautogui.hotkey('enter')
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de NIT", duration)
            rpa_logger.log_action("NIT cargado exitosamente", f"NIT: {nit}")
            
        except Exception as e:
            rpa_logger.log_error(f"Error al cargar NIT: {str(e)}", f"NIT: {nit}")
            raise

    def load_orden_compra(self, orden_compra):
        start_time = time.time()
        rpa_logger.log_action("Iniciando carga de orden de compra", f"Orden: {orden_compra}")
        
        try:
            time.sleep(1)
            coordinates = vision.get_orden_coordinates()
            pyautogui.moveTo(coordinates, duration=0.5)
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.typewrite(orden_compra, interval=0.2)
            time.sleep(1)
            pyautogui.hotkey('tab')
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de orden de compra", duration)
            rpa_logger.log_action("Orden de compra cargada exitosamente", f"Orden: {orden_compra}")
            
        except Exception as e:
            rpa_logger.log_error(f"Error al cargar orden de compra: {str(e)}", f"Orden: {orden_compra}")
            raise

    def load_fecha_entrega(self, fecha_entrega):
        start_time = time.time()
        rpa_logger.log_action("Iniciando carga de fecha de entrega", f"Fecha: {fecha_entrega}")
        
        try:
            time.sleep(1)
            coordinates = vision.get_fecha_coordinates()
            pyautogui.moveTo(coordinates, duration=0.5)
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.typewrite(fecha_entrega, interval=0.2)
            time.sleep(1)
            pyautogui.hotkey('tab')
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de fecha de entrega", duration)
            rpa_logger.log_action("Fecha de entrega cargada exitosamente", f"Fecha: {fecha_entrega}")
            
        except Exception as e:
            rpa_logger.log_error(f"Error al cargar fecha de entrega: {str(e)}", f"Fecha: {fecha_entrega}")
            raise

    def load_items(self, items):
        start_time = time.time()
        rpa_logger.log_action("Iniciando carga de items", f"Total items: {len(items)}")
        
        try:
            coordinates, row_height = vision.get_primer_articulo_coordinates()
            x = coordinates[0]
            y = coordinates[1]
            pyautogui.moveTo(x, y, duration=0.5)
            
            for i, item in enumerate(items, 1):
                item_start_time = time.time()
                rpa_logger.log_action(f"Procesando item {i}/{len(items)}", f"Código: {item['codigo']}")
                
                try:
                    y += row_height
                    pyautogui.click()
                    time.sleep(3)
                    pyautogui.typewrite(item['codigo'], interval=0.2)
                    time.sleep(3)
                    pyautogui.hotkey('tab', "tab", interval=0.2)
                    time.sleep(3)
                    pyautogui.typewrite(str(item['fecha_entrega']), interval=0.2)
                    time.sleep(3)
                    pyautogui.hotkey('tab')
                    time.sleep(3)
                    pyautogui.typewrite(str(item['cantidad']), interval=0.2)
                    time.sleep(3)
                    pyautogui.hotkey('tab')
                    time.sleep(3)
                    # pyautogui.typewrite(str(item['precio_unitario']), interval=0.2)
                    pyautogui.hotkey('tab')
                    time.sleep(3)
                    pyautogui.hotkey('tab')
                    time.sleep(3)
                    pyautogui.moveTo(x, y, duration=0.5)
                    
                    item_duration = time.time() - item_start_time
                    rpa_logger.log_performance(f"Item {i} procesado", item_duration)
                    rpa_logger.log_action(f"Item {i} cargado exitosamente", 
                                        f"Código: {item['codigo']}, Cantidad: {item['cantidad']}, Fecha: {item['fecha_entrega']}")
                    
                except Exception as e:
                    rpa_logger.log_error(f"Error al procesar item {i}: {str(e)}", 
                                       f"Código: {item['codigo']}")
                    raise
            
            total_duration = time.time() - start_time
            rpa_logger.log_performance("Carga completa de items", total_duration)
            rpa_logger.log_action("Todos los items cargados exitosamente", f"Total procesados: {len(items)}")
            
        except Exception as e:
            rpa_logger.log_error(f"Error en carga de items: {str(e)}", f"Total items: {len(items)}")
            raise

    def take_order_inserted_screenshot(self, filename):
        if not os.path.exists('./rpa/vision/reference_images/inserted_orders'):
            os.makedirs('./rpa/vision/reference_images/inserted_orders')
        saved_filename = f'./rpa/vision/reference_images/inserted_orders/{filename}'
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save(saved_filename)
        rpa_logger.info(f'Screenshot taken and saved in {saved_filename}')

    def data_loader(self, data):
        nit = data["comprador"]['nit']
        orden_compra = data['orden_compra']
        fecha_entrega = data['fecha_entrega']
        items = data['items']

        self.load_nit(nit)
        self.load_orden_compra(orden_compra)
        self.load_fecha_entrega(fecha_entrega)
        self.load_items(items)
        self.take_order_inserted_screenshot(f"{data['orden_compra']}.png")
        rpa_logger.info('loaded data successfully with RPA. Waiting for next run')

    def cancel_order(self):
        self.get_remote_desktop()
        coordinates = vision.get_cancel_order_coordinates()
        pyautogui.moveTo(coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        rpa_logger.info('Order cancelled.')

    def open_sap(self):
        try:
            self.get_remote_desktop()
            time.sleep(2)  # Aumentamos el tiempo de espera inicial
            print('opening sap')
            coordinates = vision.get_sap_coordinates()
            print(coordinates)
            if not coordinates:
                rpa_logger.error('No se pudieron obtener las coordenadas de SAP')
                return False
                
            # Verificamos que las coordenadas sean válidas
            if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                rpa_logger.error(f'Coordenadas inválidas de SAP: {coordinates}')
                return False
                
            pyautogui.moveTo(coordinates, duration=0.5)
            time.sleep(2)  # Aumentamos el tiempo de espera antes del doble clic
            pyautogui.doubleClick()
            time.sleep(10)  # Aumentamos el tiempo de espera después del doble clic
            
            # Verificamos si SAP está respondiendo
            try:
                pyautogui.hotkey('enter')
                time.sleep(30)
                # Verificamos si podemos tomar una captura de pantalla
                screenshot = pyautogui.screenshot("./rpa/vision/reference_images/sap_desktop.png")
                if screenshot:
                    rpa_logger.info('SAP opened successfully.')
                    return True
                else:
                    rpa_logger.error('No se pudo tomar captura de pantalla de SAP')
                    return False
            except Exception as e:
                rpa_logger.error(f'Error al interactuar con SAP: {str(e)}')
                return False
                
        except Exception as e:
            rpa_logger.error(f'Error opening SAP: {str(e)}')
            return False

    def close_sap(self):
        self.get_remote_desktop()
        archivo_menu_coordinates = vision.get_archivos_menu_coordinates()
        if archivo_menu_coordinates is None:
            rpa_logger.info('SAP already closed. Waiting for next run')
            return
        pyautogui.moveTo(archivo_menu_coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
        pyautogui.screenshot("./rpa/vision/reference_images/sap_archivo_menu.png")
        time.sleep(1)
        finalizar_button_coordinates = vision.get_finalizar_button_coordinates()
        pyautogui.moveTo(finalizar_button_coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(15)
        rpa_logger.info('SAP closed.')

    def open_sap_orden_de_ventas(self):
        start_time = time.time()
        rpa_logger.log_action("Iniciando apertura de SAP orden de ventas", "Navegación a módulo de ventas")
        
        try:
            modulos_menu_coordinates = vision.get_modulos_menu_coordinates()
            pyautogui.moveTo(modulos_menu_coordinates, duration=0.5)
            rpa_logger.debug(f"Coordenadas del menú módulos: {modulos_menu_coordinates}")
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.screenshot("./rpa/vision/reference_images/sap_modulos_menu.png")
            
            ventas_menu_coordinates = vision.get_ventas_menu_coordinates()
            rpa_logger.debug(f"Coordenadas del menú ventas: {ventas_menu_coordinates}")
            pyautogui.moveTo(ventas_menu_coordinates, duration=0.5)
            time.sleep(1)
            # pyautogui.click()
            time.sleep(5)
            pyautogui.screenshot("./rpa/vision/reference_images/sap_ventas_order_menu.png")
            
            orden_de_ventas_menu_coordinates = vision.get_orden_de_ventas_menu_coordinates()
            if orden_de_ventas_menu_coordinates is None:
                rpa_logger.log_error('No se pudo abrir SAP orden de ventas', 'Coordenadas no encontradas')
                return
            pyautogui.moveTo(orden_de_ventas_menu_coordinates, duration=0.1)
            time.sleep(1)
            pyautogui.click()
            time.sleep(5)
            pyautogui.screenshot("./rpa/vision/reference_images/sap_orden_de_ventas_template.png")
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Apertura de SAP orden de ventas", duration)
            rpa_logger.log_action("SAP orden de ventas abierto exitosamente", "Módulo de ventas activo")
            
        except Exception as e:
            rpa_logger.log_error(f"Error al abrir SAP orden de ventas: {str(e)}", "Error en navegación")
            raise

    def get_remote_desktop(self):
        max_retries = 3
        retry_delay = 5
        
        rpa_logger.log_action("Iniciando conexión al escritorio remoto", f"Máximo {max_retries} intentos")
        
        for attempt in range(max_retries):
            try:
                windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
                if not windows:
                    rpa_logger.warning(f'Ventana de escritorio remoto no encontrada (intento {attempt + 1}/{max_retries})')
                    if attempt < max_retries - 1:
                        self.open_remote_desktop()
                        time.sleep(retry_delay)
                        continue
                    else:
                        rpa_logger.log_error('No se pudo encontrar la ventana de escritorio remoto después de varios intentos', 'Ventana no encontrada')
                        return None
                
                window = windows[0]
                if not window.isActive:
                    window.activate()
                    time.sleep(2)  # Esperamos a que la ventana se active
                
                # Verificamos que la ventana esté realmente activa
                if window.isActive:
                    screenshot = pyautogui.screenshot("./rpa/vision/reference_images/remote_desktop.png")
                    if screenshot:
                        rpa_logger.log_action("Conexión al escritorio remoto establecida correctamente", "Ventana activa y captura exitosa")
                        return window
                    else:
                        rpa_logger.log_error('No se pudo tomar captura de pantalla del escritorio remoto', 'Error en captura')
                else:
                    rpa_logger.log_error('No se pudo activar la ventana del escritorio remoto', 'Ventana inactiva')
                
            except Exception as e:
                rpa_logger.log_error(f'Error al conectar con el escritorio remoto (intento {attempt + 1}/{max_retries}): {str(e)}', f"Intento {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    rpa_logger.log_error('No se pudo establecer conexión con el escritorio remoto después de varios intentos', 'Todos los intentos fallaron')
                    return None
        
        return None

    def open_remote_desktop(self):
        rpa_logger.log_action("Abriendo aplicación de escritorio remoto", "Búsqueda en menú de Windows")
        pyautogui.hotkey('win')
        time.sleep(1)
        pyautogui.typewrite('remote', interval=0.2)
        time.sleep(1)
        pyautogui.hotkey('enter', "enter", interval=1)
        time.sleep(10)
        rpa_logger.log_action("Aplicación de escritorio remoto abierta", "Lista para conexión")

    def run(self):
        start_time = time.time()
        rpa_logger.log_action("Iniciando proceso RPA", "Procesamiento de archivos JSON")
        
        directory = './data/outputs_json'
        try:
            files = [f for f in os.listdir(directory) if not f.startswith('.') and not f.endswith('.tmp')]
            if len(files) == 0:
                rpa_logger.info('No hay archivos para procesar. Esperando próxima ejecución')
                return
            
            rpa_logger.log_action(f"Archivos encontrados para procesar", f"Total: {len(files)} archivos")
            
            for i, file in enumerate(files, 1):
                file_start_time = time.time()
                rpa_logger.log_action(f"Procesando archivo {i}/{len(files)}", f"Archivo: {file}")
                
                try:
                    with open(f'{directory}/{file}') as f:
                        data = json.load(f)
                    
                    rpa_logger.log_action("Archivo JSON cargado exitosamente", f"Archivo: {file}")
                    
                    self.open_sap_orden_de_ventas()
                    self.data_loader(data)
                    time.sleep(1)
                    # self.cancel_order()
                    time.sleep(1)
                    # json_parser.move_json_to_processed(file)
                    
                    file_duration = time.time() - file_start_time
                    rpa_logger.log_performance(f"Archivo {file} procesado", file_duration)
                    rpa_logger.log_action(f"Archivo {file} procesado exitosamente", f"Archivo: {file}")
                    
                except json.JSONDecodeError as e:
                    rpa_logger.log_error(f'Error decodificando archivo JSON {file}: {str(e)}', f"Archivo: {file}")
                    continue
                except Exception as e:
                    rpa_logger.log_error(f'Error procesando archivo {file}: {str(e)}', f"Archivo: {file}")
                    continue
            
            total_duration = time.time() - start_time
            rpa_logger.log_performance("Proceso RPA completado", total_duration)
            rpa_logger.log_action("RPA finalizado exitosamente", f"Archivos procesados: {len(files)}")
            
        except Exception as e:
            rpa_logger.log_error(f'Error accediendo al directorio {directory}: {str(e)}', f"Directorio: {directory}")
            return

if __name__ == "__main__":
    rpa = RPA()
    rpa.close_sap()