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
juego_terminado = False
ganador = None

def dibujar_tablero():
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    VERDE = (0, 200, 0)  # Todo será verde
    
    screen.fill(BLANCO)
    # Líneas del tablero
    for i in range(1, 3):
        pygame.draw.line(screen, NEGRO, (0, i*200), (600, i*200), 3)
        pygame.draw.line(screen, NEGRO, (i*200, 0), (i*200, 600), 3)
    
    # Dibujar X y O - AMBOS EN VERDE
    for fila in range(3):
        for col in range(3):
            x_centro = col * 200 + 100
            y_centro = fila * 200 + 100
            
            if tablero[fila][col] == 1:  # X en VERDE
                pygame.draw.line(screen, VERDE, (x_centro-60, y_centro-60), (x_centro+60, y_centro+60), 8)
                pygame.draw.line(screen, VERDE, (x_centro+60, y_centro-60), (x_centro-60, y_centro+60), 8)
            elif tablero[fila][col] == 2:  # O en VERDE
                pygame.draw.circle(screen, VERDE, (x_centro, y_centro), 60, 8)
    
    # Mostrar mensaje de estado - TODO EN VERDE
    font = pygame.font.Font(None, 48)
    if juego_terminado:
        if ganador:
            simbolo = "X" if ganador == 1 else "O"
            texto = f"¡Ganó {simbolo}! Presiona R para reiniciar"
            color = VERDE  # Verde para cualquier ganador
        else:
            texto = "¡Empate! Presiona R para reiniciar"
            color = VERDE  # Verde para empate
        
        # Fondo semi-transparente para el mensaje
        overlay = pygame.Surface((600, 100))
        overlay.set_alpha(200)
        overlay.fill(BLANCO)
        screen.blit(overlay, (0, 250))
        
        text_surface = font.render(texto, True, color)
        text_rect = text_surface.get_rect(center=(300, 300))
        screen.blit(text_surface, text_rect)
    else:
        # Mostrar de quién es el turno - EN VERDE
        simbolo = "X" if turno == 1 else "O"
        texto = f"Turno: {simbolo}"
        color = VERDE  # Verde para cualquier turno
        text_surface = font.render(texto, True, color)
        text_rect = text_surface.get_rect(center=(300, 30))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

def verificar_ganador():
    """Verifica si hay un ganador en el tablero"""
    # Verificar filas
    for fila in range(3):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] != 0:
            return tablero[fila][0]
    
    # Verificar columnas
    for col in range(3):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] != 0:
            return tablero[0][col]
    
    # Verificar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != 0:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != 0:
        return tablero[0][2]
    
    return None

def tablero_lleno():
    """Verifica si el tablero está lleno (empate)"""
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == 0:
                return False
    return True

def colocar_pieza(fila, columna):
    global turno, juego_terminado, ganador
    
    if juego_terminado:
        print("🔒 El juego ya terminó. Presiona R para reiniciar.")
        return
    
    # Colocar la pieza (permitir sobreescribir)
    tablero[fila][columna] = turno
    simbolo = "X" if turno == 1 else "O"
    print(f"✅ {simbolo} en ({fila}, {columna})")
    
    # Verificar si hay ganador
    ganador = verificar_ganador()
    if ganador:
        juego_terminado = True
        simbolo_ganador = "X" if ganador == 1 else "O"
        print(f"🎉 ¡GANÓ {simbolo_ganador}!")
    elif tablero_lleno():
        juego_terminado = True
        print("🤝 ¡EMPATE!")
    else:
        # Cambiar turno solo si el juego no terminó
        turno = 2 if turno == 1 else 1
    
    dibujar_tablero()

def reiniciar_juego():
    """Reinicia el juego"""
    global tablero, turno, juego_terminado, ganador
    tablero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    turno = 1
    juego_terminado = False
    ganador = None
    print("🔄 Juego reiniciado. Turno de X")
    dibujar_tablero()

# TU CÓDIGO ORIGINAL - solo con correcciones mínimas
ruta_guardado = "/home/ta-te-ti/Escritorio/proyecto/Proyecto-Ta-te-ti/imagenes/bocabotonelesca.jpg"
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
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Reiniciar con R
                    reiniciar_juego()
        
        ret, frame = cap.read()
        
        # SOLO CUANDO ARDUINO ENVÍA DATOS (tu lógica original)
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            print(f"Arduino dice: {linea}")
            
            if ret:
                cv2.imwrite(ruta_guardado, frame)
                print(f"📸 Foto guardada en: {ruta_guardado}")
                casilla = detectar_rojo_en_imagen(ruta_guardado)
                
                # CORRECCIÓN: Cambiar != "nada" por is not None
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