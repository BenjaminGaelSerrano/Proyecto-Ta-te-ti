import serial
import cv2
import os
import time
import pygame

from analisisreturn import detectar_rojo_en_imagen

# Pygame básico para mostrar el tablero
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Ta-Te-Ti")

# Tablero y funciones básicas
tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
turno = 1

def dibujar_tablero():
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    AZUL = (0, 0, 255)
    
    screen.fill(BLANCO)
    # Líneas del tablero
    for i in range(1, 3):
        pygame.draw.line(screen, NEGRO, (0, i*200), (600, i*200), 3)
        pygame.draw.line(screen, NEGRO, (i*200, 0), (i*200, 600), 3)
    
    # Dibujar X y O
    for fila in range(3):
        for col in range(3):
            x_centro = col * 200 + 100
            y_centro = fila * 200 + 100
            
            if tablero[fila][col] == 1:  # X
                pygame.draw.line(screen, ROJO, (x_centro-60, y_centro-60), (x_centro+60, y_centro+60), 8)
                pygame.draw.line(screen, ROJO, (x_centro+60, y_centro-60), (x_centro-60, y_centro+60), 8)
            elif tablero[fila][col] == 2:  # O
                pygame.draw.circle(screen, AZUL, (x_centro, y_centro), 60, 8)
    
    pygame.display.flip()

def colocar_pieza(fila, columna):
    global turno
    # CAMBIO: Remover el if para permitir sobreescribir
    tablero[fila][columna] = turno
    simbolo = "X" if turno == 1 else "O"
    print(f"✅ {simbolo} en ({fila}, {columna}) - Sobreescrito")
    turno = 2 if turno == 1 else 1
    dibujar_tablero()  # Actualizar pantalla cuando se coloque pieza

# TU CÓDIGO ORIGINAL - solo con correcciones mínimas
ruta_guardado = "/home/Alumno26.ORTIZ.Santiago@ipm.edu.ar/Escritorio/proyecto/venv/Proyecto-Ta-te-ti/imagenes/bocaboton17_10.jpg"
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

# Dibujar tablero inicial
dibujar_tablero()

try:
    while True:
        # Manejar eventos de pygame (para poder cerrar la ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                raise KeyboardInterrupt
        
        ret, frame = cap.read()
        
        # SOLO CUANDO ARDUINO ENVÍA DATOS (tu lógica original)
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            print(f"Arduino dice: {linea}")
            
            if ret:
                # APLICAR ZOOM (ajusta el factor según necesites)
                alto, ancho = frame.shape[:2]
                factor = 0.3  # Ajusta el factor de zoom según necesites:
                # 1.0 = sin zoom | 0.7 = suave | 0.5 = 2x | 0.3 = 3x 
                
                nuevo_ancho = int(ancho * factor)
                nuevo_alto = int(alto * factor)
                
                x_inicio = (ancho - nuevo_ancho) // 2
                y_inicio = (alto - nuevo_alto) // 2
                
                frame_recortado = frame[y_inicio:y_inicio+nuevo_alto, 
                                        x_inicio:x_inicio+nuevo_ancho]
                
                cv2.imwrite(ruta_guardado, frame_recortado)
                print(f"📸 Foto guardada (con zoom) en: {ruta_guardado}")
                casilla = detectar_rojo_en_imagen(ruta_guardado)
                
                # CORRECCIÓN 1: Cambiar != "nada" por is not None
                if casilla is not None:
                    fila, columna = casilla
                    print(f"🔴 Rojo detectado en fila {fila}, columna {columna}")
                    colocar_pieza(fila, columna)
                else:
                    print("⚪ No se detectó rojo")
            else:
                print("❌ No se pudo capturar la imagen")
                
except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    ser.close()
    cap.release()
    pygame.quit()