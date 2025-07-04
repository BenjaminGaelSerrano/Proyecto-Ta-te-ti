import serial
import cv2
import os
import time 
# Ruta personalizada (puedes cambiarla)
ruta_guardado = "/home/ta-te-ti/Escritorio/Tateti/Proyecto-Ta-te-ti/imagenes/pygamefoto1.jpg"

# Asegúrate de que la carpeta exista
os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

# Abrir la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()   



# Cambia 'COM3' por el puerto de tu Arduino.
# En Linux probablemente sea '/dev/ttyUSB0' o '/dev/ttyACM0'
puerto = '/dev/ttyUSB0'
baudrate = 9600

# Abre la conexión serial
ser = serial.Serial(puerto, baudrate, timeout=1)

print("Escuchando datos del Arduino...")

try:
    while True:
        # Lee una línea del puerto serial
        ret, frame = cap.read()
        if ser.in_waiting>0:
            linea = ser.readline().decode('utf-8').strip()
            
            print(f"Arduino dice:{linea}")
            if ret:
                cv2.imwrite(ruta_guardado, frame)
                print(f"Foto guardada en: {ruta_guardado}") 
            else:
                print("No se pudo capturar la imagen")
            
                

except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    ser.close()

cap.release()
