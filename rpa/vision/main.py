import cv2
import logging
import pytesseract
import easyocr
import numpy as np
from PIL import Image
import pyautogui

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
        self.sap_ventas_order_menu_image = cv2.imread('./rpa/vision/reference_images/sap_ventas_order_menu.png', cv2.IMREAD_COLOR)
        self.sap_ventas_order_button_image = cv2.imread('./rpa/vision/reference_images/sap_ventas_order_button.png', cv2.IMREAD_COLOR)
        self.sap_archivo_menu_button_image = cv2.imread('./rpa/vision/reference_images/sap_archivo_menu_button.png', cv2.IMREAD_COLOR)
        self.sap_archivos_menu_image = cv2.imread('./rpa/vision/reference_images/sap_archivo_menu.png', cv2.IMREAD_UNCHANGED)
        self.sap_finalizar_button_image = cv2.imread('./rpa/vision/reference_images/sap_finalizar_button.png', cv2.IMREAD_COLOR)

    def get_client_coordinates(self):
        result_client = cv2.matchTemplate(self.sap_orden_de_ventas_template_image, self.client_field_image ,cv2.TM_CCOEFF_NORMED)
        min_val_client, max_val_client, min_loc_client, max_loc_client = cv2.minMaxLoc(result_client)
        w_client = self.client_field_image.shape[1]
        h_client = self.client_field_image.shape[0]
        center_point_client = (max_loc_client[0] + w_client - w_client//40, max_loc_client[1] + h_client//2)
        return center_point_client
    
    def get_orden_coordinates(self):
        result_orden = cv2.matchTemplate(self.sap_orden_de_ventas_template_image, self.orden_compra_image ,cv2.TM_CCOEFF_NORMED)
        min_val_orden, max_val_orden, min_loc_orden, max_loc_orden = cv2.minMaxLoc(result_orden)
        w_orden = self.orden_compra_image.shape[1]
        h_orden = self.orden_compra_image.shape[0]
        center_point_orden = (max_loc_orden[0] + w_orden - w_orden//30, max_loc_orden[1] + h_orden//2)
        return center_point_orden
    
    def get_fecha_coordinates(self):
        result_fecha = cv2.matchTemplate(self.sap_orden_de_ventas_template_image, self.fecha_entrega_image ,cv2.TM_CCOEFF_NORMED)
        min_val_fecha, max_val_fecha, min_loc_fecha, max_loc_fecha = cv2.minMaxLoc(result_fecha)
        w_fecha = self.fecha_entrega_image.shape[1]
        h_fecha = self.fecha_entrega_image.shape[0]
        center_point_fecha = (max_loc_fecha[0] + w_fecha - w_fecha//30, max_loc_fecha[1] + h_fecha//2)
        return center_point_fecha
    
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
        """
        Busca el botón de Orden de Ventas en la pantalla actual usando template matching
        Retorna las coordenadas del centro del botón encontrado
        """
        try:
            # Tomar captura de pantalla actual para template matching
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Realizar template matching
            result_ventas_order = cv2.matchTemplate(screenshot_cv, self.sap_ventas_order_button_image, cv2.TM_CCOEFF_NORMED)
            min_val_ventas_order, max_val_ventas_order, min_loc_ventas_order, max_loc_ventas_order = cv2.minMaxLoc(result_ventas_order)
            
            logger.info(f"Template matching del botón Orden de Ventas - Confianza: {max_val_ventas_order:.3f}")
            
            # Umbral de confianza
            if max_val_ventas_order > 0.8:
                w_ventas_order = self.sap_ventas_order_button_image.shape[1]
                h_ventas_order = self.sap_ventas_order_button_image.shape[0]
                center_point_ventas_order = (max_loc_ventas_order[0] + w_ventas_order//2, max_loc_ventas_order[1] + h_ventas_order//2)
                logger.info(f'Botón de Orden de Ventas encontrado. Coordenadas: {center_point_ventas_order}. Confianza: {max_val_ventas_order:.3f}')
                return center_point_ventas_order
            else:
                logger.warning(f'Botón de Orden de Ventas no encontrado. Confianza: {max_val_ventas_order:.3f} (umbral: 0.8)')
                return None
                
        except Exception as e:
            logger.error(f"Error en template matching del botón Orden de Ventas: {str(e)}")
            return None
    
    def get_sap_coordinates(self):
        """
        Busca el icono de SAP Business One usando template matching
        Retorna las coordenadas del centro del icono encontrado
        """
        try:
            # Tomar captura de pantalla actual para template matching
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Realizar template matching
            result_sap = cv2.matchTemplate(screenshot_cv, self.sap_icon_image, cv2.TM_CCOEFF_NORMED)
            min_val_sap, max_val_sap, min_loc_sap, max_loc_sap = cv2.minMaxLoc(result_sap)
            
            logger.info(f"Template matching del icono SAP - Confianza: {max_val_sap:.3f}")
            
            # Umbral de confianza más flexible (0.7 en lugar de 0.9)
            if max_val_sap > 0.7:
                w_sap = self.sap_icon_image.shape[1]
                h_sap = self.sap_icon_image.shape[0]
                center_point_sap = (max_loc_sap[0] + w_sap//2, max_loc_sap[1] + h_sap//2)
                logger.info(f'Icono de SAP encontrado. Coordenadas: {center_point_sap}. Confianza: {max_val_sap:.3f}')
                return center_point_sap
            else:
                logger.warning(f'Icono de SAP no encontrado. Confianza: {max_val_sap:.3f} (umbral: 0.7)')
                return None
                
        except Exception as e:
            logger.error(f"Error en template matching del icono SAP: {str(e)}")
            return None

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