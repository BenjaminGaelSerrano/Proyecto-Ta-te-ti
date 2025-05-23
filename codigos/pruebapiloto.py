import cv2

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

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
