import cv2
import logging
import pytesseract
import easyocr
import numpy as np
from PIL import Image
import pyautogui
from rpa.vision.template_matcher import template_matcher, find_template, load_template

# Configurar la ruta de Tesseract para Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create logger 
logger = logging.getLogger(__name__)
handler = logging.FileHandler('rpa_vision.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Vision:
    def __init__(self):
        self.sap_orden_de_ventas_template_image = cv2.imread('./rpa/vision/reference_images/sap_orden_de_ventas_template.png', cv2.IMREAD_UNCHANGED)
        self.client_field_image = cv2.imread('./rpa/vision/reference_images/client_field.png', cv2.IMREAD_COLOR)
        self.orden_compra_image = cv2.imread('./rpa/vision/reference_images/orden_compra.png', cv2.IMREAD_COLOR)
        self.fecha_entrega_image = cv2.imread('./rpa/vision/reference_images/fecha_entrega.png', cv2.IMREAD_COLOR)
        self.primer_articulo_image = cv2.imread('./rpa/vision/reference_images/primer_articulo.png', cv2.IMREAD_COLOR)
        self.cancel_order_image = cv2.imread('./rpa/vision/reference_images/cancel_order.png', cv2.IMREAD_COLOR)
        self.sap_desktop_image = cv2.imread('./rpa/vision/reference_images/sap_desktop.png', cv2.IMREAD_UNCHANGED)
        self.sap_icon_image = cv2.imread('./rpa/vision/reference_images/sap_icon.png', cv2.IMREAD_COLOR)
        self.remote_desktop_image = cv2.imread('./rpa/vision/reference_images/remote_desktop.png', cv2.IMREAD_UNCHANGED)
        self.sap_modulos_menu_button = cv2.imread('./rpa/vision/reference_images/sap_modulos_menu_button.png', cv2.IMREAD_COLOR)
        self.sap_modulos_menu_image = cv2.imread('./rpa/vision/reference_images/sap_modulos_menu.png', cv2.IMREAD_UNCHANGED)
        self.sap_ventas_menu_button_image = cv2.imread('./rpa/vision/reference_images/sap_ventas_menu_button.png', cv2.IMREAD_COLOR)
        self.sap_ventas_order_menu_image = cv2.imread('./rpa/vision/reference_images/sap_ventas_order_menu.png', cv2.IMREAD_UNCHANGED)
        self.sap_ventas_order_button_image = cv2.imread('./rpa/vision/reference_images/sap_ventas_order_button.png', cv2.IMREAD_COLOR)
        self.sap_archivo_menu_button_image = cv2.imread('./rpa/vision/reference_images/sap_archivo_menu_button.png', cv2.IMREAD_COLOR)
        self.sap_archivos_menu_image = cv2.imread('./rpa/vision/reference_images/sap_archivo_menu.png', cv2.IMREAD_UNCHANGED)
        self.sap_finalizar_button_image = cv2.imread('./rpa/vision/reference_images/sap_finalizar_button.png', cv2.IMREAD_COLOR)
        self.sap_totales_section_image = cv2.imread('./rpa/vision/reference_images/sap_totales_section.png', cv2.IMREAD_COLOR)
        self.scroll_to_bottom_image = cv2.imread('./rpa/vision/reference_images/scroll_to_bottom.png', cv2.IMREAD_COLOR)

    def get_client_coordinates(self):
        offset = (-self.client_field_image.shape[1]//40, 0)  # Offset específico para cliente
        return template_matcher.find_template(
            self.client_field_image, 
            self.sap_orden_de_ventas_template_image,
            offset=offset
        )
    
    def get_orden_coordinates(self):
        offset = (-self.orden_compra_image.shape[1]//30, 0)  # Offset específico para orden
        return template_matcher.find_template(
            self.orden_compra_image,
            self.sap_orden_de_ventas_template_image,
            offset=offset
        )
    
    def get_fecha_coordinates(self):
        offset = (-self.fecha_entrega_image.shape[1]//30, 0)  # Offset específico para fecha
        return template_matcher.find_template(
            self.fecha_entrega_image,
            self.sap_orden_de_ventas_template_image,
            offset=offset
        )
    
    def get_primer_articulo_coordinates(self):
        result_primer = cv2.matchTemplate(self.sap_orden_de_ventas_template_image, self.primer_articulo_image ,cv2.TM_CCOEFF_NORMED)
        min_val_primer, max_val_primer, min_loc_primer, max_loc_primer = cv2.minMaxLoc(result_primer)
        w_primer = self.primer_articulo_image.shape[1]
        h_primer = self.primer_articulo_image.shape[0]
        center_point_primer = (max_loc_primer[0] + w_primer//2, max_loc_primer[1] + h_primer//2 + h_primer//4)
        return center_point_primer, h_primer//2
    
    def get_template_image(self):
        return self.sap_orden_de_ventas_template_image

    def get_cancel_order_coordinates(self):
        result_cancel_order = cv2.matchTemplate(self.sap_orden_de_ventas_template_image, self.cancel_order_image ,cv2.TM_CCOEFF_NORMED)
        min_val_cancel_order, max_val_cancel_order, min_loc_cancel_order, max_loc_cancel_order = cv2.minMaxLoc(result_cancel_order)
        w_cancel_order = self.cancel_order_image.shape[1]
        h_cancel_order = self.cancel_order_image.shape[0]
        center_point_cancel_order = (max_loc_cancel_order[0] + w_cancel_order//2, max_loc_cancel_order[1] + h_cancel_order//2)
        return center_point_cancel_order
    
    def get_modulos_menu_coordinates(self):
        result_modulos_menu = cv2.matchTemplate(self.sap_desktop_image, self.sap_modulos_menu_button ,cv2.TM_CCOEFF_NORMED)
        min_val_modulos_menu, max_val_modulos_menu, min_loc_modulos_menu, max_loc_modulos_menu = cv2.minMaxLoc(result_modulos_menu)
        w_modulos_menu = self.sap_modulos_menu_button.shape[1]
        h_modulos_menu = self.sap_modulos_menu_button.shape[0]
        center_point_modulos_menu = (max_loc_modulos_menu[0] + w_modulos_menu//2, max_loc_modulos_menu[1] + h_modulos_menu//2)
        return center_point_modulos_menu

    def get_archivos_menu_coordinates(self):
        result_archivo_menu = cv2.matchTemplate(self.sap_desktop_image, self.sap_archivo_menu_button_image ,cv2.TM_CCOEFF_NORMED)
        min_val_archivo_menu, max_val_archivo_menu, min_loc_archivo_menu, max_loc_archivo_menu = cv2.minMaxLoc(result_archivo_menu)
        if max_val_archivo_menu < 0.8:
            logger.error('Archivos menu not found.')
            return None
        w_archivo_menu = self.sap_archivo_menu_button_image.shape[1]
        h_archivo_menu = self.sap_archivo_menu_button_image.shape[0]
        center_point_archivo_menu = (max_loc_archivo_menu[0] + w_archivo_menu//2, max_loc_archivo_menu[1] + h_archivo_menu//2)
        return center_point_archivo_menu

    def get_finalizar_button_coordinates(self):
        result_finalizar_button = cv2.matchTemplate(self.sap_archivos_menu_image, self.sap_finalizar_button_image ,cv2.TM_CCOEFF_NORMED)
        min_val_finalizar_button, max_val_finalizar_button, min_loc_finalizar_button, max_loc_finalizar_button = cv2.minMaxLoc(result_finalizar_button)
        w_finalizar_button = self.sap_finalizar_button_image.shape[1]
        h_finalizar_button = self.sap_finalizar_button_image.shape[0]
        center_point_finalizar_button = (max_loc_finalizar_button[0] + w_finalizar_button//2, max_loc_finalizar_button[1] + h_finalizar_button//2)
        return center_point_finalizar_button

    def get_totales_section_coordinates(self):
        """
        Busca la sección de totales (Total antes del descuento, Descuento, etc.) en la pantalla
        Retorna las coordenadas del área donde se encuentra esta sección
        """
        try:
            logger.info("ESTRATEGIA 3.1: Iniciando búsqueda de sección de totales")
            
            # Tomar captura de pantalla actual para template matching
            logger.info("ESTRATEGIA 3.2: Capturando pantalla para buscar sección de totales")
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            logger.info("ESTRATEGIA 3.2 COMPLETADO: Captura de pantalla procesada")
            
            # Realizar template matching con la imagen de referencia de totales
            logger.info("ESTRATEGIA 3.3: Ejecutando template matching de sección de totales")
            result_totales = cv2.matchTemplate(screenshot_cv, self.sap_totales_section_image, cv2.TM_CCOEFF_NORMED)
            min_val_totales, max_val_totales, min_loc_totales, max_loc_totales = cv2.minMaxLoc(result_totales)
            
            logger.info(f"ESTRATEGIA 3.3 COMPLETADO: Template matching ejecutado - Confianza: {max_val_totales:.3f}")
            
            # Umbral de confianza más flexible para escritorio remoto
            if max_val_totales > 0.5:  # Umbral más bajo para escritorio remoto
                w_totales = self.sap_totales_section_image.shape[1]
                h_totales = self.sap_totales_section_image.shape[0]
                
                # Calcular coordenadas del área de totales
                top_left = max_loc_totales
                bottom_right = (max_loc_totales[0] + w_totales, max_loc_totales[1] + h_totales)
                center_point_totales = (max_loc_totales[0] + w_totales//2, max_loc_totales[1] + h_totales//2)
                
                logger.info(f'ESTRATEGIA 3 EXITOSA: Sección de totales encontrada. Coordenadas: {center_point_totales}. Confianza: {max_val_totales:.3f}')
                logger.info(f'Área de totales: Top-left: {top_left}, Bottom-right: {bottom_right}')
                
                return {
                    'center': center_point_totales,
                    'top_left': top_left,
                    'bottom_right': bottom_right,
                    'width': w_totales,
                    'height': h_totales,
                    'confidence': max_val_totales
                }
            else:
                logger.warning(f'ESTRATEGIA 3 FALLIDA: Sección de totales no encontrada. Confianza: {max_val_totales:.3f} (umbral: 0.5)')
                
                # ESTRATEGIA ALTERNATIVA: Buscar por texto usando OCR
                logger.info("ESTRATEGIA 3.4: Intentando búsqueda por texto (OCR)")
                if self.find_totales_by_text(screenshot_cv):
                    logger.info("ESTRATEGIA 3.4 EXITOSA: Sección de totales encontrada por texto")
                    return {
                        'center': (screen_width//2, screen_height-100),
                        'top_left': (0, screen_height-200),
                        'bottom_right': (screen_width, screen_height),
                        'width': screen_width,
                        'height': 200,
                        'confidence': 0.6
                    }
                else:
                    logger.warning("ESTRATEGIA 3.4 FALLIDA: No se encontró sección de totales por texto")
                    return None
                
        except Exception as e:
            logger.error(f"ESTRATEGIA 3 ERROR: Error en template matching de sección de totales: {str(e)}")
            return None

    def find_totales_by_text(self, screenshot_cv):
        """
        Busca la sección de totales por texto usando OCR
        """
        try:
            # Convertir a escala de grises para mejor OCR
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            
            # Usar Tesseract para detectar texto
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(gray, config=custom_config)
            
            # Buscar palabras clave de totales
            totales_keywords = [
                "Total antes del descuento",
                "Descuento",
                "Gastos adicionales", 
                "Redondeo",
                "Impuesto",
                "Total del documento",
                "Total antes",
                "Total documento"
            ]
            
            text_lower = text.lower()
            for keyword in totales_keywords:
                if keyword.lower() in text_lower:
                    logger.info(f"ESTRATEGIA 3.4: Palabra clave encontrada: {keyword}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error en búsqueda por texto: {str(e)}")
            return False

    def find_total_antes_descuento(self):
        """
        Busca específicamente "Total antes del descuento" en la parte inferior derecha
        """
        try:
            logger.info("PASO 8.2: Buscando 'Total antes del descuento' en parte inferior derecha")
            
            # Tomar screenshot
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Obtener dimensiones de pantalla
            screen_height, screen_width = screenshot_cv.shape[:2]
            
            # Recortar solo la parte inferior derecha (último 30% de ancho y alto)
            right_bottom_x = int(screen_width * 0.7)  # Desde 70% del ancho
            right_bottom_y = int(screen_height * 0.7)  # Desde 70% del alto
            
            # Recortar la región inferior derecha
            right_bottom_region = screenshot_cv[right_bottom_y:, right_bottom_x:]
            
            # Convertir a escala de grises para OCR
            gray_region = cv2.cvtColor(right_bottom_region, cv2.COLOR_BGR2GRAY)
            
            # Usar Tesseract para detectar texto en la región
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(gray_region, config=custom_config)
            
            logger.info(f"Texto encontrado en parte inferior derecha: {text}")
            
            # Buscar específicamente "Total antes del descuento"
            if "total antes del descuento" in text.lower():
                logger.info("PASO 8.2 EXITOSO: 'Total antes del descuento' encontrado")
                return True
            else:
                logger.warning("PASO 8.2 FALLIDO: 'Total antes del descuento' no encontrado en parte inferior derecha")
                return False
                
        except Exception as e:
            logger.error(f"Error buscando 'Total antes del descuento': {str(e)}")
            return False

    def get_ventas_menu_coordinates(self):
        result_ventas_menu = cv2.matchTemplate(self.sap_modulos_menu_image, self.sap_ventas_menu_button_image ,cv2.TM_CCOEFF_NORMED)
        min_val_ventas_menu, max_val_ventas_menu, min_loc_ventas_menu, max_loc_ventas_menu = cv2.minMaxLoc(result_ventas_menu)
        if max_val_ventas_menu > 0.9:
            w_ventas_menu = self.sap_ventas_menu_button_image.shape[1]
            h_ventas_menu = self.sap_ventas_menu_button_image.shape[0]
            center_point_ventas_menu = (max_loc_ventas_menu[0] + w_ventas_menu//2, max_loc_ventas_menu[1] + h_ventas_menu//2)
            return center_point_ventas_menu
        else:
            logger.error('Ventas menu not found. Confidence: ' + str(max_val_ventas_menu) + '. Waiting for next run.')
            return None
    
    def get_orden_de_ventas_menu_coordinates(self):
        result_orden_de_ventas_menu = cv2.matchTemplate(self.sap_ventas_order_menu_image, self.sap_ventas_order_button_image ,cv2.TM_CCOEFF_NORMED)
        min_val_orden_de_ventas_menu, max_val_orden_de_ventas_menu, min_loc_orden_de_ventas_menu, max_loc_orden_de_ventas_menu = cv2.minMaxLoc(result_orden_de_ventas_menu)
        if max_val_orden_de_ventas_menu > 0.9:
            w_orden_de_ventas_menu = self.sap_ventas_order_button_image.shape[1]
            h_orden_de_ventas_menu = self.sap_ventas_order_button_image.shape[0]
            center_point_orden_de_ventas_menu = (max_loc_orden_de_ventas_menu[0] + w_orden_de_ventas_menu//2, max_loc_orden_de_ventas_menu[1] + h_orden_de_ventas_menu//2)
            return center_point_orden_de_ventas_menu
        else:
            logger.error('Orden de ventas menu not found.')
            return None
    
    def get_ventas_order_button_coordinates(self):
        """Busca el botón de Orden de Ventas en la pantalla actual"""
        logger.info("PASO 4.3: Buscando botón de Orden de Ventas")
        coordinates = template_matcher.find_template(
            self.sap_ventas_order_button_image,
            confidence=0.8
        )
        if coordinates:
            logger.info(f'PASO 4.3 EXITOSO: Botón encontrado en {coordinates}')
        else:
            logger.warning('PASO 4.3 FALLIDO: Botón no encontrado')
        return coordinates
    
    def get_sap_coordinates(self):
        """Busca el icono de SAP Business One usando template matching"""
        return template_matcher.find_template(
            self.sap_icon_image,
            confidence=0.7  # Umbral específico para SAP
        )

    def get_sap_text_coordinates(self):
        """
        Busca el texto 'SAP Business One' en la pantalla usando OCR
        Retorna las coordenadas del centro del texto encontrado
        """
        try:
            # Tomar captura de pantalla actual
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Convertir a escala de grises para mejor OCR
            gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
            
            # Usar EasyOCR para detectar texto
            reader = easyocr.Reader(['en'], gpu=False)
            results = reader.readtext(gray)
            
            # Lista de variaciones del texto SAP para buscar
            target_texts = [
                "SAP Business One",
                "SAP BusinessOne", 
                "SAP Business",
                "SAP",
                "Business One",
                "BusinessOne"
            ]
            
            logger.info(f"Buscando variaciones de SAP en la pantalla")
            
            for (bbox, text, confidence) in results:
                # Normalizar el texto para comparación
                normalized_text = text.strip().lower()
                
                logger.debug(f"Texto encontrado: '{text}' con confianza: {confidence:.2f}")
                
                # Verificar si el texto contiene alguna variación de SAP
                for target_text in target_texts:
                    target_normalized = target_text.lower()
                    
                    if target_normalized in normalized_text or normalized_text in target_normalized:
                        # Calcular el centro del bounding box
                        top_left = bbox[0]
                        bottom_right = bbox[2]
                        
                        center_x = int((top_left[0] + bottom_right[0]) / 2)
                        center_y = int((top_left[1] + bottom_right[1]) / 2)
                        
                        logger.info(f"SAP encontrado ('{target_text}') en coordenadas: ({center_x}, {center_y}) con confianza: {confidence:.2f}")
                        return (center_x, center_y)
            
            # Si no se encuentra con EasyOCR, intentar con Tesseract
            logger.info("EasyOCR no encontró el texto, intentando con Tesseract...")
            
            # Configurar Tesseract
            custom_config = r'--oem 3 --psm 6'
            tesseract_text = pytesseract.image_to_string(gray, config=custom_config)
            
            # Buscar el texto en el resultado de Tesseract
            for target_text in target_texts:
                if target_text.lower() in tesseract_text.lower():
                    # Obtener las coordenadas del texto con Tesseract
                    data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)
                    
                    for i, text in enumerate(data['text']):
                        if target_text.lower() in text.lower():
                            x = data['left'][i]
                            y = data['top'][i]
                            w = data['width'][i]
                            h = data['height'][i]
                            
                            center_x = x + w // 2
                            center_y = y + h // 2
                            
                            logger.info(f"SAP encontrado con Tesseract ('{target_text}') en coordenadas: ({center_x}, {center_y})")
                            return (center_x, center_y)
            
            logger.error("No se pudo encontrar ninguna variación de SAP en la pantalla")
            return None
            
        except Exception as e:
            logger.error(f"Error al buscar texto SAP: {str(e)}")
            return None

    def get_sap_coordinates_robust(self):
        """
        Método robusto que combina búsqueda por imagen y por texto
        Primero intenta con template matching del icono, si falla usa OCR como respaldo
        """
        logger.info("Iniciando búsqueda robusta del icono de SAP Business One")
        
        # Primero intentar con template matching del icono
        image_coordinates = self.get_sap_coordinates()
        if image_coordinates:
            logger.info("Icono de SAP encontrado por template matching")
            return image_coordinates
        
        # Si falla el template matching, intentar con OCR como respaldo
        logger.info("Template matching falló, intentando con OCR...")
        text_coordinates = self.get_sap_text_coordinates()
        if text_coordinates:
            logger.info("SAP encontrado por texto OCR")
            return text_coordinates
        
        # Si ambos fallan
        logger.error("No se pudo encontrar el icono de SAP Business One con ningún método")
        return None

    def get_scrollbar_coordinates(self):
        """Busca la barra de desplazamiento en la pantalla actual"""
        logger.info("Buscando barra de desplazamiento")
        return template_matcher.find_template(
            self.scroll_to_bottom_image,
            confidence=0.8
        )

    def image_show(self, image):
        cv2.imshow('image', image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def save_template(self):
        cv2.imwrite('./rpa/vision/reference_inmages/template.png', self.sap_orden_de_ventas_template_image)
    
    def save_click_points(self):
        cv2.imwrite('./rpa/vision/reference_inmages/click points.png', self.sap_orden_de_ventas_template_image)
    
    def return_coordinates(self):
        return {
            'client': self.get_client_coordinates(),
            'orden': self.get_orden_coordinates(),
            'fecha': self.get_fecha_coordinates(),
            'primer_articulo': self.get_primer_articulo_coordinates()
        }

if __name__ == '__main__':
    vision = Vision()
    coordinates = vision.return_coordinates()
    print(coordinates)