import serial
import cv2 
import os
import time


from analisisreturn import detectar_rojo_en_imagen
from x_o_0 import jugar
from proyectoBETA import crear_tablero
from proyectoBETA import crear_matriz_rect
from proyectoBETA import dibujar_tablero
from proyectoBETA import dibujar_figuras
from proyectoBETA import verificar_victoria
from proyectoBETA import mostrar_mensaje
from proyectoBETA import reiniciar_juego
from proyectoBETA import bucle_principal
estado_tablero = crear_tablero()
matriz = crear_matriz_rect()
lineas = {}
circulos = {}
player = 1
ganador = None

bucle_principal()
ruta_guardado = "/home/ta-te-ti/Escritorio/proyecto/Proyecto-Ta-te-ti/imagenes/bocaboton22_8sis.jpg"
os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()   
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
                casilla = detectar_rojo_en_imagen(ruta_guardado)
                jugar(linea,casilla)
                if casilla:
                    print(f"🟥 Rojo detectado en fila {casilla[0]}, columna {casilla[1]}")
                else:
                    print("❌ No se detectó rojo")
            else:
                print("❌ No se pudo capturar la imagen")
                
except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    ser.close()
    cap.release()
