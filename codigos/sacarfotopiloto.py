import cv2
import os

# Ruta personalizada (puedes cambiarla)
ruta_guardado = "/home/ta-te-ti/Escritorio/proyecto/Proyecto-Ta-te-ti/imagenes/piloto.jpg"

# Asegúrate de que la carpeta exista
os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

# Abrir la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

ret, frame = cap.read()

if ret:
    cv2.imwrite(ruta_guardado, frame)
    print(f"Foto guardada en: {ruta_guardado}")
else:
    print("No se pudo capturar la imagen")

cap.release()
