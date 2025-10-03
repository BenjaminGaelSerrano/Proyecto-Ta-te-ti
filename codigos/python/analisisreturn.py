import cv2
import numpy as np

def detectar_rojo_en_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("⚠️ No se pudo cargar la imagen.")
        return None

    alto, ancho = imagen.shape[:2]
    tercio_alto = alto // 3
    tercio_ancho = ancho // 3

    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Rangos HSV para detectar rojo con tolerancia
    rojo_bajo1 = np.array([0, 100, 100])
    rojo_alto1 = np.array([10, 255, 255])

    rojo_bajo2 = np.array([170, 100, 100])
    rojo_alto2 = np.array([180, 255, 255])

    mascara1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
    mascara2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
    mascara_rojo = cv2.bitwise_or(mascara1, mascara2)

    contornos, _ = cv2.findContours(mascara_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 100:
            M = cv2.moments(contorno)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                columna = cx // tercio_ancho
                fila = cy // tercio_alto
                return (fila, columna)  # Retorna solo la primera detección

    return None  # Si no se detecta nada

