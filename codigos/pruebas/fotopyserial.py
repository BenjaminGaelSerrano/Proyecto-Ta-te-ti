import serial
import cv2
import os
import time


from analIsis import detectar_rojo_en_imagen

# Ruta personalizada
ruta_guardado = "/home/ta-te-ti/Escritorio/Tateti/Proyecto-Ta-te-ti/imagenes/piloto.jpg"
os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

# Abrir cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()   

# Conexión serial
puerto = '/dev/ttyUSB0'
baudrate = 9600
ser = serial.Serial(puerto, baudrate, timeout=1)

print("Escuchando datos del Arduino...")

try:
    while True:
        ret, frame = cap.read()
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            print(f"Arduino dice: {linea}")

            if ret:
                cv2.imwrite(ruta_guardado, frame)
                print(f"📸 Foto guardada en: {ruta_guardado}")

               
                detectar_rojo_en_imagen(ruta_guardado)
            else:
                print("❌ No se pudo capturar la imagen")

except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    ser.close()
    cap.release()
