import cv2
import os

# Ruta personalizada (puedes cambiarla)
ruta_guardado = "/home/ta-te-ti/Escritorio/Tateti/Proyecto-Ta-te-ti/imagenes/ppiloto4.jpg"

# Asegúrate de que la carpeta exista
os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

# Intenta abrir la cámara (0 es el índice de la primera cámara)
cap = cv2.VideoCapture(0)

# Verifica que la cámara se haya abierto correctamente
if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

# Bucle principal
while True:
    ret, frame = cap.read()  # Lee un frame de la cámara
    if not ret:
        print("No se pudo recibir el frame")
        break

    cv2.imshow('Webcam', frame)  # Muestra el frame en una ventana

    if cv2.waitKey(1) & 0xFF == ord('f'):
        cv2.imwrite(ruta_guardado, frame)
        print(f"Foto guardada en: {ruta_guardado}")
    
    
    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
