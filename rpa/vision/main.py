import cv2
import logging

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
    
    def get_sap_coordinates(self):
        result_sap = cv2.matchTemplate(self.remote_desktop_image, self.sap_icon_image ,cv2.TM_CCOEFF_NORMED)
        min_val_sap, max_val_sap, min_loc_sap, max_loc_sap = cv2.minMaxLoc(result_sap)
        print(max_val_sap)
        if max_val_sap > 0.9:
            w_sap = self.sap_icon_image.shape[1]
            h_sap = self.sap_icon_image.shape[0]
            center_point_sap = (max_loc_sap[0] + w_sap//2, max_loc_sap[1] + h_sap//2)
            logger.info('SAP icon found. Coordinates: ' + str(center_point_sap) + '. Confidence: ' + str(max_val_sap))
            return center_point_sap
        else:
            logger.error('SAP icon not found. Confidence: ' + str(max_val_sap) + '. Waiting for next run.')
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