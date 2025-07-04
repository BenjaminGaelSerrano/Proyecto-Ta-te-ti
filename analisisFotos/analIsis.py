import cv2
import numpy as np

# Cargar imagen
ruta_imagen = "/home/ta-te-ti/Escritorio/Tateti/Proyecto-Ta-te-ti/imagenes/pygamefoto1.jpg"
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print("Error: no se pudo cargar la imagen.")
    exit()

# Dimensiones
alto, ancho = imagen.shape[:2]
tercio_alto = alto // 3
tercio_ancho = ancho // 3

# Convertir a HSV
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Rangos de rojo
rojo_bajo1 = np.array([0, 100, 100])
rojo_alto1 = np.array([10, 255, 255])
rojo_bajo2 = np.array([160, 100, 100])
rojo_alto2 = np.array([180, 255, 255])

# Máscara para rojo
mascara1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
mascara2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
mascara_rojo = cv2.bitwise_or(mascara1, mascara2)

# Contornos
contornos, _ = cv2.findContours(mascara_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Usamos un set para evitar repetir celdas
celdas_detectadas = set()

for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > 100:  # filtrar ruido
        M = cv2.moments(contorno)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            columna = cx // tercio_ancho
            fila = cy // tercio_alto

            # Evitar duplicados
            if (fila, columna) not in celdas_detectadas:
                celdas_detectadas.add((fila, columna))
                print(f"🟥 Rojo detectado en fila {fila}, columna {columna}")
