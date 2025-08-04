import pyautogui
import time
import os
import json
from rpa.vision.main import Vision
from rpa.simple_logger import rpa_logger
from rpa.smart_waits import smart_waits, adaptive_wait, smart_sleep
from rpa.config_manager import get_delay, get_navigation_tabs, get_retry_attempts
from rpa.error_handler import (
    error_handler, with_error_handling, ErrorType, ErrorSeverity,
    handle_template_error, handle_window_error, handle_sap_error
)

vision = Vision()

class RPA:
    def __init__(self):
        self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"

    def print_position(self):
        while True:
            print(pyautogui.position())

    @with_error_handling(ErrorType.DATA_PROCESSING, ErrorSeverity.MEDIUM, operation="load_nit")
    def load_nit(self, nit):
        start_time = time.time()
        rpa_logger.log_action("Iniciando carga de NIT", f"NIT: {nit}")
        
        # Validar NIT
        if not nit or not str(nit).strip():
            raise ValueError(f"NIT inválido: {nit}")
        
        try:
            smart_sleep('short')
            
            # Capturar template actual
            pyautogui.screenshot("./rpa/vision/reference_images/template.png")
            vision.save_template()
            
            # Limpiar campo antes de escribir (por si hay datos previos)
            pyautogui.hotkey('ctrl', 'a')
            smart_sleep('very_short')
            
            # Ingresar NIT con validación
            nit_str = str(nit).strip()
            pyautogui.typewrite(nit_str, interval=0.2)
            smart_sleep('after_input')
            smart_sleep('after_nit')  # Tiempo adicional para procesamiento
            
            # Confirmar entrada
            pyautogui.hotkey('enter')
            smart_sleep('after_input')
            
            # Navegar con tabs configurables
            tabs_count = get_navigation_tabs('after_nit')
            smart_waits.smart_tab_wait(tabs_count, "after_nit")
            for i in range(tabs_count):
                pyautogui.hotkey('tab')
                smart_sleep('after_tab')
            
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
            smart_sleep('short')
            # CORRECCIÓN: Solo usar tabs, no mover mouse ni hacer clic
            pyautogui.typewrite(orden_compra, interval=0.2)
            smart_sleep('after_input')
            # Navegar con tabs configurables después de la orden de compra
            tabs_count = get_navigation_tabs('after_order')
            smart_waits.smart_tab_wait(tabs_count, "orden_compra")
            for i in range(tabs_count):
                pyautogui.hotkey('tab')
                smart_sleep('after_tab')
            
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
            smart_sleep('short')
            # Ya estamos posicionados en el campo después de los tabs desde orden de compra
            pyautogui.typewrite(fecha_entrega, interval=0.2)
            smart_sleep('after_input')
            # CORRECCIÓN: Usar tabs configurables después de la fecha de entrega
            tabs_count = get_navigation_tabs('after_date')
            smart_waits.smart_tab_wait(tabs_count, "fecha_entrega")
            for i in range(tabs_count):
                pyautogui.hotkey('tab')
                smart_sleep('after_tab')
            
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
            # CORRECCIÓN: Solo usar navegación por teclado, sin coordenadas de mouse
            rpa_logger.log_action("Iniciando navegación por teclado", "Sin movimientos de mouse")
            
            for i, item in enumerate(items, 1):
                item_start_time = time.time()
                rpa_logger.log_action(f"Procesando item {i}/{len(items)}", f"Código: {item['codigo']}")
                
                try:
                    # CORRECCIÓN: Flujo con teclado - código + TAB + TAB + cantidad + TAB (para siguiente artículo)
                    pyautogui.typewrite(item['codigo'], interval=0.2)
                    time.sleep(3)
                    time.sleep(1)  # Espera adicional después de ingresar el código
                    pyautogui.hotkey('tab')  # Primer TAB
                    time.sleep(2)
                    pyautogui.hotkey('tab')  # Segundo TAB
                    time.sleep(2)
                    pyautogui.typewrite(str(item['cantidad']), interval=0.2)  # Cantidad después de los 2 TABs
                    time.sleep(2)
                    
                    # CORRECCIÓN: 3 TABs después de la cantidad para pasar al siguiente artículo
                    # Si es el último artículo, hacer solo 1 TAB para ir a totales
                    if i < len(items):  # Si no es el último artículo
                        pyautogui.hotkey('tab')  # Primer TAB después de cantidad
                        time.sleep(2)
                        pyautogui.hotkey('tab')  # Segundo TAB después de cantidad
                        time.sleep(2)
                        pyautogui.hotkey('tab')  # Tercer TAB después de cantidad
                        time.sleep(2)
                        rpa_logger.log_action(f"Item {i} - Navegando al siguiente artículo", f"Código: {item['codigo']}")
                    else:
                        # Último artículo: solo 1 TAB para ir a totales
                        pyautogui.hotkey('tab')  # Solo 1 TAB después de cantidad
                        time.sleep(2)
                        rpa_logger.log_action(f"Item {i} - Último artículo completado, navegando a totales", f"Código: {item['codigo']}")
                    
                    item_duration = time.time() - item_start_time
                    rpa_logger.log_performance(f"Item {i} procesado", item_duration)
                    rpa_logger.log_action(f"Item {i} cargado exitosamente", 
                                        f"Código: {item['codigo']}, Cantidad: {item['cantidad']}")
                    
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

    def scroll_to_bottom(self):
        """Baja el scroll hasta el final de la página"""
        start_time = time.time()
        rpa_logger.log_action("Iniciando scroll hacia abajo", "Buscando barra de desplazamiento vertical")
        
        try:
            # Importar el módulo de visión
            from rpa.vision import main as vision
            
            # Buscar la barra de desplazamiento usando la imagen de referencia
            rpa_logger.log_action("Buscando barra de desplazamiento", "Usando imagen de referencia: scroll_to_bottom.png")
            coordinates = vision.get_scrollbar_coordinates()
            
            if not coordinates:
                rpa_logger.log_error('No se pudo encontrar la barra de desplazamiento en la pantalla', 'Imagen de referencia no encontrada')
                return False
                
            # Verificar que las coordenadas sean válidas
            if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                rpa_logger.log_error(f'Coordenadas inválidas de scrollbar: {coordinates}', 'Formato de coordenadas incorrecto')
                return False
            
            scrollbar_x, scrollbar_y = coordinates
            rpa_logger.log_action("Barra de desplazamiento encontrada", f"Coordenadas: {coordinates}")
            
            # Hacer clic en la barra de desplazamiento
            rpa_logger.log_action("Haciendo clic en barra de desplazamiento", f"Posición: {coordinates}")
            pyautogui.click(scrollbar_x, scrollbar_y)
            time.sleep(1)
            
            # Obtener dimensiones de pantalla para calcular distancia de scroll
            screen_width, screen_height = pyautogui.size()
            
            # Arrastrar hacia abajo hasta el final
            # Calcular la distancia para bajar completamente
            scroll_distance = screen_height - 100  # Dejar un margen de 100 píxeles
            
            rpa_logger.log_action("Arrastrando scroll hacia abajo", f"Distancia: {scroll_distance} píxeles")
            pyautogui.drag(0, scroll_distance, duration=2)  # Arrastrar hacia abajo durante 2 segundos
            
            time.sleep(2)  # Esperar a que se complete el scroll
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Scroll hacia abajo completado", duration)
            rpa_logger.log_action("Scroll hacia abajo completado exitosamente", "Página desplazada al final")
            
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error al hacer scroll hacia abajo: {str(e)}", "Error en scroll")
            raise

    def take_totals_screenshot(self, filename):
        """Toma una captura de pantalla de la sección de totales"""
        start_time = time.time()
        rpa_logger.log_action("Iniciando captura de totales", f"Archivo: {filename}")
        
        try:
            # Crear directorio si no existe
            if not os.path.exists('./rpa/vision/reference_images/inserted_orders'):
                os.makedirs('./rpa/vision/reference_images/inserted_orders')
            
            # Generar nombre del archivo para totales
            base_name = filename.replace('.json', '')
            totals_filename = f'{base_name}_totales.png'
            saved_filename = f'./rpa/vision/reference_images/inserted_orders/{totals_filename}'
            
            # Tomar screenshot
            time.sleep(1)  # Esperar a que la página se estabilice
            screenshot = pyautogui.screenshot()
            screenshot.save(saved_filename)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Captura de totales completada", duration)
            rpa_logger.log_action("Captura de totales guardada exitosamente", f"Archivo: {totals_filename}")
            
        except Exception as e:
            rpa_logger.log_error(f"Error al tomar captura de totales: {str(e)}", f"Archivo: {filename}")
            raise

    def move_json_to_processed(self, filename):
        """Mueve el archivo JSON procesado a la carpeta de procesados"""
        start_time = time.time()
        rpa_logger.log_action("Iniciando movimiento de archivo procesado", f"Archivo: {filename}")
        
        try:
            import shutil
            
            # Definir rutas
            source_path = f'./data/outputs_json/{filename}'
            processed_dir = './data/outputs_json/Procesados'
            destination_path = f'{processed_dir}/{filename}'
            
            # Crear directorio de procesados si no existe
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)
                rpa_logger.log_action("PASO 8.5: Directorio de procesados creado", f"Ruta: {processed_dir}")
            
            # Verificar que el archivo fuente existe
            if not os.path.exists(source_path):
                rpa_logger.log_error(f"Archivo fuente no encontrado: {source_path}", f"Archivo: {filename}")
                return False
            
            # Mover el archivo
            rpa_logger.log_action("PASO 8.6: Moviendo archivo a procesados", f"De: {source_path} a: {destination_path}")
            shutil.move(source_path, destination_path)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Archivo movido a procesados", duration)
            rpa_logger.log_action("Archivo movido exitosamente a procesados", f"Archivo: {filename}")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error al mover archivo procesado: {str(e)}", f"Archivo: {filename}")
            return False

    def take_order_inserted_screenshot(self, filename):
        if not os.path.exists('./rpa/vision/reference_images/inserted_orders'):
            os.makedirs('./rpa/vision/reference_images/inserted_orders')
        saved_filename = f'./rpa/vision/reference_images/inserted_orders/{filename}'
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save(saved_filename)
        rpa_logger.info(f'Screenshot taken and saved in {saved_filename}')

    def data_loader(self, data, filename):
        nit = data["comprador"]['nit']
        orden_compra = data['orden_compra']
        fecha_entrega = data['fecha_entrega']
        items = data['items']

        self.load_nit(nit)
        self.load_orden_compra(orden_compra)
        self.load_fecha_entrega(fecha_entrega)
        self.load_items(items)
        
        # PASO 7: Tomar captura de pantalla completa
        rpa_logger.log_action("PASO 7: Capturando pantalla completa", "Después de procesar todos los artículos")
        self.take_totals_screenshot(filename)
        
        # PASO 8: Mover archivo JSON a procesados
        if self.move_json_to_processed(filename):
            rpa_logger.log_action("PASO 8 COMPLETADO: Procesamiento exitoso", f"Orden: {orden_compra}")
        else:
            rpa_logger.log_error("PASO 8 FALLIDO: Error al mover archivo procesado", f"Archivo: {filename}")
        
        rpa_logger.info('loaded data successfully with RPA. Waiting for next run')

    def cancel_order(self):
        self.get_remote_desktop()
        coordinates = vision.get_cancel_order_coordinates()
        pyautogui.moveTo(coordinates, duration=0.5)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        rpa_logger.info('Order cancelled.')

    @with_error_handling(ErrorType.SAP_NAVIGATION, ErrorSeverity.HIGH, operation="open_sap")
    def open_sap(self):
        max_attempts = get_retry_attempts('sap_open')
        
        for attempt in range(max_attempts):
            try:
                if not self.get_remote_desktop():
                    raise Exception("No se pudo conectar al escritorio remoto")
                
                smart_sleep('navigation_wait')
                rpa_logger.log_action("Iniciando apertura de SAP", f"Intento {attempt + 1}/{max_attempts}")
                
                # Usar el nuevo método de búsqueda robusta (icono + texto como respaldo)
                coordinates = vision.get_sap_coordinates_robust()
                
                if not coordinates:
                    raise Exception('No se pudo encontrar el icono de SAP Business One en la pantalla')
                    
                # Verificamos que las coordenadas sean válidas
                if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                    raise Exception(f'Coordenadas inválidas de SAP: {coordinates}')
                    
                rpa_logger.log_action("Icono de SAP Business One encontrado", f"Coordenadas: {coordinates}")
                
                pyautogui.moveTo(coordinates, duration=0.5)
                smart_sleep('medium')
                pyautogui.doubleClick()
                smart_sleep('sap_double_click')
                
                # Verificamos si SAP está respondiendo
                pyautogui.hotkey('enter')
                smart_sleep('sap_startup')
                
                # Verificamos si podemos tomar una captura de pantalla
                screenshot = pyautogui.screenshot("./rpa/vision/reference_images/sap_desktop.png")
                if screenshot:
                    rpa_logger.log_action("SAP abierto exitosamente", "Aplicación iniciada correctamente")
                    return True
                else:
                    raise Exception('No se pudo tomar captura de pantalla de SAP')
                    
            except Exception as e:
                if attempt == max_attempts - 1:  # Último intento
                    rpa_logger.log_error(f'Error opening SAP after {max_attempts} attempts: {str(e)}', 'Error crítico en apertura de SAP')
                    return False
                else:
                    rpa_logger.warning(f'Error opening SAP (attempt {attempt + 1}): {str(e)}. Reintentando...')
                    smart_sleep('retry_delay')
        
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
        rpa_logger.log_action("Iniciando apertura de SAP orden de ventas", "Navegación usando atajos de teclado")
        
        try:
            # Asegurar que la ventana esté activa antes de enviar comandos
            rpa_logger.log_action("PASO 4.0: Asegurando que la ventana esté activa", "Verificación de foco")
            windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
            if windows:
                window = windows[0]
                if not window.isActive:
                    window.activate()
                    time.sleep(2)
                    rpa_logger.log_action("PASO 4.0 COMPLETADO: Ventana activada", "Esperando 2 segundos")
            
            # 1. Abrir módulos con Alt + M (método mejorado)
            rpa_logger.log_action("PASO 4.1: Abriendo menú módulos", "Atajo: Alt + M")
            pyautogui.keyDown('alt')
            time.sleep(0.1)
            pyautogui.press('m')
            time.sleep(0.1)
            pyautogui.keyUp('alt')
            time.sleep(2)
            rpa_logger.log_action("PASO 4.1 COMPLETADO: Menú módulos abierto", "Esperando 2 segundos")
            
            # 2. Seleccionar Ventas con tecla 'V' (método mejorado)
            rpa_logger.log_action("PASO 4.2: Seleccionando módulo Ventas", "Tecla: V")
            pyautogui.press('v')
            time.sleep(2)
            rpa_logger.log_action("PASO 4.2 COMPLETADO: Módulo Ventas seleccionado", "Esperando 2 segundos")
            
            # 3. Buscar y hacer clic en el botón de Orden de Ventas usando la imagen de referencia
            rpa_logger.log_action("PASO 4.3: Buscando botón de Orden de Ventas", "Usando imagen de referencia: sap_ventas_order_button.png")
            orden_ventas_coordinates = vision.get_ventas_order_button_coordinates()
            
            if orden_ventas_coordinates is None:
                rpa_logger.log_error('PASO 4.3 FALLIDO: No se pudo encontrar el botón de Orden de Ventas', 'Imagen no encontrada en pantalla')
                return False
                
            rpa_logger.log_action("PASO 4.3 COMPLETADO: Botón de Orden de Ventas encontrado", f"Coordenadas: {orden_ventas_coordinates}")
            
            # 4. Hacer clic en el botón
            rpa_logger.log_action("PASO 4.4: Moviendo cursor al botón de Orden de Ventas", f"Coordenadas: {orden_ventas_coordinates}")
            pyautogui.moveTo(orden_ventas_coordinates, duration=0.5)
            time.sleep(1)
            
            rpa_logger.log_action("PASO 4.5: Haciendo clic en botón de Orden de Ventas", "Clic ejecutado")
            pyautogui.click()
            time.sleep(3)
            time.sleep(2)  # 2 segundos adicionales después de orden de venta
            rpa_logger.log_action("PASO 4.5 COMPLETADO: Clic ejecutado exitosamente", "Esperando 5 segundos para carga (3+2)")
            
            # 5. Capturar pantalla para verificar que se abrió correctamente
            rpa_logger.log_action("PASO 4.6: Capturando pantalla de verificación", "Guardando: sap_orden_de_ventas_template.png")
            pyautogui.screenshot("./rpa/vision/reference_images/sap_orden_de_ventas_template.png")
            rpa_logger.log_action("PASO 4.6 COMPLETADO: Captura de pantalla guardada", "Verificación completada")
            
            duration = time.time() - start_time
            rpa_logger.log_performance("PASO 4 COMPLETADO: Apertura de SAP orden de ventas", duration)
            rpa_logger.log_action("PASO 4 EXITOSO: SAP orden de ventas abierto exitosamente", "Módulo de ventas activo y listo para carga de datos")
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"PASO 4 FALLIDO: Error al abrir SAP orden de ventas: {str(e)}", "Error en navegación")
            return False

    @with_error_handling(ErrorType.WINDOW_CONNECTION, ErrorSeverity.HIGH, operation="get_remote_desktop")
    def get_remote_desktop(self):
        max_retries = get_retry_attempts('remote_desktop')
        retry_delay = get_delay('retry_delay') or 5.0
        
        rpa_logger.log_action("Iniciando conexión al escritorio remoto", f"Máximo {max_retries} intentos")
        
        for attempt in range(max_retries):
            try:
                windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
                if not windows:
                    if attempt < max_retries - 1:
                        rpa_logger.warning(f'Ventana no encontrada (intento {attempt + 1}/{max_retries}), abriendo escritorio remoto')
                        self.open_remote_desktop()
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise Exception('Ventana de escritorio remoto no encontrada después de varios intentos')
                
                window = windows[0]
                if not window.isActive:
                    window.activate()
                    smart_sleep('window_activation')
                
                # Verificamos que la ventana esté realmente activa
                if not window.isActive:
                    raise Exception('No se pudo activar la ventana del escritorio remoto')
                
                # Maximizar la ventana del escritorio remoto
                try:
                    rpa_logger.log_action("Maximizando ventana del escritorio remoto", "Alt+Space, X")
                    pyautogui.hotkey('alt', 'space')
                    smart_sleep('short')
                    pyautogui.typewrite('x')
                    smart_sleep('medium')
                    rpa_logger.log_action("Ventana maximizada exitosamente", "Maximización completada")
                except Exception as maximize_error:
                    rpa_logger.warning(f'Error al maximizar ventana: {str(maximize_error)} (continuando)')
                
                # Verificar con captura de pantalla
                screenshot = pyautogui.screenshot("./rpa/vision/reference_images/remote_desktop.png")
                if not screenshot:
                    raise Exception('No se pudo tomar captura de pantalla del escritorio remoto')
                
                rpa_logger.log_action("Conexión establecida exitosamente", "Ventana activa y maximizada")
                return window
                
            except Exception as e:
                if attempt == max_retries - 1:  # Último intento
                    raise Exception(f'Error crítico en conexión RDP después de {max_retries} intentos: {str(e)}')
                else:
                    rpa_logger.warning(f'Error en conexión RDP (intento {attempt + 1}): {str(e)}. Reintentando...')
                    time.sleep(retry_delay)
        
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
            # Filtrar solo archivos JSON, excluyendo directorios y archivos temporales
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))  # Solo archivos, no directorios
                    and f.endswith('.json')  # Solo archivos JSON
                    and not f.startswith('.')  # No archivos ocultos
                    and not f.endswith('.tmp')]  # No archivos temporales
            
            if len(files) == 0:
                rpa_logger.log_action("No hay archivos JSON disponibles para procesar", f"Directorio: {directory}")
                rpa_logger.log_action("Buscando archivos en directorio", f"Contenido: {os.listdir(directory)}")
                rpa_logger.info('No hay archivos para procesar. Esperando próxima ejecución')
                return
            
            rpa_logger.log_action(f"Archivos JSON encontrados para procesar", f"Total: {len(files)} archivos")
            rpa_logger.log_action("Lista de archivos encontrados", f"Archivos: {files}")
            
            for i, file in enumerate(files, 1):
                file_start_time = time.time()
                rpa_logger.log_action(f"Procesando archivo {i}/{len(files)}", f"Archivo: {file}")
                
                try:
                    with open(f'{directory}/{file}') as f:
                        data = json.load(f)
                    
                    rpa_logger.log_action("Archivo JSON cargado exitosamente", f"Archivo: {file}")
                    
                    # PASO 1: Conectar al escritorio remoto y maximizar ventana
                    rpa_logger.log_action("PASO 1: Conectando al escritorio remoto", f"Archivo: {file}")
                    if not self.get_remote_desktop():
                        rpa_logger.log_error(f'No se pudo conectar al escritorio remoto para el archivo {file}', 'Error en conexión RDP')
                        continue
                    
                    # PASO 2: Abrir SAP orden de ventas y verificar que se abrió correctamente
                    rpa_logger.log_action("PASO 2: Abriendo SAP orden de ventas", f"Archivo: {file}")
                    if not self.open_sap_orden_de_ventas():
                        rpa_logger.log_error(f'No se pudo abrir SAP orden de ventas para el archivo {file}', 'Error en navegación')
                        continue
                    
                    self.data_loader(data, file)
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
    # CORRECCIÓN: Removido close_sap() automático para evitar "x" extra
    # close_sap() solo se debe ejecutar manualmente cuando sea necesario
    # rpa.close_sap()  # Comentado para evitar "x" extra