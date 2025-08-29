import serial
import cv2
import os
import time


from analisisreturn import detectar_rojo_en_imagen
<<<<<<< HEAD
from x_o_0 import jugar

# Ruta personalizada
=======
from proyectoBETA import crear_tablero
from proyectoBETA import crear_matriz_rect
from proyectoBETA import dibujar_tablero
from proyectoBETA import dibujar_figuras
from proyectoBETA import verificar_victoria
from proyectoBETA import mostrar_mensaje
from proyectoBETA import reiniciar_juego
from proyectoBETA import bucle_principal


# ----------- VARIABLES DEL JUEGO -------------

estado_tablero = crear_tablero()
matriz = crear_matriz_rect()
lineas = {}
circulos = {}
player = 1
ganador = None

bucle_principal()

# Ruta personalizada
ruta_guardado = "/home/ta-te-ti/Escritorio/proyecto/Proyecto-Ta-te-ti/imagenes/bocaboton22_8sis.jpg"
>>>>>>> 28cfd06d1a6f96a8e046645de0dc5ad057093e43
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
<<<<<<< HEAD
                casilla = detectar_rojo_en_imagen(ruta_guardado)
                jugar(linea,casilla)
=======
                casilla = detectar_rojo_en_imagen(ruta_guardado) #en el array casilla tenemos[fila, columna]
                if casilla:
                    print(f"🟥 Rojo detectado en fila {casilla[0]}, columna {casilla[1]}")
                else:
                    print("❌ No se detectó rojo")
                #funcion_dibujar(casilla)
>>>>>>> 28cfd06d1a6f96a8e046645de0dc5ad057093e43
            else:
                print("❌ No se pudo capturar la imagen")
                
except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    ser.close()
    cap.release()
