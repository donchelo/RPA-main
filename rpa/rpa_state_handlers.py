from typing import Optional
from datetime import datetime
from .state_machine import RPAEvent, StateContext, RPAState
from .simple_logger import rpa_logger
import time


class RPAStateHandlers:
    """Manejadores específicos para cada estado del proceso RPA"""
    
    def __init__(self, rpa_instance):
        """
        Inicializa los manejadores con una instancia del RPA
        
        Args:
            rpa_instance: Instancia de la clase RPA que contiene toda la lógica de automatización
        """
        self.rpa = rpa_instance

    def handle_idle_state(self, context: StateContext, **kwargs) -> Optional[RPAEvent]:
        """Maneja el estado IDLE - no hay procesamiento activo"""
        rpa_logger.log_action("Sistema en estado IDLE", "Esperando archivos para procesar")
        # El estado IDLE no genera eventos automáticamente
        return None

    def handle_connecting_remote_desktop(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la conexión al escritorio remoto"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Conectando al escritorio remoto",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # Intentar conectar al escritorio remoto
            success = self.rpa.get_remote_desktop()
            
            if success:
                duration = time.time() - start_time
                rpa_logger.log_performance("Conexión a escritorio remoto", duration)
                context.processing_stats['remote_desktop_time'] = duration
                context.last_successful_state = RPAState.CONNECTING_REMOTE_DESKTOP
                return RPAEvent.REMOTE_DESKTOP_CONNECTED
            else:
                rpa_logger.log_error("Falló la conexión al escritorio remoto", f"Archivo: {context.current_file}")
                return RPAEvent.REMOTE_DESKTOP_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error conectando al escritorio remoto: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.REMOTE_DESKTOP_FAILED

    def handle_opening_sap(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la apertura de SAP Business One"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Abriendo SAP Business One",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # Intentar abrir SAP
            success = self.rpa.open_sap()
            
            if success:
                duration = time.time() - start_time
                rpa_logger.log_performance("Apertura de SAP", duration)
                context.processing_stats['sap_open_time'] = duration
                return RPAEvent.SAP_OPENED
            else:
                rpa_logger.log_error("Falló la apertura de SAP", f"Archivo: {context.current_file}")
                return RPAEvent.SAP_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error abriendo SAP: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.SAP_FAILED

    def handle_navigating_to_sales_order(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la navegación al módulo de orden de ventas"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Navegando a orden de ventas",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # Intentar navegar al módulo de orden de ventas
            success = self.rpa.open_sap_orden_de_ventas()
            
            if success:
                duration = time.time() - start_time
                rpa_logger.log_performance("Navegación a orden de ventas", duration)
                context.processing_stats['navigation_time'] = duration
                return RPAEvent.SALES_ORDER_OPENED
            else:
                rpa_logger.log_error("Falló la navegación a orden de ventas", f"Archivo: {context.current_file}")
                return RPAEvent.SALES_ORDER_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error navegando a orden de ventas: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.SALES_ORDER_FAILED

    def handle_loading_nit(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la carga del NIT del comprador"""
        start_time = time.time()
        
        try:
            if not context.current_data or 'comprador' not in context.current_data:
                raise ValueError("No se encontraron datos del comprador")
                
            nit = context.current_data['comprador']['nit']
            rpa_logger.log_action(
                f"ESTADO: Cargando NIT",
                f"NIT: {nit}, Archivo: {context.current_file}"
            )
            
            # Cargar el NIT
            self.rpa.load_nit(nit)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de NIT", duration)
            context.processing_stats['nit_load_time'] = duration
            return RPAEvent.NIT_LOADED
            
        except Exception as e:
            rpa_logger.log_error(f"Error cargando NIT: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.NIT_FAILED

    def handle_loading_order(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la carga de la orden de compra"""
        start_time = time.time()
        
        try:
            if not context.current_data or 'orden_compra' not in context.current_data:
                raise ValueError("No se encontraron datos de orden de compra")
                
            orden_compra = context.current_data['orden_compra']
            rpa_logger.log_action(
                f"ESTADO: Cargando orden de compra",
                f"Orden: {orden_compra}, Archivo: {context.current_file}"
            )
            
            # Cargar la orden de compra
            self.rpa.load_orden_compra(orden_compra)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de orden de compra", duration)
            context.processing_stats['order_load_time'] = duration
            return RPAEvent.ORDER_LOADED
            
        except Exception as e:
            rpa_logger.log_error(f"Error cargando orden de compra: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.ORDER_FAILED

    def handle_loading_date(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la carga de la fecha de entrega y fecha de documento."""
        start_time = time.time()

        try:
            if not context.current_data:
                raise ValueError("No se encontraron datos")

            data = context.current_data

            def _try_parse_date(date_str: str):
                if not date_str:
                    return None
                for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                    try:
                        return datetime.strptime(date_str, fmt)
                    except Exception:
                        pass
                return None

            candidates = []
            if data.get('fecha_entrega'):
                parsed = _try_parse_date(data['fecha_entrega'])
                if parsed:
                    candidates.append((data['fecha_entrega'], parsed))

            for item in data.get('items', []):
                fe = item.get('fecha_entrega')
                if fe:
                    parsed = _try_parse_date(fe)
                    if parsed:
                        candidates.append((fe, parsed))

            if not candidates:
                raise ValueError("No se encontraron fechas de entrega válidas")

            selected_original, selected_dt = max(candidates, key=lambda t: t[1])

            # Obtener fecha_documento del JSON, usar fecha_entrega como fallback
            fecha_documento = data.get('fecha_documento', selected_original)

            rpa_logger.log_action(
                "ESTADO: Cargando fechas",
                f"Entrega: {selected_original}, Documento: {fecha_documento}, Archivo: {context.current_file}"
            )

            # Cargar las fechas (entrega y documento)
            self.rpa.load_fecha_entrega(selected_original, fecha_documento)

            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de fechas", duration)
            context.processing_stats['date_load_time'] = duration
            return RPAEvent.DATE_LOADED

        except Exception as e:
            rpa_logger.log_error(f"Error cargando fechas: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.DATE_FAILED

    def handle_loading_items(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la carga de todos los items"""
        start_time = time.time()
        
        try:
            if not context.current_data or 'items' not in context.current_data:
                raise ValueError("No se encontraron datos de items")
                
            items = context.current_data['items']
            rpa_logger.log_action(
                f"ESTADO: Cargando items",
                f"Total items: {len(items)}, Archivo: {context.current_file}"
            )
            
            # Cargar todos los items
            self.rpa.load_items(items)
            
            # Esperar 2 segundos después de cargar items
            rpa_logger.log_action("Esperando 2 segundos después de cargar items", "Preparando para captura")
            time.sleep(2)
            
            duration = time.time() - start_time
            rpa_logger.log_performance("Carga de items", duration)
            context.processing_stats['items_load_time'] = duration
            context.processing_stats['items_count'] = len(items)
            return RPAEvent.ITEMS_LOADED
            
        except Exception as e:
            rpa_logger.log_error(f"Error cargando items: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.ITEMS_FAILED


    def handle_taking_screenshot(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la captura de pantalla para validación"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Tomando captura de pantalla",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # Tomar captura de pantalla
            success = self.rpa.take_totals_screenshot(context.current_file)
            
            if success:
                duration = time.time() - start_time
                rpa_logger.log_performance("Captura de pantalla", duration)
                context.processing_stats['screenshot_time'] = duration
                return RPAEvent.SCREENSHOT_TAKEN
            else:
                rpa_logger.log_error("Falló la captura de pantalla", f"Archivo: {context.current_file}")
                return RPAEvent.SCREENSHOT_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error tomando captura de pantalla: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.SCREENSHOT_FAILED

    def handle_moving_json(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja el movimiento del JSON a la carpeta de procesados"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Moviendo JSON a procesados",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # Mover el archivo JSON
            success = self.rpa.move_json_to_processed(context.current_file)
            
            if success:
                duration = time.time() - start_time
                rpa_logger.log_performance("Movimiento de JSON", duration)
                context.processing_stats['json_move_time'] = duration
                
                # Validar que ambos archivos estén listos para Make.com
                validation_result = self.rpa.validate_files_for_makecom(context.current_file)
                if validation_result['ready_for_makecom']:
                    rpa_logger.log_action(
                        "PROCESO COMPLETADO: Archivos validados para Make.com",
                        f"Archivo: {context.current_file}"
                    )
                    return RPAEvent.JSON_MOVED
                else:
                    rpa_logger.log_error(
                        "VALIDACIÓN FALLIDA: Archivos no están listos para Make.com",
                        f"Archivo: {context.current_file}, Status: {validation_result}"
                    )
                    return RPAEvent.JSON_FAILED
            else:
                rpa_logger.log_error("Falló el movimiento del JSON", f"Archivo: {context.current_file}")
                return RPAEvent.JSON_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error moviendo JSON: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.JSON_FAILED

    def handle_positioning_mouse(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja el posicionamiento del mouse en el botón 'Agregar y'"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Posicionando mouse en botón 'Agregar y'",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # Posicionar mouse en la esquina inferior derecha del botón "Agregar y"
            success = self.rpa.position_mouse_on_agregar_button()
            
            if success:
                duration = time.time() - start_time
                rpa_logger.log_performance("Posicionamiento del mouse", duration)
                context.processing_stats['mouse_position_time'] = duration
                rpa_logger.log_action("Mouse posicionado correctamente en botón 'Agregar y'", f"Archivo: {context.current_file}")
                return RPAEvent.MOUSE_POSITIONED
            else:
                rpa_logger.log_error("Falló el posicionamiento del mouse", f"Archivo: {context.current_file}")
                return RPAEvent.MOUSE_POSITION_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error posicionando mouse: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.MOUSE_POSITION_FAILED

    def handle_completed_state(self, context: StateContext, **kwargs) -> Optional[RPAEvent]:
        """Maneja el estado de proceso completado"""
        # Calcular y loggear estadísticas finales
        if context.start_time:
            total_time = time.time() - context.start_time
            context.processing_stats['total_processing_time'] = total_time
            
            rpa_logger.log_action(
                f"PROCESO COMPLETADO EXITOSAMENTE",
                f"Archivo: {context.current_file}, Tiempo total: {total_time:.2f}s"
            )
            
            # Log estadísticas detalladas si están disponibles
            if context.processing_stats:
                stats_msg = ", ".join([f"{k}: {v:.2f}s" if isinstance(v, float) else f"{k}: {v}" 
                                     for k, v in context.processing_stats.items()])
                rpa_logger.log_action("Estadísticas de procesamiento", stats_msg)
        
        return None

    def handle_error_state(self, context: StateContext, **kwargs) -> Optional[RPAEvent]:
        """Maneja el estado de error"""
        rpa_logger.log_error(
            f"SISTEMA EN ESTADO DE ERROR",
            f"Archivo: {context.current_file}, Error: {context.error_message}, Intento: {context.retry_count}/{context.max_retries}"
        )
        
        # No genera eventos automáticamente - depende de la lógica de manejo de errores
        return None

    def handle_retrying_state(self, context: StateContext, **kwargs) -> Optional[RPAEvent]:
        """Maneja el estado de reintento"""
        rpa_logger.log_action(
            f"REINTENTANDO PROCESAMIENTO",
            f"Archivo: {context.current_file}, Intento: {context.retry_count}/{context.max_retries}"
        )
        
        # Limpiar el mensaje de error para el reintento
        context.error_message = None
        
        # Reiniciar el proceso
        return RPAEvent.START_PROCESSING