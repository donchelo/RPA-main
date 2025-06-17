import pyautogui
import time
import os
import json
from rpa.vision.main import Vision
from json_parser.main import JsonParser
import logging

vision = Vision()
json_parser = JsonParser()

# Create logger 
logger = logging.getLogger(__name__)
handler = logging.FileHandler('rpa.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class RPA:
    def __init__(self):
        self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"

    def print_position(self):
        while True:
            print(pyautogui.position())

    def load_nit(self, nit):
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
        logger.info(f'loaded nit {nit} for sales order with RPA')

    def load_orden_compra(self, orden_compra):
        time.sleep(1)
        coordinates = vision.get_orden_coordinates()
        pyautogui.moveTo(coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.typewrite(orden_compra, interval=0.2)
        time.sleep(1)
        pyautogui.hotkey('tab')
        logger.info(f'loaded orden_compra {orden_compra} for sales order with RPA')

    def load_fecha_entrega(self, fecha_entrega):
        time.sleep(1)
        coordinates = vision.get_fecha_coordinates()
        pyautogui.moveTo(coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.typewrite(fecha_entrega, interval=0.2)
        time.sleep(1)
        pyautogui.hotkey('tab')
        logger.info(f'loaded fecha_entrega {fecha_entrega} for sales order with RPA')

    def load_items(self, items):
        coordinates, row_height = vision.get_primer_articulo_coordinates()
        x = coordinates[0]
        y = coordinates[1]
        pyautogui.moveTo(x, y, duration=0.5)
        for item in items:
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
            pyautogui.typewrite(str(item['precio_unitario']), interval=0.2)
            time.sleep(3)
            pyautogui.hotkey('tab')
            time.sleep(3)
            pyautogui.moveTo(x, y, duration=0.5)
            logger.info(f'loaded item {item["codigo"]}, {item["cantidad"]}, {item["fecha_entrega"]}, {item["precio_unitario"]} for sales order with RPA')

    def data_loader(self, data):
        nit = data["comprador"]['nit']
        orden_compra = data['orden_compra']
        fecha_entrega = data['fecha_entrega']
        items = data['items']

        self.load_nit(nit)
        self.load_orden_compra(orden_compra)
        self.load_fecha_entrega(fecha_entrega)
        self.load_items(items)
        logger.info('loaded data successfully with RPA. Waiting for next run')

    def cancel_order(self):
        self.get_remote_desktop()
        coordinates = vision.get_cancel_order_coordinates()
        pyautogui.moveTo(coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        logger.info('Order cancelled.')

    def open_sap(self):
        try:
            self.get_remote_desktop()
            time.sleep(2)  # Aumentamos el tiempo de espera inicial
            print('opening sap')
            coordinates = vision.get_sap_coordinates()
            print(coordinates)
            if not coordinates:
                logger.error('No se pudieron obtener las coordenadas de SAP')
                return False
                
            # Verificamos que las coordenadas sean válidas
            if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                logger.error(f'Coordenadas inválidas de SAP: {coordinates}')
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
                    logger.info('SAP opened successfully.')
                    return True
                else:
                    logger.error('No se pudo tomar captura de pantalla de SAP')
                    return False
            except Exception as e:
                logger.error(f'Error al interactuar con SAP: {str(e)}')
                return False
                
        except Exception as e:
            logger.error(f'Error opening SAP: {str(e)}')
            return False

    def close_sap(self):
        self.get_remote_desktop()
        archivo_menu_coordinates = vision.get_archivos_menu_coordinates()
        if archivo_menu_coordinates is None:
            logger.info('SAP already closed. Waiting for next run')
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
        logger.info('SAP closed.')

    def open_sap_orden_de_ventas(self):
        modulos_menu_coordinates = vision.get_modulos_menu_coordinates()
        pyautogui.moveTo(modulos_menu_coordinates, duration=0.5)
        print(f"modulos_menu_coordinates: {modulos_menu_coordinates}")
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.screenshot("./rpa/vision/reference_images/sap_modulos_menu.png")
        ventas_menu_coordinates = vision.get_ventas_menu_coordinates()
        print(f"ventas_menu_coordinates: {ventas_menu_coordinates}")
        pyautogui.moveTo(ventas_menu_coordinates, duration=0.5)
        time.sleep(1)
        # pyautogui.click()
        time.sleep(5)
        pyautogui.screenshot("./rpa/vision/reference_images/sap_ventas_order_menu.png")
        orden_de_ventas_menu_coordinates = vision.get_orden_de_ventas_menu_coordinates()
        if orden_de_ventas_menu_coordinates is None:
            print('Could not open SAP orden de ventas. Waiting for next run')
            logger.info('Could not open SAP orden de ventas. Waiting for next run')
            return
        pyautogui.moveTo(orden_de_ventas_menu_coordinates, duration=0.1)
        time.sleep(1)
        pyautogui.click()
        time.sleep(5)
        pyautogui.screenshot("./rpa/vision/reference_images/sap_orden_de_ventas_template.png")
        logger.info('SAP orden de ventas opened.')

    def get_remote_desktop(self):
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
                if not windows:
                    logger.warning(f'Ventana de escritorio remoto no encontrada (intento {attempt + 1}/{max_retries})')
                    if attempt < max_retries - 1:
                        self.open_remote_desktop()
                        time.sleep(retry_delay)
                        continue
                    else:
                        logger.error('No se pudo encontrar la ventana de escritorio remoto después de varios intentos')
                        return None
                
                window = windows[0]
                if not window.isActive:
                    window.activate()
                    time.sleep(2)  # Esperamos a que la ventana se active
                
                # Verificamos que la ventana esté realmente activa
                if window.isActive:
                    screenshot = pyautogui.screenshot("./rpa/vision/reference_images/remote_desktop.png")
                    if screenshot:
                        logger.info('Conexión al escritorio remoto establecida correctamente')
                        return window
                    else:
                        logger.error('No se pudo tomar captura de pantalla del escritorio remoto')
                else:
                    logger.error('No se pudo activar la ventana del escritorio remoto')
                
            except Exception as e:
                logger.error(f'Error al conectar con el escritorio remoto (intento {attempt + 1}/{max_retries}): {str(e)}')
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error('No se pudo establecer conexión con el escritorio remoto después de varios intentos')
                    return None
        
        return None

    def open_remote_desktop(self):
        pyautogui.hotkey('win')
        time.sleep(1)
        pyautogui.typewrite('remote', interval=0.2)
        time.sleep(1)
        pyautogui.hotkey('enter', "enter", interval=1)
        time.sleep(10)
        logger.info('Remote desktop opened.')

    def run(self):
        directory = './data/outputs_json'
        try:
            files = [f for f in os.listdir(directory) if not f.startswith('.') and not f.endswith('.tmp')]
            if len(files) == 0:
                logger.info('No files to process. Waiting for next run')
                return
            for file in files:
                try:
                    with open(f'{directory}/{file}') as f:
                        data = json.load(f)
                    self.open_sap_orden_de_ventas()
                    self.data_loader(data)
                    time.sleep(1)
                    # self.cancel_order()
                    time.sleep(1)
                    # json_parser.move_json_to_processed(file)
                except json.JSONDecodeError as e:
                    logger.error(f'Error decoding JSON file {file}: {str(e)}')
                    continue
                except Exception as e:
                    logger.error(f'Error processing file {file}: {str(e)}')
                    continue
            logger.info('RPA finished. Waiting for next run')
        except Exception as e:
            logger.error(f'Error accessing directory {directory}: {str(e)}')
            return

if __name__ == "__main__":
    rpa = RPA()
    rpa.close_sap()