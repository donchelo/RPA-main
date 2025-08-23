from typing import Optional
from datetime import datetime
from .state_machine import RPAEvent, StateContext, RPAState
from .simple_logger import rpa_logger
import time
import os


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
            # PASO 1: Ir directamente al escritorio remoto
            rpa_logger.log_action(
                "Iniciando conexión directa al escritorio remoto",
                "Sin retrasos - procediendo inmediatamente"
            )
            
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
        """Maneja la apertura de SAP Business One y detecta dónde está actualmente"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Detectando ubicación actual y abriendo SAP Business One",
            f"Archivo: {context.current_file}"
        )
        
        try:
            from rpa.vision.main import Vision
            vision = Vision()
            
            # PASO 1: Detectar dónde estamos actualmente
            rpa_logger.log_action(
                "Detectando ubicación actual en el sistema",
                "Verificando estado de SAP y escritorio remoto"
            )
            
            # Verificar si ya estamos en SAP desktop
            if vision.is_sap_desktop_visible():
                rpa_logger.log_action(
                    "SAP Business One ya está abierto y visible",
                    "Saltando directamente a navegación de órdenes de ventas"
                )
                duration = time.time() - start_time
                context.processing_stats['sap_already_open_time'] = duration
                return RPAEvent.SAP_OPENED
            
            # Verificar si estamos en el escritorio remoto pero SAP no está abierto
            rpa_logger.log_action(
                "SAP no detectado, verificando si estamos en escritorio remoto",
                "Buscando icono de SAP para abrir"
            )
            
            # Buscar el icono de SAP para abrirlo
            sap_coordinates = vision.get_sap_coordinates_robust()
            if sap_coordinates:
                rpa_logger.log_action(
                    "Icono de SAP encontrado en escritorio remoto",
                    "Procediendo a abrir SAP Business One"
                )
                
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
            else:
                rpa_logger.log_error(
                    "No se encontró el icono de SAP en el escritorio remoto",
                    "Verificar que SAP esté instalado y visible"
                )
                return RPAEvent.SAP_FAILED
                
        except Exception as e:
            rpa_logger.log_error(f"Error detectando ubicación o abriendo SAP: {str(e)}", f"Archivo: {context.current_file}")
            return RPAEvent.SAP_FAILED

    def handle_navigating_to_sales_order(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la navegación al módulo de orden de ventas"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Navegando a orden de ventas",
            f"Archivo: {context.current_file}"
        )
        
        try:
            from rpa.vision.main import Vision
            vision = Vision()
            
            # PASO 1: Verificar si ya estamos en el formulario de órdenes de ventas
            rpa_logger.log_action(
                "Verificando si ya estamos en el formulario de órdenes de ventas",
                "Buscando elementos característicos del formulario"
            )
            
            # Verificar si ya estamos en el formulario de órdenes de ventas
            if vision.is_sales_order_form_visible():
                rpa_logger.log_action(
                    "Ya estamos en el formulario de órdenes de ventas",
                    "Saltando directamente a carga de datos"
                )
                duration = time.time() - start_time
                context.processing_stats['already_in_form_time'] = duration
                return RPAEvent.SALES_ORDER_OPENED
            
            # Si no estamos en el formulario, navegar a él
            rpa_logger.log_action(
                "No estamos en el formulario de órdenes de ventas",
                "Procediendo con navegación al módulo"
            )
            
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

            # Obtener fecha_documento del JSON, buscar también fecha_orden como alternativa
            fecha_documento = data.get('fecha_documento') or data.get('fecha_orden', selected_original)

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
        """Maneja la confirmación de captura de pantalla (ya tomada en el estado anterior)"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Confirmando captura de pantalla final",
            f"Archivo: {context.current_file}"
        )
        
        try:
            # La screenshot ya fue tomada en el estado POSITIONING_MOUSE después del clic
            # Solo confirmamos que el proceso fue exitoso
            duration = time.time() - start_time
            context.processing_stats['screenshot_confirmation_time'] = duration
            rpa_logger.log_action("Captura de pantalla final confirmada", f"Archivo: {context.current_file}")
            return RPAEvent.SCREENSHOT_TAKEN
                
        except Exception as e:
            rpa_logger.log_error(f"Error confirmando captura de pantalla: {str(e)}", f"Archivo: {context.current_file}")
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
            success = self.rpa.position_mouse_on_agregar_button(context.current_file)
            
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

    def handle_uploading_to_google_drive_state(self, context: StateContext, **kwargs) -> RPAEvent:
        """Maneja la subida de archivos a Google Drive en orden específico: PNG primero, luego PDF"""
        start_time = time.time()
        rpa_logger.log_action(
            f"ESTADO: Subiendo archivos a Google Drive",
            f"Archivo: {context.current_file}"
        )
        
        try:
            from rpa.google_drive_oauth_uploader import GoogleDriveOAuthUploader
            uploader = GoogleDriveOAuthUploader()
            
            # Extraer nombre base del archivo
            if context.current_file.endswith('.PDF.json'):
                base_name = context.current_file.replace('.PDF.json', '')
            elif context.current_file.endswith('.pdf.json'):
                # CORREGIDO: Para archivos como "4500225658.pdf.json" → "4500225658"
                base_name = context.current_file.replace('.pdf.json', '')
            elif context.current_file.endswith('.json'):
                base_name = context.current_file.replace('.json', '')
            else:
                base_name = context.current_file
            
            rpa_logger.log_action(
                "Iniciando subida ordenada a Google Drive",
                f"Base: {base_name}, Orden: PNG primero, luego PDF"
            )
            
            # Buscar archivos en orden específico
            search_locations = [
                './data/outputs_json/Procesados/',
                './data/outputs_json/',
                './data/',
                './'
            ]
            
            files_uploaded = []
            
            # PASO 1: Subir PNG primero
            png_names = [
                f"{base_name}.png",  # Nombre base
                f"{base_name}.PDF.png"  # Nombre completo del JSON
            ]
            
            png_uploaded = False
            for png_name in png_names:
                for location in search_locations:
                    png_path = os.path.join(location, png_name)
                    if os.path.exists(png_path):
                        rpa_logger.log_action(
                            "Subiendo PNG (PASO 1)",
                            f"Archivo: {png_name}, Ubicación: {location}"
                        )
                        
                        result = uploader.upload_file(png_path)
                        if result and result.get('success'):
                            files_uploaded.append({
                                'type': 'PNG',
                                'original_path': png_path,
                                'drive_info': result
                            })
                            png_uploaded = True
                            rpa_logger.log_action(
                                "PNG subido exitosamente (PASO 1)",
                                f"ID: {result.get('id')}, Enlace: {result.get('link')}"
                            )
                            break
                if png_uploaded:
                    break
            
            # PASO 2: Subir PDF después
            pdf_name_upper = f"{base_name}.PDF"
            pdf_uploaded = False
            
            # Buscar .PDF mayúscula primero
            for location in search_locations:
                pdf_path = os.path.join(location, pdf_name_upper)
                if os.path.exists(pdf_path):
                    rpa_logger.log_action(
                        "Subiendo PDF (PASO 2)",
                        f"Archivo: {pdf_name_upper}, Ubicación: {location}"
                    )
                    
                    result = uploader.upload_file(pdf_path)
                    if result and result.get('success'):
                        files_uploaded.append({
                            'type': 'PDF',
                            'original_path': pdf_path,
                            'drive_info': result
                        })
                        pdf_uploaded = True
                        rpa_logger.log_action(
                            "PDF subido exitosamente (PASO 2)",
                            f"ID: {result.get('id')}, Enlace: {result.get('link')}"
                        )
                        break
            
            # Si no se encontró .PDF mayúscula, buscar .pdf minúscula
            if not pdf_uploaded:
                pdf_name = f"{base_name}.pdf"
                for location in search_locations:
                    pdf_path = os.path.join(location, pdf_name)
                    if os.path.exists(pdf_path):
                        rpa_logger.log_action(
                            "Subiendo PDF (PASO 2 - minúscula)",
                            f"Archivo: {pdf_name}, Ubicación: {location}"
                        )
                        
                        result = uploader.upload_file(pdf_path)
                        if result and result.get('success'):
                            files_uploaded.append({
                                'type': 'PDF',
                                'original_path': pdf_path,
                                'drive_info': result
                            })
                            pdf_uploaded = True
                            rpa_logger.log_action(
                                "PDF subido exitosamente (PASO 2)",
                                f"ID: {result.get('id')}, Enlace: {result.get('link')}"
                            )
                            break
            
            # Verificar resultado final
            if len(files_uploaded) > 0:
                duration = time.time() - start_time
                context.processing_stats['google_drive_upload_time'] = duration
                
                rpa_logger.log_action(
                    "ARCHIVOS SUBIDOS EXITOSAMENTE A GOOGLE DRIVE",
                    f"Archivo: {context.current_file}, Archivos subidos: {len(files_uploaded)}/2, "
                    f"Tiempo: {duration:.2f}s"
                )
                
                # Loggear resumen de archivos subidos
                for file_info in files_uploaded:
                    rpa_logger.log_action(
                        f"Archivo subido: {file_info.get('type')}",
                        f"ID: {file_info.get('drive_info', {}).get('id', 'N/A')}, "
                        f"Enlace: {file_info.get('drive_info', {}).get('link', 'N/A')}"
                    )
                
                return RPAEvent.GOOGLE_DRIVE_UPLOADED
            else:
                rpa_logger.log_error(
                    "FALLA EN SUBIDA A GOOGLE DRIVE - No se subió ningún archivo",
                    f"Archivo: {context.current_file}"
                )
                return RPAEvent.GOOGLE_DRIVE_FAILED
                
        except Exception as e:
            rpa_logger.log_error(
                f"Error durante subida a Google Drive: {str(e)}",
                f"Archivo: {context.current_file}"
            )
            return RPAEvent.GOOGLE_DRIVE_FAILED

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