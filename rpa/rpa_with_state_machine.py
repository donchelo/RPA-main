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
from rpa.state_machine import StateMachine, RPAState, RPAEvent
from rpa.rpa_state_handlers import RPAStateHandlers

vision = Vision()


class RPAWithStateMachine:
    """Versión del RPA que utiliza máquina de estados para control de flujo"""
    
    def __init__(self):
        self.remote_desktop_window = "20.96.6.64 - Conexión a Escritorio remoto"
        
        # Inicializar máquina de estados
        self.state_machine = StateMachine()
        self.state_handlers = RPAStateHandlers(self)
        
        # Registrar todos los manejadores de estado
        self._register_state_handlers()
        
        # Registrar callbacks de entrada y salida si es necesario
        self._register_callbacks()

    def _register_state_handlers(self):
        """Registra todos los manejadores de estado"""
        self.state_machine.register_state_handler(
            RPAState.IDLE, self.state_handlers.handle_idle_state
        )
        self.state_machine.register_state_handler(
            RPAState.CONNECTING_REMOTE_DESKTOP, self.state_handlers.handle_connecting_remote_desktop
        )
        self.state_machine.register_state_handler(
            RPAState.OPENING_SAP, self.state_handlers.handle_opening_sap
        )
        self.state_machine.register_state_handler(
            RPAState.NAVIGATING_TO_SALES_ORDER, self.state_handlers.handle_navigating_to_sales_order
        )
        self.state_machine.register_state_handler(
            RPAState.LOADING_NIT, self.state_handlers.handle_loading_nit
        )
        self.state_machine.register_state_handler(
            RPAState.LOADING_ORDER, self.state_handlers.handle_loading_order
        )
        self.state_machine.register_state_handler(
            RPAState.LOADING_DATE, self.state_handlers.handle_loading_date
        )
        self.state_machine.register_state_handler(
            RPAState.LOADING_ITEMS, self.state_handlers.handle_loading_items
        )
        self.state_machine.register_state_handler(
            RPAState.TAKING_SCREENSHOT, self.state_handlers.handle_taking_screenshot
        )
        self.state_machine.register_state_handler(
            RPAState.MOVING_JSON, self.state_handlers.handle_moving_json
        )
        self.state_machine.register_state_handler(
            RPAState.COMPLETED, self.state_handlers.handle_completed_state
        )
        self.state_machine.register_state_handler(
            RPAState.ERROR, self.state_handlers.handle_error_state
        )
        self.state_machine.register_state_handler(
            RPAState.RETRYING, self.state_handlers.handle_retrying_state
        )

    def _register_callbacks(self):
        """Registra callbacks de entrada y salida de estados si son necesarios"""
        # Callback de entrada para estado de error
        def on_error_entry(context, **kwargs):
            rpa_logger.log_action(
                "ENTRANDO A ESTADO DE ERROR",
                f"Archivo: {context.current_file}, Intento: {context.retry_count}"
            )
        
        self.state_machine.register_entry_callback(RPAState.ERROR, on_error_entry)
        
        # Callback de entrada para estado completado
        def on_completed_entry(context, **kwargs):
            rpa_logger.log_action(
                "PROCESO COMPLETADO - ENTRANDO A ESTADO FINAL",
                f"Archivo: {context.current_file}"
            )
        
        self.state_machine.register_entry_callback(RPAState.COMPLETED, on_completed_entry)

    def process_single_file(self, file_path: str, data: dict) -> bool:
        """
        Procesa un solo archivo utilizando la máquina de estados
        
        Args:
            file_path: Ruta del archivo JSON a procesar
            data: Datos del archivo JSON ya cargados
            
        Returns:
            bool: True si el procesamiento fue exitoso, False en caso contrario
        """
        file_name = os.path.basename(file_path)
        rpa_logger.log_action(
            f"Iniciando procesamiento con máquina de estados",
            f"Archivo: {file_name}"
        )
        
        # Reiniciar la máquina de estados para este archivo
        self.state_machine.reset()
        
        # Iniciar el procesamiento
        success = self.state_machine.start_processing(file_name, data)
        if not success:
            rpa_logger.log_error(f"No se pudo iniciar el procesamiento", f"Archivo: {file_name}")
            return False
        
        # Ejecutar el bucle de la máquina de estados
        max_iterations = 100  # Prevenir bucles infinitos
        iteration = 0
        
        while (self.state_machine.get_current_state() not in [RPAState.COMPLETED, RPAState.IDLE] 
               and iteration < max_iterations):
            
            iteration += 1
            current_state = self.state_machine.get_current_state()
            
            rpa_logger.log_action(
                f"Ejecutando estado: {current_state.value}",
                f"Iteración: {iteration}, Archivo: {file_name}"
            )
            
            try:
                # Ejecutar el estado actual
                next_event = self.state_machine.execute_current_state()
                
                if next_event is None:
                    # El estado no generó un evento, posiblemente es un estado final
                    if current_state == RPAState.COMPLETED:
                        rpa_logger.log_action("Procesamiento completado exitosamente", f"Archivo: {file_name}")
                        return True
                    elif current_state == RPAState.IDLE:
                        rpa_logger.log_action("Sistema regresó a estado IDLE", f"Archivo: {file_name}")
                        return False
                    else:
                        rpa_logger.log_error(
                            f"Estado {current_state.value} no generó evento",
                            f"Archivo: {file_name}"
                        )
                        break
                
                # Ejecutar la transición
                transition_success = self.state_machine.trigger_event(next_event)
                if not transition_success:
                    rpa_logger.log_error(
                        f"Falló la transición con evento {next_event.value}",
                        f"Estado actual: {current_state.value}, Archivo: {file_name}"
                    )
                    break
                
                # Manejo especial para errores
                if next_event == RPAEvent.ERROR_OCCURRED:
                    context = self.state_machine.get_context()
                    self.state_machine.handle_error(context.error_message or "Error desconocido")
                
            except Exception as e:
                rpa_logger.log_error(
                    f"Error ejecutando estado {current_state.value}: {str(e)}",
                    f"Archivo: {file_name}"
                )
                # Intentar manejar el error
                self.state_machine.handle_error(str(e))
        
        # Verificar el resultado final
        final_state = self.state_machine.get_current_state()
        
        if final_state == RPAState.COMPLETED:
            rpa_logger.log_action("Procesamiento completado exitosamente", f"Archivo: {file_name}")
            return True
        elif iteration >= max_iterations:
            rpa_logger.log_error(
                f"Procesamiento detenido: máximo de iteraciones alcanzado",
                f"Estado final: {final_state.value}, Archivo: {file_name}"
            )
            return False
        else:
            rpa_logger.log_error(
                f"Procesamiento terminó en estado: {final_state.value}",
                f"Archivo: {file_name}"
            )
            return False

    def run(self):
        """Ejecuta el procesamiento de todos los archivos JSON disponibles"""
        start_time = time.time()
        rpa_logger.log_action("Iniciando RPA con máquina de estados", "Buscando archivos JSON")
        
        directory = './data/outputs_json'
        
        try:
            # Filtrar solo archivos JSON válidos
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))
                    and f.endswith('.json')
                    and not f.startswith('.')
                    and not f.endswith('.tmp')]
            
            if len(files) == 0:
                rpa_logger.log_action(
                    "No hay archivos JSON disponibles para procesar",
                    f"Directorio: {directory}"
                )
                return
            
            rpa_logger.log_action(
                f"Archivos encontrados para procesar",
                f"Total: {len(files)} archivos"
            )
            
            successful_files = 0
            failed_files = 0
            
            for i, file in enumerate(files, 1):
                file_path = os.path.join(directory, file)
                rpa_logger.log_action(
                    f"Procesando archivo {i}/{len(files)}",
                    f"Archivo: {file}"
                )
                
                try:
                    # Cargar datos del archivo JSON
                    with open(file_path) as f:
                        data = json.load(f)
                    
                    rpa_logger.log_action("Archivo JSON cargado", f"Archivo: {file}")
                    
                    # Procesar el archivo usando la máquina de estados
                    success = self.process_single_file(file_path, data)
                    
                    if success:
                        successful_files += 1
                        rpa_logger.log_action(
                            f"Archivo procesado exitosamente",
                            f"Archivo: {file}"
                        )
                    else:
                        failed_files += 1
                        rpa_logger.log_error(
                            f"Falló el procesamiento del archivo",
                            f"Archivo: {file}"
                        )
                    
                except json.JSONDecodeError as e:
                    failed_files += 1
                    rpa_logger.log_error(
                        f"Error decodificando archivo JSON: {str(e)}",
                        f"Archivo: {file}"
                    )
                    continue
                    
                except Exception as e:
                    failed_files += 1
                    rpa_logger.log_error(
                        f"Error inesperado procesando archivo: {str(e)}",
                        f"Archivo: {file}"
                    )
                    continue
            
            # Estadísticas finales
            total_duration = time.time() - start_time
            rpa_logger.log_performance("Procesamiento RPA completado", total_duration)
            rpa_logger.log_action(
                "Resumen de procesamiento",
                f"Exitosos: {successful_files}, Fallidos: {failed_files}, Total: {len(files)}"
            )
            
        except Exception as e:
            rpa_logger.log_error(
                f"Error accediendo al directorio {directory}: {str(e)}",
                f"Directorio: {directory}"
            )
            return

    def get_state_info(self) -> dict:
        """Retorna información del estado actual de la máquina de estados"""
        return self.state_machine.get_state_info()

    def reset_state_machine(self):
        """Reinicia la máquina de estados"""
        self.state_machine.reset()
        rpa_logger.log_action("Máquina de estados reiniciada manualmente", "Estado: IDLE")

    # === MÉTODOS DE RPA ORIGINALES ===
    # Estos métodos mantienen la funcionalidad original del RPA
    # y son utilizados por los manejadores de estado

    def print_position(self):
        while True:
            print(pyautogui.position())

    @with_error_handling(ErrorType.DATA_PROCESSING, ErrorSeverity.MEDIUM, operation="load_nit")
    def load_nit(self, nit):
        start_time = time.time()
        rpa_logger.log_action("Iniciando carga de NIT", f"NIT: {nit}")
        
        if not nit or not str(nit).strip():
            raise ValueError(f"NIT inválido: {nit}")
        
        try:
            smart_sleep('short')
            
            pyautogui.screenshot("./rpa/vision/reference_images/template.png")
            vision.save_template()
            
            pyautogui.hotkey('ctrl', 'a')
            smart_sleep('very_short')
            
            nit_str = str(nit).strip()
            pyautogui.typewrite(nit_str, interval=0.2)
            smart_sleep('after_input')
            smart_sleep('after_nit')
            
            pyautogui.hotkey('enter')
            smart_sleep('after_input')
            
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
            pyautogui.typewrite(orden_compra, interval=0.2)
            smart_sleep('after_input')
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
            pyautogui.typewrite(fecha_entrega, interval=0.2)
            smart_sleep('after_input')
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
            rpa_logger.log_action("Iniciando navegación por teclado", "Sin movimientos de mouse")
            
            for i, item in enumerate(items, 1):
                item_start_time = time.time()
                rpa_logger.log_action(f"Procesando item {i}/{len(items)}", f"Código: {item['codigo']}")
                
                try:
                    pyautogui.typewrite(item['codigo'], interval=0.2)
                    time.sleep(3)
                    time.sleep(1)
                    pyautogui.hotkey('tab')
                    time.sleep(2)
                    pyautogui.hotkey('tab')
                    time.sleep(2)
                    pyautogui.typewrite(str(item['cantidad']), interval=0.2)
                    time.sleep(2)
                    
                    if i < len(items):
                        pyautogui.hotkey('tab')
                        time.sleep(2)
                        pyautogui.hotkey('tab')
                        time.sleep(2)
                        pyautogui.hotkey('tab')
                        time.sleep(2)
                        rpa_logger.log_action(f"Item {i} - Navegando al siguiente artículo", f"Código: {item['codigo']}")
                    else:
                        pyautogui.hotkey('tab')
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
        start_time = time.time()
        rpa_logger.log_action("Iniciando scroll hacia abajo", "Buscando barra de desplazamiento vertical")
        
        try:
            rpa_logger.log_action("Buscando barra de desplazamiento", "Usando imagen de referencia: scroll_to_bottom.png")
            coordinates = vision.get_scrollbar_coordinates()
            
            if not coordinates:
                rpa_logger.log_error('No se pudo encontrar la barra de desplazamiento en la pantalla', 'Imagen de referencia no encontrada')
                return False
                
            if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                rpa_logger.log_error(f'Coordenadas inválidas de scrollbar: {coordinates}', 'Formato de coordenadas incorrecto')
                return False
            
            scrollbar_x, scrollbar_y = coordinates
            rpa_logger.log_action("Barra de desplazamiento encontrada", f"Coordenadas: {coordinates}")
            
            rpa_logger.log_action("Haciendo clic en barra de desplazamiento", f"Posición: {coordinates}")
            pyautogui.click(scrollbar_x, scrollbar_y)
            time.sleep(1)
            
            screen_width, screen_height = pyautogui.size()
            scroll_distance = screen_height - 100
            
            rpa_logger.log_action("Arrastrando scroll hacia abajo", f"Distancia: {scroll_distance} píxeles")
            pyautogui.drag(0, scroll_distance, duration=2)
            
            time.sleep(2)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Scroll hacia abajo completado", duration)
            rpa_logger.log_action("Scroll hacia abajo completado exitosamente", "Página desplazada al final")
            
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error al hacer scroll hacia abajo: {str(e)}", "Error en scroll")
            raise

    def take_totals_screenshot(self, filename):
        start_time = time.time()
        rpa_logger.log_action("Iniciando captura de pantalla para validación", f"Archivo: {filename}")
        
        try:
            processed_dir = './data/outputs_json/Procesados'
            
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)
                rpa_logger.log_action("Directorio de procesados creado", f"Ruta: {processed_dir}")
            
            base_name = filename.replace('.json', '')
            validation_filename = f'{base_name}.png'
            saved_filepath = os.path.join(processed_dir, validation_filename)
            
            time.sleep(1)
            screenshot = pyautogui.screenshot()
            screenshot.save(saved_filepath)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Captura de pantalla para validación", duration)
            rpa_logger.log_action("Captura de validación guardada exitosamente", f"Archivo: {validation_filename}")
            rpa_logger.log_action("Ruta completa del screenshot", f"Ubicación: {saved_filepath}")
            
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error al tomar captura de pantalla: {str(e)}", f"Archivo: {filename}")
            return False

    def move_json_to_processed(self, filename):
        start_time = time.time()
        rpa_logger.log_action("Iniciando movimiento de archivo procesado", f"Archivo: {filename}")
        
        try:
            import shutil
            
            source_path = f'./data/outputs_json/{filename}'
            processed_dir = './data/outputs_json/Procesados'
            destination_path = os.path.join(processed_dir, filename)
            
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)
                rpa_logger.log_action("Directorio de procesados creado", f"Ruta: {processed_dir}")
            
            if not os.path.exists(source_path):
                rpa_logger.log_error(f"Archivo fuente no encontrado: {source_path}", f"Archivo: {filename}")
                return False
            
            rpa_logger.log_action("Moviendo archivo JSON a procesados", f"De: {source_path} a: {destination_path}")
            shutil.move(source_path, destination_path)
            
            screenshot_name = filename.replace('.json', '.png')
            screenshot_path = os.path.join(processed_dir, screenshot_name)
            
            files_status = {
                'json_exists': os.path.exists(destination_path),
                'screenshot_exists': os.path.exists(screenshot_path),
                'json_path': destination_path,
                'screenshot_path': screenshot_path
            }
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Movimiento de archivo a procesados", duration)
            rpa_logger.log_action("Archivo JSON movido exitosamente", f"Archivo: {filename}")
            rpa_logger.log_action("Estado de archivos para Make.com", f"Status: {files_status}")
            
            return True
            
        except Exception as e:
            rpa_logger.log_error(f"Error al mover archivo procesado: {str(e)}", f"Archivo: {filename}")
            return False

    def validate_files_for_makecom(self, filename):
        processed_dir = './data/outputs_json/Procesados'
        
        json_path = os.path.join(processed_dir, filename)
        screenshot_name = filename.replace('.json', '.png')
        screenshot_path = os.path.join(processed_dir, screenshot_name)
        
        validation_result = {
            'json_exists': os.path.exists(json_path),
            'screenshot_exists': os.path.exists(screenshot_path),
            'json_size': os.path.getsize(json_path) if os.path.exists(json_path) else 0,
            'screenshot_size': os.path.getsize(screenshot_path) if os.path.exists(screenshot_path) else 0,
            'ready_for_makecom': False
        }
        
        validation_result['ready_for_makecom'] = (
            validation_result['json_exists'] and 
            validation_result['screenshot_exists'] and
            validation_result['json_size'] > 0 and
            validation_result['screenshot_size'] > 0
        )
        
        if validation_result['ready_for_makecom']:
            rpa_logger.log_action("Archivos validados para Make.com", f"JSON: {filename}, Screenshot: {screenshot_name}")
        else:
            rpa_logger.log_error("Validación fallida para Make.com", f"Status: {validation_result}")
        
        return validation_result

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
                
                coordinates = vision.get_sap_coordinates_robust()
                
                if not coordinates:
                    raise Exception('No se pudo encontrar el icono de SAP Business One en la pantalla')
                    
                if not isinstance(coordinates, tuple) or len(coordinates) != 2:
                    raise Exception(f'Coordenadas inválidas de SAP: {coordinates}')
                    
                rpa_logger.log_action("Icono de SAP Business One encontrado", f"Coordenadas: {coordinates}")
                
                pyautogui.moveTo(coordinates, duration=0.5)
                smart_sleep('medium')
                pyautogui.doubleClick()
                smart_sleep('sap_double_click')
                
                pyautogui.hotkey('enter')
                smart_sleep('sap_startup')
                
                screenshot = pyautogui.screenshot("./rpa/vision/reference_images/sap_desktop.png")
                if screenshot:
                    rpa_logger.log_action("SAP abierto exitosamente", "Aplicación iniciada correctamente")
                    return True
                else:
                    raise Exception('No se pudo tomar captura de pantalla de SAP')
                    
            except Exception as e:
                if attempt == max_attempts - 1:
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
            rpa_logger.log_action("PASO 4.0: Asegurando que la ventana esté activa", "Verificación de foco")
            windows = pyautogui.getWindowsWithTitle(self.remote_desktop_window)
            if windows:
                window = windows[0]
                if not window.isActive:
                    window.activate()
                    time.sleep(2)
                    rpa_logger.log_action("PASO 4.0 COMPLETADO: Ventana activada", "Esperando 2 segundos")
            
            rpa_logger.log_action("PASO 4.1: Abriendo menú módulos", "Atajo: Alt + M")
            pyautogui.keyDown('alt')
            time.sleep(0.1)
            pyautogui.press('m')
            time.sleep(0.1)
            pyautogui.keyUp('alt')
            time.sleep(2)
            rpa_logger.log_action("PASO 4.1 COMPLETADO: Menú módulos abierto", "Esperando 2 segundos")
            
            rpa_logger.log_action("PASO 4.2: Seleccionando módulo Ventas", "Tecla: V")
            pyautogui.press('v')
            time.sleep(2)
            rpa_logger.log_action("PASO 4.2 COMPLETADO: Módulo Ventas seleccionado", "Esperando 2 segundos")
            
            rpa_logger.log_action("PASO 4.3: Buscando botón de Orden de Ventas", "Usando imagen de referencia: sap_ventas_order_button.png")
            orden_ventas_coordinates = vision.get_ventas_order_button_coordinates()
            
            if orden_ventas_coordinates is None:
                rpa_logger.log_error('PASO 4.3 FALLIDO: No se pudo encontrar el botón de Orden de Ventas', 'Imagen no encontrada en pantalla')
                return False
                
            rpa_logger.log_action("PASO 4.3 COMPLETADO: Botón de Orden de Ventas encontrado", f"Coordenadas: {orden_ventas_coordinates}")
            
            rpa_logger.log_action("PASO 4.4: Moviendo cursor al botón de Orden de Ventas", f"Coordenadas: {orden_ventas_coordinates}")
            pyautogui.moveTo(orden_ventas_coordinates, duration=0.5)
            time.sleep(1)
            
            rpa_logger.log_action("PASO 4.5: Haciendo clic en botón de Orden de Ventas", "Clic ejecutado")
            pyautogui.click()
            time.sleep(3)
            time.sleep(2)
            rpa_logger.log_action("PASO 4.5 COMPLETADO: Clic ejecutado exitosamente", "Esperando 5 segundos para carga (3+2)")
            
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
                
                if not window.isActive:
                    raise Exception('No se pudo activar la ventana del escritorio remoto')
                
                try:
                    rpa_logger.log_action("Maximizando ventana del escritorio remoto", "Win + Flecha Arriba")
                    pyautogui.hotkey('win', 'up')
                    smart_sleep('medium')
                    rpa_logger.log_action("Ventana maximizada exitosamente", "Maximización completada")
                except Exception as maximize_error:
                    rpa_logger.warning(f'Error al maximizar ventana: {str(maximize_error)} (continuando)')
                
                screenshot = pyautogui.screenshot("./rpa/vision/reference_images/remote_desktop.png")
                if not screenshot:
                    raise Exception('No se pudo tomar captura de pantalla del escritorio remoto')
                
                rpa_logger.log_action("Conexión establecida exitosamente", "Ventana activa y maximizada")
                return window
                
            except Exception as e:
                if attempt == max_retries - 1:
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


if __name__ == "__main__":
    rpa = RPAWithStateMachine()
    rpa.run()